"""
Data loading utilities for the DRM dashboard
"""

import pandas as pd
import os
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from typing import Dict, List, Optional

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


# Import centralized country utilities
from .country_utils import get_subsaharan_countries, load_subsaharan_countries_dict, load_subsaharan_countries_and_regions_dict

# Re-export for backward compatibility
__all__ = ['get_subsaharan_countries', 'load_subsaharan_countries_dict', 'load_subsaharan_countries_and_regions_dict', 'load_wdi_data', 'load_urbanization_indicators_dict', 'load_urbanization_indicators_notes_dict', 'load_undesa_urban_projections']