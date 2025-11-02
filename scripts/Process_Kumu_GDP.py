"""
# https://zenodo.org/records/16741980
Process Kummu GDP raster data for Sub-Saharan African countries

This script:
1. Loads the polygon shapefile with country boundaries
2. Loads the high-resolution GDP raster data (30 arcsec resolution)
3. For each SSA country, clips the raster to the country boundary
4. Extracts the 2020 GDP data
5. Creates and saves 3D-style elevation visualization images

Data source: Kummu et al. GDP dataset
- Raster: rast_gdpTot_1990_2020_30arcsec.tif (higher resolution)
- Polygons: polyg_adm0_gdp_perCapita_1990_2022.gpkg
"""

import os
import sys
import rasterio
from rasterio.mask import mask
from rasterio.warp import transform_bounds
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import contextily as cx
import jenkspy
import warnings
from matplotlib.patches import Patch


# Add project root to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from src.utils.country_utils import load_subsaharan_countries_dict

# Suppress warnings
warnings.filterwarnings('ignore')


def load_gdp_data():
    """Load GDP raster data"""
    
    # Path to raster file - using high-resolution 30 arcsec raster
    raster_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 
                               'rast_gdpTot_1990_2020_30arcsec.tif')
    
    # Open raster data
    raster = rasterio.open(raster_path)
    
    return raster


def load_top_cities(iso3, country_gdf, raster_crs, n_cities=5):
    """
    Load and filter top N cities by population for a country
    
    Args:
        iso3: ISO3 country code
        country_gdf: GeoDataFrame with country boundary
        raster_crs: CRS of the raster data
        n_cities: Number of top cities to return (default 5)
        
    Returns:
        GeoDataFrame with top N cities, or None if file not found
    """
    # Path to Africapolis centroids
    cities_path = r'C:\Users\jqnmu\OneDrive\World_Bank_DRM\Datasets\Africapolis\Africapolis_2023\africapolis2023.gpkg'
    
    if not os.path.exists(cities_path):
        print(f"  Warning: Cities file not found: {cities_path}")
        return None
    
    try:
        # Load all cities
        cities = gpd.read_file(cities_path)
        
        # Reproject to country CRS if needed
        if cities.crs != country_gdf.crs:
            cities = cities.to_crs(country_gdf.crs)
        
        # Filter cities within country boundary
        country_geom = country_gdf.geometry.iloc[0]
        cities_in_country = cities[cities.geometry.within(country_geom) | 
                                   cities.geometry.intersects(country_geom)]
        
        if cities_in_country.empty:
            print(f"  Info: No cities found in {iso3}")
            return None
        
        # Sort by Pop2020 and get top N
        if 'Pop2020' in cities_in_country.columns:
            top_cities = cities_in_country.nlargest(n_cities, 'Pop2020')
        else:
            print(f"  Warning: 'Pop2020' column not found in cities data")
            return None
        
        # Reproject to Web Mercator for visualization
        top_cities = top_cities.to_crs(3857)
        
        return top_cities
    except Exception as e:
        print(f"  Warning: Could not load cities data: {e}")
        return None


def load_gadm_shapefile(iso3):
    """Load GADM shapefile for a specific country
    
    Args:
        iso3: ISO3 country code
        
    Returns:
        GeoDataFrame with country boundary
    """
    # GADM data path - outside project root
    gadm_base = r'C:\Users\jqnmu\OneDrive\World_Bank_DRM\Datasets\GADM4.1'
    shapefile_path = os.path.join(gadm_base, iso3, f'gadm41_{iso3}_0.shp')
    
    if not os.path.exists(shapefile_path):
        raise FileNotFoundError(f"GADM shapefile not found: {shapefile_path}")
    
    # Load shapefile
    gdf = gpd.read_file(shapefile_path)
    
    return gdf


def get_2020_band_index(raster):
    """
    Get the band index for 2020 data
    
    Args:
        raster: Rasterio dataset
        
    Returns:
        Band index for 2020 (1-indexed for rasterio)
    """
    # High-resolution raster has bands: 1990, 1995, 2000, 2005, 2010, 2015, 2020
    # Band 7 is 2020
    band_index = 7
    
    if band_index > raster.count:
        raise ValueError(f"Band {band_index} exceeds total bands {raster.count}")
    
    return band_index


