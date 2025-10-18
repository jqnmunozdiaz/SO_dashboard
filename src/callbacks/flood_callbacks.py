"""
Orchestrator for flood exposure callbacks
"""

from dash import Input, Output, html, dcc
from .flood.National_Flood_Exposure_callbacks import register_national_flood_exposure_callbacks
from .flood.National_Flood_Exposure_Relative_callbacks import register_national_flood_exposure_relative_callbacks
from .country_benchmark_callbacks import register_country_benchmark_options_callback, register_combined_benchmark_options_callback

try:
    from ..utils.flood_ui_helpers import create_flood_type_selector, create_return_period_selector
    from ..utils.ui_helpers import create_benchmark_selectors, create_combined_benchmark_selector
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.flood_ui_helpers import create_flood_type_selector, create_return_period_selector
    from src.utils.ui_helpers import create_benchmark_selectors, create_combined_benchmark_selector


def register_callbacks(app):
    """Register all flood exposure callbacks"""
    
    # Register individual chart callbacks
    register_national_flood_exposure_callbacks(app)
    register_national_flood_exposure_relative_callbacks(app)
    
    # Register combined benchmark dropdown callback
    register_combined_benchmark_options_callback(app, 'flood-combined-benchmark-selector')
    
    @app.callback(
        Output('flood-exposure-content', 'children'),
        Input('flood-exposure-subtabs', 'active_tab')
    )
    def render_flood_exposure_chart(active_subtab):
        """Render the appropriate flood exposure visualization"""
        
        if active_subtab == 'national-flood-exposure':
            return html.Div([
                # Flood type selector
                create_flood_type_selector('flood-type-selector'),
                
                # Chart
                dcc.Graph(id="national-flood-exposure-chart"),
                
                # Data source note
                html.Div([
                    html.P([
                        html.B("Data Source: "), 
                        "Fathom3 flood maps (2020) and GHSL Built-up Surface (2023).",
                        html.Br(),
                        html.B("Note: "), 
                        "This chart shows the total built-up area exposed to flooding for different return periods. "
                        "A 1-in-100 year flood has a 1% probability of occurring in any given year and typically affects "
                        "larger areas than more frequent floods. ",
                        html.A("Learn more about flood return periods", 
                               href="https://www.gfdrr.org/en/100-year-flood", 
                               target="_blank",
                               style={'color': '#295e84', 'text-decoration': 'underline'}),
                        "."
                    ], className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        
        elif active_subtab == 'national-flood-exposure-relative':
            return html.Div([
                # Flood type selector
                create_flood_type_selector('flood-type-selector-relative'),
                
                # Return period selector
                create_return_period_selector('flood-return-period-selector-relative'),
                
                # Combined benchmark selector
                create_combined_benchmark_selector(
                    dropdown_id='flood-combined-benchmark-selector',
                    default_regional_codes=[]
                ),
                
                # Chart
                dcc.Graph(id="national-flood-exposure-relative-chart"),
                
                # Data source note
                html.Div([
                    html.P([
                        html.B("Data Source: "), 
                        "Fathom3 flood maps (2020) and GHSL Built-up Surface (2023).",
                        html.Br(),
                        html.B("Note: "), 
                        "This chart shows the percentage of total built-up area exposed to flooding for different return periods. "
                        "Values represent the proportion of a country's built-up area that falls within flood-prone zones. ",
                        html.A("Learn more about flood return periods", 
                               href="https://www.gfdrr.org/en/100-year-flood", 
                               target="_blank",
                               style={'color': '#295e84', 'text-decoration': 'underline'}),
                        "."
                    ], className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        
        return html.Div("Select a subtab to view flood exposure data")
