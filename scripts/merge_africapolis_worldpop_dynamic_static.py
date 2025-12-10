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

# Define file paths
data_dir = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025')
dynamic_file = os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_dynamic.csv')
static_file = os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_static_2020.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'africapolis_worldpop_merged.csv')

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

# Save merged file
print(f"\nSaving merged WorldPop stats data to: {output_file}")
df_merged.to_csv(output_file, index=False)

print(f"\nWorldPop stats processing complete!")
print(f"  Total unique cities: {df_merged['unique_id'].nunique()}")
print(f"  Total rows: {len(df_merged)}")

#%%
# Process flood (ftm) files

ftm_dynamic_file = os.path.join(data_dir, 'df_agglo_worldpop_ftm_stats_geom_dynamic.csv')
ftm_static_file = os.path.join(data_dir, 'df_agglo_worldpop_ftm_stats_geom_static_2020.csv')
ftm_output_file = os.path.join(project_root, 'data', 'processed', 'africapolis_worldpop_ftm_merged.csv')

# Load flood files
df_ftm_dynamic = pd.read_csv(ftm_dynamic_file)
df_ftm_static = pd.read_csv(ftm_static_file)

print(f"\nFTM dynamic file shape: {df_ftm_dynamic.shape}")
print(f"FTM static file shape: {df_ftm_static.shape}")

# Filter for FLUVIAL_PLUVIAL_DEFENDED only
df_ftm_dynamic = df_ftm_dynamic[df_ftm_dynamic['ftm_flood_type'] == 'FLUVIAL_PLUVIAL_DEFENDED'].copy()
df_ftm_static = df_ftm_static[df_ftm_static['ftm_flood_type'] == 'FLUVIAL_PLUVIAL_DEFENDED'].copy()

print(f"\nAfter filtering for FLUVIAL_PLUVIAL_DEFENDED:")
print(f"  FTM dynamic rows: {len(df_ftm_dynamic)}")
print(f"  FTM static rows: {len(df_ftm_static)}")

# Filter for 2015, 2020, and 2025
df_ftm_2015 = df_ftm_dynamic[df_ftm_dynamic['worldpop_year'] == 2015].copy()
df_ftm_2020 = df_ftm_dynamic[df_ftm_dynamic['worldpop_year'] == 2020].copy()
df_ftm_2025 = df_ftm_static[df_ftm_static['worldpop_year'] == 2025].copy()

print(f"\nRows by year:")
print(f"  2015 (from dynamic): {len(df_ftm_2015)}")
print(f"  2020 (from dynamic): {len(df_ftm_2020)}")
print(f"  2025 (from static): {len(df_ftm_2025)}")

# Combine all three years
df_ftm_merged = pd.concat([df_ftm_2015, df_ftm_2020, df_ftm_2025], ignore_index=True)

print(f"\nFTM merged shape before filtering: {df_ftm_merged.shape}")
print(f"Unique IDs before filtering: {df_ftm_merged['unique_id'].nunique()}")

# Remove cities with ids_with_missing from the first processing
df_ftm_merged = df_ftm_merged[~df_ftm_merged['unique_id'].isin(ids_with_missing)].copy()

print(f"\nAfter removing cities with missing population data:")
print(f"  Remaining rows: {len(df_ftm_merged)}")
print(f"  Remaining unique IDs: {df_ftm_merged['unique_id'].nunique()}")

# Save FTM merged file
print(f"\nSaving merged flood (FTM) data to: {ftm_output_file}")
df_ftm_merged.to_csv(ftm_output_file, index=False)

#%%

