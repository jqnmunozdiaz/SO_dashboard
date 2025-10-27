"""
Data loading utilities for the DRM dashboard
"""

import pandas as pd
import os
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from typing import Dict, Optional

def load_emdat_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load EM-DAT disaster data for African countries
    
    Args:
        file_path: Path to processed EM-DAT CSV file
        
    Returns:
        DataFrame with EM-DAT disaster data
    """
    if file_path is None:
        # Get the absolute path to the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..')
        file_path = os.path.join(project_root, 'data', 'processed', 'african_disasters_emdat.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"EM-DAT data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading EM-DAT data: {str(e)}")


def load_wdi_data(indicator_code: str, file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load World Development Indicators data for a specific indicator
    
    Args:
        indicator_code: WDI indicator code (e.g., 'EN.POP.SLUM.UR.ZS')
        file_path: Path to WDI CSV file (optional)
        
    Returns:
        DataFrame with WDI data (columns: Country Code, Year, Value)
    """
    if file_path is None:
        # Get the absolute path to the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..')
        file_path = os.path.join(project_root, 'data', 'processed', 'wdi', f'{indicator_code}.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"WDI data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading WDI data: {str(e)}")


def load_urbanization_indicators_dict() -> Dict[str, str]:
    """
    Load urbanization indicators dictionary from CSV file
    
    Returns:
        Dictionary mapping indicator codes to indicator names
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    csv_path = os.path.join(project_root, 'data', 'Definitions', 'urbanization_indicators_selection.csv')
    try:
        df = pd.read_csv(csv_path)
        return dict(zip(df['Indicator_Code'], df['Indicator_Name']))
    except FileNotFoundError:
        print(f"Warning: Urbanization indicators file not found at {csv_path}")
        return {}
    except Exception as e:
        print(f"Warning: Error loading urbanization indicators: {str(e)}")
        return {}


def load_urbanization_indicators_notes_dict() -> Dict[str, str]:
    """
    Load urbanization indicators notes from CSV file
    
    Returns:
        Dictionary mapping indicator codes to their notes/descriptions
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    csv_path = os.path.join(project_root, 'data', 'Definitions', 'urbanization_indicators_selection.csv')
    try:
        df = pd.read_csv(csv_path)
        return dict(zip(df['Indicator_Code'], df['Note']))
    except FileNotFoundError:
        print(f"Warning: Urbanization indicators file not found at {csv_path}")
        return {}
    except Exception as e:
        print(f"Warning: Error loading urbanization indicators notes: {str(e)}")
        return {}


def load_undesa_urban_projections() -> pd.DataFrame:
    """
    Load UNDESA urban population projections consolidated data
    
    Returns:
        DataFrame with columns: ISO3, indicator, year, value
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'UNDESA_Country', 'UNDESA_urban_projections_consolidated.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"UNDESA urban projections data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading UNDESA urban projections data: {str(e)}")


def load_undesa_urban_growth_rates() -> pd.DataFrame:
    """
    Load pre-calculated UN DESA urban population growth rates
    
    Returns:
        DataFrame with columns: ISO3, year, indicator, value
        where value represents year-over-year percentage change
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'UNDESA_Country', 'UNDESA_urban_growth_rates_consolidated.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"UNDESA urban growth rates data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading UNDESA urban growth rates data: {str(e)}")


def load_city_size_distribution() -> pd.DataFrame:
    """
    Load individual cities data for Sub-Saharan African countries
    
    Returns:
        DataFrame with columns: Country Code, Country Name, City Name, Year, Population, Size Category
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'cities_individual.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"City size distribution data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading city size distribution data: {str(e)}")


def load_city_agglomeration_counts() -> pd.DataFrame:
    """
    Load number of agglomerations by city size category for Sub-Saharan African countries
    
    Returns:
        DataFrame with columns: Country Code, Country Name, Size Category, Year, Number of Agglomerations
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'city_agglomeration_counts.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"City agglomeration counts data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading city agglomeration counts data: {str(e)}")


def load_population_data(country_iso: str) -> pd.DataFrame:
    """
    Load total population data for a specific country from WPP 2024
    
    Args:
        country_iso: ISO3 country code
        
    Returns:
        DataFrame with columns: year, population (actual count, not in millions)
    """
    try:
        # Get the absolute path to the project root directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..')
        file_path = os.path.join(project_root, 'data', 'processed', 'WPP2024_Total_Population.csv')
        
        # Load WPP 2024 population data
        pop_data = pd.read_csv(file_path)
        
        # Filter for the specific country
        pop_data = pop_data[pop_data['ISO3'] == country_iso][['Year', 'population']].copy()
                       
        return pop_data
        
    except FileNotFoundError:
        raise Exception(f"WPP 2024 population data file not found.")
    except Exception as e:
        raise Exception(f"Error loading population data for {country_iso}: {str(e)}")


def load_jmp_water_data() -> pd.DataFrame:
    """
    Load JMP WASH urban drinking water data for Sub-Saharan Africa in long format
    
    Returns:
        DataFrame with columns: Country Code, Year, Indicator, Value
        Indicators: 'At least basic', 'Limited (more than 30 mins)', 'Unimproved', 'Surface water'
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'jmp_water', 'urban_drinking_water_ssa.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"JMP water data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading JMP water data: {str(e)}")


def load_jmp_sanitation_data() -> pd.DataFrame:
    """
    Load JMP WASH urban sanitation data for Sub-Saharan Africa in long format

    Returns:
        DataFrame with columns: Country Code, Year, Indicator, Value
        Indicators: 'At least basic', 'Limited', 'Unimproved', 'Open defecation'
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'jmp_sanitation', 'urban_sanitation_ssa.csv')

    try:
        df = pd.read_csv(file_path)
        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"JMP sanitation data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading JMP sanitation data: {str(e)}")


