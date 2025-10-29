"""
Orchestrator for flood projections callbacks
Handles the "Projections of Flood Risk" main tab
"""

from dash import Input, Output, html, dcc

from .flood_projections.Precipitation_callbacks import register_precipitation_callbacks
from .flood_projections.Urbanization_vs_Climate_Change_callbacks import register_urbanization_vs_climate_change_callbacks
from ..utils.ui_helpers import create_download_trigger_button, create_methodological_note_button
from ..utils.country_utils import get_subsaharan_countries
from config.settings import CHART_STYLES


def register_callbacks(app):
    """Register all flood projections callbacks"""
    
    # Register individual chart callbacks
    register_precipitation_callbacks(app)
    register_urbanization_vs_climate_change_callbacks(app)
    
    # Callback to filter country dropdown options based on active flood projections subtab
    @app.callback(
        Output('main-country-filter', 'options', allow_duplicate=True),
        Input('flood-projections-subtabs', 'active_tab'),
        prevent_initial_call=True
    )
    def update_country_filter_options_flood_projections(projections_subtab):
        """Update country filter options for flood projections tabs - hide regional aggregates for all flood projection subtabs"""
        try:
            # Get individual countries (without regional aggregates)
            countries = get_subsaharan_countries()
            
            # Sort countries alphabetically by name
            countries = sorted(countries, key=lambda x: x['name'])
            
            # For all flood projections tabs, only show individual countries (no regional aggregates)
            return [{'label': country['name'], 'value': country['code']} for country in countries]
                
        except Exception as e:
            print(f"Error updating country filter options for flood projections: {str(e)}")
            # Fallback to individual countries only
            countries = get_subsaharan_countries()
            countries = sorted(countries, key=lambda x: x['name'])
            return [{'label': country['name'], 'value': country['code']} for country in countries]
    
    def create_precipitation_tab_content():
        """Helper function to create precipitation patterns tab content"""
        
        # Return period checkboxes selector
        rp_selector = html.Div([
            html.Label('Return Periods:', className='filter-label'),
            dcc.Checklist(
                id='precipitation-rp-selector',
                options=[
                    {'label': ' 5-year (20% annual probability)', 'value': 5},
                    {'label': ' 10-year (10% annual probability)', 'value': 10},
                    {'label': ' 100-year (1% annual probability)', 'value': 100}
                ],
                value=[5, 10, 100],  # All selected by default
                className='benchmark-checkboxes',
                inline=True,
                labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
            )
        ], className='filter-container')
        
        # Data source note
        data_source = "World Bank Climate Change Knowledge Portal (CCKP) - Future precipitation return periods based on climate projections."
        note_prefix = "This chart shows how precipitation patterns are projected to change by 2050 under different climate scenarios (SSP pathways). "
        
        note_text = [
            html.B("Data Source: "), 
            data_source,
            html.Br(),
            html.B("Note: "), 
            note_prefix,
            "The 'Today' marker represents current conditions, while the colored dots show future projections. ",
            "Values moving to the right indicate increased frequency of precipitation events. ",
            "SSP1-1.9 represents the most optimistic scenario with strong climate mitigation, ",
            "while SSP5-8.5 represents a high-emissions scenario."
        ]
        
        return html.Div([
            # Return period selector
            rp_selector,
            
            # Chart
            dcc.Graph(id='precipitation-chart'),
            
            # Data source note
            html.Div([
                html.P(note_text, className="indicator-note"),
                html.Div([
                    create_download_trigger_button('precipitation-download'),
                    create_methodological_note_button()
                ], className="buttons-container")
            ], className="indicator-note-container")
        ], className="chart-container")
    
    def create_urbanization_vs_climate_change_tab_content():
        """Helper function to create urbanization vs climate change comparison tab content"""
        
        # Data source note
        data_source = "Fathom3 flood maps (2020), GHSL Built-up Surface (2023), UN World Population Prospects (2022), and IPCC climate scenarios."
        note_prefix = "This chart compares built-up area exposed to flooding under different future scenarios. "
        
        note_text = [
            html.B("Data Source: "), 
            data_source,
            html.Br(),
            html.B("Note: "), 
            note_prefix,
            "Demographic scenarios (left group) show flood exposure changes based on population growth and urbanization, ",
            "assuming constant built-up area per capita from 2020. ",
            "Climate change scenarios (right group) show exposure changes from climate-driven flood pattern changes. ",
            "The horizontal dashed line represents 2020 baseline conditions. ",
            "Bars above this line indicate increased flood exposure."
        ]
        
        return html.Div([
            # Chart (no additional filters needed - uses main country filter)
            dcc.Graph(id='urbanization-vs-climate-change-chart'),
            
            # Data source note
            html.Div([
                html.P(note_text, className="indicator-note"),
                html.Div([
                    create_download_trigger_button('urbanization-vs-climate-change-download'),
                    create_methodological_note_button()
                ], className="buttons-container")
            ], className="indicator-note-container")
        ], className="chart-container")
    
    @app.callback(
        Output('flood-projections-content', 'children'),
        Input('flood-projections-subtabs', 'active_tab'),
        prevent_initial_call=False
    )
    def render_flood_projections_chart(active_subtab):
        """Render the appropriate flood projections visualization"""
        
        # Create both tab contents
        precipitation_content = create_precipitation_tab_content()
        urbanization_vs_climate_content = create_urbanization_vs_climate_change_tab_content()
        
        # Return both, but only display the active one
        return html.Div([
            html.Div(
                precipitation_content,
                style={'display': 'block' if active_subtab == 'precipitation' else 'none'}
            ),
            html.Div(
                urbanization_vs_climate_content,
                style={'display': 'block' if active_subtab == 'urbanization-vs-climate' else 'none'}
            )
        ])

