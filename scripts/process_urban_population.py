#%%
'''  Get urban projection data from UN DESA '''

import pandas as pd
import warnings
warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils.country_utils import load_subsaharan_countries_dict
from src.utils.benchmark_config import get_benchmark_names

# Load countries from centralized CSV + regional aggregates
SUB_SAHARAN_COUNTRIES = list(load_subsaharan_countries_dict().keys())
REGIONAL_CODES = list(get_benchmark_names().keys())
ALL_COUNTRY_CODES = SUB_SAHARAN_COUNTRIES + REGIONAL_CODES

# Create mapping between Country Code and ISO3 from WUP locations file
locations_df = pd.read_csv('data/raw/Urban/WUP2018-F00-LOCATIONS_clean.csv')
country_code_to_iso3 = dict(zip(locations_df['Country Code'].astype(int), locations_df['ISO3']))

def load_wup_excel(file_path, sheet_name='Data', skiprows=16):
    """Load WUP Excel file and map country codes to ISO3."""
    df = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=skiprows, header=0)
    df['ISO3'] = df['Country code'].astype(int).map(country_code_to_iso3)
    return df.set_index('ISO3')

def CountryFile(ISO3):
    df = pd.DataFrame()
    
    # Retrieve WPP 2022 estimates
    for prob in ['Median', 'Lower 95', 'Lower 80', 'Upper 80', 'Upper 95']:
        wpp = pd.read_excel('data/raw/Urban/UN_PPP2022_Output_PopTot.xlsx', sheet_name = prob, skiprows = 16, header = 0)
        wpp['ISO3'] = wpp['Location code'].astype(int).map(country_code_to_iso3)
        wpp = wpp.set_index('ISO3') # Map Location code to ISO3 and set as index
        
        for year in range(2022, 2101):
            df.at[f'wpp_{prob.lower().replace(" ", "")}', year] = wpp.at[ISO3, year]/1000
        # Fill 2021 values with 2022 values interpolaitng between 2022 and 2023
        delta = df.at[f'wpp_{prob.lower().replace(" ", "")}', 2023] - df.at[f'wpp_{prob.lower().replace(" ", "")}', 2022]
        df.at[f'wpp_{prob.lower().replace(" ", "")}', 2021] = (df.at[f'wpp_{prob.lower().replace(" ", "")}', 2022] - delta)
    
    # Retrieve WUP 2018 estimates
    wup_urban_prop = load_wup_excel('data/raw/Urban/WUP2018-F02-Proportion_Urban.xlsx')
    wup_urban_pop = load_wup_excel('data/raw/Urban/WUP2018-F03-Urban_Population.xlsx')
    wup_rural_pop = load_wup_excel('data/raw/Urban/WUP2018-F04-Rural_Population.xlsx')

    for year in range(1950, 2055, 5):
        df.at['wup_urban_prop', year] = wup_urban_prop.at[ISO3, year]/100
        df.at['wup_urban_pop', year] = wup_urban_pop.at[ISO3, year]/1000
        df.at['wup_rural_pop', year] = wup_rural_pop.at[ISO3, year]/1000

    # Interpolate for every year between 1950 and 2050
    for var in ['wup_urban_prop', 'wup_urban_pop', 'wup_rural_pop']:
        for year in range(1950, 2050, 5):
            for k in range(1, 5):
                df.at[var, year + k] = df.at[var, year] + (df.at[var, year + 5] - df.at[var, year]) * k / 5

    # Calculate 'wup_rural_prop' as 1 - 'wup_urban_prop' for all years
    for year in range(1950, 2051):
        df.at['wup_rural_prop', year] = 1 - df.at['wup_urban_prop', year]
    
    for aoi in ['urban', 'rural']:
        for prob in ['median', 'lower95', 'lower80', 'upper80', 'upper95']:
            for year in range(2025, 2051, 1):
                df.at[f'{aoi}_pop_{prob}', year] = df.at[f'wup_{aoi}_pop', year] * (df.at[f'wpp_{prob}', year] / df.at['wpp_median', year])
                # I'm not sure why I need the relative values, commenting out for now
                # df.at[f'{aoi}_pop_{prob}_rel', year] = df.at[f'{aoi}_pop_{prob}', year] / df.at[f'{aoi}_pop_{prob}', 2025]

    # Reorder columns by year in ascending order
    year_columns = [col for col in df.columns if isinstance(col, int)]
    return df[sorted(year_columns)]

# Process all Sub-Saharan African countries

for ISO3 in SUB_SAHARAN_COUNTRIES:
    df = CountryFile(ISO3)
    output_path = f'data/processed/UNDESA_Country/{ISO3}_urban_population_projections.csv'
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
        file_path = f'data/processed/UNDESA_Country/{iso3}_urban_population_projections.csv'
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
    output_path = f'data/processed/UNDESA_Country/{region_code}_urban_population_projections.csv'
    regional_df.to_csv(output_path)
    print(f"Saved regional aggregate to {output_path}")

#%%

# Consolidate all UNDESA urban population projection files into one long format DataFrame

consolidated_data = []
for ISO3 in ALL_COUNTRY_CODES:
    print(ISO3)
    
    # Read the CSV file
    df = pd.read_csv(f"data/processed/UNDESA_Country/{ISO3}_urban_population_projections.csv", index_col=0)
    
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

# Save consolidated DataFrame
final_df.to_csv('data/processed/UNDESA_Country/UNDESA_urban_projections_consolidated.csv', index=False)

# %%
