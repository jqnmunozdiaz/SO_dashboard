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
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from src.utils.city_helpers import categorize_city_size

# Define whether to use dynamic city extents for 2015 and 2020
use_dynamic_city_extents = False
africapolis_year_extent = 2020  # Year of Africapolis extents to use if not using dynamic

# Define file paths
data_dir = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025')
dynamic_file = os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_dynamic.csv')
static_file = os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_static_2020.csv')

# Load the files
df_dynamic = pd.read_csv(dynamic_file)
df_static = pd.read_csv(static_file)

if use_dynamic_city_extents: # Filter dynamic file for 2015 and 2020 AND Filter static file for 2025
    df_2015 = df_dynamic[df_dynamic['worldpop_year'] == 2015].copy()
    df_2020 = df_dynamic[df_dynamic['worldpop_year'] == 2020].copy()
    df_2025 = df_static[df_static['worldpop_year'] == 2025].copy()
else:
    df_2015 = df_static[df_static['worldpop_year'] == 2015].copy()
    df_2020 = df_static[df_static['worldpop_year'] == 2020].copy()
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
if use_dynamic_city_extents:
    df_ftm_2015 = df_ftm_dynamic[df_ftm_dynamic['worldpop_year'] == 2015].copy()
    df_ftm_2020 = df_ftm_dynamic[df_ftm_dynamic['worldpop_year'] == 2020].copy()
    df_ftm_2025 = df_ftm_static[df_ftm_static['worldpop_year'] == 2025].copy()
else:
    df_ftm_2015 = df_ftm_static[df_ftm_static['worldpop_year'] == 2015].copy()
    df_ftm_2020 = df_ftm_static[df_ftm_static['worldpop_year'] == 2020].copy()
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
africapolis_gpkg = os.path.join(project_root, 'data', 'raw', 'Africapolis_GIS_2024.gpkg')
gdf_africapolis = gpd.read_file(africapolis_gpkg)

# Create unique_id in Africapolis data (ISO3_Agglomeration_ID)
gdf_africapolis['unique_id'] = gdf_africapolis['ISO3'] + '_' + gdf_africapolis['Agglomeration_ID'].astype(int).astype(str)

# Filter for selected geometry year
gdf_africapolis = gdf_africapolis[gdf_africapolis['Select_Geometry_Year'] == africapolis_year_extent].copy()

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

# Merge Africapolis population into final dataset
df_final_merged = df_final_merged.merge(
    df_africapolis_pop,
    on=['unique_id', 'worldpop_year'],
    how='left',
    validate='m:1'  # Many ftm rows to one africapolis row per unique_id/year
)

# Remove cities where africapolis_pop is 0 in any year
# First, identify unique_ids with zero population in any year
ids_with_zero_pop = df_final_merged[df_final_merged['africapolis_pop'] == 0]['unique_id'].unique()

if len(ids_with_zero_pop) > 0:
    print(f"Found {len(ids_with_zero_pop)} unique cities with africapolis_pop = 0 in at least one year")
    
    # Get rows that will be removed for analysis
    rows_to_remove = df_final_merged[df_final_merged['unique_id'].isin(ids_with_zero_pop)].copy()
    
    # Get unique agglomerations and their largest worldpop_population_total
    agglomeration_stats = rows_to_remove.groupby(['Agglomeration_Name', 'ISO3'])['worldpop_population_total'].max().reset_index()
    agglomeration_stats = agglomeration_stats.sort_values('worldpop_population_total', ascending=False)
    
    print(f"Removing {len(rows_to_remove)} total rows (across all years and return periods)")
    print(f"\nTop 10 cities by worldpop_population_total being removed:")
    for idx, row in agglomeration_stats.head(10).iterrows():
        print(f"{row['Agglomeration_Name']:40s} ({row['ISO3']}) - Pop: {row['worldpop_population_total']:>12,.0f}")
    
    # Remove all rows with these unique_ids
    df_final_merged = df_final_merged[~df_final_merged['unique_id'].isin(ids_with_zero_pop)].copy()

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

# Calculate CAGR for built-up and population metrics
# Define metric configurations: (column_prefix, metric_name)
format_1_metrics = [
    ('worldpop_built_km2', 'worldpop_built_cagr'),
    ('africapolis_pop', 'africapolis_pop_cagr')
]

# Define time periods for CAGR calculation
year_periods = [(2015, 2020), (2020, 2025)]

