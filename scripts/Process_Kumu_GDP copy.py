"""
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
from rasterio.transform import rowcol
from rasterio import transform as rio_transform
import geopandas as gpd
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
import matplotlib.colors as mcolors
import contextily as cx
from PIL import Image
from scipy.ndimage import gaussian_filter
import warnings

# Add project root to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from src.utils.country_utils import load_subsaharan_countries_dict

# Suppress warnings
warnings.filterwarnings('ignore')


def load_gdp_data():
    """Load GDP raster and polygon data"""
    
    # Paths to data files - using high-resolution 30 arcsec raster
    raster_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 
                               'rast_gdpTot_1990_2020_30arcsec.tif')
    polygon_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu',
                                'polyg_adm0_gdp_perCapita_1990_2022.gpkg')

    
    # Load polygon data
    polygons = gpd.read_file(polygon_path)
    
    # Open raster data
    raster = rasterio.open(raster_path)
    
    return raster, polygons


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
    # Clip the raster to the polygon and set outside to 0 (not NaN)
    out_image, out_transform = mask(
        raster,
        [polygon_geom],
        crop=True,
        filled=True,
        all_touched=True,
        nodata=0.0,
    )
    
    # Extract the specific band (out_image shape is (bands, H, W))
    band_data = out_image[band_index - 1]  # Convert to 0-indexed
    # Ensure dtype is float for later processing
    band_data = band_data.astype(float, copy=False)
    
    return band_data, out_transform


def create_gdp_visualization(
    data: np.ndarray,
    transform,
    country_geom,
    country_name: str,
    iso3: str,
    output_dir: str,
    raster_crs=None,
) -> None:
    """
    Render a professional 3D view of a clipped raster with a flat basemap at the bottom.

    - Uses Plotly for smooth lighting and export-quality rendering
    - Preserves NaN outside the polygon so nothing is drawn beyond the country
    - Adds the country polygon outline on the base for context

    Args:
        data: 2D array of GDP values clipped to country extent. Must keep NaN outside polygon
        transform: Affine transform returned by rasterio.mask (out_transform) for the clipped raster
        country_geom: Shapely geometry for the country in the same CRS as raster
        country_name: Country name label
        iso3: ISO3 code used in filename
        output_dir: Output folder path
    """

    # Validate data contains something to plot
    valid_mask = np.isfinite(data) & (data > 0)
    if not np.any(valid_mask):
        print(f"  Warning: No valid GDP data for {country_name}")
        return

    # Downsample for performance if very large
    h_full, w_full = data.shape
    downsample = max(1, max(h_full, w_full) // 400)
    data_viz = data[::downsample, ::downsample]
    valid_mask_viz = valid_mask[::downsample, ::downsample]

    # Mask-preserving Gaussian smoothing (avoid bleeding across NaN)
    data_filled = np.nan_to_num(data_viz, nan=0.0)
    mask_f = valid_mask_viz.astype(float)
    sigma = 1.4
    num = gaussian_filter(data_filled, sigma=sigma)
    den = gaussian_filter(mask_f, sigma=sigma)
    with np.errstate(divide='ignore', invalid='ignore'):
        smooth = np.where(den > 1e-6, num / den, np.nan)

    # Non-log scaling for spike effect (gentle power transform)
    smooth[smooth < 0] = 0
    z = np.power(smooth, 0.55)

    # Normalize z to a consistent range (percentile based)
    z_valid = z[np.isfinite(z)]
    z99 = np.percentile(z_valid, 99) if z_valid.size else 1.0
    z = (z / (z99 if z99 > 0 else 1.0)) * 100.0
    z[~valid_mask_viz] = np.nan

    # Coordinate grids in pixel space
    h, w = z.shape
    x = np.arange(w)
    y = np.arange(h)

    # Base layer (country footprint) at z=0, NaN outside
    base_z = np.where(valid_mask_viz, 0.0, np.nan)

    # Build textured basemap with OSM using contextily
    # Compute bounds in Web Mercator (EPSG:3857)
    geom_series = gpd.GeoSeries([country_geom], crs=raster_crs)
    geom_web = geom_series.to_crs(3857)
    wmin, smin, wmax, smax = geom_web.total_bounds

    # Fetch OSM tile image for bounds
    osm_img, osm_ext = cx.bounds2img(wmin, smin, wmax, smax, source=cx.providers.OpenStreetMap.Mapnik)
    # Resize OSM image to (h, w)
    osm_pil = Image.fromarray(osm_img)
    osm_resized = np.asarray(osm_pil.resize((w, h), resample=Image.BILINEAR))
    # Normalize to [0,1] and ensure RGBA
    if osm_resized.shape[2] == 3:
        # add alpha channel
        alpha = np.full((h, w, 1), 255, dtype=np.uint8)
        osm_resized = np.concatenate([osm_resized, alpha], axis=2)
    facecolors = (osm_resized / 255.0)

    # Matplotlib 3D rendering
    fig = plt.figure(figsize=(14, 11), dpi=200)
    ax = fig.add_subplot(111, projection='3d')

    # Plot basemap as a flat textured plane at z=0
    X, Y = np.meshgrid(np.arange(w), np.arange(h))
    ax.plot_surface(X, Y, np.zeros_like(base_z), rstride=1, cstride=1, facecolors=facecolors,
                    linewidth=0, antialiased=True, shade=False, alpha=0.95)

    # GDP surface
    cmap = mcolors.LinearSegmentedColormap.from_list(
        'gdp_pro', ['#FFF5D6', '#CBE6C8', '#8EC9BE', '#57A7B1', '#2E7EA0', '#1F5F86', '#143D5C'], N=256
    )
    norm = mcolors.Normalize(vmin=np.nanpercentile(z, 2), vmax=np.nanpercentile(z, 98))
    surf = ax.plot_surface(X, Y, z, cmap=cmap, norm=norm, linewidth=0, antialiased=True,
                           rstride=1, cstride=1, shade=True, alpha=0.96)

    # Outline country border on base
    polys = [country_geom] if country_geom.geom_type == 'Polygon' else list(country_geom.geoms)
    for poly in polys:
        xs, ys = np.array(poly.exterior.coords).T
        rows, cols = rowcol(transform, xs, ys)
        cols = np.clip(np.array(cols) // downsample, 0, w - 1)
        rows = np.clip(np.array(rows) // downsample, 0, h - 1)
        ax.plot(cols, rows, zs=0.5, zdir='z', color='#9E8155', linewidth=2.5, alpha=0.9)
        for interior in poly.interiors:
            xi, yi = np.array(interior.coords).T
            ri, ci = rowcol(transform, xi, yi)
            ci = np.clip(np.array(ci) // downsample, 0, w - 1)
            ri = np.clip(np.array(ri) // downsample, 0, h - 1)
            ax.plot(ci, ri, zs=0.5, zdir='z', color='#9E8155', linewidth=1.8, alpha=0.9)

    # Camera from south-west: lower-left looking to NE
    ax.view_init(elev=28, azim=225)

    # Clean aesthetics
    ax.grid(False)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_xlabel(''); ax.set_ylabel(''); ax.set_zlabel('')
    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.fill = False
        axis.pane.set_edgecolor('none')
        try:
            axis.line.set_color('none')
        except Exception:
            pass
    ax.set_facecolor('white')
    fig.patch.set_facecolor('white')

    # Colorbar
    mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=10, pad=0.08)
    cbar.set_label('GDP concentration (relative)', rotation=270, labelpad=18, fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    plt.title(f'{country_name} – GDP concentration (2020)', fontsize=14, color='#2E2E2E')
    plt.tight_layout()

    # Save
    filename = f"{iso3}_{country_name.replace(' ', '_')}_GDP_2020_3D.png"
    filepath = os.path.join(output_dir, filename)
    plt.savefig(filepath, dpi=220, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {filename}")


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
    
    # Load GDP data
    raster, polygons = load_gdp_data()
    
    # Get 2020 band index
    band_2020 = get_2020_band_index(raster)
    
    # Ensure polygons are in same CRS as raster
    if polygons.crs != raster.crs:
        print(f"\nReprojecting polygons from {polygons.crs} to {raster.crs}")
        polygons = polygons.to_crs(raster.crs)
    
    # Process each country
    print("\n" + "=" * 80)
    print("Processing individual countries...")
    print("=" * 80 + "\n")
    
    processed_count = 0
    skipped_count = 0

    for iso3, country_name in [('LSO', 'Lesotho')]: #sorted(ssa_countries.items()):
        print(f"Processing: {country_name} ({iso3})")
        
        # Find country polygon (column is 'iso3' in this dataset)
        if 'iso3' not in polygons.columns:
            print(f"  Error: 'iso3' column not found in polygon data")
            skipped_count += 1
            continue
            
        country_polygon = polygons[polygons['iso3'] == iso3]
        
        if country_polygon.empty:
            print(f"  Warning: No polygon found for {country_name} ({iso3})")
            skipped_count += 1
            continue
        
        try:
            # Get the geometry
            geom = country_polygon.geometry.iloc[0]
            
            # Clip raster to country boundary for 2020
            gdp_data, out_transform = clip_raster_to_polygon(raster, geom, band_2020)
            
            # Create visualization with geometry and transform
            create_gdp_visualization(
                gdp_data,
                out_transform,
                geom,
                country_name,
                iso3,
                output_dir,
                raster_crs=raster.crs,
            )
            
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
