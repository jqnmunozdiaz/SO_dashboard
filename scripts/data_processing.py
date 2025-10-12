"""
Data processing script for cleaning and preparing disaster data
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def process_emdat_data(input_file: str, output_file: str):
    """
    Process EM-DAT disaster data
    
    Args:
        input_file: Path to raw EM-DAT CSV file
        output_file: Path to save processed data
    """
    logger.info(f"Processing EM-DAT data from {input_file}")
    
    try:
        # Read raw data
        df = pd.read_csv(input_file)
        
        # Basic data cleaning
        df['Year'] = pd.to_datetime(df['Year'], format='%Y', errors='coerce').dt.year
        
        # Filter for Sub-Saharan Africa countries
        ssa_countries = get_ssa_country_list()
        df = df[df['Country'].isin(ssa_countries)]
        
        # Standardize disaster types
        disaster_type_mapping = {
            'Flood': 'flood',
            'Drought': 'drought',
            'Storm': 'storm',
            'Earthquake': 'earthquake',
            'Wildfire': 'wildfire',
            'Epidemic': 'epidemic',
            'Volcanic activity': 'volcanic'
        }
        
        df['disaster_type'] = df['Disaster Type'].map(disaster_type_mapping)
        
        # Clean numeric columns
        numeric_columns = ['Total Deaths', 'No Injured', 'No Affected', 'Total Damages (000 US$)']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Rename columns
        column_mapping = {
            'Year': 'year',
            'Country': 'country',
            'ISO': 'country_code',
            'Total Deaths': 'deaths',
            'No Injured': 'injured',
            'No Affected': 'affected_population',
            'Total Damages (000 US$)': 'economic_damage_usd'
        }
        
        df = df.rename(columns=column_mapping)
        
        # Convert economic damage from thousands to actual USD
        if 'economic_damage_usd' in df.columns:
            df['economic_damage_usd'] = df['economic_damage_usd'] * 1000
        
        # Select relevant columns
        output_columns = [
            'year', 'country', 'country_code', 'disaster_type',
            'deaths', 'injured', 'affected_population', 'economic_damage_usd'
        ]
        
        df_output = df[output_columns].copy()
        
        # Remove rows with missing essential data
        df_output = df_output.dropna(subset=['year', 'country', 'disaster_type'])
        
        # Save processed data
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df_output.to_csv(output_file, index=False)
        
        logger.info(f"Processed data saved to {output_file}")
        logger.info(f"Shape: {df_output.shape}")
        
    except Exception as e:
        logger.error(f"Error processing EM-DAT data: {str(e)}")
        raise


def process_world_bank_urbanization_data(input_file: str, output_file: str):
    """
    Process World Bank urbanization data
    
    Args:
        input_file: Path to raw World Bank CSV file
        output_file: Path to save processed data
    """
    logger.info(f"Processing World Bank urbanization data from {input_file}")
    
    try:
        # Read raw data
        df = pd.read_csv(input_file)
        
        # Reshape from wide to long format (years as columns to rows)
        id_vars = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code']
        year_columns = [col for col in df.columns if col.isdigit()]
        
        df_long = pd.melt(df, id_vars=id_vars, value_vars=year_columns, 
                         var_name='year', value_name='value')
        
        # Convert year to integer
        df_long['year'] = pd.to_numeric(df_long['year'])
        
        # Filter for relevant indicators
        urban_indicators = {
            'SP.URB.TOTL.IN.ZS': 'urban_population_pct',
            'SP.URB.GROW': 'urban_growth_rate',
            'EN.POP.DNST': 'population_density',
            'SP.POP.TOTL': 'total_population'
        }
        
        df_long = df_long[df_long['Indicator Code'].isin(urban_indicators.keys())]
        
        # Map indicator codes to readable names
        df_long['indicator'] = df_long['Indicator Code'].map(urban_indicators)
        
        # Filter for Sub-Saharan Africa countries
        ssa_countries = get_ssa_country_list()
        df_long = df_long[df_long['Country Name'].isin(ssa_countries)]
        
        # Pivot to get indicators as columns
        df_pivot = df_long.pivot_table(
            index=['Country Name', 'Country Code', 'year'],
            columns='indicator',
            values='value',
            aggfunc='first'
        ).reset_index()
        
        # Rename columns
        df_pivot = df_pivot.rename(columns={
            'Country Name': 'country',
            'Country Code': 'country_code'
        })
        
        # Clean data
        df_pivot = df_pivot.dropna(subset=['year'])
        
        # Save processed data
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df_pivot.to_csv(output_file, index=False)
        
        logger.info(f"Processed urbanization data saved to {output_file}")
        logger.info(f"Shape: {df_pivot.shape}")
        
    except Exception as e:
        logger.error(f"Error processing World Bank data: {str(e)}")
        raise


def generate_sample_flood_risk_data(output_file: str):
    """
    Generate sample flood risk data for development
    
    Args:
        output_file: Path to save generated data
    """
    logger.info("Generating sample flood risk data")
    
    try:
        countries = get_ssa_country_list()
        scenarios = ['current', '2030', '2050']
        
        data = []
        np.random.seed(42)  # For reproducible results
        
        for country in countries:
            country_code = get_country_code(country)
            base_risk = np.random.uniform(3, 9)
            
            for scenario in scenarios:
                # Risk increases over time
                multiplier = {'current': 1.0, '2030': 1.1, '2050': 1.2}[scenario]
                
                risk_level = min(10, base_risk * multiplier + np.random.normal(0, 0.5))
                exposure = np.random.uniform(4, 9)
                sensitivity = np.random.uniform(4, 9)
                adaptive_capacity = np.random.uniform(3, 7)
                
                data.append({
                    'country': country,
                    'country_code': country_code,
                    'scenario': scenario,
                    'flood_risk_level': round(risk_level, 2),
                    'exposure': round(exposure, 2),
                    'sensitivity': round(sensitivity, 2),
                    'adaptive_capacity': round(adaptive_capacity, 2),
                    'population_at_risk': int(np.random.lognormal(12, 1)),
                    'infrastructure_value_at_risk': int(np.random.lognormal(20, 1.5))
                })
        
        df = pd.DataFrame(data)
        
        # Save data
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df.to_csv(output_file, index=False)
        
        logger.info(f"Sample flood risk data saved to {output_file}")
        logger.info(f"Shape: {df.shape}")
        
    except Exception as e:
        logger.error(f"Error generating flood risk data: {str(e)}")
        raise


def get_ssa_country_list():
    """Get list of Sub-Saharan African countries"""
    return [
        'Nigeria', 'Kenya', 'Ethiopia', 'Ghana', 'Tanzania', 'Uganda',
        'Mozambique', 'Madagascar', 'Cameroon', 'Mali', 'Burkina Faso',
        'Niger', 'Senegal', 'Chad', 'Rwanda', 'Benin', 'Burundi', 'Togo',
        'Sierra Leone', 'Liberia', 'Central African Republic', 'Mauritania',
        'Gambia', 'Guinea-Bissau', 'Guinea', 'Ivory Coast', 'Zambia',
        'Zimbabwe', 'Botswana', 'Namibia', 'South Africa', 'Lesotho',
        'Eswatini', 'Malawi', 'Angola', 'Democratic Republic of Congo',
        'Republic of Congo', 'Gabon', 'Equatorial Guinea', 
        'São Tomé and Príncipe', 'Cabo Verde', 'Comoros', 'Mauritius',
        'Seychelles', 'Djibouti', 'Eritrea', 'Somalia', 'South Sudan', 'Sudan'
    ]


def get_country_code(country_name):
    """Get ISO country code for a country name"""
    country_codes = {
        'Nigeria': 'NGA', 'Kenya': 'KEN', 'Ethiopia': 'ETH', 'Ghana': 'GHA',
        'Tanzania': 'TZA', 'Uganda': 'UGA', 'Mozambique': 'MOZ', 
        'Madagascar': 'MDG', 'Cameroon': 'CMR', 'Mali': 'MLI',
        'Burkina Faso': 'BFA', 'Niger': 'NER', 'Senegal': 'SEN',
        'Chad': 'TCD', 'Rwanda': 'RWA', 'Benin': 'BEN', 'Burundi': 'BDI',
        'Togo': 'TGO', 'Sierra Leone': 'SLE', 'Liberia': 'LBR',
        'Central African Republic': 'CAF', 'Mauritania': 'MRT',
        'Gambia': 'GMB', 'Guinea-Bissau': 'GNB', 'Guinea': 'GIN',
        'Ivory Coast': 'CIV', 'Zambia': 'ZMB', 'Zimbabwe': 'ZWE',
        'Botswana': 'BWA', 'Namibia': 'NAM', 'South Africa': 'ZAF',
        'Lesotho': 'LSO', 'Eswatini': 'SWZ', 'Malawi': 'MWI',
        'Angola': 'AGO', 'Democratic Republic of Congo': 'COD',
        'Republic of Congo': 'COG', 'Gabon': 'GAB', 
        'Equatorial Guinea': 'GNQ', 'São Tomé and Príncipe': 'STP',
        'Cabo Verde': 'CPV', 'Comoros': 'COM', 'Mauritius': 'MUS',
        'Seychelles': 'SYC', 'Djibouti': 'DJI', 'Eritrea': 'ERI',
        'Somalia': 'SOM', 'South Sudan': 'SSD', 'Sudan': 'SDN'
    }
    return country_codes.get(country_name, 'UNK')


if __name__ == "__main__":
    # Example usage
    print("Data processing script for DRM Dashboard")
    
    # Create sample data if raw data files don't exist
    data_dir = "data/processed"
    os.makedirs(data_dir, exist_ok=True)
    
    # Generate sample flood risk data
    generate_sample_flood_risk_data(os.path.join(data_dir, "flood_risk.csv"))
    
    print("Sample data generation complete!")