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
import warnings
from rasterio.features import rasterize
import time
from functools import wraps


# Add project root to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from src.utils.country_utils import load_subsaharan_countries_dict

# Suppress warnings
warnings.filterwarnings('ignore')

# Timing decorator for performance analysis
def timing_decorator(func):
    """Decorator to measure function execution time"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"  ⏱️  {func.__name__}: {elapsed:.2f}s")
        return result
    return wrapper

# Cache for loaded city data to avoid reloading
_CITIES_CACHE = None

def load_gdp_data():
    """Load GDP raster data"""
    
    # Path to raster file - using high-resolution 30 arcsec raster
    raster_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 
                               'rast_gdpTot_1990_2020_30arcsec.tif')
    
    # Open raster data
    raster = rasterio.open(raster_path)
    
    return raster


def load_population_data():
    """Load population raster data"""
    
    # Path to raster file - 1km resolution population data for 2020
    raster_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 
                               'global_pop_2020_CN_1km_R2025A_UA_v1.tif')
    
    # Open raster data
    raster = rasterio.open(raster_path)
    
    return raster


def load_top_cities(iso3, country_gdf, n_cities=5):
    """
    Load and filter top N cities by population for a country (WITH CACHING)
    
    Args:
        iso3: ISO3 country code
        country_gdf: GeoDataFrame with country boundary
        n_cities: Number of top cities to return (default 5)
        
    Returns:
        GeoDataFrame with top N cities, or None if file not found
    """
    global _CITIES_CACHE
    
    cities_path = r'C:\Users\jqnmu\OneDrive\World_Bank_DRM\Datasets\Africapolis\Africapolis_2023\africapolis2023.gpkg'
    
    if not os.path.exists(cities_path):
        return None
    
    # Load cities only once and cache
    if _CITIES_CACHE is None:
        print(f"  📥 Loading cities data (one-time load)...")
        _CITIES_CACHE = gpd.read_file(cities_path)
    
    cities = _CITIES_CACHE.copy()
    
    # Reproject to country CRS if needed
    if cities.crs != country_gdf.crs:
        cities = cities.to_crs(country_gdf.crs)
    
    # Filter cities within country boundary
    country_geom = country_gdf.geometry.iloc[0]
    cities_in_country = cities[cities.geometry.within(country_geom) | 
                               cities.geometry.intersects(country_geom)]
    
    if cities_in_country.empty or 'Pop2020' not in cities_in_country.columns:
        return None
    
    # Sort by Pop2020 and get top N, then reproject to Web Mercator
    top_cities = cities_in_country.nlargest(n_cities, 'Pop2020')
    return top_cities.to_crs(3857)


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


@timing_decorator
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
    
    print(f"    📊 Clipped raster shape: {band_data.shape}, Non-zero pixels: {np.count_nonzero(band_data > 0):,}")
    
    return band_data, out_transform





def add_basemap_to_axis(ax, crs='EPSG:3857', source=None, alpha=1.0, zoom='auto'):
    """
    Add basemap to matplotlib axis (WITH ERROR RECOVERY)
    
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
        start = time.time()
        cx.add_basemap(ax, crs=crs, source=source, zoom=zoom, alpha=alpha)
        elapsed = time.time() - start
        print(f"  ⏱️  Basemap download: {elapsed:.2f}s")
        return True
    except Exception as e:
        print(f"  ⚠️  Basemap failed ({str(e)}), continuing without basemap...")
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
        
        ax.annotate(city_name, xy=(x, y), xytext=(5, 5), 
                   textcoords='offset points',
                   fontsize=fontsize, fontweight=fontweight, 
                   color=color, zorder=zorder)


