"""
EM-DAT Data Cleaning Script for African Countries
Processes the raw EM-DAT Excel file and creates a cleaned CSV for the dashboard
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Sub-Saharan African countries list (ISO3 codes) - Excludes North African countries
SUB_SAHARAN_COUNTRIES = {
    'AGO': 'Angola', 'BEN': 'Benin', 'BWA': 'Botswana', 'BFA': 'Burkina Faso',
    'BDI': 'Burundi', 'CMR': 'Cameroon', 'CPV': 'Cape Verde', 'CAF': 'Central African Republic',
    'TCD': 'Chad', 'COM': 'Comoros', 'COG': 'Congo', 'COD': 'Democratic Republic of Congo',
    'DJI': 'Djibouti', 'GNQ': 'Equatorial Guinea', 'ERI': 'Eritrea', 'SWZ': 'Eswatini',
    'ETH': 'Ethiopia', 'GAB': 'Gabon', 'GMB': 'Gambia', 'GHA': 'Ghana', 'GIN': 'Guinea',
    'GNB': 'Guinea-Bissau', 'CIV': 'Ivory Coast', 'KEN': 'Kenya', 'LSO': 'Lesotho', 'LBR': 'Liberia',
    'MDG': 'Madagascar', 'MWI': 'Malawi', 'MLI': 'Mali', 'MRT': 'Mauritania',
    'MUS': 'Mauritius', 'MOZ': 'Mozambique', 'NAM': 'Namibia', 'NER': 'Niger',
    'NGA': 'Nigeria', 'RWA': 'Rwanda', 'STP': 'São Tomé and Príncipe', 'SEN': 'Senegal',
    'SYC': 'Seychelles', 'SLE': 'Sierra Leone', 'SOM': 'Somalia', 'ZAF': 'South Africa',
    'SSD': 'South Sudan', 'SDN': 'Sudan', 'TZA': 'Tanzania', 'TGO': 'Togo',
    'UGA': 'Uganda', 'ZMB': 'Zambia', 'ZWE': 'Zimbabwe'
}

# North African countries to exclude
NORTH_AFRICAN_COUNTRIES = {'DZA', 'EGY', 'LBY', 'MAR', 'TUN'}


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
        
        # Filter for Sub-Saharan African countries only
        ssa_iso_codes = list(SUB_SAHARAN_COUNTRIES.keys())
        
        # Check available country columns
        country_columns = [col for col in df.columns if 'country' in col.lower() or 'iso' in col.lower()]
        logger.info(f"Available country columns: {country_columns}")
        
        # Try to identify the correct country column
        country_col = None
        for col in df.columns:
            if col.upper() in ['ISO', 'ISO3', 'COUNTRY_ISO', 'ISO_CODE']:
                country_col = col
                break
            elif 'iso' in col.lower():
                country_col = col
                break
        
        if country_col is None:
            # Try country name column
            for col in df.columns:
                if col.upper() in ['COUNTRY', 'COUNTRY_NAME']:
                    country_col = col
                    break
                elif 'country' in col.lower():
                    country_col = col
                    break
        
        if country_col:
            logger.info(f"Using country column: {country_col}")
            unique_countries = df[country_col].unique()
            logger.info(f"Unique countries/codes found: {unique_countries[:20]}...")  # Show first 20
            
            # Filter for Sub-Saharan African countries only
            if any(code in str(unique_countries) for code in ssa_iso_codes):
                # Filtering by ISO codes
                df_africa = df[df[country_col].isin(ssa_iso_codes)]
                # Also exclude North African countries explicitly if they exist
                df_africa = df_africa[~df_africa[country_col].isin(NORTH_AFRICAN_COUNTRIES)]
            else:
                # Try filtering by country names
                ssa_names = list(SUB_SAHARAN_COUNTRIES.values())
                df_africa = df[df[country_col].isin(ssa_names)]
                # Exclude North African countries by name as well
                north_african_names = ['Algeria', 'Egypt', 'Libya', 'Morocco', 'Tunisia']
                df_africa = df_africa[~df_africa[country_col].isin(north_african_names)]
        else:
            logger.warning("Could not identify country column, using all data")
            df_africa = df.copy()
        
        logger.info(f"African data shape: {df_africa.shape}")
        
        # Standardize column names
        column_mapping = {}
        for col in df_africa.columns:
            col_lower = col.lower().strip()
            
            # Map common EM-DAT column names
            if col_lower in ['year', 'start year']:
                column_mapping[col] = 'year'
            elif col_lower in ['country', 'country name']:
                column_mapping[col] = 'country'
            elif col_lower in ['iso', 'iso3', 'country iso', 'iso_code']:
                column_mapping[col] = 'country_code'
            elif col_lower in ['disaster group', 'disaster_group']:
                column_mapping[col] = 'disaster_group'
            elif col_lower in ['disaster subgroup', 'disaster_subgroup']:
                column_mapping[col] = 'disaster_subgroup'
            elif col_lower in ['disaster type', 'disaster_type']:
                column_mapping[col] = 'disaster_type'
            elif col_lower in ['disaster subtype', 'disaster_subtype']:
                column_mapping[col] = 'disaster_subtype'
            elif col_lower in ['total deaths', 'deaths', 'total_deaths']:
                column_mapping[col] = 'deaths'
            elif col_lower in ['no injured', 'injured', 'total_injured']:
                column_mapping[col] = 'injured'
            elif col_lower in ['no affected', 'affected', 'total_affected']:
                column_mapping[col] = 'affected_population'
            elif col_lower in ['no homeless', 'homeless', 'total_homeless']:
                column_mapping[col] = 'homeless'
            elif col_lower in ['total damages (\'000 us$)', 'total damages', 'damage', 'economic_damage']:
                column_mapping[col] = 'economic_damage_usd'
            elif col_lower in ['start date', 'date']:
                column_mapping[col] = 'start_date'
            elif col_lower in ['location', 'admin units']:
                column_mapping[col] = 'location'
        
        # Rename columns
        df_clean = df_africa.rename(columns=column_mapping)
        logger.info(f"Mapped columns: {column_mapping}")
        
        # Process year column
        if 'year' in df_clean.columns:
            df_clean['year'] = pd.to_numeric(df_clean['year'], errors='coerce')
            df_clean = df_clean.dropna(subset=['year'])
            df_clean['year'] = df_clean['year'].astype(int)
        elif 'start_date' in df_clean.columns:
            # Extract year from start date
            df_clean['year'] = pd.to_datetime(df_clean['start_date'], errors='coerce').dt.year
            df_clean = df_clean.dropna(subset=['year'])
            df_clean['year'] = df_clean['year'].astype(int)
        
        # Clean numeric columns
        numeric_columns = ['deaths', 'injured', 'affected_population', 'homeless', 'economic_damage_usd']
        for col in numeric_columns:
            if col in df_clean.columns:
                # Handle string values like "No Data", "Unknown", etc.
                df_clean[col] = df_clean[col].replace(['No Data', 'Unknown', '', 'nan', 'NaN'], np.nan)
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                df_clean[col] = df_clean[col].fillna(0)
        
        # Convert economic damage from thousands to actual USD
        if 'economic_damage_usd' in df_clean.columns:
            df_clean['economic_damage_usd'] = df_clean['economic_damage_usd'] * 1000
        
        # Standardize disaster types
        if 'disaster_type' in df_clean.columns:
            disaster_type_mapping = {
                'Drought': 'drought',
                'Flood': 'flood',
                'Storm': 'storm',
                'Earthquake': 'earthquake',
                'Wildfire': 'wildfire',
                'Epidemic': 'epidemic',
                'Volcanic activity': 'volcanic',
                'Landslide': 'landslide',
                'Extreme temperature': 'extreme_temperature',
                'Mass movement': 'mass_movement'
            }
            
            # Apply mapping (case insensitive)
            df_clean['disaster_type_clean'] = df_clean['disaster_type'].str.strip()
            for old_name, new_name in disaster_type_mapping.items():
                mask = df_clean['disaster_type_clean'].str.contains(old_name, case=False, na=False)
                df_clean.loc[mask, 'disaster_type_clean'] = new_name
            
            # Use cleaned disaster type
            df_clean['disaster_type'] = df_clean['disaster_type_clean']
            df_clean = df_clean.drop('disaster_type_clean', axis=1)
        
        # Ensure we have country codes
        if 'country_code' not in df_clean.columns and 'country' in df_clean.columns:
            # Create country code mapping
            name_to_code = {v: k for k, v in SUB_SAHARAN_COUNTRIES.items()}
            df_clean['country_code'] = df_clean['country'].map(name_to_code)
        
        # Fill missing country names
        if 'country' not in df_clean.columns and 'country_code' in df_clean.columns:
            df_clean['country'] = df_clean['country_code'].map(SUB_SAHARAN_COUNTRIES)
        
        # Select relevant columns for the dashboard
        output_columns = [
            'year', 'country', 'country_code', 'disaster_type', 'disaster_subtype',
            'deaths', 'injured', 'affected_population', 'homeless', 'economic_damage_usd',
            'location'
        ]
        
        # Keep only columns that exist
        available_columns = [col for col in output_columns if col in df_clean.columns]
        df_output = df_clean[available_columns].copy()
        
        # Remove rows with missing essential data
        df_output = df_output.dropna(subset=['year'])
        if 'country' in df_output.columns:
            df_output = df_output.dropna(subset=['country'])
        if 'disaster_type' in df_output.columns:
            df_output = df_output.dropna(subset=['disaster_type'])
        
        # Sort by year and country
        sort_columns = ['year']
        if 'country' in df_output.columns:
            sort_columns.append('country')
        df_output = df_output.sort_values(sort_columns)
        
        # Save processed data
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df_output.to_csv(output_file, index=False)
        
        logger.info(f"Processed data saved to {output_file}")
        logger.info(f"Final shape: {df_output.shape}")
        logger.info(f"Year range: {df_output['year'].min()} - {df_output['year'].max()}")
        logger.info(f"Countries: {df_output['country'].nunique() if 'country' in df_output.columns else 'Unknown'}")
        logger.info(f"Disaster types: {df_output['disaster_type'].nunique() if 'disaster_type' in df_output.columns else 'Unknown'}")
        
        # Display summary statistics
        print("\n=== DATA SUMMARY ===")
        print(f"Total disasters: {len(df_output)}")
        print(f"Years covered: {df_output['year'].min()} - {df_output['year'].max()}")
        
        if 'country' in df_output.columns:
            print(f"\nTop 10 countries by disaster count:")
            print(df_output['country'].value_counts().head(10))
        
        if 'disaster_type' in df_output.columns:
            print(f"\nDisasters by type:")
            print(df_output['disaster_type'].value_counts())
        
        if 'deaths' in df_output.columns:
            total_deaths = df_output['deaths'].sum()
            print(f"\nTotal deaths: {total_deaths:,}")
        
        if 'affected_population' in df_output.columns:
            total_affected = df_output['affected_population'].sum()
            print(f"Total affected population: {total_affected:,}")
        
        if 'economic_damage_usd' in df_output.columns:
            total_damage = df_output['economic_damage_usd'].sum()
            print(f"Total economic damage: ${total_damage:,.0f}")
        
        return df_output
        
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