"""
Centralized country data loading utilities for the DRM Dashboard
"""

import pandas as pd
import os
from typing import Dict


def load_subsaharan_countries_dict() -> Dict[str, str]:
    """
    Load Sub-Saharan African countries from CSV file
    
    Returns:
        Dictionary mapping ISO codes to country names
    """
    csv_path = os.path.join('data', 'Definitions', 'sub_saharan_countries.csv')
    try:
        df = pd.read_csv(csv_path, names=['code', 'name'])
        return dict(zip(df['code'], df['name']))
    except FileNotFoundError:
        print(f"Warning: Sub-Saharan country list file not found at {csv_path}")
        return {}


def load_non_sub_saharan_countries_dict() -> Dict[str, str]:
    """
    Load non-Sub-Saharan African countries from CSV file
    
    Returns:
        Dictionary mapping ISO codes to country names
    """
    csv_path = os.path.join('data', 'Definitions', 'non_sub_saharan_african_countries.csv')
    try:
        df = pd.read_csv(csv_path, names=['code', 'name'])
        return dict(zip(df['code'], df['name']))
    except FileNotFoundError:
        print(f"Warning: Non-Sub-Saharan country list file not found at {csv_path}")
        return {}


def get_subsaharan_countries() -> list:
    """
    Get list of Sub-Saharan African countries with codes
    
    Returns:
        List of dictionaries with country names and ISO codes
    """
    countries_dict = load_subsaharan_countries_dict()
    return [{'name': name, 'code': code} for code, name in countries_dict.items()]