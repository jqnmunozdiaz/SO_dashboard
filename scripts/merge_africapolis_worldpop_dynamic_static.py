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
import geopandas as gpd
import os

# Get project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

#%%
# Add Africapolis population data

# Load Africapolis GeoPackage
africapolis_gpkg = os.path.join(project_root, 'data', 'raw', 'Africapolis_GIS_2024.gpkg')
gdf_africapolis = gpd.read_file(africapolis_gpkg)

# Create unique_id in Africapolis data (ISO3_Agglomeration_ID)
gdf_africapolis['unique_id'] = gdf_africapolis['ISO3'] + '_' + gdf_africapolis['Agglomeration_ID'].astype(int).astype(str)

# Reshape Africapolis population data to long format for years 2015, 2020, 2025
africapolis_pop = []
for year in [2015, 2020, 2025]:
    year_data = gdf_africapolis[['unique_id', f'Population_{year}']].copy()
    year_data['worldpop_year'] = year
    year_data = year_data.rename(columns={f'Population_{year}': 'africapolis_pop'})
    africapolis_pop.append(year_data)

df_africapolis_pop = pd.concat(africapolis_pop, ignore_index=True)

# Convert africapolis_pop to numeric and handle any non-numeric values
df_africapolis_pop['africapolis_pop'] = pd.to_numeric(df_africapolis_pop['africapolis_pop'], errors='coerce')

# Remove only exact duplicates (same values across all columns)
exact_duplicates = df_africapolis_pop.duplicated(keep='first')
if exact_duplicates.any():
    print(f"\nWarning: Found {exact_duplicates.sum()} exact duplicate rows in Africapolis data")
    print("Removing exact duplicates")
    df_africapolis_pop = df_africapolis_pop.drop_duplicates(keep='first')

# Check for non-exact duplicates (same keys but different values)
key_duplicates = df_africapolis_pop.duplicated(subset=['unique_id', 'worldpop_year'], keep=False)
if key_duplicates.any():
    print(f"\nERROR: Found {key_duplicates.sum()} non-exact duplicates with same unique_id/year but different population values")
    print("Problematic rows:")
    print(df_africapolis_pop[key_duplicates].sort_values(['unique_id', 'worldpop_year']))
    raise ValueError("Cannot merge: Africapolis data has conflicting population values for same unique_id/year")

# Merge Africapolis population into final dataset
df_final_merged = df_final_merged.merge(
    df_africapolis_pop,
    on=['unique_id', 'worldpop_year'],
    how='left',
    validate='m:1'  # Many ftm rows to one africapolis row per unique_id/year
)

# Save the final merged dataset with Africapolis population
print(f"\nSaving updated dataset with Africapolis population to: {final_output_file}")
df_final_merged.to_csv(final_output_file, index=False)

#%%
# Create wide format version (format_1) for growth rate analysis
# This format has years as column suffixes and includes CAGR calculations

format_1_output = os.path.join(project_root, 'data', 'processed', 'africapolis_worldpop_final_merged_format_1.csv')

# Get unique cities (one row per unique_id, ignoring return periods)
# Use first return period for each city/year combination
df_wide = df_final_merged[df_final_merged['ftm_return_period'] == df_final_merged['ftm_return_period'].min()].copy()

# Pivot built-up surface to wide format
built_pivot = df_wide.pivot_table(
    index=['unique_id', 'ISO3', 'Agglomeration_Name'],
    columns='worldpop_year',
    values='worldpop_built_surface_km2',
    aggfunc='first'
).reset_index()

# Rename built columns
built_pivot.columns.name = None
built_pivot = built_pivot.rename(columns={
    2015: 'worldpop_built_km2_2015',
    2020: 'worldpop_built_km2_2020',
    2025: 'worldpop_built_km2_2025'
})

# Pivot Africapolis population to wide format
pop_pivot = df_wide.pivot_table(
    index='unique_id',
    columns='worldpop_year',
    values='africapolis_pop',
    aggfunc='first'
).reset_index()

# Rename population columns
pop_pivot.columns.name = None
pop_pivot = pop_pivot.rename(columns={
    2015: 'africapolis_pop_2015',
    2020: 'africapolis_pop_2020',
    2025: 'africapolis_pop_2025'
})

# Merge pivoted data
df_format_1 = built_pivot.merge(pop_pivot, on='unique_id', how='left')

# Calculate CAGR for built-up surface (2015-2020)
df_format_1['worldpop_built_cagr_2015_2020'] = (
    (df_format_1['worldpop_built_km2_2020'] / df_format_1['worldpop_built_km2_2015']) ** (1/5) - 1
)

# Calculate CAGR for built-up surface (2020-2025)
df_format_1['worldpop_built_cagr_2020_2025'] = (
    (df_format_1['worldpop_built_km2_2025'] / df_format_1['worldpop_built_km2_2020']) ** (1/5) - 1
)

# Calculate CAGR for Africapolis population (2015-2020)
df_format_1['africapolis_pop_cagr_2015_2020'] = (
    (df_format_1['africapolis_pop_2020'] / df_format_1['africapolis_pop_2015']) ** (1/5) - 1
)

# Calculate CAGR for Africapolis population (2020-2025)
df_format_1['africapolis_pop_cagr_2020_2025'] = (
    (df_format_1['africapolis_pop_2025'] / df_format_1['africapolis_pop_2020']) ** (1/5) - 1
)

# Calculate built-up per capita (km2 per person)
df_format_1['buppercapita_2015'] = df_format_1['worldpop_built_km2_2015'] / df_format_1['africapolis_pop_2015'] * 1e6
df_format_1['buppercapita_2020'] = df_format_1['worldpop_built_km2_2020'] / df_format_1['africapolis_pop_2020'] * 1e6
df_format_1['buppercapita_2025'] = df_format_1['worldpop_built_km2_2025'] / df_format_1['africapolis_pop_2025'] * 1e6

# Replace inf values with NaN (division by zero cases)
df_format_1 = df_format_1.replace([float('inf'), float('-inf')], pd.NA)


# Save format_1 file
print(f"\nSaving format_1 dataset to: {format_1_output}")
df_format_1.to_csv(format_1_output, index=False)


# %%
