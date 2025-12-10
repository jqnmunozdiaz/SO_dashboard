#%%
"""
Combines all columns from both files using ISO_A3 as the merge key.
"""

import pandas as pd
import os

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define file paths
data_dir = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025')
df_file = os.path.join(data_dir, 'df_country_worldpop_stats.csv')
dfft_file = os.path.join(data_dir, 'df_country_worldpop_ftm_stats.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'df_country_worldpop_stats_merged.csv')

# Load both CSV files
df = pd.read_csv(df_file)
df = df[['ISO_A3', 'worldpop_year', 'worldpop_population_total', 'worldpop_built_surface_km2', 'worldpop_built_volume_m3']]

dfft = pd.read_csv(dfft_file)
dfft = dfft[['ISO_A3', 'worldpop_year', 'ftm_return_period', 'ftm_flood_type', 'worldpop_population_ftm_total', 'worldpop_population_ftm_share', 'worldpop_built_surface_ftm_km2', 'worldpop_built_surface_ftm_share', 'worldpop_built_volume_ftm_m3', 'worldpop_built_volume_ftm_share']]

dfft = dfft[dfft['ftm_flood_type'] == 'FLUVIAL_PLUVIAL_DEFENDED']

# Merge on ISO_A3 and worldpop_year
# Keep all columns from both dataframes, avoiding duplicates of common columns
merge_keys = ['ISO_A3', 'worldpop_year']

# Merge the dataframes
df_merged = pd.merge(
    df, 
    dfft,
    on=merge_keys,
    how='outer',  # Use outer join to keep all countries from both files
    suffixes=('_df', '_dfft')  # Add suffixes if there are any other duplicate columns
)

# Check for any missing values after merge
if df_merged[merge_keys].isnull().any().any():
    print("\nWarning: Some merge keys have null values after merge")
    print(df_merged[df_merged[merge_keys].isnull().any(axis=1)][merge_keys])
else:
    print("\nAll merge keys are complete - successful merge!")

# Display column names
print(f"\nTotal columns in merged file: {len(df_merged.columns)}")
print("\nColumn names:")
for i, col in enumerate(df_merged.columns, 1):
    print(f"  {i}. {col}")

# Save the merged file
print(f"\nSaving merged data to: {output_file}")
df_merged.to_csv(output_file, index=False)

#%%

df = pd.read_csv(os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_dynamic.csv'))
df = df[['ISO3', 'unique_id', 'Agglomeration_Name', 'africapolis_geometry_year', 'worldpop_year', 'worldpop_population_total', 'worldpop_built_surface_km2']]

# Identify unique_ids that have data in both 2020 and 2025
ids_2020 = set(df[df['worldpop_year'] == 2020]['unique_id'])
ids_2025 = set(df[df['worldpop_year'] == 2025]['unique_id'])
ids_both_years = ids_2020.intersection(ids_2025)

# Calculate CAGR only for cities with data in both years
df['worldpop_built_surface_km2_CAGR_2020_2025'] = None

for unique_id in ids_both_years:
    value_2020 = df.loc[(df['unique_id'] == unique_id) & (df['worldpop_year'] == 2020), 'worldpop_built_surface_km2'].values
    value_2025 = df.loc[(df['unique_id'] == unique_id) & (df['worldpop_year'] == 2025), 'worldpop_built_surface_km2'].values
    
    if len(value_2020) > 0 and len(value_2025) > 0 and value_2020[0] > 0:
        cagr = (value_2025[0] / value_2020[0]) ** (1/5) - 1
        df.loc[df['unique_id'] == unique_id, 'worldpop_built_surface_km2_CAGR_2020_2025'] = cagr

# Keep only rows where worldpop_year is 2025
df = df[df['worldpop_year'] == 2025]

#%%
import matplotlib.pyplot as plt

# Create histogram of CAGR values
plt.figure(figsize=(10, 6))
plt.hist(df['worldpop_built_surface_km2_CAGR_2020_2025'].dropna(), bins=50, edgecolor='black')
plt.xlabel('CAGR (2020-2025)')
plt.ylabel('Frequency')
plt.title('Distribution of Built Surface Area CAGR (2020-2025)')
plt.grid(True, alpha=0.3)
plt.show()

# Print summary statistics
print(f"\nCAGR Summary Statistics:")
print(df['worldpop_built_surface_km2_CAGR_2020_2025'].describe())



# %%
# df_agglo_worldpop_ftm_stats_geom_dynamic