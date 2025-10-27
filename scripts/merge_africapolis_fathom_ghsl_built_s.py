#%%
"""
Merge Africapolis Fathom and GHSL Built-up Area and Population Data

This script processes and merges:
- africapolis_ftm3_current_ghsl2023_built_s.csv with africapolis_ghsl2023_built_s.csv
- africapolis_ftm3_current_ghsl2023_pop.csv with africapolis_ghsl2023_pop.csv
Then merges both datasets (built-up and population) on agglosID and ghsl_year
"""

import pandas as pd
import os

# Define file paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# files
fathom_built_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ftm3_current_ghsl2023_built_s.csv')
ghsl_built_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ghsl2023_built_s.csv')
fathom_pop_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ftm3_current_ghsl2023_pop.csv')
ghsl_pop_file = os.path.join(project_root, 'data', 'raw', 'Fathom3-GHSL', 'africapolis_ghsl2023_pop.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'africapolis_fathom_ghsl_merged.csv')
output_file_simple = os.path.join(project_root, 'data', 'processed', 'africapolis_ghsl_simple.csv')
output_file_5cities = os.path.join(project_root, 'data', 'processed', 'africapolis_fathom_ghsl_merged_5citiespercountry.csv')

# Load fathom built-up data
fathom_built_df = pd.read_csv(fathom_built_file)

# Filter for FLUVIAL_PLUVIAL_DEFENDED only
fathom_built_df = fathom_built_df[fathom_built_df['flood_type'] == 'FLUVIAL_PLUVIAL_DEFENDED']

# Drop unnecessary columns
fathom_built_df = fathom_built_df.drop(columns=['flood_type', 'ghsl_type', 'ftm3_ghsl_new_built_s_km2', 'ftm3_ghsl_rate_built_s_%', 'fathom_year'])

# Pivot fathom data to have return periods as columns
fathom_built_pivot = fathom_built_df.pivot(
    index=['ISO3', 'agglosID', 'agglosName', 'ghsl_year'], 
    columns='return_period', 
    values='ftm3_ghsl_total_built_s_km2').reset_index()

# Load GHSL built-up data
ghsl_built_df = pd.read_csv(ghsl_built_file)

# Drop unnecessary columns from GHSL data
ghsl_built_df = ghsl_built_df.drop(columns=['ghsl_type', 'ghsl_new_built_s_km2', 'ghsl_rate_built_s_%'])

# Merge GHSL data with Fathom pivot data on agglosID and ghsl_year
built_df = pd.merge(ghsl_built_df, fathom_built_pivot[['agglosID', 'ghsl_year', '1in5', '1in10', '1in100']], 
                    on=['agglosID', 'ghsl_year'], how='left')

# Replace the NaN values in columns 1in5, 1in10, 1in100 with 0
built_df[['1in5', '1in10', '1in100']] = built_df[['1in5', '1in10', '1in100']].fillna(0)

# Drop rows where 'ghsl_total_built_s_km2' is NaN
built_df = built_df.dropna(subset=['ghsl_total_built_s_km2'])

# Rename columns
built_df = built_df.rename(columns={
    'ghsl_total_built_s_km2': 'BU',
    '1in5': 'BU_1in5', 
    '1in10': 'BU_1in10', 
    '1in100': 'BU_1in100'
})

# Create columns for percentage of built-up area affected by flooding
built_df['BU_1in5_pct'] = (built_df['BU_1in5'] / built_df['BU']) * 100
built_df['BU_1in10_pct'] = (built_df['BU_1in10'] / built_df['BU']) * 100
built_df['BU_1in100_pct'] = (built_df['BU_1in100'] / built_df['BU']) * 100

# Load fathom population data
fathom_pop_df = pd.read_csv(fathom_pop_file)

# Filter for FLUVIAL_PLUVIAL_DEFENDED only
fathom_pop_df = fathom_pop_df[fathom_pop_df['flood_type'] == 'FLUVIAL_PLUVIAL_DEFENDED']

# Drop unnecessary columns
fathom_pop_df = fathom_pop_df.drop(columns=['flood_type', 'ghsl_type', 'ftm3_ghsl_new_pop_#', 'ftm3_ghsl_rate_pop_%', 'fathom_year'])

# Pivot fathom data to have return periods as columns
fathom_pop_pivot = fathom_pop_df.pivot(
    index=['ISO3', 'agglosID', 'agglosName', 'ghsl_year'], 
    columns='return_period', 
    values='ftm3_ghsl_total_pop_#').reset_index()

# Load GHSL population data
ghsl_pop_df = pd.read_csv(ghsl_pop_file)

# Drop unnecessary columns from GHSL data
ghsl_pop_df = ghsl_pop_df.drop(columns=['ghsl_type', 'ghsl_new_pop_#', 'ghsl_rate_pop_%'])

# Merge GHSL data with Fathom pivot data on agglosID and ghsl_year
pop_df = pd.merge(ghsl_pop_df, fathom_pop_pivot[['agglosID', 'ghsl_year', '1in5', '1in10', '1in100']], 
                  on=['agglosID', 'ghsl_year'], how='left')

# Replace the NaN values in columns 1in5, 1in10, 1in100 with 0
pop_df[['1in5', '1in10', '1in100']] = pop_df[['1in5', '1in10', '1in100']].fillna(0)

# Drop rows where 'ghsl_total_pop_#' is NaN
pop_df = pop_df.dropna(subset=['ghsl_total_pop_#'])

# Rename columns
pop_df = pop_df.rename(columns={
    'ghsl_total_pop_#': 'POP',
    '1in5': 'POP_1in5', 
    '1in10': 'POP_1in10', 
    '1in100': 'POP_1in100'
})

# Create columns for percentage of population affected by flooding
pop_df['POP_1in5_pct'] = (pop_df['POP_1in5'] / pop_df['POP']) * 100
pop_df['POP_1in10_pct'] = (pop_df['POP_1in10'] / pop_df['POP']) * 100
pop_df['POP_1in100_pct'] = (pop_df['POP_1in100'] / pop_df['POP']) * 100

# Merge built-up and population data on agglosID and ghsl_year
# Keep ISO3, agglosID, agglosName, ghsl_year from built_df, and add population columns
final_df = pd.merge(
    built_df,
    pop_df[['agglosID', 'ghsl_year', 'POP', 'POP_1in5', 'POP_1in10', 'POP_1in100', 
            'POP_1in5_pct', 'POP_1in10_pct', 'POP_1in100_pct']],
    on=['agglosID', 'ghsl_year'],
    how='left'
)
    
# Save to CSV
os.makedirs(os.path.dirname(output_file), exist_ok=True)
final_df.to_csv(output_file, index=False)

#%% Keep only largest agglomeration entries
    
# Filter for 2020 to select top cities based on population
temp_df = final_df[final_df['ghsl_year'] == 2020].copy()

# Group by ISO3 and select top 5 cities by POP (population)
top_cities = temp_df.groupby('ISO3').apply(lambda x: x.nlargest(5, 'POP')).reset_index(drop=True)

# Get the unique agglosID of the selected top cities
selected_agglosID = top_cities['agglosID'].unique()

# Filter final_df to keep only rows for the selected agglosID (across all years)
df5 = final_df[final_df['agglosID'].isin(selected_agglosID)]

# Save CSV
df5.to_csv(output_file_5cities, index=False)

#%%

simple_df = final_df[['ISO3', 'agglosName', 'agglosID', 'ghsl_year', 'POP', 'BU']]

simple_df = simple_df[simple_df['ghsl_year'].isin([2000, 2020])]

# Calculate growth between 2000 and 2020 for POP and BU
growth_df = simple_df.pivot(index=['ISO3', 'agglosName', 'agglosID'], columns='ghsl_year', values=['POP', 'BU']).reset_index()

growth_df['POP_CAGR_2000_2020'] = ((growth_df[('POP', 2020)] / growth_df[('POP', 2000)]) ** (1/20) - 1) * 100
growth_df['BU_CAGR_2000_2020'] = ((growth_df[('BU', 2020)] / growth_df[('BU', 2000)]) ** (1/20) - 1) * 100

growth_df.columns = ['ISO3', 'agglosName', 'agglosID', 'POP_2000', 'POP_2020', 'BU_2000', 'BU_2020', 'POP_CAGR_2000_2020', 'BU_CAGR_2000_2020']

# Save to simple output file
growth_df.to_csv(output_file_simple, index=False)
