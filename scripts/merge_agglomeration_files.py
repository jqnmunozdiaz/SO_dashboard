"""
Merge agglomeration_population_stats.csv and agglomeration_builtup_stats.csv
Combines all columns from both files using unique_id as the merge key.
"""

import pandas as pd
import os

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define file paths
data_dir = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025')
pop_file = os.path.join(data_dir, 'agglomeration_population_stats.csv')
builtup_file = os.path.join(data_dir, 'agglomeration_builtup_stats.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'agglomeration_population_builtup_merged.csv')

# Load both CSV files
df_pop = pd.read_csv(pop_file)
df_builtup = pd.read_csv(builtup_file)

# Check common columns
common_cols = set(df_pop.columns) & set(df_builtup.columns)

# Identify merge keys (common identifier columns)
merge_keys = ['unique_id', 'ISO3', 'Country', 'geometry_year_africapolis', 'Agglomeration_Name', 'Surface km2']

df_merged = pd.merge(
    df_pop, 
    df_builtup,
    on=merge_keys,
    how='outer',  # Use outer join to keep all records from both files
    suffixes=('_pop', '_builtup'),  # Add suffixes if there are any other duplicate columns
)

# Save the merged file
print(f"\nSaving merged data to: {output_file}")
df_merged.to_csv(output_file, index=False)
