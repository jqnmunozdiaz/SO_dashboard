#%%
"""
Merge dynamic and static Africapolis WorldPop data
Combines df_agglo_worldpop_stats_geom_dynamic and df_agglo_worldpop_stats_geom_static_2020
to create a consolidated dataset with three years per unique_id:
- 2015: from dynamic file
- 2020: from dynamic file  
- 2025: from static file
"""

import pandas as pd
import os

# Get project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a = 3

# Define file paths
data_dir = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025')
dynamic_file = os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_dynamic.csv')
static_file = os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_static_2020.csv')

# Load the files
df_dynamic = pd.read_csv(dynamic_file)
df_static = pd.read_csv(static_file)

# Filter dynamic file for 2015 and 2020 AND Filter static file for 2025
df_2015 = df_dynamic[df_dynamic['worldpop_year'] == 2015].copy()
df_2020 = df_dynamic[df_dynamic['worldpop_year'] == 2020].copy()
df_2025 = df_static[df_static['worldpop_year'] == 2025].copy()

# Combine all three years
df_merged = pd.concat([df_2015, df_2020, df_2025], ignore_index=True)

# Remove cities where any year has missing population data
ids_with_missing = df_merged[df_merged['worldpop_population_total'].isna()]['unique_id'].unique()
df_merged = df_merged[~df_merged['unique_id'].isin(ids_with_missing)].copy()

#%%
# Process flood (ftm) files

ftm_dynamic_file = os.path.join(data_dir, 'df_agglo_worldpop_ftm_stats_geom_dynamic.csv')
ftm_static_file = os.path.join(data_dir, 'df_agglo_worldpop_ftm_stats_geom_static_2020.csv')

# Load flood files
df_ftm_dynamic = pd.read_csv(ftm_dynamic_file)
df_ftm_static = pd.read_csv(ftm_static_file)

# Filter for FLUVIAL_PLUVIAL_DEFENDED only
df_ftm_dynamic = df_ftm_dynamic[df_ftm_dynamic['ftm_flood_type'] == 'FLUVIAL_PLUVIAL_DEFENDED'].copy()
df_ftm_static = df_ftm_static[df_ftm_static['ftm_flood_type'] == 'FLUVIAL_PLUVIAL_DEFENDED'].copy()

# Filter for 2015, 2020, and 2025
df_ftm_2015 = df_ftm_dynamic[df_ftm_dynamic['worldpop_year'] == 2015].copy()
df_ftm_2020 = df_ftm_dynamic[df_ftm_dynamic['worldpop_year'] == 2020].copy()
df_ftm_2025 = df_ftm_static[df_ftm_static['worldpop_year'] == 2025].copy()

# Combine all three years
df_ftm_merged = pd.concat([df_ftm_2015, df_ftm_2020, df_ftm_2025], ignore_index=True)

# Remove cities with ids_with_missing from the first processing
df_ftm_merged = df_ftm_merged[~df_ftm_merged['unique_id'].isin(ids_with_missing)].copy()

#%%
# Merge both datasets into final consolidated file
# Add worldpop_population_total, worldpop_built_surface_km2, worldpop_built_volume_m3
# from africapolis_worldpop_merged to africapolis_worldpop_ftm_merged

final_output_file = os.path.join(project_root, 'data', 'processed', 'africapolis_worldpop_final_merged.csv')

# Select columns to merge from worldpop dataset
merge_columns = ['unique_id', 'worldpop_year', 
                 'worldpop_population_total', 
                 'worldpop_built_surface_km2', 
                 'worldpop_built_volume_m3']

df_worldpop_subset = df_merged[merge_columns]

# Perform left merge to keep all ftm rows and add worldpop data
# The ftm dataset has multiple rows per unique_id/year (one per return period)
df_final_merged = df_ftm_merged.merge(
    df_worldpop_subset,
    on=['unique_id', 'worldpop_year'],
    how='left',
    validate='m:1'  # Many ftm rows to one worldpop row
)

# Save the final merged dataset
print(f"\nSaving final merged dataset to: {final_output_file}")
df_final_merged.to_csv(final_output_file, index=False)

