#%%
'''  Get urban projection data from UN DESA (WUP2025 and WPP2024) '''

import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils.country_utils import load_subsaharan_countries_dict
from src.utils.benchmark_config import get_benchmark_names
from src.utils.data_loader import load_WUP_urban_projections
# Get project root for output paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load countries from centralized CSV + regional aggregates
SUB_SAHARAN_COUNTRIES = list(load_subsaharan_countries_dict().keys())
REGIONAL_CODES = list(get_benchmark_names().keys())
ALL_COUNTRY_CODES = SUB_SAHARAN_COUNTRIES + REGIONAL_CODES

# Load WUP2025 data (already includes ISO3 codes)
def load_wup2025_data():
    """Load WUP2025 population data with ISO3 codes."""
    df = pd.read_csv('data/processed/WUP/WUP2025_National_Definitions_Population_processed_pivoted.csv')
    return df.set_index('ISO3_Code')

def CountryFile(ISO3):
    # Use a dictionary to collect data before creating DataFrame
    data_dict = {}
    
    # Retrieve WPP 2024 estimates (total population with uncertainty)
    wpp_sheets = {
        'Median': 'wpp_median',
        'Lower 95': 'wpp_lower95',
        'Lower 80': 'wpp_lower80',
        'Upper 80': 'wpp_upper80',
        'Upper 95': 'wpp_upper95'
    }
    
    # Create mapping from location code to ISO3 for WPP data
    locations_df = pd.read_csv('data/raw/Urban/WUP2018-F00-LOCATIONS_clean.csv')
    location_code_to_iso3 = dict(zip(locations_df['Country Code'].astype(int), locations_df['ISO3']))
    
    for sheet_name, indicator_name in wpp_sheets.items():
        wpp = pd.read_excel('data/raw/Urban/UN_PPP2024_Output_PopTot.xlsx', sheet_name=sheet_name, skiprows=16, header=0)
        wpp['ISO3'] = wpp['Location code'].astype(int).map(location_code_to_iso3)
        wpp = wpp.set_index('ISO3')
        
        # Initialize indicator row
        data_dict[indicator_name] = {}
        
        # Extract data for years 2024-2100 (convert from thousands to millions)
        if ISO3 in wpp.index:
            for year in range(2024, 2101):
                if year in wpp.columns:
                    data_dict[indicator_name][year] = wpp.at[ISO3, year] / 1000
            
            # Backfill 2021-2023 by linear interpolation
            if 2024 in data_dict[indicator_name] and 2025 in data_dict[indicator_name]:
                delta = data_dict[indicator_name][2025] - data_dict[indicator_name][2024]
                data_dict[indicator_name][2023] = data_dict[indicator_name][2024] - delta
                data_dict[indicator_name][2022] = data_dict[indicator_name][2023] - delta
                data_dict[indicator_name][2021] = data_dict[indicator_name][2022] - delta
    
    # Retrieve WUP2025 historical and projection data
    wup2025 = load_wup2025_data()
    
    # Initialize WUP indicator rows
    for indicator in ['wup_urban_pop', 'wup_rural_pop', 'wup_urban_prop', 'wup_rural_prop']:
        data_dict[indicator] = {}
    
    if ISO3 in wup2025.index:
        country_wup = wup2025.loc[[ISO3]].copy()
        
        for _, row in country_wup.iterrows():
            year = int(row['Year'])
            # Store historical/projection data (convert from actual population to millions)
            data_dict['wup_urban_pop'][year] = row['Urban_Pop'] / 1e6
            data_dict['wup_rural_pop'][year] = row['Rural_Pop'] / 1e6
            data_dict['wup_urban_prop'][year] = row['Urbanization_Rate']
            data_dict['wup_rural_prop'][year] = 1 - row['Urbanization_Rate']
    
    # Create DataFrame from dictionary (more efficient than incremental assignment)
    df = pd.DataFrame(data_dict).T
    
    # Calculate urban/rural population projections with uncertainty bounds
    for aoi in ['urban', 'rural']:
        for prob in ['median', 'lower95', 'lower80', 'upper80', 'upper95']:
            indicator_name = f'{aoi}_pop_{prob}'
            data_dict[indicator_name] = {}
            
            wpp_col = f'wpp_{prob}'
            wup_pop_col = f'wup_{aoi}_pop'
            
            # Calculate for all years where we have both WUP proportions and WPP total population
            for year in range(1950, 2101):
                if (year in df.columns and 
                    wpp_col in df.index and 
                    wup_pop_col in df.index and
                    pd.notna(df.at[wup_pop_col, year]) and 
                    pd.notna(df.at['wpp_median', year]) and 
                    pd.notna(df.at[wpp_col, year])):
                    # Scale WUP population by ratio of WPP uncertainty to WPP median
                    data_dict[indicator_name][year] = df.at[wup_pop_col, year] * (
                        df.at[wpp_col, year] / df.at['wpp_median', year]
                    )
    
    # Rebuild DataFrame with all indicators at once
    df = pd.DataFrame(data_dict).T
    
    # Reorder columns by year in ascending order
    year_columns = [col for col in df.columns if isinstance(col, int)]
    return df[sorted(year_columns)]

