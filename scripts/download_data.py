"""
Data download script for fetching external data sources
"""

import requests
import pandas as pd
import os
import zipfile
from urllib.parse import urljoin
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download_world_bank_data(indicators, countries, years, output_dir):
    """
    Download data from World Bank API
    
    Args:
        indicators: List of World Bank indicator codes
        countries: List of country ISO codes
        years: Range of years (start:end)
        output_dir: Directory to save downloaded data
    """
    base_url = "https://api.worldbank.org/v2/"
    
    os.makedirs(output_dir, exist_ok=True)
    
    for indicator in indicators:
        logger.info(f"Downloading {indicator}...")
        
        # Construct API URL
        countries_str = ";".join(countries) if countries else "all"
        url = f"{base_url}country/{countries_str}/indicator/{indicator}"
        
        params = {
            'format': 'json',
            'date': f"{years[0]}:{years[1]}",
            'per_page': 10000
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if len(data) > 1 and data[1]:  # Check if data exists
                df = pd.DataFrame(data[1])
                
                # Save to CSV
                filename = f"wb_{indicator}_{years[0]}_{years[1]}.csv"
                filepath = os.path.join(output_dir, filename)
                df.to_csv(filepath, index=False)
                
                logger.info(f"Saved {len(df)} records to {filename}")
            else:
                logger.warning(f"No data found for {indicator}")
                
        except requests.RequestException as e:
            logger.error(f"Error downloading {indicator}: {str(e)}")


def download_natural_earth_data(output_dir):
    """
    Download country boundaries from Natural Earth
    
    Args:
        output_dir: Directory to save downloaded data
    """
    logger.info("Downloading Natural Earth country boundaries...")
    
    url = "https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/ne_50m_admin_0_countries.zip"
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        zip_path = os.path.join(output_dir, "ne_countries.zip")
        
        # Download zip file
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(output_dir)
        
        # Remove zip file
        os.remove(zip_path)
        
        logger.info("Natural Earth data downloaded and extracted")
        
    except requests.RequestException as e:
        logger.error(f"Error downloading Natural Earth data: {str(e)}")


def get_ssa_country_codes():
    """Get ISO codes for Sub-Saharan African countries"""
    return [
        'AGO', 'BEN', 'BWA', 'BFA', 'BDI', 'CMR', 'CPV', 'CAF', 'TCD', 'COM',
        'COG', 'COD', 'CIV', 'DJI', 'GNQ', 'ERI', 'ETH', 'GAB', 'GMB', 'GHA',
        'GIN', 'GNB', 'KEN', 'LSO', 'LBR', 'MDG', 'MWI', 'MLI', 'MRT', 'MUS',
        'MOZ', 'NAM', 'NER', 'NGA', 'RWA', 'STP', 'SEN', 'SYC', 'SLE', 'SOM',
        'ZAF', 'SSD', 'SDN', 'SWZ', 'TZA', 'TGO', 'UGA', 'ZMB', 'ZWE'
    ]


def download_all_data():
    """Download all required data sources"""
    logger.info("Starting data download process...")
    
    # World Bank indicators
    wb_indicators = [
        'SP.URB.TOTL.IN.ZS',  # Urban population (% of total)
        'SP.URB.GROW',        # Urban population growth (annual %)
        'EN.POP.DNST',        # Population density
        'SP.POP.TOTL',        # Total population
        'NY.GDP.MKTP.CD',     # GDP (current US$)
    ]
    
    # Download World Bank data
    download_world_bank_data(
        indicators=wb_indicators,
        countries=get_ssa_country_codes(),
        years=[2000, 2023],
        output_dir='data/external/world_bank'
    )
    
    # Download Natural Earth boundaries
    download_natural_earth_data('data/external/natural_earth')
    
    logger.info("Data download process completed")


if __name__ == "__main__":
    download_all_data()