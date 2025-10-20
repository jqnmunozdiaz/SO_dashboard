#%%
"""
Process JMP WASH sanitation data for Sub-Saharan Africa
Extracts urban sanitation access indicators from JMP_WASH_HH_2025_by_country-2.xlsx
"""

import pandas as pd
import os
import sys

# Add parent directory to path to import utilities
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Load Sub-Saharan African countries and regions
from src.utils.country_utils import load_subsaharan_countries_dict
ssa_countries = load_subsaharan_countries_dict()

# Get project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
raw_file = os.path.join(project_root, 'data', 'raw', 'JMP_WASH_HH_2025_by_country-2.xlsx')
output_dir = os.path.join(project_root, 'data', 'processed', 'jmp_sanitation')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

indicator_columns = ['At least basic', 'Limited (shared)', 'Unimproved', 'Open defecation']

#%%
# Read the 'san' sheet for sanitation data
df = pd.read_excel(raw_file, sheet_name='san')

# Select relevant columns including population data
sanitation_data = df[['iso3', 'year', 'pop_t', 'prop_u', 'san_basal_u', 'san_lim_u', 'san_unimp_u', 'san_ns_u']].copy()

# Rename columns to the project's target schema
sanitation_data.columns = ['Country Code', 'Year', 'Total Population (thousands)', 'Urban Population Proportion'] + indicator_columns

# Convert year to integer
sanitation_data['Year'] = sanitation_data['Year'].astype(int)

# Divide indicator columns by 100 to convert from percentage to decimal
for col in indicator_columns:
    sanitation_data[col] = sanitation_data[col] / 100

# Calculate urban population: pop_t (thousands) * prop_u (proportion) prop_u is already a percentage (0-100), so just multiply by pop_t * 10 to get actual urban population
sanitation_data['Urban Population'] = sanitation_data['Total Population (thousands)'] * sanitation_data['Urban Population Proportion'] * 10

# Filter sanitation data to only SSA countries
sanitation_data = sanitation_data[sanitation_data['Country Code'].isin(ssa_countries.keys())]

# Drop the original population columns
sanitation_data = sanitation_data.drop(['Total Population (thousands)', 'Urban Population Proportion'], axis=1)

# Remove rows with missing country code or year
sanitation_data = sanitation_data.dropna(subset=['Country Code', 'Year'])

# Remove rows with missing indicator values
sanitation_data = sanitation_data.dropna(subset=indicator_columns, how='all')
#%% 

# Load WB Classification for region mapping
wb_classification = pd.read_csv(os.path.join(project_root, 'data', 'Definitions', 'WB_Classification.csv'))
wb_ssa = wb_classification[wb_classification['Region Code'] == 'SSA'][['ISO3', 'Subregion Code']].copy()

# Create region mapping
country_to_subregion = wb_ssa.set_index('ISO3')['Subregion Code'].to_dict()

# Add subregion column
sanitation_data['Subregion'] = sanitation_data['Country Code'].map(country_to_subregion)

# Prepare regional aggregates list
regional_aggregates = []

# Define a helper function to aggregate regional data
def aggregate_regional_data(data, region_code):
    """
    Aggregate data for a region by calculating weighted averages for indicators.
    
    Args:
        data: DataFrame with country-level data
        region_code: String code for the region (e.g., 'SSA', 'AFE', 'AFW')
    
    Returns:
        List of dictionaries with aggregated data
    """
    aggregates = []
    for year in data['Year'].unique():
        year_data = data[data['Year'] == year].copy()
        
        # Calculate total urban population for this year
        total_urban_pop = year_data['Urban Population'].sum()
        
        if total_urban_pop > 0:
            # Calculate weighted average for each indicator
            regional_row = {'Country Code': region_code, 'Subregion': region_code, 'Year': year, 'Urban Population': total_urban_pop}
            
            for indicator in indicator_columns:
                # Weighted average: sum(value * weight) / sum(weight)
                weighted_value = (year_data[indicator] * year_data['Urban Population']).sum() / total_urban_pop
                regional_row[indicator] = weighted_value
            
            aggregates.append(regional_row)
    
    return aggregates

# 1. SSA: aggregate all Sub-Saharan Africa countries
regional_aggregates.extend(aggregate_regional_data(sanitation_data, 'SSA'))

# 2. AFE and AFW: aggregate by subregion
for subregion in ['AFE', 'AFW']:
    subregion_data = sanitation_data[sanitation_data['Subregion'] == subregion].copy()
    regional_aggregates.extend(aggregate_regional_data(subregion_data, subregion))

# Convert regional aggregates to DataFrame
regional_df = pd.DataFrame(regional_aggregates)

# Combine country-level and regional data (still in wide format)
combined_data = pd.concat([sanitation_data, regional_df], ignore_index=True)

# ===== NOW CONVERT TO LONG FORMAT =====
final_data = combined_data.melt(
    id_vars=['Country Code', 'Year'],
    value_vars=indicator_columns,
    var_name='Indicator',
    value_name='Value'
)

# Clean up
final_data = final_data.dropna(subset=['Value'])

# Sort final data
final_data = final_data.sort_values(by=['Country Code', 'Year', 'Indicator'])

# Save long format file
output_file = os.path.join(output_dir, 'urban_sanitation_ssa.csv')
final_data.to_csv(output_file, index=False)

print(f"\n✓ Saved: {output_file}")
print(f"Total records: {len(final_data)}")
print(f"Countries: {final_data[final_data['Country Code'].str.len() == 3]['Country Code'].nunique()}")
print(f"Regions: {sorted(final_data[final_data['Country Code'].str.len() == 3]['Country Code'].unique())}")

