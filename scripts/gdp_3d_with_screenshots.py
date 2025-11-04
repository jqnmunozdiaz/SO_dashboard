"""
3D GDP Column Visualization with Automated Screenshot Export

This script creates 3D column visualizations with basemap and automatically
exports them as PNG images using Selenium WebDriver.
"""

import os
import sys
import rasterio
from rasterio.mask import mask
import geopandas as gpd
import numpy as np
import pandas as pd
from rasterio.features import rasterize
import pydeck as pdk
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Add project root to path for imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.insert(0, project_root)

from src.utils.country_utils import load_subsaharan_countries_dict

# Configuration
YEAR = 2020
BAND_INDEX = 7

# Map style - use CARTO basemap (no API key required) Options: 'dark', 'light', 'positron', 'voyager'
MAP_STYLE = 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'

# Image export settings
WAIT_TIME = 5  # Seconds to wait for map to load

# Country-specific visualization settings
# Adjust zoom, pitch, bearing, elevation_scale, latitude, longitude, and image dimensions per country as needed
# If latitude/longitude not specified, will use mean of data points
COUNTRY_SETTINGS = {
    'AGO': {'zoom': 5.7, 'pitch': 50, 'bearing': 10, 'elevation_scale': 300, 'width': 1560, 'height': 1080},
    'BDI': {'zoom': 8, 'pitch': 50, 'bearing': 10, 'elevation_scale': 100, 'width': 1280, 'height': 1080},
    'BEN': {'zoom': 6.7, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1080, 'height': 1080},
    'BFA': {'zoom': 6.7, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1720, 'height': 1080},
    'BWA': {'zoom': 6, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1720, 'height': 1080},
    'CAF': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'CIV': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'CMR': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 100, 'width': 1920, 'height': 1080},
    'COD': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 300, 'width': 1920, 'height': 1080},
    'COG': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'COM': {'zoom': 9.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 30, 'width': 1720, 'height': 1080},
    'CPV': {'zoom': 8.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1720, 'height': 1080},
    'ERI': {'zoom': 7.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'ETH': {'zoom': 5.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'GAB': {'zoom': 6.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'GHA': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'GIN': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'GMB': {'zoom': 8.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'GNB': {'zoom': 7.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'GNQ': {'zoom': 7.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'KEN': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'LBR': {'zoom': 7.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'LSO': {'zoom': 7.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'MDG': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'MLI': {'zoom': 5.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'MOZ': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'MRT': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'MUS': {'zoom': 9.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'MWI': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'NAM': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'NER': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'NGA': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'RWA': {'zoom': 8.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'SDN': {'zoom': 5.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'SEN': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'SLE': {'zoom': 7.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'SOM': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'SSD': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'STP': {'zoom': 9.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'SWZ': {'zoom': 8.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'TCD': {'zoom': 5.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'TGO': {'zoom': 7.0, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'TZA': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'UGA': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'ZAF': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'ZMB': {'zoom': 5.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
    'ZWE': {'zoom': 6.5, 'pitch': 50, 'bearing': 10, 'elevation_scale': 250, 'width': 1920, 'height': 1080},
}

COUNTRIES = ['BEN']  # Test with just Benin first
COUNTRIES = list(COUNTRY_SETTINGS.keys())  # Process all countries in settings

def load_gdp_data():
    """Load GDP raster data"""
    raster_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 
                               'rast_gdpTot_1990_2020_30arcsec.tif')
    raster = rasterio.open(raster_path)
    print(f"GDP Raster loaded: {raster.count} bands, CRS: {raster.crs}")
    return raster


def load_gadm_shapefile(iso3):
    """Load GADM shapefile for a specific country"""
    gadm_base = r'C:\Users\jqnmu\OneDrive\World_Bank_DRM\Datasets\GADM4.1'
    shapefile_path = os.path.join(gadm_base, iso3, f'gadm41_{iso3}_0.shp')
    
    if not os.path.exists(shapefile_path):
        raise FileNotFoundError(f"GADM shapefile not found: {shapefile_path}")
    
    gdf = gpd.read_file(shapefile_path)
    return gdf


def clip_raster_to_polygon(raster, polygon_geom, band_index):
    """Clip raster to polygon boundary and extract specific band"""
    out_image, out_transform = mask(
        raster,
        [polygon_geom],
        crop=True,
        filled=True,
        all_touched=True,
        nodata=np.nan
    )
    
    band_data = out_image[band_index - 1]
    band_data = band_data.astype(float, copy=False)
    
    height, width = band_data.shape
    polygon_mask = rasterize(
        [polygon_geom],
        out_shape=(height, width),
        transform=out_transform,
        all_touched=True,
        fill=0,
        default_value=1
    ).astype(bool)
    
    band_data = np.where(polygon_mask & np.isnan(band_data), 0.0, band_data)
    return band_data, out_transform


def raster_to_dataframe(data, transform, downsample=1):
    """Convert raster data to DataFrame with lat/lon coordinates"""
    height, width = data.shape
    
    rows = np.arange(0, height, downsample)
    cols = np.arange(0, width, downsample)
    
    col_coords, row_coords = np.meshgrid(cols, rows)
    
    col_flat = col_coords.flatten()
    row_flat = row_coords.flatten()
    
    values = data[::downsample, ::downsample].flatten()
    
    lon, lat = rasterio.transform.xy(transform, row_flat, col_flat)
    
    df = pd.DataFrame({
        'lon': lon,
        'lat': lat,
        'values': values
    })

    df = df[df['values'].notna()] 
    df['values'] = df['values'] / df['values'].max()

    return df


def create_column_visualization(df, country_name, iso3, settings, map_style=MAP_STYLE):
    """Create 3D column visualization with basemap context"""
    
    # Use custom lat/lon if provided, otherwise use mean of data points
    latitude = settings.get('latitude', df['lat'].mean())
    longitude = settings.get('longitude', df['lon'].mean())
    
    print(latitude, longitude)
    
    view_state = pdk.ViewState(
        latitude=latitude,
        longitude=longitude,
        zoom=settings['zoom'],
        pitch=settings['pitch'],
        bearing=settings['bearing']
    )
    
    color_range_hexagons = [
            [253, 231, 37],    # Yellow (low)
            [170, 220, 50],    # Yellow-green
            [94, 201, 98],     # Green
            [33, 145, 140],    # Teal
            [46, 114, 161],    # Light blue
            [59, 82, 139],     # Blue
            [49, 42, 123],     # Dark blue-purple
            [68, 1, 84]        # Dark purple (high)
        ]
    
    # HexagonLayer aggregates points into hexagons
    # Use getElevationWeight and elevationAggregation instead of get_elevation
    column_layer = pdk.Layer(
        'HexagonLayer',
        data=df,
        get_position='[lon, lat]',
        get_elevation_weight='values',  # Use GDP value as weight
        elevation_aggregation='SUM',  # Sum GDP values in each hexagon
        get_color_weight='values',  # Color also based on GDP
        color_aggregation='SUM',
        elevation_scale=settings['elevation_scale'],  # Country-specific height scaling
        radius=1000,  # Hexagon radius in meters
        extruded=True,
        pickable=True,
        auto_highlight=True,
        color_range=color_range_hexagons
    )
    
    deck = pdk.Deck(
        layers=[column_layer],  # Border layer first (underneath)
        initial_view_state=view_state,
        map_style=map_style
    )
    
    return deck


def export_to_png_selenium(html_path, output_path, width=1920, height=1080):
    """
    Export visualization to PNG using Selenium WebDriver
    
    Args:
        html_path: Path to HTML file
        output_path: Path to save PNG
        width: Screenshot width
        height: Screenshot height
    """
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in background
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(f'--window-size={width},{height}')
    
    # Initialize driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Load HTML file
    file_url = f'file:///{os.path.abspath(html_path).replace(os.sep, "/")}'
    print(f"  Loading visualization... Waiting {WAIT_TIME} seconds for map to load...")
    driver.get(file_url)
    
    # Wait for map to render
    time.sleep(WAIT_TIME)
    
    # Take screenshot
    driver.save_screenshot(output_path)
    
    driver.quit()
    print(f"  ✓ Image saved: {output_path}")
    return True

def main():
    """Main execution function"""
    
    # Create output directories
    output_dir = os.path.join(project_root, 'data')
    html_dir = os.path.join(output_dir, 'raw', 'html_3d_files')
    img_dir = os.path.join(output_dir, 'processed', 'gdp_pop_raster_images_3d')
    os.makedirs(html_dir, exist_ok=True)
    os.makedirs(img_dir, exist_ok=True)
    
    ssa_countries = load_subsaharan_countries_dict()
    
    gdp_raster = load_gdp_data()
    
    for iso3 in COUNTRIES:
        country_name = ssa_countries.get(iso3, iso3)
        print(f"\n{'='*60}")
        print(f"Processing: {country_name} ({iso3})")
        print(f"{'='*60}")
        
        # Get country-specific settings or use defaults
        settings = COUNTRY_SETTINGS.get(iso3, {
            'zoom': 0, 'pitch': 50, 'bearing': 0, 'elevation_scale': 100, 'width': 1920, 'height': 1080
        })
        print(f"  Settings: zoom={settings['zoom']}, pitch={settings['pitch']}, bearing={settings['bearing']}, elevation_scale={settings['elevation_scale']}, size={settings['width']}x{settings['height']}")
        if settings['zoom'] == 0:
            continue
        
        country_gdf = load_gadm_shapefile(iso3)
        
        gdp_country_gdf = country_gdf.copy()
        
        gdp_geom = gdp_country_gdf.geometry.iloc[0]
        
        gdp_data, gdp_transform = clip_raster_to_polygon(gdp_raster, gdp_geom, BAND_INDEX)
        df = raster_to_dataframe(gdp_data, gdp_transform)
        deck = create_column_visualization(df, country_name, iso3, settings)
        
        # Save HTML
        html_filename = f'{iso3}_gdp_3d.html'
        html_path = os.path.join(html_dir, html_filename)
        deck.to_html(html_path)
        print(f"  HTML saved: {html_path}")
        
        # Export to PNG using Selenium
        img_filename = f'{iso3}_GDP_2020.png'
        img_path = os.path.join(img_dir, img_filename)
        
        success = export_to_png_selenium(html_path, img_path, width=settings['width'], height=settings['height'])
        os.remove(html_path)
        if success:
            print(f"\n✓ Completed: {country_name}")
    
    gdp_raster.close()
    
if __name__ == "__main__":
    main()
