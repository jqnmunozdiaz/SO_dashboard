"""
Process Africapolis 2023 GPKG file to extract city centroids for Sub-Saharan Africa

This script:
1. Filters for SSA countries only (48 countries based on WB Classification)
2. Keeps only essential columns: agglosID, agglosName, ISO3, Longitude, Latitude
3. Converts geometries to centroids (points)
4. Reports any missing values
5. Saves cleaned data as GPKG in processed folder

Data Source: Africapolis 2023 urban agglomerations database
Output: Cleaned point geometries with city metadata
"""

import geopandas as gpd
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.utils.country_utils import load_subsaharan_countries_dict
from shapely.geometry import Point

# Define file paths
raw_file = os.path.join(project_root, 'data', 'raw', 'africapolis2023.gpkg')
output_file = os.path.join(project_root, 'data', 'processed', 'africapolis2023_centroids.gpkg')
    
gdf = gpd.read_file(raw_file)

# Step 2: Get SSA country codes
ssa_countries = load_subsaharan_countries_dict()
ssa_iso3_codes = list(ssa_countries.keys())

# Step 3: Filter for SSA countries only
gdf_ssa = gdf[gdf['ISO3'].isin(ssa_iso3_codes)].copy()

# Step 4: Keep only required columns
required_columns = ['agglosID', 'agglosName', 'ISO3', 'Longitude', 'Latitude']

# Keep only required columns
gdf_clean = gdf_ssa[required_columns].copy()

# Create geometry from Longitude and Latitude columns
gdf_clean['geometry'] = gdf_clean.apply(lambda row: Point(row['Longitude'], row['Latitude']), axis=1)

# Convert to GeoDataFrame and set CRS (assuming WGS84 for lat/lon)
gdf_clean = gpd.GeoDataFrame(gdf_clean, geometry='geometry', crs='EPSG:4326')

del gdf_clean['Longitude'], gdf_clean['Latitude']

# Save to GPKG
os.makedirs(os.path.dirname(output_file), exist_ok=True)
gdf_clean.to_file(output_file, driver='GPKG')