def load_cities_growth_rate() -> pd.DataFrame:
    """
    Load Africapolis-GHSL2023 city growth rate data (2000-2020)
    
    Returns:
        DataFrame with columns: ISO3, agglosID, agglosName, pop_2010, pop_2020, pop_cagr, 
                                built_up_2010, built_up_2020, built_up_cagr, size_category
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'africapolis_ghsl2023_cagr_2000_2020.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Cities growth rate data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading cities growth rate data: {str(e)}")


def load_africapolis_ghsl_simple() -> pd.DataFrame:
    """
    Load Africapolis-GHSL simple data for cities growth visualization
    
    Returns:
        DataFrame with columns: ISO3, agglosName, agglosID, POP_2000, POP_2020, 
                                BU_2000, BU_2020, POP_CAGR_2000_2020, BU_CAGR_2000_2020
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'africapolis_ghsl_simple.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Africapolis GHSL simple data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading Africapolis GHSL simple data: {str(e)}")


def load_africapolis_centroids() -> pd.DataFrame:
    """
    Load Africapolis city centroids with coordinates
    
    Returns:
        DataFrame with columns: agglosID, agglosName, ISO3, Longitude, Latitude
    """
    # Get the absolute path to the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..', '..')
    file_path = os.path.join(project_root, 'data', 'processed', 'africapolis2023_centroids.csv')
    
    try:
        df = pd.read_csv(file_path)
        return df
        
    except FileNotFoundError:
        raise FileNotFoundError(f"Africapolis centroids data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading Africapolis centroids data: {str(e)}")


def load_urban_density_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load built-up per capita data aggregated by country and year.

    Args:
        file_path: Optional custom file path to the built-up per capita CSV.

    Returns:
        DataFrame with columns: ISO3, year, population, built_up_km2, built_up_per_capita_m2
    """
    if file_path is None:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.join(current_dir, '..', '..')
        file_path = os.path.join(project_root, 'data', 'processed', 'built_up_per_capita_m2_by_country_year.csv')

    try:
        df = pd.read_csv(file_path)
        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"Built-up per capita data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading built-up per capita data: {str(e)}")


# Import centralized country utilities
from .country_utils import get_subsaharan_countries, load_subsaharan_countries_dict, load_subsaharan_countries_and_regions_dict

# Re-export for backward compatibility
__all__ = ['get_subsaharan_countries', 'load_subsaharan_countries_dict', 'load_subsaharan_countries_and_regions_dict', 'load_wdi_data', 'load_urbanization_indicators_dict', 'load_urbanization_indicators_notes_dict', 'load_undesa_urban_projections', 'load_city_size_distribution', 'load_city_agglomeration_counts', 'load_population_data', 'load_jmp_water_data', 'load_jmp_sanitation_data', 'load_cities_growth_rate', 'load_urban_density_data']