"""
Data loading utilities for the DRM dashboard
"""

import pandas as pd
import os
from typing import Dict, List, Optional


def load_disaster_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load historical disaster data
    
    Args:
        file_path: Path to disaster data file
        
    Returns:
        DataFrame with disaster data
    """
    if file_path is None:
        file_path = os.path.join('data', 'processed', 'disasters.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        # Return sample data if file doesn't exist
        return create_sample_disaster_data()


def load_urbanization_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load urbanization trend data
    
    Args:
        file_path: Path to urbanization data file
        
    Returns:
        DataFrame with urbanization data
    """
    if file_path is None:
        file_path = os.path.join('data', 'processed', 'urbanization.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return create_sample_urbanization_data()


def load_flood_risk_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load flood risk assessment data
    
    Args:
        file_path: Path to flood risk data file
        
    Returns:
        DataFrame with flood risk data
    """
    if file_path is None:
        file_path = os.path.join('data', 'processed', 'flood_risk.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        return create_sample_flood_risk_data()


def load_country_geometries(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load country boundary geometries for mapping
    
    Args:
        file_path: Path to geospatial data file
        
    Returns:
        GeoDataFrame with country boundaries
    """
    try:
        import geopandas as gpd
        if file_path is None:
            file_path = os.path.join('data', 'external', 'ssa_boundaries.geojson')
        
        gdf = gpd.read_file(file_path)
        return gdf
    except ImportError:
        print("GeoPandas not installed. Install with: pip install geopandas")
        return pd.DataFrame()
    except FileNotFoundError:
        print(f"Geospatial data file not found: {file_path}")
        return pd.DataFrame()


def create_sample_disaster_data() -> pd.DataFrame:
    """Create sample disaster data for development/testing"""
    import numpy as np
    
    countries = ['Nigeria', 'Kenya', 'Ethiopia', 'Ghana', 'Tanzania', 'Uganda', 
                'Mozambique', 'Madagascar', 'Cameroon', 'Mali']
    country_codes = ['NGA', 'KEN', 'ETH', 'GHA', 'TZA', 'UGA', 'MOZ', 'MDG', 'CMR', 'MLI']
    disaster_types = ['flood', 'drought', 'storm', 'earthquake', 'wildfire', 'epidemic']
    
    np.random.seed(42)  # For reproducible results
    
    data = []
    for year in range(2000, 2024):
        for country, code in zip(countries, country_codes):
            # Generate random number of disasters per country per year
            num_disasters = np.random.poisson(3)
            
            for _ in range(num_disasters):
                disaster_type = np.random.choice(disaster_types)
                
                # Generate realistic values based on disaster type and country
                base_affected = np.random.lognormal(10, 1.5)  # Log-normal for population
                base_damage = np.random.lognormal(15, 1.2)    # Log-normal for economic damage
                
                data.append({
                    'year': year,
                    'country': country,
                    'country_code': code,
                    'disaster_type': disaster_type,
                    'affected_population': int(base_affected),
                    'economic_damage_usd': base_damage,
                    'deaths': np.random.poisson(50),
                    'injured': np.random.poisson(200)
                })
    
    return pd.DataFrame(data)


def create_sample_urbanization_data() -> pd.DataFrame:
    """Create sample urbanization data for development/testing"""
    countries = ['Nigeria', 'Kenya', 'Ethiopia', 'Ghana', 'Tanzania', 'Uganda', 
                'Rwanda', 'Senegal', 'Burkina Faso', 'Ivory Coast']
    country_codes = ['NGA', 'KEN', 'ETH', 'GHA', 'TZA', 'UGA', 'RWA', 'SEN', 'BFA', 'CIV']
    
    data = []
    for country, code in zip(countries, country_codes):
        for year in range(2000, 2024):
            # Generate urbanization trends with some variation
            base_urban_pct = {
                'Nigeria': 35, 'Kenya': 25, 'Ethiopia': 15, 'Ghana': 45,
                'Tanzania': 25, 'Uganda': 20, 'Rwanda': 12, 'Senegal': 40,
                'Burkina Faso': 25, 'Ivory Coast': 45
            }.get(country, 30)
            
            urban_pct = base_urban_pct + (year - 2000) * 0.8 + np.random.normal(0, 1)
            urban_growth = 3.5 + np.random.normal(0, 0.5)
            pop_density = base_urban_pct * 3 + (year - 2000) * 2 + np.random.normal(0, 5)
            
            data.append({
                'year': year,
                'country': country,
                'country_code': code,
                'urban_population_pct': max(0, urban_pct),
                'urban_growth_rate': max(0, urban_growth),
                'population_density': max(0, pop_density),
                'total_population': np.random.lognormal(15, 0.5)
            })
    
    return pd.DataFrame(data)


def create_sample_flood_risk_data() -> pd.DataFrame:
    """Create sample flood risk data for development/testing"""
    countries = ['Nigeria', 'Kenya', 'Ethiopia', 'Ghana', 'Tanzania', 'Uganda', 
                'Mozambique', 'Madagascar', 'Cameroon', 'Mali']
    country_codes = ['NGA', 'KEN', 'ETH', 'GHA', 'TZA', 'UGA', 'MOZ', 'MDG', 'CMR', 'MLI']
    scenarios = ['current', '2030', '2050']
    
    data = []
    for country, code in zip(countries, country_codes):
        base_risk = np.random.uniform(3, 9)  # Base flood risk level
        
        for scenario in scenarios:
            # Risk increases over time
            multiplier = {'current': 1.0, '2030': 1.1, '2050': 1.2}[scenario]
            
            risk_level = min(10, base_risk * multiplier)
            exposure = np.random.uniform(4, 9)
            sensitivity = np.random.uniform(4, 9)
            adaptive_capacity = np.random.uniform(3, 7)
            
            data.append({
                'country': country,
                'country_code': code,
                'scenario': scenario,
                'flood_risk_level': risk_level,
                'exposure': exposure,
                'sensitivity': sensitivity,
                'adaptive_capacity': adaptive_capacity,
                'population_at_risk': np.random.lognormal(12, 1),
                'infrastructure_value_at_risk': np.random.lognormal(20, 1.5)
            })
    
    return pd.DataFrame(data)


def get_subsaharan_countries() -> List[Dict[str, str]]:
    """
    Get list of Sub-Saharan African countries with codes
    
    Returns:
        List of dictionaries with country names and ISO codes
    """
    return [
        {'name': 'Nigeria', 'code': 'NGA'},
        {'name': 'Kenya', 'code': 'KEN'},
        {'name': 'Ethiopia', 'code': 'ETH'},
        {'name': 'Ghana', 'code': 'GHA'},
        {'name': 'Tanzania', 'code': 'TZA'},
        {'name': 'Uganda', 'code': 'UGA'},
        {'name': 'Mozambique', 'code': 'MOZ'},
        {'name': 'Madagascar', 'code': 'MDG'},
        {'name': 'Cameroon', 'code': 'CMR'},
        {'name': 'Mali', 'code': 'MLI'},
        {'name': 'Burkina Faso', 'code': 'BFA'},
        {'name': 'Niger', 'code': 'NER'},
        {'name': 'Senegal', 'code': 'SEN'},
        {'name': 'Chad', 'code': 'TCD'},
        {'name': 'Rwanda', 'code': 'RWA'},
        {'name': 'Benin', 'code': 'BEN'},
        {'name': 'Burundi', 'code': 'BDI'},
        {'name': 'Togo', 'code': 'TGO'},
        {'name': 'Sierra Leone', 'code': 'SLE'},
        {'name': 'Liberia', 'code': 'LBR'},
        {'name': 'Central African Republic', 'code': 'CAF'},
        {'name': 'Mauritania', 'code': 'MRT'},
        {'name': 'Gambia', 'code': 'GMB'},
        {'name': 'Guinea-Bissau', 'code': 'GNB'},
        {'name': 'Guinea', 'code': 'GIN'},
        {'name': 'Ivory Coast', 'code': 'CIV'},
        {'name': 'Zambia', 'code': 'ZMB'},
        {'name': 'Zimbabwe', 'code': 'ZWE'},
        {'name': 'Botswana', 'code': 'BWA'},
        {'name': 'Namibia', 'code': 'NAM'},
        {'name': 'South Africa', 'code': 'ZAF'},
        {'name': 'Lesotho', 'code': 'LSO'},
        {'name': 'Eswatini', 'code': 'SWZ'},
        {'name': 'Malawi', 'code': 'MWI'},
        {'name': 'Angola', 'code': 'AGO'},
        {'name': 'Democratic Republic of Congo', 'code': 'COD'},
        {'name': 'Republic of Congo', 'code': 'COG'},
        {'name': 'Gabon', 'code': 'GAB'},
        {'name': 'Equatorial Guinea', 'code': 'GNQ'},
        {'name': 'São Tomé and Príncipe', 'code': 'STP'},
        {'name': 'Cape Verde', 'code': 'CPV'},
        {'name': 'Comoros', 'code': 'COM'},
        {'name': 'Mauritius', 'code': 'MUS'},
        {'name': 'Seychelles', 'code': 'SYC'},
        {'name': 'Djibouti', 'code': 'DJI'},
        {'name': 'Eritrea', 'code': 'ERI'},
        {'name': 'Somalia', 'code': 'SOM'},
        {'name': 'South Sudan', 'code': 'SSD'},
        {'name': 'Sudan', 'code': 'SDN'}
    ]