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


def register_main_callbacks(app):
    """Register main navigation callbacks"""
    
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

