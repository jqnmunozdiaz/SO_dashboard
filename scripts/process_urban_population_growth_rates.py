"""
Process urban population growth rates from UN DESA projections
Calculates annualized CAGR (Compound Annual Growth Rate) for 5-year periods
Outputs: data/processed/UNDESA_Country/UNDESA_urban_growth_rates_consolidated.csv
"""

import pandas as pd
import os
import sys

# Add project root to path for imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from src.utils.data_loader import load_undesa_urban_projections

undesa_data = load_undesa_urban_projections()

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
output_dir = os.path.join(project_root, 'data', 'processed', 'UNDESA_Country')
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'UNDESA_urban_growth_rates_consolidated.csv')

# Save to CSV
growth_rates_df.to_csv(output_path, index=False)
