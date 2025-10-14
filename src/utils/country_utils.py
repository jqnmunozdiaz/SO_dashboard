"""
Centralized country data loading utilities for the DRM Dashboard
"""

import pandas as pd
import os
from typing import Dict


def load_subsaharan_countries_dict() -> Dict[str, str]:
    """
    Load Sub-Saharan African countries from World Bank Classification file
    
    Returns:
        Dictionary mapping ISO codes to country names
    """
    wb_classification_file = 'data/Definitions/WB_Classification.csv'
    try:
        wb_df = pd.read_csv(wb_classification_file)
        # Filter for Sub-Saharan Africa region (Region Code == 'SSA')
        ssa_df = wb_df[wb_df['Region Code'] == 'SSA']
        return dict(zip(ssa_df['ISO3'], ssa_df['Country']))
    except FileNotFoundError:
        print(f"Warning: World Bank classification file not found at {wb_classification_file}")
        return {}
    except Exception as e:
        print(f"Error loading Sub-Saharan countries from WB classification: {str(e)}")
        return {}


def get_subsaharan_countries() -> list:
    """
    Get list of Sub-Saharan African countries with codes
    
    Returns:
        List of dictionaries with country names and ISO codes
    """
    countries_dict = load_subsaharan_countries_dict()
    return [{'name': name, 'code': code} for code, name in countries_dict.items()]


def load_wb_regional_classifications():
    """
    Load World Bank regional classifications and create regional mappings
    
    Returns:
        Tuple of (afe_countries, afw_countries, ssa_countries) as lists of ISO3 codes
    """
    wb_classification_file = 'data/Definitions/WB_Classification.csv'
    try:
        wb_df = pd.read_csv(wb_classification_file)
        
        # Create regional mappings
        afe_countries = wb_df[wb_df['Subregion Code'] == 'AFE']['ISO3'].tolist()
        afw_countries = wb_df[wb_df['Subregion Code'] == 'AFW']['ISO3'].tolist()
        ssa_countries = afe_countries + afw_countries  # SSA is AFE + AFW
        
        return afe_countries, afw_countries, ssa_countries
        
    except FileNotFoundError:
        print(f"Warning: World Bank classification file not found at {wb_classification_file}")
        return [], [], []
    except Exception as e:
        print(f"Error loading World Bank classifications: {str(e)}")
        return [], [], []


def load_subsaharan_countries_and_regions_dict() -> Dict[str, str]:
    """
    Load Sub-Saharan African countries and regions with their full names
    
    Returns:
        Dictionary mapping ISO codes to country/region names (includes SSA, AFE, AFW regions)
    """
    # Get individual countries first
    countries_dict = load_subsaharan_countries_dict()
    
    # Add regional aggregates with full names
    regions_dict = {
        'SSA': 'Sub-Saharan Africa',
        'AFE': 'Eastern & Southern Africa',
        'AFW': 'Western & Central Africa'
    }
    
    # Combine countries and regions
    return {**countries_dict, **regions_dict}


def get_countries_with_regions() -> list:
    """
    Get list of Sub-Saharan African countries with regional aggregates at the end
    
    Returns:
        List of dictionaries with country names and codes, followed by regional options
    """
    # Get individual countries first
    countries = get_subsaharan_countries()
    
    # Sort countries alphabetically by name
    countries = sorted(countries, key=lambda x: x['name'])
    
    # Add regional aggregates at the end
    regional_options = [
        {'name': 'Sub-Saharan Africa', 'code': 'SSA'},
        {'name': 'Eastern & Southern Africa', 'code': 'AFE'},
        {'name': 'Western & Central Africa', 'code': 'AFW'}
    ]
    
    return countries + regional_options