# Process all Sub-Saharan African countries
for ISO3 in SUB_SAHARAN_COUNTRIES:
    df = CountryFile(ISO3)
    output_path = f'data/processed/WUP/{ISO3}_urban_population_projections.csv'
    df.to_csv(output_path)
    print(f"Successfully processed {ISO3}")

#%%
# Aggregate values for regional codes AFE, AFW, SSA based on countries in those regions as specified in the WB_Classification file

wb_classification_file = 'data/Definitions/WB_Classification.csv'
wb_df = pd.read_csv(wb_classification_file)

# Create regional mappings
regional_mappings = {
    'AFE': wb_df[wb_df['Subregion Code'] == 'AFE']['ISO3'].tolist(),
    'AFW': wb_df[wb_df['Subregion Code'] == 'AFW']['ISO3'].tolist(),
    'SSA': wb_df[wb_df['Region Code'] == 'SSA']['ISO3'].tolist()  # All Sub-Saharan countries
}
# Define indicators that should be summed (population values)
sum_indicators = [
    'wpp_median', 'wpp_lower95', 'wpp_lower80', 'wpp_upper80', 'wpp_upper95',
    'wup_urban_pop', 'wup_rural_pop',
    'urban_pop_median', 'urban_pop_lower95', 'urban_pop_lower80', 'urban_pop_upper80', 'urban_pop_upper95',
    'rural_pop_median', 'rural_pop_lower95', 'rural_pop_lower80', 'rural_pop_upper80', 'rural_pop_upper95'
]

# Define relative indicators (these are derived, so we'll skip them for now)
relative_indicators = [
    'urban_pop_median_rel', 'urban_pop_lower95_rel', 'urban_pop_lower80_rel', 
    'urban_pop_upper80_rel', 'urban_pop_upper95_rel'
]

# Process each region
for region_code, country_list in regional_mappings.items():
    print(f"\nProcessing region: {region_code}")
       
    # Load data for all countries in this region
    country_data = {}
    for iso3 in country_list:
        file_path = f'data/processed/WUP/{iso3}_urban_population_projections.csv'
        df = pd.read_csv(file_path, index_col=0)
        country_data[iso3] = df
        
    # Get all possible years from all countries (keep as strings to match DataFrame columns)
    all_years = set()
    for df in country_data.values():
        all_years.update(df.columns)
    all_years = sorted(all_years)
    
    # Get all indicators from the first available country
    first_country_data = next(iter(country_data.values()))
    all_indicators = first_country_data.index.tolist()
    
    # Initialize regional DataFrame
    regional_df = pd.DataFrame(index=all_indicators, columns=all_years)
    
    # Process each indicator
    for indicator in sum_indicators:
        print(f"Processing indicator: {indicator}")
        for year in all_years:
            # Sum the population values
            total_value = 0
            countries_with_data = 0
            for iso3, df in country_data.items():
                if year in df.columns and indicator in df.index:
                    value = df.loc[indicator, year]
                    if pd.notna(value):
                        total_value += value
                        countries_with_data += 1
            
            regional_df.loc[indicator, year] = total_value if countries_with_data > 0 else pd.NA
    
    # Process proportion indicators (proportion_indicators = 'wup_urban_prop', 'wup_rural_prop')
    for year in all_years:
        regional_df.loc['wup_urban_prop', year] = regional_df.loc['wup_urban_pop', year] / (regional_df.loc['wup_urban_pop', year] + regional_df.loc['wup_rural_pop', year]) if pd.notna(regional_df.loc['wup_urban_pop', year]) else pd.NA
        regional_df.loc['wup_rural_prop', year] = 1 - regional_df.loc['wup_urban_prop', year]

    # Save regional data
    output_path = f'data/processed/WUP/{region_code}_urban_population_projections.csv'
    regional_df.to_csv(output_path)
    print(f"Saved regional aggregate to {output_path}")

