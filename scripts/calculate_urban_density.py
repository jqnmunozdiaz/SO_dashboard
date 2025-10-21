#%%
"""
Calculate urban population density by country and year from Africapolis GHSL 2023 data.

This script:
1. Loads population and built surface data from separate CSV files
2. Aggregates total urban population and total built-up area by country and year
3. Calculates population density (population per km²)
4. Outputs the aggregated dataset to a CSV file
"""

import pandas as pd
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Define file paths
pop_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ghsl2023_pop.csv')
built_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ghsl2023_built_s.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'urban_density_by_country_year.csv')

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

# Calculate population density (population per km²)
agg_df['population_density'] = agg_df['population'] / agg_df['built_up_km2']

# Load World Bank regional classifications
from src.utils.country_utils import load_wb_regional_classifications

afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()

# Calculate regional aggregates
regional_data = []

for year in agg_df['year'].unique():
    year_data = agg_df[agg_df['year'] == year]
    
    # AFE (Eastern & Southern Africa)
    afe_data = year_data[year_data['ISO3'].isin(afe_countries)]
    if not afe_data.empty:
        afe_pop = afe_data['population'].sum()
        afe_built = afe_data['built_up_km2'].sum()
        if afe_built > 0:
            regional_data.append({
                'ISO3': 'AFE',
                'year': year,
                'population': afe_pop,
                'built_up_km2': afe_built,
                'population_density': afe_pop / afe_built
            })
    
    # AFW (Western & Central Africa)
    afw_data = year_data[year_data['ISO3'].isin(afw_countries)]
    if not afw_data.empty:
        afw_pop = afw_data['population'].sum()
        afw_built = afw_data['built_up_km2'].sum()
        if afw_built > 0:
            regional_data.append({
                'ISO3': 'AFW',
                'year': year,
                'population': afw_pop,
                'built_up_km2': afw_built,
                'population_density': afw_pop / afw_built
            })
    
    # SSA (Sub-Saharan Africa = AFE + AFW)
    ssa_data = year_data[year_data['ISO3'].isin(ssa_countries)]
    if not ssa_data.empty:
        ssa_pop = ssa_data['population'].sum()
        ssa_built = ssa_data['built_up_km2'].sum()
        if ssa_built > 0:
            regional_data.append({
                'ISO3': 'SSA',
                'year': year,
                'population': ssa_pop,
                'built_up_km2': ssa_built,
                'population_density': ssa_pop / ssa_built
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