def create_categorical_legend(ax, breaks, colors, value_formatter=None, 
                             title='Value Range', loc='lower center', 
                             fontsize=13, title_fontsize=14, ncol=3, bbox_to_anchor=(0.5, -0.15)):
    """
    Create categorical legend with value ranges
    
    Args:
        ax: Matplotlib axis
        breaks: List of break values from classification
        colors: List of colors for each bin
        value_formatter: Function to format values (optional)
        title: Legend title
        loc: Legend location (default 'lower center')
        fontsize: Font size for labels (default 13)
        title_fontsize: Font size for title (default 14)
        ncol: Number of columns (default 3)
        bbox_to_anchor: Position anchor for legend (default (0.5, -0.15))
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
        legend_elements.append(Patch(facecolor=color, edgecolor='#333333', label=label, alpha=1.0))
    
    legend = ax.legend(handles=legend_elements, loc=loc, fontsize=fontsize,
             title=title, title_fontproperties={'weight': 'bold', 'size': title_fontsize},
             framealpha=1.0, facecolor='white', edgecolor='#333333', fancybox=False, shadow=False,
             ncol=ncol, bbox_to_anchor=bbox_to_anchor, borderaxespad=0)
    
    # Explicitly set the legend frame to be fully opaque with no transparency
    frame = legend.get_frame()
    frame.set_alpha(1.0)
    frame.set_facecolor('white')
    frame.set_edgecolor('#333333')
    frame.set_linewidth(1.5)
    
    # Set zorder to ensure legend is drawn on top of everything
    legend.set_zorder(1000)


@timing_decorator
def compute_jenks_breaks(data, n_classes=9, method='smart_sample'):
    """
    Compute classification breaks using optimized methods for large raster data
    
    Args:
        data: numpy array of values
        n_classes: number of classes
        method: 'hybrid' (RECOMMENDED - FisherJenks on non-zero values) or 
                'smart_sample' (fallback - jenkspy on sample)
        
    Returns:
        List of break values
    """
    # Get non-NaN values
    valid_mask = ~np.isnan(data)
    valid_values = data[valid_mask]
    
    n_values = len(valid_values)
    print(f"    📊 Valid values: {n_values:,}")
    
    if method == 'smart_sample':
        # SMART SAMPLING: Sample intelligently based on data distribution
        # Much faster than full Jenks but maintains quality
        
        max_sample = 100000
        
        if n_values > max_sample:
            # Sample more heavily from extremes and middle
            sorted_vals = np.sort(valid_values)
            
            # Take samples from different quantiles to preserve distribution
            n_per_quantile = max_sample // 10
            samples = []
            for i in range(10):
                start_idx = int(i * n_values / 10)
                end_idx = int((i + 1) * n_values / 10)
                quantile_sample = sorted_vals[start_idx:end_idx]
                
                if len(quantile_sample) > n_per_quantile:
                    indices = np.linspace(0, len(quantile_sample) - 1, n_per_quantile, dtype=int)
                    samples.extend(quantile_sample[indices])
                else:
                    samples.extend(quantile_sample)
            
            sample_values = np.array(samples)
            print(f"    ⚡ Smart sampling: {len(sample_values):,} values from {n_values:,}")
        else:
            sample_values = valid_values
        
        # Use jenkspy on sample
        import jenkspy
        breaks = jenkspy.jenks_breaks(sample_values, n_classes=n_classes)
        return breaks
    
    else:
        raise ValueError(f"Unknown method: {method}. Use 'hybrid' or 'smart_sample'")


@timing_decorator
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
    no_bins = 8
    
    # Get data statistics for all non-NaN values (including zeros)
    valid_data_mask = ~np.isnan(data)
    
    # Use optimized Jenks classification
    breaks = compute_jenks_breaks(data, n_classes=no_bins)
    print(f"  📊 Jenks breaks ({no_bins} bins): {[f'{b:.2e}' for b in breaks]}")
    
    # Classify data using Jenks breaks
    data_viz = np.digitize(data, breaks) - 1  # Get bin indices (0-8)
    data_viz = data_viz.astype(float)
    data_viz[~valid_data_mask] = np.nan  # Restore NaN outside polygon
    
    # Create figure with proper size and white background
    fig, ax = plt.subplots(figsize=(14, 12), dpi=200)
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(1.0)
    ax.set_facecolor('white')
    
    # Get bounds for basemap in Web Mercator (EPSG:3857)
    geom_gdf = gpd.GeoDataFrame([1], geometry=[country_geom], crs=raster_crs)
    geom_web = geom_gdf.to_crs(3857)
    minx, miny, maxx, maxy = geom_web.total_bounds
    
    # Set axis limits first (required for contextily)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect('equal')
    
    # Add basemap BEFORE plotting data (so it's underneath)
    add_basemap_to_axis(ax)
    
    # Create custom colormap for n_bins (discrete classification)
    colors = ['#FFFEF5', '#FFF5C0', '#FFEB8B', '#FFD560', '#FFAF48', 
              '#F57C56', '#E24952', '#C1254E', '#8B1538']  # 9 colors for up to 8 bins
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
    cities = load_top_cities(iso3, country_gdf_for_cities, n_cities=5)
    add_city_labels(ax, cities, name_column='agglosName', fontsize=15)
    
    # Styling
    ax.axis('off')
    
    # Create categorical legend (bottom outside, multiple columns)
    create_categorical_legend(
        ax, breaks, colors,
        title='2020 GDP (USD, 2017 PPP)',
        loc='lower center',
        fontsize=11,
        title_fontsize=13,
        ncol=4,
        bbox_to_anchor=(0.5, -0.05)
    )
    
    # Tight layout with space for legend
    plt.tight_layout()
    
    # Save with explicit no-transparency settings
    filename = f"{iso3}_GDP_2020.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none', transparent=False)
    plt.close()

    print(f"  Saved visualization: {filename}")


@timing_decorator
def create_population_visualization(data, transform, country_geom, country_name, iso3, output_dir, raster_crs):
    """
    Create and save 2D Population visualization with OSM basemap context
    
    Args:
        data: Population data array (2D)
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
        print(f"  Warning: No valid population data for {country_name}")
        return
    
    # Configuration
    no_bins = 8
    
    # Get data statistics for all non-NaN values (including zeros)
    valid_data_mask = ~np.isnan(data)
    
    # Use optimized Jenks classification
    breaks = compute_jenks_breaks(data, n_classes=no_bins)
    print(f"  📊 Jenks breaks ({no_bins} bins): {[f'{b:.2e}' for b in breaks]}")
    
    # Classify data using Jenks breaks
    data_viz = np.digitize(data, breaks) - 1  # Get bin indices (0-8)
    data_viz = data_viz.astype(float)
    data_viz[~valid_data_mask] = np.nan  # Restore NaN outside polygon
    
    # Create figure with proper size and white background
    fig, ax = plt.subplots(figsize=(14, 12), dpi=200)
    fig.patch.set_facecolor('white')
    fig.patch.set_alpha(1.0)
    ax.set_facecolor('white')
    
    # Get bounds for basemap in Web Mercator (EPSG:3857)
    geom_gdf = gpd.GeoDataFrame([1], geometry=[country_geom], crs=raster_crs)
    geom_web = geom_gdf.to_crs(3857)
    minx, miny, maxx, maxy = geom_web.total_bounds
    
    # Set axis limits first (required for contextily)
    ax.set_xlim(minx, maxx)
    ax.set_ylim(miny, maxy)
    ax.set_aspect('equal')
    
    # Add basemap BEFORE plotting data (so it's underneath)
    add_basemap_to_axis(ax)
    
    # Create custom colormap for n_bins (discrete classification) - same as GDP
    colors = ['#FFFEF5', '#FFF5C0', '#FFEB8B', '#FFD560', '#FFAF48', 
              '#F57C56', '#E24952', '#C1254E', '#8B1538']  # 9 colors for up to 8 bins
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
    
    # Plot Population data with Jenks classification
    im = ax.imshow(data_viz, extent=extent, origin='upper', 
                   cmap=cmap, norm=norm, alpha=1, interpolation='none')
    
    # Add country boundary
    geom_web.boundary.plot(ax=ax, color="#4A4A4A", linewidth=2, alpha=1.0, zorder=10)
    
    # Load and add top 5 cities
    country_gdf_for_cities = gpd.GeoDataFrame([1], geometry=[country_geom], crs=raster_crs)
    cities = load_top_cities(iso3, country_gdf_for_cities, n_cities=5)
    add_city_labels(ax, cities, name_column='agglosName', fontsize=15)
    
    # Styling
    ax.axis('off')
    
    # Custom value formatter for population
    def population_formatter(start_val, end_val):
        """Format population values in thousands (K) or millions (M)"""
        if start_val >= 1e6:
            start_label = f'{start_val/1e6:.1f}M'
        elif start_val >= 1e3:
            start_label = f'{start_val/1e3:.1f}K'
        else:
            start_label = f'{start_val:.0f}'
        
        if end_val >= 1e6:
            end_label = f'{end_val/1e6:.1f}M'
        elif end_val >= 1e3:
            end_label = f'{end_val/1e3:.1f}K'
        else:
            end_label = f'{end_val:.0f}'
        
        return f'{start_label} - {end_label}'
    
    # Create categorical legend (bottom outside, multiple columns)
    create_categorical_legend(
        ax, breaks, colors,
        value_formatter=population_formatter,
        title='2020 Population',
        loc='lower center',
        fontsize=11,
        title_fontsize=13,
        ncol=4,
        bbox_to_anchor=(0.5, -0.05)
    )
    
    # Tight layout with space for legend
    plt.tight_layout()
    
    # Save with explicit no-transparency settings
    filename = f"{iso3}_POP_2020.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=200, bbox_inches='tight', facecolor='white', edgecolor='none', transparent=False)
    plt.close()

    print(f"  Saved visualization: {filename}")