#%% # Consolidate all UNDESA urban population projection files into one long format DataFrame

consolidated_data = []
for ISO3 in ALL_COUNTRY_CODES:
    print(ISO3)
    
    # Read the CSV file
    df = pd.read_csv(f"data/processed/WUP/{ISO3}_urban_population_projections.csv", index_col=0)
    
    # Convert to long format
    # Reset index to make the indicator names a column
    df = df.reset_index()
    df.rename(columns={'index': 'indicator'}, inplace=True)
    
    # Melt the DataFrame to convert years to rows
    df_long = pd.melt(
        df,
        id_vars=['indicator'],
        var_name='year',
        value_name='value'
    )
    
    # Add country information
    df_long['ISO3'] = ISO3

    # Convert year to integer (handle potential string years)
    df_long['year'] = pd.to_numeric(df_long['year'], errors='coerce')
    
    # Remove rows with NaN values (years or values)
    df_long = df_long.dropna(subset=['year', 'value'])
    
    # Reorder columns for better readability
    df_long = df_long[['ISO3', 'indicator', 'year', 'value']]

    consolidated_data.append(df_long)
    
# Concatenate all DataFrames
final_df = pd.concat(consolidated_data, ignore_index=True)

# Sort by country, indicator, and year for better organization
final_df = final_df.sort_values(['ISO3', 'indicator', 'year']).reset_index(drop=True)

# Filter to keep only years that are multiples of 5 between 1950 and 2100
final_df = final_df[(final_df['year'] % 5 == 0) & (final_df['year'] >= 1950) & (final_df['year'] <= 2050)]

# Save consolidated DataFrame
final_df.to_csv('data/processed/WUP/WUP2025_urban_projections_consolidated.csv', index=False)

# %%
# Remove individual country files after consolidation

for ISO3 in ALL_COUNTRY_CODES:
    file_path = f'data/processed/WUP/{ISO3}_urban_population_projections.csv'
    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"Removed {file_path}")

#%%

"""
Process urban population growth rates from UN DESA projections
Calculates annualized CAGR (Compound Annual Growth Rate) for 5-year periods
Outputs: data/processed/WUP/WUP2025_urban_growth_rates_consolidated.csv
"""

undesa_data = load_WUP_urban_projections()
countries = undesa_data['ISO3'].unique() # Get unique countries
all_growth_rates = []

