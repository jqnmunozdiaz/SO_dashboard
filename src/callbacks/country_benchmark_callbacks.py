"""
Shared callbacks for country benchmark dropdowns
Provides reusable callback registration for populating country benchmark options
"""

from dash import Input, Output

try:
    from ..utils.country_utils import load_subsaharan_countries_dict
    from ..utils.benchmark_config import get_benchmark_names
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.country_utils import load_subsaharan_countries_dict
    from src.utils.benchmark_config import get_benchmark_names


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


def register_combined_benchmark_options_callback(app, output_id, default_regional_codes=None):
    """
    Register a callback to populate combined benchmark dropdown with countries and regions.
    Countries are listed first alphabetically, followed by regional benchmarks.
    
    Args:
        app: Dash app instance
        output_id: ID of the dropdown to populate (e.g., 'slums-combined-benchmark-selector')
        default_regional_codes: List of regional codes to select by default (e.g., ['SSA'])
    """
    @app.callback(
        [Output(output_id, 'options'), Output(output_id, 'value')],
        [Input('main-country-filter', 'value')]
    )
    def populate_combined_benchmark_options(selected_country):
        """Populate dropdown with countries (excluding selected) and regions"""
        try:
            countries_dict = load_subsaharan_countries_dict()
            regional_names = get_benchmark_names()
            
            # Create country options list excluding the selected country and regional codes
            country_options = []
            for iso_code, country_name in countries_dict.items():
                # Exclude selected country and regional aggregates (SSA, AFE, AFW)
                if iso_code != selected_country and iso_code not in regional_names:
                    country_options.append({'label': country_name, 'value': iso_code})
            
            # Sort countries by name
            country_options.sort(key=lambda x: x['label'])
            
            # Add regional benchmarks at the end
            regional_options = [
                {'label': f"{name}", 'value': code}
                for code, name in regional_names.items()
            ]
            
            # Combine countries and regions
            all_options = country_options + regional_options
            
            # Set default value if provided
            default_value = default_regional_codes if default_regional_codes else []
            
            return all_options, default_value
        
        except Exception as e:
            print(f"Error populating combined benchmark options for {output_id}: {str(e)}")
            return [], []