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
    """Return empty DataFrame - no sample data"""
    return pd.DataFrame(columns=['year', 'country', 'country_code', 'disaster_type', 
                               'affected_population', 'economic_damage_usd', 'deaths', 'injured'])


def create_sample_urbanization_data() -> pd.DataFrame:
    """Return empty DataFrame - no sample data"""
    return pd.DataFrame(columns=['year', 'country', 'country_code', 'urban_population_pct', 
                               'urban_growth_rate', 'population_density', 'total_population'])


def create_sample_flood_risk_data() -> pd.DataFrame:
    """Return empty DataFrame - no sample data"""
    return pd.DataFrame(columns=['country', 'country_code', 'scenario', 'flood_risk_level', 
                               'exposure', 'sensitivity', 'adaptive_capacity', 
                               'population_at_risk', 'infrastructure_value_at_risk'])


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
        
        # Keep only real data - no proxy calculations
        # If affected_population is missing, leave it as NaN or remove rows
        if 'affected_population' not in df.columns:
            df['affected_population'] = pd.NA
        
        # Keep only real data - no proxy calculations
        if 'economic_damage_usd' not in df.columns:
            df['economic_damage_usd'] = pd.NA
        
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
        return pd.DataFrame(columns=['year', 'country', 'country_code', 'disaster_type', 
                                   'affected_population', 'economic_damage_usd', 'deaths', 'injured'])
    except Exception as e:
        print(f"Error loading real disaster data: {str(e)}")
        return pd.DataFrame(columns=['year', 'country', 'country_code', 'disaster_type', 
                                   'affected_population', 'economic_damage_usd', 'deaths', 'injured'])


# Import centralized country utilities
from .country_utils import get_subsaharan_countries, load_subsaharan_countries_dict

# Re-export for backward compatibility
__all__ = ['get_subsaharan_countries', 'load_subsaharan_countries_dict']