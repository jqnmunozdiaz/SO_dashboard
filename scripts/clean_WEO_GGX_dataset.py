"""
WEO (World Economic Outlook) GGX_NGDP Data Cleaning Script for Sub-Saharan African Countries
Processes the raw WEO XLS/TSV file and creates a cleaned CSV file containing the most recent government expenditure values.
"""

import os
import sys
import pandas as pd

# Resolve project root to import centralized country utilities
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
sys.path.append(PROJECT_ROOT)

from src.utils.country_utils import load_subsaharan_countries_dict

# Define file paths relative to project root
input_file = os.path.join(PROJECT_ROOT, 'data', 'raw', 'WEO_Data.xlsx')
output_file = os.path.join(PROJECT_ROOT, 'data', 'processed', 'WEO_GGX_NGDP_cleaned.csv')
  
print(f"Loading raw WEO data from: {input_file}...")
# Read the excel file
df = pd.read_excel(input_file)

# Cast column names to string to handle numeric and string years robustly
df.columns = df.columns.astype(str)

# Filter for our specific subject code: General government total expenditure in percent of GDP (GGX_NGDP)
df_exp = df[df['WEO Subject Code'] == 'GGX_NGDP'].copy()

if df_exp.empty:
    sys.exit("Error: No rows found matching WEO Subject Code 'GGX_NGDP'.")
    
# Get centralized list of Sub-Saharan African countries
ssa_countries = load_subsaharan_countries_dict()

# Filter for SSA countries using the ISO column
df_ssa = df_exp[df_exp['ISO'].isin(ssa_countries.keys())].copy()

print(f"Found {len(df_ssa)} SSA countries in the dataset.")

# Convert '2025' column to numeric, converting string N/As (like 'n/a' or '--') to NaN
df_ssa['2025'] = pd.to_numeric(df_ssa['2025'], errors='coerce')
    
# Extract the 2025 value for each country
cleaned_records = []
for _, row in df_ssa.iterrows():
    iso = row['ISO']
    # Use official country name from country utilities if available, else fallback to WEO's name
    country_name = ssa_countries.get(iso, row['Country'])
    
    val = row['2025']
    
    # Skip if no valid value was found (handles the "remove the n/a" requirement)
    if pd.notna(val):
        cleaned_records.append({
            'ISO3': iso,
            'Country': country_name,
            'Value': val,
            'Year': 2025
        })
        
# Create a DataFrame from the cleaned records
cleaned_df = pd.DataFrame(cleaned_records)

if cleaned_df.empty:
    sys.exit("Warning: Cleaned dataset is empty. No valid values found.")
    
# Ensure output directory exists
output_dir = os.path.dirname(output_file)
if output_dir:
    os.makedirs(output_dir, exist_ok=True)
    
# Sort for clean presentation
cleaned_df = cleaned_df.sort_values('ISO3').reset_index(drop=True)

# Save to CSV
cleaned_df.to_csv(output_file, index=False)
print(f"Successfully saved {len(cleaned_df)} rows to: {output_file}")
print("WEO GGX_NGDP data cleaning completed successfully!")
