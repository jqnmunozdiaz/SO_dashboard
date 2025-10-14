"""
Main callback controller that handles tab switching and content rendering
"""

from dash import Input, Output, html, clientside_callback, ClientsideFunction
from src.layouts.world_bank_layout import (
    create_world_bank_disaster_tab_content, 
    create_world_bank_urbanization_tab_content,
    create_world_bank_flood_exposure_tab_content,
    create_world_bank_flood_projections_tab_content
)

try:
    from ..utils.country_utils import load_subsaharan_countries_and_regions_dict
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict


def register_main_callbacks(app):
    """Register main navigation callbacks"""
    
    @app.callback(
        Output('dynamic-header-title', 'children'),
        Input('main-country-filter', 'value')
    )
    def update_header_title(selected_country):
        """Update header title based on selected country"""
        try:
            if selected_country:
                # Load country and region mapping
                countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
                country_name = countries_and_regions_dict.get(selected_country, selected_country)
                return f"Sub-Saharan Africa DRM Dashboard | {country_name}"
            else:
                return "Sub-Saharan Africa DRM Dashboard"
        except Exception:
            return "Sub-Saharan Africa DRM Dashboard"
    
    @app.callback(
        Output('tab-content', 'children'),
        Input('main-tabs', 'active_tab')
    )
    def render_tab_content(active_tab):
        """Render content based on active tab"""
        
        if active_tab == 'disasters':
            return create_world_bank_disaster_tab_content()
        elif active_tab == 'urbanization':
            return create_world_bank_urbanization_tab_content()
        elif active_tab == 'flood-exposure':
            return create_world_bank_flood_exposure_tab_content()
        elif active_tab == 'flood-projections':
            return create_world_bank_flood_projections_tab_content()
        else:
            return html.Div([
                html.H3("Welcome to the Sub-Saharan Africa DRM Dashboard"),
                html.P("Select a tab above to begin exploring the data.")
            ])

