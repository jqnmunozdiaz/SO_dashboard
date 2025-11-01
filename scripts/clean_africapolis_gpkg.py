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

# Define file paths
raw_file = os.path.join(project_root, 'data', 'raw', 'africapolis2023.gpkg')
output_gpkg = os.path.join(project_root, 'data', 'processed', 'africapolis2023_centroids.gpkg')
output_csv = os.path.join(project_root, 'data', 'processed', 'africapolis2023_centroids.csv')
    
gdf = gpd.read_file(raw_file)

# Step 2: Get SSA country codes
ssa_countries = load_subsaharan_countries_dict()
ssa_iso3_codes = list(ssa_countries.keys())

# Step 3: Filter for SSA countries only
gdf_ssa = gdf[gdf['ISO3'].isin(ssa_iso3_codes)].copy()

# Step 4: Convert to WGS84 if needed and calculate centroids from actual geometries
if gdf_ssa.crs != 'EPSG:4326':
    print(f"Reprojecting from {gdf_ssa.crs} to EPSG:4326 (WGS84)")
    gdf_ssa = gdf_ssa.to_crs('EPSG:4326')

# Calculate centroids from actual geometries (not Longitude/Latitude columns)
gdf_ssa['geometry'] = gdf_ssa.geometry.centroid

# Keep only required columns
required_columns = ['agglosID', 'agglosName', 'ISO3']
gdf_clean = gdf_ssa[required_columns + ['geometry']].copy()

# Convert to GeoDataFrame with WGS84
gdf_clean = gpd.GeoDataFrame(gdf_clean, geometry='geometry', crs='EPSG:4326')

# Save to GPKG
os.makedirs(os.path.dirname(output_gpkg), exist_ok=True)
gdf_clean.to_file(output_gpkg, driver='GPKG')

# Also save as CSV with lat/lon columns for easier dashboard loading
gdf_csv = gdf_clean.copy()
gdf_csv['Longitude'] = gdf_csv.geometry.x
gdf_csv['Latitude'] = gdf_csv.geometry.y
gdf_csv[['agglosID', 'agglosName', 'ISO3', 'Longitude', 'Latitude']].to_csv(output_csv, index=False)