# Calculate CAGR for all combinations of metrics and time periods
for col_prefix, cagr_prefix in format_1_metrics:
    for year1, year2 in year_periods:
        col_year1 = f'{col_prefix}_{year1}'
        col_year2 = f'{col_prefix}_{year2}'
        cagr_col = f'{cagr_prefix}_{year1}_{year2}'
        df_format_1[cagr_col] = ((df_format_1[col_year2] / df_format_1[col_year1]) ** (1/5) - 1)

# Calculate built-up per capita, size category, and convert population to integers for each year
for year in [2015, 2020, 2025]:
    df_format_1[f'buppercapita_{year}'] = df_format_1[f'worldpop_built_km2_{year}'] / df_format_1[f'africapolis_pop_{year}'] * 1e6
    df_format_1[f'size_category_{year}'] = df_format_1[f'africapolis_pop_{year}'].apply(categorize_city_size)
    df_format_1[f'africapolis_pop_{year}'] = df_format_1[f'africapolis_pop_{year}'].round().astype('Int64')

# Replace inf values with NaN (division by zero cases)
df_format_1 = df_format_1.replace([float('inf'), float('-inf')], pd.NA)

# Save format_1 file
print(f"\nSaving format_1 dataset to: {format_1_output}")
df_format_1.to_csv(format_1_output, index=False)

#%%
# Create format_2 for city flood exposure analysis
# This format pivots all data to have one row per unique_id

format_2_output = os.path.join(project_root, 'data', 'processed', 'africapolis_worldpop_final_merged_format_2.csv')

# Start with the long format data that has flood information
df_format_2_base = df_final_merged.copy()

df_format_2_base['worldpop_population_total'] = df_format_2_base['africapolis_pop'] # Use africapolis_pop as total population
df_format_2_base['worldpop_population_ftm_total'] = df_format_2_base['worldpop_population_total'] * df_format_2_base['worldpop_population_ftm_share'] # Calculate exposed population

# Pivot to wide format
df_format_2 = df_format_2_base.pivot_table(
    index=['unique_id', 'ISO3', 'Agglomeration_Name'],
    columns=['worldpop_year', 'ftm_return_period'],
    values=['worldpop_population_ftm_total', # Exposed
            'worldpop_population_ftm_share', # Share exposed TRUE
            'worldpop_population_total', # Total population
            'africapolis_pop', #TRUE 
            'worldpop_built_surface_ftm_km2', # Exposed
            'worldpop_built_surface_ftm_share', # Share exposed
            'worldpop_built_surface_km2' # Total built-up
        ],  
    aggfunc='first'
)

# Flatten the multi-level column names. Format: {metric}_rp{return_period}_{year}
df_format_2.columns = [f'{metric}_rp{rp}_{year}' for metric, year, rp in df_format_2.columns]
df_format_2 = df_format_2.reset_index()

# Calculate CAGR for flood exposure metrics
# Define metric configurations: (column_base, cagr_name_prefix)
metrics = [
    ('worldpop_population_ftm_total', 'pop_ftm3_fluvial_pluvial_flood'),
    ('worldpop_built_surface_ftm_km2', 'built_ftm3_fluvial_pluvial_flood')
]

# Define time periods for CAGR calculation
year_periods = [(2015, 2020), (2020, 2025)]

# Calculate CAGR for all combinations of metrics, return periods, and time periods
for rp in [10, 100]:
    for col_base, cagr_prefix in metrics:
        for year1, year2 in year_periods:
            col_year1 = f'{col_base}_rp{rp}_{year1}'
            col_year2 = f'{col_base}_rp{rp}_{year2}'
            cagr_col = f'{cagr_prefix}_rp{rp}_cagr_{year1}_{year2}'
            df_format_2[cagr_col] = ((df_format_2[col_year2] / df_format_2[col_year1]) ** (1/5) - 1)

for year in [2015, 2020, 2025]:
    df_format_2[f'africapolis_pop_{year}'] = df_format_2[f'africapolis_pop_rp10_{year}'].round().astype('Int64')

# Replace inf values with NaN (division by zero cases)
df_format_2 = df_format_2.replace([float('inf'), float('-inf')], pd.NA)

# Save format_2 file
print(f"\nSaving format_2 dataset to: {format_2_output}")
df_format_2.to_csv(format_2_output, index=False)

# %%