for country in countries:    
    # Filter data for this country
    country_data = undesa_data[undesa_data['ISO3'] == country].copy()
    
    # Pivot data for easier access
    country_pivot = country_data.pivot(index='year', columns='indicator', values='value')
    
    # Sort by year to ensure proper ordering
    country_pivot = country_pivot.sort_index()
    
    # Calculate annualized growth rates (CAGR) for historical data (wup_urban_pop and wup_rural_pop)
    for aoi in ['urban', 'rural']:
        col_name = f'wup_{aoi}_pop'
        if col_name in country_pivot.columns:
            growth_rate_col = f'{aoi}_growth_rate'
            # Calculate CAGR: ((end_value / start_value) ^ (1/years)) - 1) * 100
            # For 5-year periods, years = 5
            country_pivot[growth_rate_col] = (
                (country_pivot[col_name] / country_pivot[col_name].shift(1)) ** (1/5) - 1
            ) * 100
            
            # Convert back to long format
            growth_data = country_pivot[[growth_rate_col]].reset_index()
            growth_data['ISO3'] = country
            growth_data['indicator'] = growth_rate_col
            growth_data = growth_data.rename(columns={growth_rate_col: 'value'})
            growth_data = growth_data[['ISO3', 'year', 'indicator', 'value']]
            all_growth_rates.append(growth_data)
    
    # Calculate annualized growth rates (CAGR) for projections (median and uncertainty bounds)
    for aoi in ['urban', 'rural']:
        # Median growth rate
        median_col = f'{aoi}_pop_median'
        if median_col in country_pivot.columns:
            growth_rate_col = f'{aoi}_median_growth_rate'
            country_pivot[growth_rate_col] = (
                (country_pivot[median_col] / country_pivot[median_col].shift(1)) ** (1/5) - 1
            ) * 100
            
            # Fill 2025 with historical growth rate for continuity
            historical_growth_col = f'{aoi}_growth_rate'
            if 2025 in country_pivot.index and historical_growth_col in country_pivot.columns:
                country_pivot.loc[2025, growth_rate_col] = country_pivot.loc[2025, historical_growth_col]
            
            growth_data = country_pivot[[growth_rate_col]].reset_index()
            growth_data['ISO3'] = country
            growth_data['indicator'] = growth_rate_col
            growth_data = growth_data.rename(columns={growth_rate_col: 'value'})
            growth_data = growth_data[['ISO3', 'year', 'indicator', 'value']]
            all_growth_rates.append(growth_data)
        
        # Lower and upper 80% growth rates
        for bound in ['lower80', 'upper80']:
            col_name = f'{aoi}_pop_{bound}'
            if col_name in country_pivot.columns:
                growth_rate_col = f'{aoi}_{bound}_growth_rate'
                country_pivot[growth_rate_col] = (
                    (country_pivot[col_name] / country_pivot[col_name].shift(1)) ** (1/5) - 1
                ) * 100
                
                # Fill 2025 with historical growth rate for continuity
                historical_growth_col = f'{aoi}_growth_rate'
                if 2025 in country_pivot.index and historical_growth_col in country_pivot.columns:
                    country_pivot.loc[2025, growth_rate_col] = country_pivot.loc[2025, historical_growth_col]
                
                growth_data = country_pivot[[growth_rate_col]].reset_index()
                growth_data['ISO3'] = country
                growth_data['indicator'] = growth_rate_col
                growth_data = growth_data.rename(columns={growth_rate_col: 'value'})
                growth_data = growth_data[['ISO3', 'year', 'indicator', 'value']]
                all_growth_rates.append(growth_data)
        
        # Lower and upper 95% growth rates
        for bound in ['lower95', 'upper95']:
            col_name = f'{aoi}_pop_{bound}'
            if col_name in country_pivot.columns:
                growth_rate_col = f'{aoi}_{bound}_growth_rate'
                country_pivot[growth_rate_col] = (
                    (country_pivot[col_name] / country_pivot[col_name].shift(1)) ** (1/5) - 1
                ) * 100
                
                # Fill 2025 with historical growth rate for continuity
                historical_growth_col = f'{aoi}_growth_rate'
                if 2025 in country_pivot.index and historical_growth_col in country_pivot.columns:
                    country_pivot.loc[2025, growth_rate_col] = country_pivot.loc[2025, historical_growth_col]
                
                growth_data = country_pivot[[growth_rate_col]].reset_index()
                growth_data['ISO3'] = country
                growth_data['indicator'] = growth_rate_col
                growth_data = growth_data.rename(columns={growth_rate_col: 'value'})
                growth_data = growth_data[['ISO3', 'year', 'indicator', 'value']]
                all_growth_rates.append(growth_data)

# Combine all growth rates
growth_rates_df = pd.concat(all_growth_rates, ignore_index=True)

growth_rates_df = growth_rates_df.dropna(subset=['value'])
# Sort by country and year
growth_rates_df = growth_rates_df.sort_values(['ISO3', 'year', 'indicator'])

# Define output path
output_dir = os.path.join(project_root, 'data', 'processed', 'WUP')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'WUP2025_urban_growth_rates_consolidated.csv')

# Save to CSV
growth_rates_df.to_csv(output_path, index=False)

# %%
