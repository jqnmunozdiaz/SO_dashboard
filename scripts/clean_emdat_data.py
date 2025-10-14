"""
EM-DAT Data Cleaning Script for African Countries
Processes the raw EM-DAT Excel file and creates a cleaned CSV for the dashboard
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
from src.utils.country_utils import load_subsaharan_countries_dict, load_wb_regional_classifications
from config.settings import DATA_CONFIG

# Load World Bank regional classifications from centralized utilities
afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()

def clean_emdat_data(input_file, output_file):
    """
    Clean and process EM-DAT data for African countries
    
    Args:
        input_file: Path to raw EM-DAT Excel file
        output_file: Path to save cleaned CSV file
    """
    
    try:
        # Read the Excel file
        df = pd.read_excel(input_file)
                
        # Only keep rows where Disaster Type is in a predefined list of relevant types defined in 'disaster_type_selection.txt'
        with open('data/Definitions/disaster_type_selection.txt', 'r') as f:
            relevant_disasters = [line.strip() for line in f.readlines()]
        df = df[df['Disaster Type'].isin(relevant_disasters)]
        
        df = df[[ 'Disaster Type', 'ISO', 'Start Year', 'Total Deaths', 'Total Affected']]  # Columns, adjust as needed        
        df = df.rename(columns={'Start Year': 'Year'})
                           
        # Filter for Sub-Saharan African countries only by ISO codes
        df = df[df['ISO'].isin(ssa_countries)]
        
        # Process year column
        df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
        df = df.dropna(subset=['Year'])
        df['Year'] = df['Year'].astype(int)
        
        # Clean numeric columns
        numeric_columns = ['Total Deaths', 'Total Affected']
        for col in numeric_columns:
            # Handle string values like "No Data", "Unknown", etc.
            df[col] = df[col].replace(['No Data', 'Unknown', '', 'nan', 'NaN'], np.nan)
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(0)
            df[col] = df[col].astype(int) # Ensure deaths and affected_population are integers
    
        # Clean disaster types (just strip whitespace)
        df['Disaster Type'] = df['Disaster Type'].str.strip()
               
        # Remove rows with missing essential data
        df = df.dropna(subset=['Year', 'ISO', 'Disaster Type'])
        
        # Sort by year and country
        sort_columns = ['Year', 'ISO']
        df = df.sort_values(sort_columns)
        
        # Filter data from configured starting year onwards for consistent historical analysis
        start_year = DATA_CONFIG['emdat_start_year']
        df = df[df['Year'] >= start_year]
        
        # Compute regional aggregates
        regional_data = []
        
        # Define regional mappings
        region_mappings = {
            'AFE': afe_countries,
            'AFW': afw_countries,
            'SSA': ssa_countries
        }
        
        # Group by disaster type and year for aggregation
        for disaster_type in df['Disaster Type'].unique():
            for year in df['Year'].unique():
         
                # Filter data for this disaster type and year
                disaster_year_data = df[(df['Disaster Type'] == disaster_type) & (df['Year'] == year)]
                
                # Calculate aggregates for each region
                for region_code, country_list in region_mappings.items():
                    region_data = disaster_year_data[disaster_year_data['ISO'].isin(country_list)]
                    if not region_data.empty:
                        region_row = {
                            'Disaster Type': disaster_type,
                            'ISO': region_code,
                            'Year': year,
                            'Total Deaths': region_data['Total Deaths'].sum(),
                            'Total Affected': region_data['Total Affected'].sum()
                        }
                        regional_data.append(region_row)
        
        # Convert regional data to DataFrame and append to main data
        if regional_data:
            regional_df = pd.DataFrame(regional_data)
            df = pd.concat([df, regional_df], ignore_index=True)
        
        # Sort by year, ISO, and disaster type
        df = df.sort_values(['Year', 'ISO', 'Disaster Type'])
        
        # Save processed data
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
                                
        return df
        
    except Exception as e:
        print(f"Error processing EM-DAT data: {str(e)}")
        raise

if __name__ == "__main__":
    # File paths
    input_file = "data/raw/public_emdat_custom_request_2025-10-13_3908a057-51e5-4e3b-9c0a-3724c3e8dcf3.xlsx"
    output_file = "data/processed/african_disasters_emdat.csv"
    
    print("Starting EM-DAT data cleaning for African countries...")
    
    # Clean the data
    cleaned_data = clean_emdat_data(input_file, output_file)
    
    print(f"\nData cleaning complete! Clean data saved to: {output_file}")