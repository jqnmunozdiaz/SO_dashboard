"""
Merge country_population_stats.csv and country_builtup_stats.csv
Combines all columns from both files using ISO_A3 as the merge key.
"""

import pandas as pd
import os

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define file paths
data_dir = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025')
pop_file = os.path.join(data_dir, 'country_population_stats.csv')
builtup_file = os.path.join(data_dir, 'country_builtup_stats.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'country_population_builtup_merged.csv')

print("Loading data files...")
print(f"Population file: {pop_file}")
print(f"Built-up file: {builtup_file}")

# Load both CSV files
df_pop = pd.read_csv(pop_file)
df_builtup = pd.read_csv(builtup_file)

print(f"\nPopulation data shape: {df_pop.shape}")
print(f"Built-up data shape: {df_builtup.shape}")

# Check common columns
common_cols = set(df_pop.columns) & set(df_builtup.columns)
print(f"\nCommon columns: {common_cols}")

# Merge on ISO_A3, WB_NAME, and surface_area_km2
# Keep all columns from both dataframes, avoiding duplicates of common columns
merge_keys = ['ISO_A3']

# Merge the dataframes
df_merged = pd.merge(
    df_pop, 
    df_builtup,
    on=merge_keys,
    how='outer',  # Use outer join to keep all countries from both files
    suffixes=('_pop', '_builtup')  # Add suffixes if there are any other duplicate columns
)

print(f"\nMerged data shape: {df_merged.shape}")
print(f"Number of countries: {len(df_merged)}")

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

print("\nMerge complete!")
print(f"Output file: {output_file}")

# Display first few rows
print("\nFirst 3 rows of merged data:")
print(df_merged.head(3))