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
        file_path = os.path.join('data', 'processed', 'african_disasters_emdat.csv')
    
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
        file_path = os.path.join('data', 'processed', 'wdi', f'{indicator_code}.csv')
    
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
    csv_path = os.path.join('data', 'Definitions', 'urbanization_indicators_selection.csv')
    try:
        df = pd.read_csv(csv_path)
        return dict(zip(df['Indicator_Code'], df['Indicator_Name']))
    except FileNotFoundError:
        print(f"Warning: Urbanization indicators file not found at {csv_path}")
        return {}
    except Exception as e:
        print(f"Warning: Error loading urbanization indicators: {str(e)}")
        return {}


# Import centralized country utilities
from .country_utils import get_subsaharan_countries, load_subsaharan_countries_dict

# Re-export for backward compatibility
__all__ = ['get_subsaharan_countries', 'load_subsaharan_countries_dict', 'load_wdi_data', 'load_urbanization_indicators_dict']