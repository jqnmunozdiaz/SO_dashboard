"""
Script to scale Buildings PML curves using AAL-based scaling factors.

For each country and hazard:
1. Retrieve the total AAL (sum of AAL across all sectors and subsectors).
2. Retrieve the Buildings sector AAL (sum of AAL across all Buildings subsectors).
3. Compute a scaling factor: scaling_factor = total_aal / buildings_aal.
4. Filter for Buildings PML (sector == 'Buildings', subsector == 'all', risk_metric_abbr == 'PML').
5. Apply the scaling factor to each row of the Loss column to produce a new "Overall Loss" for each RP.
6. Save the results in a new script and output file.
"""

import os
import sys
import pandas as pd
import numpy as np

# Set up file paths relative to the script location
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

processed_dir = os.path.join(project_root, 'data', 'processed', 'GIRI')
input_file_path = os.path.join(processed_dir, 'GIRI_Processed.csv')
output_file_path = os.path.join(processed_dir, 'GIRI_Overall_Loss.csv')

print("=" * 70)
print("             GIRI PML SCALING AND OVERALL LOSS COMPUTATION")
print("=" * 70)

print(f"Reading GIRI Processed data from:\n  {input_file_path}\n")
if not os.path.exists(input_file_path):
    print(f"Error: Processed file not found at {input_file_path}")
    sys.exit(1)

df = pd.read_csv(input_file_path)
print(f"Loaded dataset of shape: {df.shape}")

# 1. Filter for AAL to compute the scaling factors
df_aal = df[df['risk_metric_abbr'] == 'AAL'].copy()

# 2. Compute total AAL per country and hazard
total_aal = df_aal.groupby(['iso3cd', 'hazard'])['Loss'].sum().reset_index(name='Total_AAL')

# 3. Compute Buildings sector AAL per country and hazard
buildings_aal = df_aal[df_aal['sector'] == 'Buildings'].groupby(['iso3cd', 'hazard'])['Loss'].sum().reset_index(name='Buildings_AAL')

# 4. Merge total AAL and Buildings sector AAL, then compute scaling factor
scaling_df = pd.merge(total_aal, buildings_aal, on=['iso3cd', 'hazard'], how='left').fillna(0)

# Avoid division by zero by using np.where. If Buildings_AAL is 0, scaling factor defaults to 1.0
scaling_df['Scaling_Factor'] = np.where(
    scaling_df['Buildings_AAL'] > 0,
    scaling_df['Total_AAL'] / scaling_df['Buildings_AAL'],
    1.0
)

# Print direct checks for zero/missing Buildings AAL
zero_count = (scaling_df['Buildings_AAL'] == 0).sum()
print(f"Zero Buildings AAL combinations found: {zero_count}")
if zero_count > 0:
    print("Warning: The following combinations had 0/missing Buildings AAL and fell back to 1.0:")
    print(scaling_df[scaling_df['Buildings_AAL'] == 0][['iso3cd', 'hazard']])

print(f"Computed scaling factors for {len(scaling_df)} country-hazard combinations.")

# 5. Filter for target PML rows: sector == 'Buildings', subsector == 'all', risk_metric_abbr == 'PML'
df_pml = df[
    (df['sector'] == 'Buildings') & 
    (df['subsector'] == 'all') & 
    (df['risk_metric_abbr'] == 'PML')
].copy()

print(f"Found {len(df_pml)} rows matching Buildings PML (sector='Buildings', subsector='all', risk_metric='PML').")

# 6. Merge scaling factors back into the target PML dataset
merged_df = pd.merge(
    df_pml, 
    scaling_df[['iso3cd', 'hazard', 'Total_AAL', 'Buildings_AAL', 'Scaling_Factor']], 
    on=['iso3cd', 'hazard'], 
    how='left'
)

# Print direct checks for missing scaling factors before fillna
nan_count = merged_df['Scaling_Factor'].isna().sum()
print(f"Missing scaling factors (NaN) found before fillna: {nan_count}")
if nan_count > 0:
    print("Warning: Some PML curves lacked corresponding AAL data and fell back to 1.0.")

# Fill any missing scaling factors with 1.0
merged_df['Scaling_Factor'] = merged_df['Scaling_Factor'].fillna(1.0)

# Rename Loss to Buildings_Loss
merged_df = merged_df.rename(columns={'Loss': 'Buildings_Loss'})

# 7. Apply scaling factor to 'Buildings_Loss' column to produce 'Loss' (Overall Loss)
merged_df['Loss'] = merged_df['Buildings_Loss'] * merged_df['Scaling_Factor']

# Replace "Buildings" in sector column by "all_assets"
merged_df['sector'] = merged_df['sector'].replace('Buildings', 'all_assets')

# Keep and organize columns (Deleting subsector and risk_metric_abbr columns)
final_cols = [
    'iso3cd', 'hazard', 'sector', 'Loss', 'RP', 
    'Buildings_Loss', 'Total_AAL', 'Buildings_AAL', 'Scaling_Factor',
    'CAP_Stock', 'GDP'
]
output_df = merged_df[final_cols].copy()

# Sort by country, hazard, and Return Period (RP) ascending
output_df = output_df.sort_values(by=['iso3cd', 'hazard', 'RP']).reset_index(drop=True)

# Ensure the parent directories exist and save to CSV
os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
output_df.to_csv(output_file_path, index=False)

print("\n" + "=" * 70)
print(f"Overall PML Loss dataset saved successfully to:\n  {output_file_path}")
print(f"Final output shape: {output_df.shape}")
print("=" * 70)

# Print a preview of the resulting dataset
print("\nPreview of the first 15 rows of the scaled dataset:")
preview_cols = ['iso3cd', 'hazard', 'Loss', 'RP', 'Buildings_Loss', 'Scaling_Factor']
print(output_df[preview_cols].head(15).to_string(index=False, formatters={
    'Buildings_Loss': lambda x: f"${x:,.2f}",
    'Scaling_Factor': lambda x: f"{x:.4f}",
    'Loss': lambda x: f"${x:,.2f}",
    'RP': lambda x: f"{int(x)}"
}))
print("=" * 70)
