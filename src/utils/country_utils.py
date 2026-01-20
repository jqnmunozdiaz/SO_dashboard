"""
Centralized country data loading utilities for the DRM Dashboard
"""

import pandas as pd
import os
from functools import lru_cache
from typing import Dict, List, Tuple

# Module-level constants
_PROJECT_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
_WB_CLASSIFICATION_FILE = os.path.join(_PROJECT_ROOT, 'data', 'Definitions', 'WB_Classification.csv')

REGIONS = {
    'SSA': 'Sub-Saharan Africa',
    'AFE': 'Eastern & Southern Africa',
    'AFW': 'Western & Central Africa'
}


@lru_cache(maxsize=1)
def _load_wb_classification() -> pd.DataFrame:
    """Load and cache the World Bank classification CSV file."""
    try:
        return pd.read_csv(_WB_CLASSIFICATION_FILE)
    except FileNotFoundError:
        print(f"Warning: World Bank classification file not found at {_WB_CLASSIFICATION_FILE}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error loading World Bank classifications: {e}")
        return pd.DataFrame()


def load_subsaharan_countries_dict() -> Dict[str, str]:
    """
    Load Sub-Saharan African countries from World Bank Classification file.
    
    Returns:
        Dictionary mapping ISO codes to country names
    """
    df = _load_wb_classification()
    if df.empty:
        return {}
    ssa_df = df[df['Region Code'] == 'SSA']
    return dict(zip(ssa_df['ISO3'], ssa_df['Country']))


def get_subsaharan_countries() -> List[dict]:
    """
    Get list of Sub-Saharan African countries with codes.
    
    Returns:
        List of dictionaries with country names and ISO codes
    """
    return [{'name': name, 'code': code} for code, name in load_subsaharan_countries_dict().items()]


def load_wb_regional_classifications() -> Tuple[List[str], List[str], List[str]]:
    """
    Load World Bank regional classifications and create regional mappings.
    
    Returns:
        Tuple of (afe_countries, afw_countries, ssa_countries) as lists of ISO3 codes
    """
    df = _load_wb_classification()
    if df.empty:
        return [], [], []
    
    afe_countries = df[df['Subregion Code'] == 'AFE']['ISO3'].tolist()
    afw_countries = df[df['Subregion Code'] == 'AFW']['ISO3'].tolist()
    return afe_countries, afw_countries, afe_countries + afw_countries


def get_all_regional_mappings() -> Dict[str, List[str]]:
    """
    Dynamically load all World Bank regions and subregions with their country lists.
    
    Reads all unique Region Codes and Subregion Codes from WB_Classification.csv
    and maps each to its list of ISO3 country codes.
    
    Returns:
        Dictionary mapping region/subregion codes to lists of ISO3 country codes.
        Example: {'SSA': ['AGO', 'BDI', ...], 'AFE': ['AGO', 'BDI', ...], 'EAP': [...], ...}
    """
    df = _load_wb_classification()
    if df.empty:
        return {}
    
    mappings = {}
    
    # Get all unique region codes and their countries
    for region_code in df['Region Code'].dropna().unique():
        mappings[region_code] = df[df['Region Code'] == region_code]['ISO3'].tolist()
    
    # Get all unique subregion codes and their countries
    for subregion_code in df['Subregion Code'].dropna().unique():
        mappings[subregion_code] = df[df['Subregion Code'] == subregion_code]['ISO3'].tolist()
    
    return mappings


def load_subsaharan_countries_and_regions_dict() -> Dict[str, str]:
    """
    Load Sub-Saharan African countries and regions with their full names.
    
    Returns:
        Dictionary mapping ISO codes to country/region names (includes SSA, AFE, AFW regions)
    """
    return {**load_subsaharan_countries_dict(), **REGIONS}


def get_countries_with_regions() -> List[dict]:
    """
    Get list of Sub-Saharan African countries with regional aggregates at the end.
    
    Returns:
        List of dictionaries with country names and codes, followed by regional options
    """
    countries = sorted(get_subsaharan_countries(), key=lambda x: x['name'])
    regional_options = [{'name': name, 'code': code} for code, name in REGIONS.items()]
    return countries + regional_options