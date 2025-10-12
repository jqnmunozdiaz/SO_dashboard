"""
Data loading utilities for the DRM dashboard
"""

import pandas as pd
import os
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


# Import centralized country utilities
from .country_utils import get_subsaharan_countries, load_subsaharan_countries_dict

# Re-export for backward compatibility
__all__ = ['get_subsaharan_countries', 'load_subsaharan_countries_dict']