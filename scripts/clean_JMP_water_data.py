#%%
"""
Process JMP WASH drinking water data for Sub-Saharan Africa
Extracts urban drinking water access indicators from JMP_WASH_HH_2025_by_country-2.xlsx
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
output_dir = os.path.join(project_root, 'data', 'processed', 'jmp_water')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

indicator_columns = ['At least basic', 'Limited (more than 30 mins)', 'Unimproved', 'Surface water']

#%%
# Read the 'wat' sheet which has ISO3 codes and structured data
df = pd.read_excel(raw_file, sheet_name='wat')

# Select relevant columns including population data
water_data = df[['iso3', 'year', 'pop_t', 'prop_u', 'wat_basal_u', 'wat_lim_u', 'wat_unimp_u', 'wat_ns_u']].copy()

# Rename columns to the project's target schema
water_data.columns = ['Country Code', 'Year', 'Total Population (thousands)', 'Urban Population Proportion'] + indicator_columns

# Convert year to integer
water_data['Year'] = water_data['Year'].astype(int)

# Divide indicator columns by 100 to convert from percentage to decimal
for col in indicator_columns:
    water_data[col] = water_data[col] / 100

# Calculate urban population: pop_t (thousands) * prop_u (proportion) prop_u is already a percentage (0-100), so just multiply by pop_t * 10 to get actual urban population
water_data['Urban Population'] = water_data['Total Population (thousands)'] * water_data['Urban Population Proportion'] * 10

# Filter water data to only SSA countries
water_data = water_data[water_data['Country Code'].isin(ssa_countries.keys())]

# Drop the original population columns
water_data = water_data.drop(['Total Population (thousands)', 'Urban Population Proportion'], axis=1)

# Remove rows with missing country code or year
water_data = water_data.dropna(subset=['Country Code', 'Year'])

# Remove rows with missing indicator values
water_data = water_data.dropna(subset=indicator_columns, how='all')
#%%

# Load WB Classification for region mapping
wb_classification = pd.read_csv(os.path.join(project_root, 'data', 'Definitions', 'WB_Classification.csv'))
wb_ssa = wb_classification[wb_classification['Region Code'] == 'SSA'][['ISO3', 'Subregion Code']].copy()

# Create region mapping
country_to_subregion = wb_ssa.set_index('ISO3')['Subregion Code'].to_dict()

# Add subregion column
water_data['Subregion'] = water_data['Country Code'].map(country_to_subregion)

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
regional_aggregates.extend(aggregate_regional_data(water_data, 'SSA'))

# 2. AFE and AFW: aggregate by subregion
for subregion in ['AFE', 'AFW']:
    subregion_data = water_data[water_data['Subregion'] == subregion].copy()
    regional_aggregates.extend(aggregate_regional_data(subregion_data, subregion))

# Convert regional aggregates to DataFrame
regional_df = pd.DataFrame(regional_aggregates)

# Combine country-level and regional data (still in wide format)
combined_data = pd.concat([water_data, regional_df], ignore_index=True)

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
output_file = os.path.join(output_dir, 'urban_drinking_water_ssa.csv')
final_data.to_csv(output_file, index=False)

print(f"\n✓ Saved: {output_file}")
print(f"Total records: {len(final_data)}")
print(f"Countries: {final_data[final_data['Country Code'].str.len() == 3]['Country Code'].nunique()}")
print(f"Regions: {sorted(final_data[final_data['Country Code'].str.len() == 3]['Country Code'].unique())}")
