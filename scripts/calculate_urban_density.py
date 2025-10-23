#%%
"""
Calculate built-up per capita by country and year from Africapolis GHSL 2023 data.

This script:
1. Loads population and built surface data from separate CSV files
2. Aggregates total urban population and total built-up area by country and year
3. Calculates built-up per capita (m² per person)
4. Outputs the aggregated dataset to a CSV file
"""

import pandas as pd
import os
import sys
from src.utils.country_utils import load_wb_regional_classifications

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Define file paths
pop_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ghsl2023_pop.csv')
built_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ghsl2023_built_s.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'built_up_per_capita_m2_by_country_year.csv')

pop_df = pd.read_csv(pop_file)
built_df = pd.read_csv(built_file)

# Merge datasets on agglosID and ghsl_year
df = pd.merge(
    pop_df[['ISO3', 'agglosID', 'ghsl_year', 'ghsl_total_pop_#']],
    built_df[['agglosID', 'ghsl_year', 'ghsl_total_built_s_km2']],
    on=['agglosID', 'ghsl_year'],
    how='inner'
)

# Rename columns for clarity
df = df.rename(columns={
    'ghsl_year': 'year',
    'ghsl_total_pop_#': 'population',
    'ghsl_total_built_s_km2': 'built_up_km2'
})

# Remove rows with missing values
df = df.dropna(subset=['ISO3', 'year', 'population', 'built_up_km2'])

# Aggregate by country and year
agg_df = df.groupby(['ISO3', 'year']).agg({
    'population': 'sum',
    'built_up_km2': 'sum'
}).reset_index()

# Calculate built-up per capita (m² per person)
agg_df['built_up_per_capita_m2'] = (agg_df['built_up_km2'] / agg_df['population']) * 1000000

# Load World Bank regional classifications
afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()

# Calculate regional aggregates
regional_data = []

# Define regions for the loop
regions = [
    ('AFE', afe_countries),
    ('AFW', afw_countries),
    ('SSA', ssa_countries)
]

for year in agg_df['year'].unique():
    year_data = agg_df[agg_df['year'] == year]
    
    for region_code, countries in regions:
        region_data = year_data[year_data['ISO3'].isin(countries)]
        if not region_data.empty:
            pop = region_data['population'].sum()
            built = region_data['built_up_km2'].sum()
            if pop > 0:
                regional_data.append({
                    'ISO3': region_code,
                    'year': year,
                    'population': pop,
                    'built_up_km2': built,
                    'built_up_per_capita_m2': (built / pop) * 1000000
                })

# Append regional data to country data
if regional_data:
    regional_df = pd.DataFrame(regional_data)
    agg_df = pd.concat([agg_df, regional_df], ignore_index=True)

# Sort by country and year
agg_df = agg_df.sort_values(['ISO3', 'year'])

# Save to CSV
os.makedirs(os.path.dirname(output_file), exist_ok=True)
agg_df.to_csv(output_file, index=False)
