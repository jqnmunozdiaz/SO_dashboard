"""
Script to clean and process GIRI Risk Metrics dataset.
Filters the raw export_all_metrics.csv file for:
- climate_scenario == 'Existing climate'
- risk_metric_abbr in ['AAL', 'PML']
- iso3cd in relevant project countries (Sub-Saharan Africa)
And retains/renames the specified columns.

PROMPT: adjust this script to clean the dataset. I want only the following columns: iso3cd, hazard, sector, subsector, climate_scenario=='Existing climate', risk_metric_abbr in 'AAL, 'PML', column: value_axis_1 (rename it to "Loss"), value_axis_2 (rename it to RP), 'pop', 'cap_stock_capita', 'gdp_capita'
"""

import os
import sys
import pandas as pd

# Import centralized country utilities
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)
from src.utils.country_utils import load_subsaharan_countries_dict

# Set up file paths relative to the script location
raw_file_path = os.path.join(project_root, 'data', 'raw', 'GIRI', 'export_all_metrics.csv')
processed_dir = os.path.join(project_root, 'data', 'processed', 'GIRI')
processed_file_path = os.path.join(processed_dir, 'GIRI_Processed.csv')
aals_file_path = os.path.join(processed_dir, 'GIRI_AALs.csv')

# Create the output directory if it doesn't exist
os.makedirs(processed_dir, exist_ok=True)

print(f"Reading raw data from: {raw_file_path}")

# Columns to load
cols_to_load = [
    'iso3cd', 'hazard', 'sector', 'subsector', 
    'climate_scenario', 'risk_metric_abbr', 
    'value_axis_1', 'value_axis_2', 
    'pop', 'cap_stock_capita', 'gdp_capita'
]

# Load the CSV file
df = pd.read_csv(raw_file_path, usecols=cols_to_load, low_memory=False)

# 1. Filter by ISO3 codes relevant to the project (Sub-Saharan African countries)
ssa_countries = list(load_subsaharan_countries_dict().keys())
df = df[df['iso3cd'].isin(ssa_countries)].copy()

# 2. Filter by climate_scenario == 'Existing climate'
df = df[df['climate_scenario'] == 'Existing climate'].copy()

# 3. Filter by risk_metric_abbr in ['AAL', 'PML']
df = df[df['risk_metric_abbr'].isin(['AAL', 'PML'])].copy()

# 3.5. Remove rows where hazard is "Landslide", "Tsunami", or "Tropical cyclone"
df = df[~df['hazard'].str.lower().isin(['landslide', 'tsunami', 'tropical cyclone'])].copy()

# Rename columns
df.rename(
    columns={
        'value_axis_1': 'Loss',
        'value_axis_2': 'RP'
    }, 
    inplace=True
)

# Compute GDP = pop * gdp_capita
df['GDP'] = df['pop'] * df['gdp_capita']

# Keep only the requested columns (including the computed GDP)
final_cols = [
    'iso3cd', 'hazard', 'sector', 'subsector', 'risk_metric_abbr', 
    'Loss', 'RP', 'pop', 'cap_stock_capita', 'gdp_capita', 'GDP'
]
df = df[final_cols].copy()

# Save cleaned dataset
df.to_csv(processed_file_path, index=False)
print(f"Cleaned dataset saved successfully to: {processed_file_path}")
print(f"Final shape: {df.shape}")

# 4. Generate GIRI_AALs.csv (sum of AALs per country and hazard, including a "Combined" hazard type)
print("Generating GIRI_AALs summary dataset...")
df_aal = df[df['risk_metric_abbr'] == 'AAL'].copy()

# Aggregate AAL per country and hazard
aal_summary = df_aal.groupby(['iso3cd', 'hazard']).agg({
    'Loss': 'sum',
    'pop': 'first',
    'cap_stock_capita': 'first',
    'gdp_capita': 'first',
    'GDP': 'first'
}).reset_index()

# Generate "Combined" hazard type per country
combined_aal = aal_summary.groupby('iso3cd').agg({
    'Loss': 'sum',
    'pop': 'first',
    'cap_stock_capita': 'first',
    'gdp_capita': 'first',
    'GDP': 'first'
}).reset_index()
combined_aal['hazard'] = 'Combined'

# Combine individual hazards and the Combined hazard
giri_aals = pd.concat([aal_summary, combined_aal], ignore_index=True)

# Reorder and sort columns for output
final_aal_cols = ['iso3cd', 'hazard', 'Loss', 'pop', 'cap_stock_capita', 'gdp_capita', 'GDP']
giri_aals = giri_aals[final_aal_cols].sort_values(['iso3cd', 'hazard']).reset_index(drop=True)

# Save GIRI_AALs to CSV
giri_aals.to_csv(aals_file_path, index=False)
print(f"GIRI_AALs summary dataset saved successfully to: {aals_file_path}")
print(f"GIRI_AALs shape: {giri_aals.shape}")