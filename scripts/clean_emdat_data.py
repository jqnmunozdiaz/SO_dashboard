"""
EM-DAT Data Cleaning Script for African Countries
Processes the raw EM-DAT Excel file and creates a cleaned CSV for the dashboard
"""

import pandas as pd
import numpy as np
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import centralized country utilities
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils.country_utils import load_subsaharan_countries_dict, load_non_sub_saharan_countries_dict

# Load countries from centralized CSV
SUB_SAHARAN_COUNTRIES = load_subsaharan_countries_dict()

# Non-Sub-Saharan African countries to exclude
NON_SUB_SAHARAN_COUNTRIES = set(load_non_sub_saharan_countries_dict().keys())


def clean_emdat_data(input_file, output_file):
    """
    Clean and process EM-DAT data for African countries
    
    Args:
        input_file: Path to raw EM-DAT Excel file
        output_file: Path to save cleaned CSV file
    """
    logger.info(f"Processing EM-DAT data from {input_file}")
    
    try:
        # Read the Excel file
        df = pd.read_excel(input_file)
        logger.info(f"Original data shape: {df.shape}")
        logger.info(f"Columns: {list(df.columns)}")
        
        # Display first few rows to understand structure
        logger.info("First 5 rows:")
        logger.info(df.head().to_string())

        df = df[df['Disaster Group'] == 'Natural']
        # Only keep rows where Disaster Type is in a predefined list of relevant types defined in 'disaster_type_selection.txt'
        with open('data/raw/disaster_type_selection.txt', 'r') as f:
            relevant_disasters = [line.strip() for line in f.readlines()]
        df = df[df['Disaster Type'].isin(relevant_disasters)]
        
        df = df[[ 'Disaster Type', 'ISO', 'Start Year', 'Total Deaths', 'Total Affected']]  # Example columns, adjust as needed        
        df = df.rename(columns={'Start Year': 'Year'})
            
        # Filter for Sub-Saharan African countries only
        ssa_iso_codes = list(SUB_SAHARAN_COUNTRIES.keys())
               
        # Filter for Sub-Saharan African countries only by ISO codes
        df = df[df['ISO'].isin(ssa_iso_codes)]
        logger.info(f"African data shape: {df.shape}")
        
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
        
        # Filter recent years for better dashboard performance (last 50 years)
        current_year = 2025
        df = df[df['Year'] >= (current_year - 50)]
        
        # Save processed data
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
                        
        return df
        
    except Exception as e:
        logger.error(f"Error processing EM-DAT data: {str(e)}")
        raise

if __name__ == "__main__":
    # File paths
    input_file = "data/raw/public_emdat_custom_request_2025-10-10_34470450-8ec8-4c41-97f9-eb266c759d8b.xlsx"
    output_file = "data/processed/african_disasters_emdat.csv"
    
    print("Starting EM-DAT data cleaning for African countries...")
    
    # Clean the data
    cleaned_data = clean_emdat_data(input_file, output_file)
    
    print(f"\nData cleaning complete! Clean data saved to: {output_file}")
    print("You can now use this data in the dashboard callbacks.")