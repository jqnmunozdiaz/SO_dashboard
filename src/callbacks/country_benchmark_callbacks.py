"""
Shared callbacks for country benchmark dropdowns
Provides reusable callback registration for populating country benchmark options
"""

from dash import Input, Output, State

from ..utils.country_utils import load_subsaharan_countries_dict
from ..utils.benchmark_config import get_benchmark_names


def register_country_benchmark_options_callback(app, output_id):
    """
    Register a callback to populate country benchmark dropdown options.
    
    Args:
        app: Dash app instance
        output_id: ID of the dropdown to populate (e.g., 'slums-country-benchmark-selector')
    """
    @app.callback(
        Output(output_id, 'options'),
        [Input('main-country-filter', 'value')]
    )
    def populate_country_benchmark_options(selected_country):
        """Populate country benchmark dropdown with all SSA countries except the selected one"""
        try:
            countries_dict = load_subsaharan_countries_dict()
            
            # Create options list excluding the selected country
            options = []
            for iso_code, country_name in countries_dict.items():
                if iso_code != selected_country:  # Exclude selected country
                    options.append({'label': country_name, 'value': iso_code})
            
            # Sort by country name
            options.sort(key=lambda x: x['label'])
            return options
        
        except Exception as e:
            print(f"Error populating country benchmark options for {output_id}: {str(e)}")
            return []


def register_combined_benchmark_options_callback(app, output_id, default_regional_codes=None, use_full_regions=False):
    """
    Register a callback to populate combined benchmark dropdown with countries and regions.
    Regional benchmarks are listed first, followed by countries alphabetically.
    
    Args:
        app: Dash app instance
        output_id: ID of the dropdown to populate (e.g., 'slums-combined-benchmark-selector')
        default_regional_codes: List of regional codes to select by default (e.g., ['SSA'])
        use_full_regions: If True, use FULL_REGIONAL_BENCHMARK_CONFIG (all WB regions);
                         if False, use BENCHMARK_CONFIG (SSA, AFE, AFW only)
    """
    # Import the appropriate regional names function based on use_full_regions flag
    if use_full_regions:
        from ..utils.benchmark_config import get_full_regional_benchmark_names
        get_regional_names = get_full_regional_benchmark_names
    else:
        get_regional_names = get_benchmark_names
    
    # Also read the flood-benchmark-store if present so we can set the dropdown value
    # from the persisted store when available. This prevents the options callback from
    # overwriting server-rendered initial values with an empty list.
    @app.callback(
        [Output(output_id, 'options'), Output(output_id, 'value')],
        [Input('main-country-filter', 'value')],
        [State('flood-benchmark-store', 'data')]
    )
    def populate_combined_benchmark_options(selected_country, stored_benchmarks):
        """Populate dropdown with countries (excluding selected) and regions"""
        try:
            countries_dict = load_subsaharan_countries_dict()
            regional_names = get_regional_names()
            
            # Create country options list excluding the selected country and regional codes
            country_options = []
            for iso_code, country_name in countries_dict.items():
                # Exclude selected country and regional aggregates
                if iso_code != selected_country and iso_code not in regional_names:
                    country_options.append({'label': country_name, 'value': iso_code})
            
            # Sort countries by name
            country_options.sort(key=lambda x: x['label'])
            
            # Add regional benchmarks at the beginning
            regional_options = [
                {'label': f"{name}", 'value': code}
                for code, name in regional_names.items()
            ]
            
            # Combine regions and countries (regions first)
            all_options = regional_options + country_options
            
            # Build set of valid codes for this dropdown
            valid_codes = set(regional_names.keys()) | set(countries_dict.keys())
            
            # Prefer the stored benchmarks (from the persistent store) if available.
            # Filter to only include codes valid for this dropdown's config.
            # Fall back to the default_regional_codes provided at registration time.
            if stored_benchmarks:
                # Filter stored benchmarks to only include valid codes for this dropdown
                default_value = [code for code in stored_benchmarks if code in valid_codes]
            else:
                default_value = default_regional_codes if default_regional_codes else []

            return all_options, default_value
        
        except Exception as e:
            print(f"Error populating combined benchmark options for {output_id}: {str(e)}")
            return [], []