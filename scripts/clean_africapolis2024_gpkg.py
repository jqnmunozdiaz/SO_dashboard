#%%
import pandas as pd
import geopandas as gpd
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.utils.country_utils import load_subsaharan_countries_dict
from src.utils.city_helpers import get_city_size_category

# Define file paths
raw_file = os.path.join(project_root, 'data', 'raw', 'Africapolis_GIS_2024.gpkg')
output_csv = os.path.join(project_root, 'data', 'processed', 'cities_individual.csv')

gdf = gpd.read_file(raw_file)

# Step 2: Get SSA country codes
ssa_countries = load_subsaharan_countries_dict()
ssa_iso3_codes = list(ssa_countries.keys())

# Step 3: Filter for SSA countries only
gdf = gdf[gdf['ISO3'].isin(ssa_iso3_codes)]
gdf = gdf[gdf['Select_Geometry_Year'] == 2020]

gdf = gdf[['Agglomeration_Name', 'ISO3', 'Population_2015', 'Population_2020', 'Population_2025', 'Population_2030', 'Population_2035']]

# Convert population columns to int64
population_cols = [col for col in gdf.columns if col.startswith('Population_')]

# Rename columns
gdf = gdf.rename(columns={
    'ISO3': 'Country Code',
    'Agglomeration_Name': 'City Name'
})

# Melt the Population columns into long format
gdf = pd.melt(
    gdf,
    id_vars=['City Name', 'Country Code'],
    value_vars=population_cols,
    var_name='Year',
    value_name='Population'
)

gdf['Population'] = gdf['Population'] / 1000
# Extract year from 'Year' column (remove 'Population_' prefix and convert to int)
gdf['Year'] = gdf['Year'].str.replace('Population_', '').astype(int)

# Create 'Size Category' based on population ranges (population is in thousands)
gdf['Size Category'] = gdf['Population'].apply(get_city_size_category)
# Save to CSV
gdf.to_csv(output_csv, index=False)