def save_clipped_raster(data, transform, raster_crs, iso3, country_name, output_dir):
    """
    Save clipped raster as GeoTIFF
    
    Args:
        data: GDP data array (2D)
        transform: Rasterio affine transform for the clipped raster
        raster_crs: CRS of the raster data
        iso3: ISO3 country code
        country_name: Name of country
        output_dir: Directory to save raster
    """
    raster_filename = f"{iso3}_{country_name.replace(' ', '_')}_GDP_2020.tif"
    raster_filepath = os.path.join(output_dir, raster_filename)
    
    try:
        # Remove existing file if it exists
        if os.path.exists(raster_filepath):
            try:
                os.remove(raster_filepath)
            except PermissionError:
                print(f"  Warning: Could not overwrite {raster_filename} (file may be open)")
                import time
                raster_filename = f"{iso3}_{country_name.replace(' ', '_')}_GDP_2020_{int(time.time())}.tif"
                raster_filepath = os.path.join(output_dir, raster_filename)
        
        with rasterio.open(
            raster_filepath,
            'w',
            driver='GTiff',
            height=data.shape[0],
            width=data.shape[1],
            count=1,
            dtype=data.dtype,
            crs=raster_crs,
            transform=transform,
            nodata=np.nan,
            compress='lzw'
        ) as dst:
            dst.write(data, 1)
        
        print(f"  Saved raster: {raster_filename}")
    except Exception as e:
        print(f"  Warning: Could not save raster: {e}")


def clip_raster_to_polygon(raster, polygon_geom, band_index):
    """
    Clip raster to polygon boundary and extract specific band
    
    Args:
        raster: Rasterio dataset
        polygon_geom: Geometry to clip to
        band_index: Band number to extract (1-indexed)
        
    Returns:
        Tuple of (clipped_data, clipped_transform)
    """
    # Clip the raster to the polygon - set outside to NaN
    out_image, out_transform = mask(
        raster,
        [polygon_geom],
        crop=True,
        filled=True,
        all_touched=True,
        nodata=np.nan
    )
    
    # Extract the specific band
    # out_image shape is (bands, height, width)
    band_data = out_image[band_index - 1]  # Convert to 0-indexed
    band_data = band_data.astype(float, copy=False)
    
    # Within the polygon: convert NaN to 0 (missing data becomes 0)
    # Outside the polygon: keep as NaN (for transparency)
    # Create a mask of the polygon interior
    from rasterio.features import rasterize
    from rasterio.transform import array_bounds
    
    # Get the shape and create a mask
    height, width = band_data.shape
    polygon_mask = rasterize(
        [polygon_geom],
        out_shape=(height, width),
        transform=out_transform,
        all_touched=True,
        fill=0,
        default_value=1
    ).astype(bool)
    
    # Inside polygon: NaN -> 0, outside polygon: keep as NaN
    band_data = np.where(polygon_mask & np.isnan(band_data), 0.0, band_data)
    
    return band_data, out_transform


def expand_bounds(minx, miny, maxx, maxy, buffer_pct=0.05):
    """
    Expand geographic bounds by a percentage buffer
    
    Args:
        minx, miny, maxx, maxy: Original bounds
        buffer_pct: Percentage to expand (default 0.05 = 5%)
        
    Returns:
        Tuple of expanded (minx, miny, maxx, maxy)
    """
    width = maxx - minx
    height = maxy - miny
    buffer = max(width, height) * buffer_pct
    return (
        minx - buffer,
        miny - buffer,
        maxx + buffer,
        maxy + buffer
    )


def add_basemap_to_axis(ax, crs='EPSG:3857', source=None, alpha=1.0, zoom='auto'):
    """
    Add basemap to matplotlib axis
    
    Args:
        ax: Matplotlib axis
        crs: Coordinate reference system (default 'EPSG:3857')
        source: Contextily basemap source (default CartoDB.Positron)
        alpha: Transparency (default 1.0)
        zoom: Zoom level (default 'auto')
        
    Returns:
        bool: True if successful, False otherwise
    """
    if source is None:
        source = cx.providers.CartoDB.Positron
    
    try:
        cx.add_basemap(ax, crs=crs, source=source, zoom=zoom, alpha=alpha)
        print(f"  Basemap added successfully")
        return True
    except Exception as e:
        print(f"  Warning: Could not fetch basemap: {e}")
        return False


def add_city_labels(ax, cities_gdf, name_column='agglosName', fontsize=15, 
                   fontweight='bold', color='#333333', zorder=16):
    """
    Add city labels to map at centroid locations
    
    Args:
        ax: Matplotlib axis
        cities_gdf: GeoDataFrame with city geometries
        name_column: Column containing city names
        fontsize: Font size for labels (default 15)
        fontweight: Font weight (default 'bold')
        color: Text color (default '#333333')
        zorder: Drawing order (default 16)
    """
    if cities_gdf is None or cities_gdf.empty:
        return
    
    for idx, row in cities_gdf.iterrows():
        geom = row.geometry
        x, y = geom.centroid.x, geom.centroid.y
        
        # Get city name from specified column or fallback options
        if name_column in row.index:
            city_name = row[name_column]
        elif 'CITY_NAME' in row.index:
            city_name = row['CITY_NAME']
        elif 'NAME' in row.index:
            city_name = row['NAME']
        else:
            city_name = f"City {idx}"
        
        ax.annotate(city_name, xy=(x, y), xytext=(5, 5), 
                   textcoords='offset points',
                   fontsize=fontsize, fontweight=fontweight, 
                   color=color, zorder=zorder)


