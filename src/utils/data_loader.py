"""
Data loading utilities for the DRM dashboard
"""

import pandas as pd
import os

from typing import Dict, Optional


def _get_project_root() -> str:
    """Get the absolute path to the project root directory"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(current_dir, '..', '..')


def _load_csv(file_path: str, error_context: str, **kwargs) -> pd.DataFrame:
    """
    Generic CSV loader with consistent error handling
    
    Args:
        file_path: Path to CSV file
        error_context: Context string for error messages
        **kwargs: Additional arguments to pass to pd.read_csv
        
    Returns:
        DataFrame loaded from CSV with original filename attached as metadata
    """
    try:
        df = pd.read_csv(file_path, **kwargs)
        # Attach original filename (without extension) as metadata
        df.attrs['original_filename'] = os.path.splitext(os.path.basename(file_path))[0]
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"{error_context} data file not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error loading {error_context} data: {str(e)}")

def load_emdat_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """Load EM-DAT disaster data for African countries"""
    if file_path is None:
        project_root = _get_project_root()
        file_path = os.path.join(project_root, 'data', 'processed', 'african_disasters_emdat.csv')
    
    return _load_csv(file_path, "EM-DAT")


def load_wdi_data(indicator_code: str, file_path: Optional[str] = None) -> pd.DataFrame:
    """Load World Development Indicators data for a specific indicator"""
    if file_path is None:
        project_root = _get_project_root()
        file_path = os.path.join(project_root, 'data', 'processed', 'wdi', f'{indicator_code}.csv')
    
    return _load_csv(file_path, "WDI")


def load_urbanization_indicators_dict() -> Dict[str, str]:
    """Load dictionary mapping urbanization indicator codes to names"""
    project_root = _get_project_root()
    csv_path = os.path.join(project_root, 'data', 'Definitions', 'urbanization_indicators_selection.csv')
    try:
        df = _load_csv(csv_path, "Urbanization indicators")
        return dict(zip(df['Indicator_Code'], df['Indicator_Name']))
    except Exception:
        print(f"Warning: Urbanization indicators file not found at {csv_path}")
        return {}


def load_urbanization_indicators_notes_dict() -> Dict[str, str]:
    """Load dictionary mapping urbanization indicator codes to notes"""
    project_root = _get_project_root()
    csv_path = os.path.join(project_root, 'data', 'Definitions', 'urbanization_indicators_selection.csv')
    try:
        df = _load_csv(csv_path, "Urbanization indicators")
        return dict(zip(df['Indicator_Code'], df['Note']))
    except Exception:
        print(f"Warning: Urbanization indicators notes file not found at {csv_path}")
        return {}


def load_undesa_urban_projections() -> pd.DataFrame:
    """Load UNDESA urban population projections (ISO3, indicator, year, value)"""
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'UNDESA_Country', 'UNDESA_urban_projections_consolidated.csv')
    return _load_csv(file_path, "UNDESA urban projections")


def load_undesa_urban_growth_rates() -> pd.DataFrame:
    """Load UN DESA urban population year-over-year growth rates"""
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'UNDESA_Country', 'UNDESA_urban_growth_rates_consolidated.csv')
    return _load_csv(file_path, "UNDESA urban growth rates")


def load_WUP_urban_projections() -> pd.DataFrame:
    """
    Load WUP2025 urban population projections combined with WPP2024 uncertainty bounds.
    
    Returns:
        DataFrame with columns: ['ISO3', 'indicator', 'year', 'value']
        
    Indicators include:
        - wpp_median, wpp_lower95, wpp_lower80, wpp_upper80, wpp_upper95: WPP total population
        - wup_urban_pop, wup_rural_pop: WUP urbanization data
        - wup_urban_prop, wup_rural_prop: WUP urbanization rates
        - urban_pop_median, urban_pop_lower95, etc.: Urban population with uncertainty
        - rural_pop_median, rural_pop_lower95, etc.: Rural population with uncertainty
    """
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'WUP', 'WUP2025_urban_projections_consolidated.csv')
    return _load_csv(file_path, "WUP2025 urban projections")


def load_WUP_urban_growth_rates() -> pd.DataFrame:
    """
    Load WUP2025 urban population growth rates (CAGR for 5-year periods).
    
    Returns:
        DataFrame with columns: ['ISO3', 'year', 'indicator', 'value']
        
    Indicators include:
        - urban_growth_rate, rural_growth_rate: Historical growth rates
        - urban_median_growth_rate, rural_median_growth_rate: Median projections
        - urban_lower80_growth_rate, urban_upper80_growth_rate: 80% confidence intervals
        - urban_lower95_growth_rate, urban_upper95_growth_rate: 95% confidence intervals
        - (same for rural)
    """
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'WUP', 'WUP2025_urban_growth_rates_consolidated.csv')
    return _load_csv(file_path, "WUP2025 urban growth rates")


def load_city_size_distribution() -> pd.DataFrame:
    """Load individual cities data for Sub-Saharan Africa"""
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'cities_individual.csv')
    return _load_csv(file_path, "City size distribution")


def load_population_data(country_iso: str) -> pd.DataFrame:
    """Load WPP 2024 total population data for a specific country"""
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
    """Load JMP WASH urban drinking water data for Sub-Saharan Africa"""
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'jmp_water', 'urban_drinking_water_ssa.csv')
    return _load_csv(file_path, "JMP water")


def load_jmp_sanitation_data() -> pd.DataFrame:
    """Load JMP WASH urban sanitation data for Sub-Saharan Africa"""
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'jmp_sanitation', 'urban_sanitation_ssa.csv')
    return _load_csv(file_path, "JMP sanitation")


def load_cities_data() -> pd.DataFrame:
    """Load city population and built-up area data with size categories"""
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'africapolis_worldpop_final_merged_format_1.csv')
    return _load_csv(file_path, "Cities data")


def load_africapolis_ghsl_simple() -> pd.DataFrame:
    """Load Africapolis-GHSL cities growth data (2000-2020)"""
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'africapolis_ghsl_simple.csv')
    return _load_csv(file_path, "Africapolis GHSL simple")


def load_africapolis_centroids() -> pd.DataFrame:
    """Load Africapolis city centroids with coordinates"""
    project_root = _get_project_root()
    file_path = os.path.join(project_root, 'data', 'processed', 'africapolis2024_centroids.csv')
    return _load_csv(file_path, "Africapolis centroids")


def load_urban_density_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """Load built-up area per capita by country and year"""
    if file_path is None:
        project_root = _get_project_root()
        file_path = os.path.join(project_root, 'data', 'processed', 'built_up_per_capita_m2_by_country_year.csv')

    return _load_csv(file_path, "Built-up per capita")


def load_precipitation_data(var_name: str = '1day', file_path: Optional[str] = None) -> pd.DataFrame:
    """Load future precipitation return period projections from CCKP"""
    if file_path is None:
        project_root = _get_project_root()
        file_path = os.path.join(project_root, 'data', 'processed', f'ReturnPeriods-{var_name}-clean.csv')
    
    return _load_csv(file_path, "Precipitation")


def load_flood_projections_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """Load consolidated flood exposure projections for Sub-Saharan Africa"""
    if file_path is None:
        project_root = _get_project_root()
        file_path = os.path.join(project_root, 'data', 'processed', 'ALL_SSA_BUexp_projected_consolidated.csv')
    
    return _load_csv(file_path, "Flood projections", index_col=0)


def load_wup2025_level1_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """Load WUP 2025 Level 1 population by Cities/Towns/Rural categories"""
    if file_path is None:
        project_root = _get_project_root()
        file_path = os.path.join(project_root, 'data', 'processed', 'WUP', 'WUP2025_Level1_Population_Surface_processed.csv')
    
    return _load_csv(file_path, "WUP2025 Level1")


def load_wup2025_national_data(file_path: Optional[str] = None) -> pd.DataFrame:
    """Load WUP 2025 National Definitions with urbanization rates"""
    if file_path is None:
        project_root = _get_project_root()
        file_path = os.path.join(project_root, 'data', 'processed', 'WUP', 'WUP2025_National_Definitions_Population_processed_pivoted.csv')
    
    return _load_csv(file_path, "WUP2025 National Definitions")


# Import centralized country utilities
from .country_utils import get_subsaharan_countries, load_subsaharan_countries_dict, load_subsaharan_countries_and_regions_dict

# Re-export for backward compatibility
__all__ = [
    # Country utilities (re-exported from country_utils)
    'get_subsaharan_countries',
    'load_subsaharan_countries_dict',
    'load_subsaharan_countries_and_regions_dict',
    # EM-DAT
    'load_emdat_data',
    # WDI
    'load_wdi_data',
    'load_urbanization_indicators_dict',
    'load_urbanization_indicators_notes_dict',
    # UNDESA
    'load_undesa_urban_projections',
    'load_undesa_urban_growth_rates',
    # WUP
    'load_WUP_urban_projections',
    'load_WUP_urban_growth_rates',
    'load_wup2025_level1_data',
    'load_wup2025_national_data',
    # Cities
    'load_city_size_distribution',
    'load_cities_data',
    'load_africapolis_ghsl_simple',
    'load_africapolis_centroids',
    # Population
    'load_population_data',
    # JMP WASH
    'load_jmp_water_data',
    'load_jmp_sanitation_data',
    # Urban density
    'load_urban_density_data',
    # Climate/Flood projections
    'load_precipitation_data',
    'load_flood_projections_data',
]