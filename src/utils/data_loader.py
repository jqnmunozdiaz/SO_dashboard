"""
Data loading utilities for the DRM dashboard
"""

import pandas as pd
import numpy as np
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


def load_real_disaster_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load real EM-DAT disaster data for African countries
    
    Args:
        file_path: Path to processed EM-DAT CSV file
        
    Returns:
        DataFrame with real disaster data
    """
    if file_path is None:
        file_path = os.path.join('data', 'processed', 'african_disasters_emdat.csv')
    
    try:
        # Read CSV and handle duplicate column names
        df = pd.read_csv(file_path)
        
        # Fix duplicate column names if they exist
        cols = pd.Series(df.columns)
        for dup in cols[cols.duplicated()].unique():
            cols[cols[cols == dup].index.values.tolist()] = [dup + '_' + str(i) if i != 0 else dup 
                                                            for i in range(sum(cols == dup))]
        df.columns = cols
        
        # Clean and standardize the data
        if 'year' in df.columns:
            df['year'] = pd.to_numeric(df['year'], errors='coerce')
            df = df.dropna(subset=['year'])
            df['year'] = df['year'].astype(int)
        
        # Ensure we have the required columns
        if 'country' not in df.columns or 'country_code' not in df.columns:
            raise ValueError("Missing required columns (country, country_code)")
        
        # Clean numeric columns
        numeric_columns = ['deaths', 'injured', 'affected_population', 'homeless', 'economic_damage_usd']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # Add affected_population column if missing (using deaths as proxy)
        if 'affected_population' not in df.columns and 'deaths' in df.columns:
            df['affected_population'] = df['deaths'] * 10  # Rough estimate
        elif 'affected_population' not in df.columns:
            df['affected_population'] = 1000  # Default value
        
        # Add economic_damage_usd if missing
        if 'economic_damage_usd' not in df.columns:
            df['economic_damage_usd'] = df.get('deaths', 0) * 100000  # Rough estimate
        
        # Standardize disaster types to match dashboard categories
        if 'disaster_type' in df.columns:
            disaster_mapping = {
                'flood': 'flood',
                'drought': 'drought', 
                'storm': 'storm',
                'earthquake': 'earthquake',
                'wildfire': 'wildfire',
                'epidemic': 'epidemic',
                'volcanic': 'volcanic',
                'extreme_temperature': 'extreme_temperature',
                'mass_movement': 'landslide'
            }
            
            # Map disaster types, keeping unmapped types as 'other'
            df['disaster_type_mapped'] = df['disaster_type'].map(disaster_mapping).fillna('other')
            df['disaster_type'] = df['disaster_type_mapped']
            df = df.drop('disaster_type_mapped', axis=1)
        
        # Filter recent years for better dashboard performance (last 50 years)
        current_year = 2025
        df = df[df['year'] >= (current_year - 50)]
        
        return df
        
    except FileNotFoundError:
        print(f"Real disaster data file not found: {file_path}")
        print("Falling back to sample data")
        return create_sample_disaster_data()
    except Exception as e:
        print(f"Error loading real disaster data: {str(e)}")
        print("Falling back to sample data")
        return create_sample_disaster_data()


def get_subsaharan_countries() -> List[Dict[str, str]]:
    """
    Get list of Sub-Saharan African countries with codes (excludes North African countries)
    
    Returns:
        List of dictionaries with country names and ISO codes
    """
    # Sub-Saharan African countries (excluding North Africa: Algeria, Egypt, Libya, Morocco, Tunisia)
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
    
    return [{'name': name, 'code': code} for code, name in SUB_SAHARAN_COUNTRIES.items()]