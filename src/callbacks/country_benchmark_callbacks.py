"""
Shared callbacks for country benchmark dropdowns
Provides reusable callback registration for populating country benchmark options
"""

from dash import Input, Output

try:
    from ..utils.country_utils import load_subsaharan_countries_dict
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.country_utils import load_subsaharan_countries_dict


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