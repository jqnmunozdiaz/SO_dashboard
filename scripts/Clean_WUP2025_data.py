"""
Process WUP2025 data files
- Filter DEGURBA Level1 data by columns and categories
- Filter Population by size class data by columns
- Filter for Sub-Saharan Africa countries only
- Save processed files to data/processed/WUP/
"""

import pandas as pd
import os
import sys

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)

# Import centralized country utilities
from src.utils.country_utils import load_wb_regional_classifications

# Load World Bank regional classifications
afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()

"""
Process WUP2025-DB-DEGURBA-Level1-Population-Surface-Data.csv
Keep only columns: ISO3_Code, Category, Year, Pop
Delete rows where Category is 'Cities and Towns' or 'Total'
Add regional aggregates for SSA, AFE, AFW
"""

# Read raw data
raw_path = os.path.join(project_root, 'data', 'raw', 'WUP2025', 
                        'WUP2025-DB-DEGURBA-Level1-Population-Surface-Data.csv')
df = pd.read_csv(raw_path, low_memory=False)

# Keep only specified columns
df = df[['ISO3_Code', 'Category', 'Year', 'Pop']]

# Filter for Sub-Saharan African countries only
df = df[df['ISO3_Code'].isin(ssa_countries)]

# Delete rows where Category is 'Cities and Towns' or 'Total'
df = df[~df['Category'].isin(['Cities and Towns', 'Total'])]

# Convert population from thousands to actual values
df['Pop'] = df['Pop'] * 1000

# Create regional aggregates
regional_data = []
region_mappings = {
    'AFE': afe_countries,
    'AFW': afw_countries,
    'SSA': ssa_countries
}

# Group by category and year for aggregation
for category in df['Category'].unique():
    for year in df['Year'].unique():
        # Filter data for this category and year
        category_year_data = df[(df['Category'] == category) & (df['Year'] == year)]
        
        # Calculate aggregates for each region
        for region_code, country_list in region_mappings.items():
            region_data = category_year_data[category_year_data['ISO3_Code'].isin(country_list)]
            if not region_data.empty:
                region_row = {
                    'ISO3_Code': region_code,
                    'Category': category,
                    'Year': year,
                    'Pop': region_data['Pop'].sum()
                }
                regional_data.append(region_row)

# Convert regional data to DataFrame and append to main data
if regional_data:
    regional_df = pd.DataFrame(regional_data)
    df = pd.concat([df, regional_df], ignore_index=True)

# Sort by year, ISO3_Code, and category
df = df.sort_values(['Year', 'ISO3_Code', 'Category'])

# Create output directory if it doesn't exist
output_dir = os.path.join(project_root, 'data', 'processed', 'WUP')
os.makedirs(output_dir, exist_ok=True)

# Save processed data
output_path = os.path.join(output_dir, 'WUP2025_Level1_Population_Surface_processed.csv')
df.to_csv(output_path, index=False)


"""
Process WUP2025-DB-DEGURBA-Population-by-size-class-of-cities.csv
Keep only columns: ISO3_Code, Category, Year, Cities, Pop
Add regional aggregates for SSA, AFE, AFW
"""

# Read raw data
raw_path = os.path.join(project_root, 'data', 'raw', 'WUP2025', 
                        'WUP2025-DB-DEGURBA-Population-by-size-class-of-cities.csv')
df = pd.read_csv(raw_path, low_memory=False)

# Keep only specified columns
df = df[['ISO3_Code', 'Category', 'Year', 'Cities', 'Pop']]

# Filter for Sub-Saharan African countries only
df = df[df['ISO3_Code'].isin(ssa_countries)]

# Convert population from thousands to actual values
df['Pop'] = df['Pop'] * 1000

# Create regional aggregates
regional_data = []
region_mappings = {
    'AFE': afe_countries,
    'AFW': afw_countries,
    'SSA': ssa_countries
}

# Group by category and year for aggregation
for category in df['Category'].unique():
    for year in df['Year'].unique():
        # Filter data for this category and year
        category_year_data = df[(df['Category'] == category) & (df['Year'] == year)]
        
        # Calculate aggregates for each region
        for region_code, country_list in region_mappings.items():
            region_data = category_year_data[category_year_data['ISO3_Code'].isin(country_list)]
            if not region_data.empty:
                region_row = {
                    'ISO3_Code': region_code,
                    'Category': category,
                    'Year': year,
                    'Cities': region_data['Cities'].sum(),
                    'Pop': region_data['Pop'].sum()
                }
                regional_data.append(region_row)

# Convert regional data to DataFrame and append to main data
if regional_data:
    regional_df = pd.DataFrame(regional_data)
    df = pd.concat([df, regional_df], ignore_index=True)

# Sort by year, ISO3_Code, and category
df = df.sort_values(['Year', 'ISO3_Code', 'Category'])

# Create output directory if it doesn't exist
output_dir = os.path.join(project_root, 'data', 'processed', 'WUP')
os.makedirs(output_dir, exist_ok=True)

# Save processed data
output_path = os.path.join(output_dir, 'WUP2025_Population_by_Size_Class_processed.csv')
df.to_csv(output_path, index=False)