def create_categorical_legend(ax, breaks, colors, value_formatter=None, 
                             title='Value Range', loc='upper left', 
                             fontsize=13, title_fontsize=14):
    """
    Create categorical legend with value ranges
    
    Args:
        ax: Matplotlib axis
        breaks: List of break values from classification
        colors: List of colors for each bin
        value_formatter: Function to format values (optional)
        title: Legend title
        loc: Legend location (default 'upper left')
        fontsize: Font size for labels (default 13)
        title_fontsize: Font size for title (default 14)
    """
    from matplotlib.patches import Patch
    
    no_bins = len(colors)
    legend_elements = []
    
    for i in range(no_bins):
        start_val = breaks[i]
        end_val = breaks[i + 1]
        
        # Use custom formatter if provided, otherwise use default
        if value_formatter:
            label = value_formatter(start_val, end_val)
        else:
            # Default formatter with escaped $ to prevent italics
            if start_val >= 1e6:
                start_label = f'\\${start_val/1e6:.1f}M'
            elif start_val >= 1e3:
                start_label = f'\\${start_val/1e3:.0f}K'
            else:
                start_label = f'\\${start_val:.0f}'
            
            if end_val >= 1e6:
                end_label = f'\\${end_val/1e6:.1f}M'
            elif end_val >= 1e3:
                end_label = f'\\${end_val/1e3:.0f}K'
            else:
                end_label = f'\\${end_val:.0f}'
            
            label = f'{start_label} - {end_label}'
        
        color = colors[i]
        legend_elements.append(Patch(facecolor=color, edgecolor='#333333', label=label))
    
    ax.legend(handles=legend_elements, loc=loc, fontsize=fontsize,
             title=title, title_fontproperties={'weight': 'bold', 'size': title_fontsize},
             framealpha=0.95, edgecolor='#333333', fancybox=True, shadow=True)


def create_gdp_visualization(data, transform, country_geom, country_name, iso3, output_dir, raster_crs):
    """
    Create and save 2D GDP visualization with OSM basemap context
    Also saves the clipped raster as GeoTIFF
    
    Args:
        data: GDP data array (2D)
        transform: Rasterio affine transform for the clipped raster
        country_geom: Shapely geometry for country polygon
        country_name: Name of country
        iso3: ISO3 code
        output_dir: Directory to save image
        raster_crs: CRS of the raster data
    """
    # Check if data has any valid values
    valid_mask = data > 0
    if not np.any(valid_mask):
        print(f"  Warning: No valid GDP data for {country_name}")
        return
    
    # Configuration
    no_bins = 9
    
    # Get data statistics for all non-NaN values (including zeros)
    valid_data_mask = ~np.isnan(data)
    
    # Get non-NaN values for Jenks classification
    valid_values = data[valid_data_mask]
    
    # Create n_bins using Jenks natural breaks classification
    breaks = jenkspy.jenks_breaks(valid_values, n_classes=no_bins)
    print(f"  Jenks breaks ({no_bins} bins): {[f'{b:.2e}' for b in breaks]}")
    
    # Classify data using Jenks breaks
    data_viz = np.digitize(data, breaks) - 1  # Get bin indices (0-8)
    data_viz = data_viz.astype(float)
    data_viz[~valid_data_mask] = np.nan  # Restore NaN outside polygon
    
    # Create figure with proper size
    fig, ax = plt.subplots(figsize=(14, 12), dpi=200)
    
    # Get bounds for basemap in Web Mercator (EPSG:3857)
    geom_gdf = gpd.GeoDataFrame([1], geometry=[country_geom], crs=raster_crs)
    geom_web = geom_gdf.to_crs(3857)
    minx, miny, maxx, maxy = geom_web.total_bounds
    
    # Expand bounds to show neighboring countries
    minx, miny, maxx, maxy = expand_bounds(minx, miny, maxx, maxy, buffer_pct=0.05)
    
    # Set axis limits first (required for contextily)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect('equal')
    
    # Add basemap BEFORE plotting data (so it's underneath)
    add_basemap_to_axis(ax)
    
    # Create custom colormap for n_bins (discrete classification)
    colors = ['#FFFEF5', '#FFF5C0', '#FFEB8B', '#FFD560', '#FFAF48', 
              '#F57C56', '#E24952', '#C1254E', '#8B1538']  # 9 colors for up to 9 bins
    colors = colors[:no_bins]  # Use only as many colors as bins
    cmap = mcolors.ListedColormap(colors)
    cmap.set_bad(alpha=0)  # Transparent only for NaN (outside polygon)
    
    # Create discrete normalization for n_bins
    norm = mcolors.BoundaryNorm(boundaries=np.arange(-0.5, no_bins + 0.5, 1), ncolors=no_bins)
    
    # Compute extent in Web Mercator for plotting
    west, south, east, north = transform_bounds(raster_crs, 'EPSG:3857', 
                                                  *rasterio.transform.array_bounds(
                                                      data.shape[0], data.shape[1], transform))
    extent = [west, east, south, north]
    
    # Plot GDP data with Jenks classification
    im = ax.imshow(data_viz, extent=extent, origin='upper', 
                   cmap=cmap, norm=norm, alpha=1, interpolation='none')
    
    # Add country boundary
    geom_web.boundary.plot(ax=ax, color="#4A4A4A", linewidth=2, alpha=1.0, zorder=10)
    
    # Load and add top 5 cities
    country_gdf_for_cities = gpd.GeoDataFrame([1], geometry=[country_geom], crs=raster_crs)
    cities = load_top_cities(iso3, country_gdf_for_cities, raster_crs, n_cities=5)
    add_city_labels(ax, cities, name_column='agglosName', fontsize=15)
    
    # Styling
    ax.axis('off')
    
    # Create categorical legend
    create_categorical_legend(
        ax, breaks, colors,
        title='2020 GDP\n(USD, 2017 PPP)',
        loc='upper left',
        fontsize=13,
        title_fontsize=14
    )
    
    # Tight layout
    plt.tight_layout()
    
    # Save
    filename = f"{iso3}_{country_name.replace(' ', '_')}_GDP_2020_2D.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close()

    print(f"  Saved visualization: {filename}")


