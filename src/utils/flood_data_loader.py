"""
Utility functions for loading flood exposure data
"""

import pandas as pd
import os

def load_flood_exposure_data(data_type='built_s'):
    """
    Load flood exposure data from Fathom3-GHSL dataset
    
    Args:
        data_type: Type of data to load ('built_s', 'pop', etc.)
        
    Returns:
        DataFrame with flood exposure data
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(project_root, 'data', 'processed', 'flood', 
                             f'country_ftm3_current_ghsl2023_{data_type}.csv')
    
    df = pd.read_csv(file_path)
    return df


def load_ghsl_total_buildup_data():
    """
    Load GHSL total built-up area data for normalization
    
    Returns:
        DataFrame with total built-up area by country and year
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(project_root, 'data', 'processed', 'flood', 
                             'country_ghsl2023_built_s.csv')
    
    df = pd.read_csv(file_path)
    return df[['ISO_A3', 'ghsl_year', 'ghsl_total_built_s_km2']]


def load_ghsl_total_population_data():
    """
    Load GHSL total population data for normalization
    
    Returns:
        DataFrame with total population by country and year
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(project_root, 'data', 'processed', 'flood', 
                             'country_ghsl2023_pop.csv')
    
    df = pd.read_csv(file_path)
    return df[['ISO_A3', 'ghsl_year', 'ghsl_total_pop_#']]


def get_flood_types():
    """
    Get list of available flood types
    
    Returns:
        List of flood type strings
    """
    df = load_flood_exposure_data('built_s')
    return sorted(df['flood_type'].unique().tolist())


def get_return_periods():
    """
    Get list of available return periods
    
    Returns:
        List of return period strings
    """
    df = load_flood_exposure_data('built_s')
    return sorted(df['return_period'].unique().tolist())


def filter_flood_data(df, iso3_code, flood_type=None):
    """
    Filter flood data by country and optionally by flood type
    
    Args:
        df: DataFrame with flood exposure data
        iso3_code: ISO3 country code
        flood_type: Optional flood type to filter by
        
    Returns:
        Filtered DataFrame
    """
    filtered = df[df['ISO_A3'] == iso3_code].copy()
    
    if flood_type:
        filtered = filtered[filtered['flood_type'] == flood_type]
    
    return filtered


def load_city_flood_exposure_data():
    """
    Load city-level flood exposure data from africapolis_fathom_ghsl_merged_5citiespercountry.csv
    
    Returns:
        DataFrame with city-level flood exposure data including:
        - ISO3, agglosID, agglosName, ghsl_year
        - BU, BU_1in5, BU_1in10, BU_1in100 (built-up area)
        - BU_1in5_pct, BU_1in10_pct, BU_1in100_pct (built-up percentages)
        - POP, POP_1in5, POP_1in10, POP_1in100 (population)
        - POP_1in5_pct, POP_1in10_pct, POP_1in100_pct (population percentages)
    """
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(project_root, 'data', 'processed', 
                             'africapolis_fathom_ghsl_merged_5citiespercountry.csv')
    
    df = pd.read_csv(file_path)
    return df