def process_all_countries():
    """Main processing function"""
    
    print("=" * 80)
    print("Processing GDP and Population Data for Sub-Saharan African Countries")
    print("=" * 80)
    
    # Create output directory
    output_dir = os.path.join(project_root, 'data', 'processed', 'gdp_pop_raster_images')
    os.makedirs(output_dir, exist_ok=True)
    print(f"\nOutput directory: {output_dir}\n")
    
    # Load SSA countries
    ssa_countries = load_subsaharan_countries_dict()
    print(f"Processing {len(ssa_countries)} Sub-Saharan African countries\n")
    
    # Load GDP raster
    gdp_raster = load_gdp_data()
    
    # Load Population raster
    pop_raster = load_population_data()
    
    # Get 2020 band index for GDP (population has only 1 band)
    band_2020 = 7
    
    # Process each country
    print("\n" + "=" * 80)
    print("Processing individual countries...")
    print("=" * 80 + "\n")
    
    processed_count = 0
    skipped_count = 0

    # test = [('LSO', 'Lesotho')]
    for iso3, country_name in sorted(ssa_countries.items()):
        country_start_time = time.time()
        print(f"\n{'='*60}")
        print(f"Processing: {country_name} ({iso3})")
        print(f"{'='*60}")
        
        try:
            # Load GADM shapefile for this country
            country_gdf = load_gadm_shapefile(iso3)
            
            # === Process GDP Data ===
            # Reproject to GDP raster CRS if needed
            gdp_country_gdf = country_gdf.copy()
            if gdp_country_gdf.crs != gdp_raster.crs:
                print(f"  Reprojecting GDP from {gdp_country_gdf.crs} to {gdp_raster.crs}")
                gdp_country_gdf = gdp_country_gdf.to_crs(gdp_raster.crs)
            
            # Get the geometry
            gdp_geom = gdp_country_gdf.geometry.iloc[0]
            
            # Clip GDP raster to country boundary for 2020
            gdp_data, gdp_transform = clip_raster_to_polygon(gdp_raster, gdp_geom, band_2020)
                        
            # Create GDP visualization
            create_gdp_visualization(gdp_data, gdp_transform, gdp_geom, country_name, iso3, output_dir, gdp_raster.crs)
            
            # === Process Population Data ===
            # Reproject to population raster CRS if needed
            pop_country_gdf = country_gdf.copy()
            if pop_country_gdf.crs != pop_raster.crs:
                print(f"  Reprojecting Population from {pop_country_gdf.crs} to {pop_raster.crs}")
                pop_country_gdf = pop_country_gdf.to_crs(pop_raster.crs)
            
            # Get the geometry
            pop_geom = pop_country_gdf.geometry.iloc[0]
            
            # Clip population raster to country boundary (single band, so band_index=1)
            pop_data, pop_transform = clip_raster_to_polygon(pop_raster, pop_geom, band_index=1)
            
            # Create population visualization
            create_population_visualization(pop_data, pop_transform, pop_geom, country_name, iso3, output_dir, pop_raster.crs)
            
            processed_count += 1
            
            # Print total time for this country
            country_elapsed = time.time() - country_start_time
            print(f"\n✅ Total time for {country_name}: {country_elapsed:.2f}s ({country_elapsed/60:.1f} min)")
            
        except Exception as e:
            print(f"  ❌ Error processing {country_name}: {str(e)}")
            import traceback
            traceback.print_exc()
            skipped_count += 1
            continue
    
    # Close rasters
    gdp_raster.close()
    pop_raster.close()
    
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