def process_all_countries():
    """Main processing function"""
    
    print("=" * 80)
    print("Processing Kummu GDP Data for Sub-Saharan African Countries")
    print("=" * 80)
    
    # Create output directory
    output_dir = os.path.join(project_root, 'data', 'processed', 'gdp_pop_raster_images')
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nOutput directory: {output_dir}\n")
    
    # Load SSA countries
    ssa_countries = load_subsaharan_countries_dict()
    print(f"Processing {len(ssa_countries)} Sub-Saharan African countries\n")
    
    # Load GDP raster
    raster = load_gdp_data()
    
    # Get 2020 band index
    band_2020 = get_2020_band_index(raster)
    
    # Process each country
    print("\n" + "=" * 80)
    print("Processing individual countries...")
    print("=" * 80 + "\n")
    
    processed_count = 0
    skipped_count = 0

    test = [('LSO', 'Lesotho')]
    for iso3, country_name in test: # sorted(ssa_countries.items())
        print(f"Processing: {country_name} ({iso3})")
        
        try:
            # Load GADM shapefile for this country
            country_gdf = load_gadm_shapefile(iso3)
            
            # Reproject to raster CRS if needed
            if country_gdf.crs != raster.crs:
                print(f"  Reprojecting from {country_gdf.crs} to {raster.crs}")
                country_gdf = country_gdf.to_crs(raster.crs)
            
            # Get the geometry (first feature - should be only one for admin level 0)
            geom = country_gdf.geometry.iloc[0]
            
            # Clip raster to country boundary for 2020
            gdp_data, out_transform = clip_raster_to_polygon(raster, geom, band_2020)
            
            # Save raster
            save_clipped_raster(gdp_data, out_transform, raster.crs, iso3, country_name, output_dir)
            
            # Create visualization
            create_gdp_visualization(gdp_data, out_transform, geom, country_name, iso3, output_dir, raster.crs)
            
            processed_count += 1
            
        except Exception as e:
            print(f"  Error processing {country_name}: {str(e)}")
            skipped_count += 1
            continue
    
    # Close raster
    raster.close()
    
    # Summary
    print("\n" + "=" * 80)
    print("Processing Complete!")
    print("=" * 80)
    print(f"Total countries: {len(ssa_countries)}")
    print(f"Successfully processed: {processed_count}")
    print(f"Skipped: {skipped_count}")
    print(f"\nImages saved to: {output_dir}")


if __name__ == "__main__":
    process_all_countries()
