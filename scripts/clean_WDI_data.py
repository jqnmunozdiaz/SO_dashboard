"""
WDI (World Development Indicators) Data Cleaning Script for Sub-Saharan African Countries
Processes the raw WDI CSV file and creates cleaned CSV files for each urbanization indicator
"""

import pandas as pd
import numpy as np
import os
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

# Import centralized country utilities
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils.country_utils import load_subsaharan_countries_dict, load_non_sub_saharan_countries_dict
from config.settings import DATA_CONFIG

# Load countries from centralized CSV + regional aggregates
SUB_SAHARAN_COUNTRIES = load_subsaharan_countries_dict()
# Add regional codes for benchmarking
REGIONAL_CODES = {'SSA': 'Sub-Saharan Africa', 'AFE': 'Eastern and Southern Africa', 'AFW': 'Western and Central Africa'}
ALL_COUNTRY_CODES = {**SUB_SAHARAN_COUNTRIES, **REGIONAL_CODES}


def clean_wdi_data(input_file, output_dir, indicators_file):
    """
    Clean and process WDI data for Sub-Saharan African countries and regional benchmarks
    Creates separate CSV files for each indicator
    
    Args:
        input_file: Path to raw WDI CSV file (WDICSV.csv)
        output_dir: Directory to save cleaned CSV files
        indicators_file: Path to CSV file with indicator codes and names to process
    """
    try:
        # Load indicator codes and names from CSV file
        indicators_df = pd.read_csv(indicators_file)
        indicator_codes = indicators_df['Indicator_Code'].tolist()
        # Create mapping of codes to names for consistent naming
        indicator_names_map = dict(zip(indicators_df['Indicator_Code'], indicators_df['Indicator_Name']))
        
        # Read the main WDI CSV file
        df = pd.read_csv(input_file)
        
        # Filter for our target countries and regions
        target_codes = list(ALL_COUNTRY_CODES.keys())
        df = df[df['Country Code'].isin(target_codes)]
        
        # Filter for our target indicators
        df = df[df['Indicator Code'].isin(indicator_codes)]
        
        if df.empty:
            return
        
        # Get year columns (skip the first 4 metadata columns)
        year_columns = [col for col in df.columns if col.isdigit()]
        
        # Filter years from configured starting year onwards
        start_year = DATA_CONFIG['emdat_start_year']
        year_columns = [col for col in year_columns if int(col) >= start_year]
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Process each indicator separately
        for indicator_code in indicator_codes:
            # Filter for current indicator
            indicator_df = df[df['Indicator Code'] == indicator_code].copy()
            
            if indicator_df.empty:
                continue
            
            # Select relevant columns
            base_columns = ['Country Code']
            selected_columns = base_columns + year_columns
            indicator_df = indicator_df[selected_columns]
            
            # Melt the data from wide to long format
            melted_df = indicator_df.melt(
                id_vars=base_columns,
                value_vars=year_columns,
                var_name='Year',
                value_name='Value'
            )
            
            # Clean the data
            melted_df['Year'] = melted_df['Year'].astype(int)
            
            # Handle missing values - replace with NaN for percentage indicators, keep as NaN
            melted_df['Value'] = pd.to_numeric(melted_df['Value'], errors='coerce')
            
            # Remove rows with missing essential data
            melted_df = melted_df.dropna(subset=['Year', 'Country Code', 'Value'])
                  
            # Sort by year and country
            melted_df = melted_df.sort_values(['Year', 'Country Code'])
                  
            # Save to CSV
            output_file = os.path.join(output_dir, f"{indicator_code}.csv")
            melted_df.to_csv(output_file, index=False)
        return True
        
    except Exception as e:
        print(f"Error processing WDI data: {str(e)}")
        raise


if __name__ == "__main__":
    # File paths
    input_file = "data/raw/WDI_CSV/WDICSV.csv"
    output_dir = "data/processed/wdi"
    indicators_file = "data/Definitions/urbanization_indicators_selection.csv"
    
    # Clean the data
    success = clean_wdi_data(input_file, output_dir, indicators_file)
    
    if success:
        print(f"\nData cleaning complete! Clean data saved to: {output_dir}")
    else:
        print("\nData cleaning failed. Check the logs for details.")