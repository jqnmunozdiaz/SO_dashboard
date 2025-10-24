"""
Orchestrator for flood exposure callbacks
"""

from dash import Input, Output, State, html, dcc
from .flood.National_Flood_Exposure_callbacks import register_national_flood_exposure_callbacks
from .flood.National_Flood_Exposure_Relative_callbacks import register_national_flood_exposure_relative_callbacks
from .flood.National_Flood_Exposure_Population_callbacks import register_national_flood_exposure_population_callbacks
from .flood.National_Flood_Exposure_Population_Relative_callbacks import register_national_flood_exposure_population_relative_callbacks
from .country_benchmark_callbacks import register_country_benchmark_options_callback, register_combined_benchmark_options_callback

try:
    from ..utils.flood_ui_helpers import create_flood_type_selector, create_return_period_selector, create_measurement_type_selector
    from ..utils.ui_helpers import create_benchmark_selectors, create_combined_benchmark_selector, create_download_trigger_button, create_methodological_note_button
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.flood_ui_helpers import create_flood_type_selector, create_return_period_selector, create_measurement_type_selector
    from src.utils.ui_helpers import create_benchmark_selectors, create_combined_benchmark_selector, create_download_trigger_button, create_methodological_note_button


def register_callbacks(app):
    """Register all flood exposure callbacks"""
    
    # Register individual chart callbacks
    register_national_flood_exposure_callbacks(app)
    register_national_flood_exposure_relative_callbacks(app)
    register_national_flood_exposure_population_callbacks(app)
    register_national_flood_exposure_population_relative_callbacks(app)
    
    # Register combined benchmark dropdown callbacks
    register_combined_benchmark_options_callback(app, 'flood-combined-benchmark-selector')
    register_combined_benchmark_options_callback(app, 'flood-combined-benchmark-selector-population')
    
    def create_buildup_tab_content(measurement_type='absolute'):
        """Helper function to create built-up tab content based on measurement type"""
        
        # Determine which filters to show based on measurement type
        filters = [create_measurement_type_selector('flood-measurement-type-selector', default_value=measurement_type)]
        
        # Show return period selector and benchmark dropdown only for relative view
        if measurement_type == 'relative':
            filters.append(create_combined_benchmark_selector(
                dropdown_id='flood-combined-benchmark-selector',
                default_regional_codes=[]
            ))
            filters.append(create_return_period_selector('flood-return-period-selector-relative'))
        
        # Determine which chart to render and download button
        chart_id = 'national-flood-exposure-relative-chart' if measurement_type == 'relative' else 'national-flood-exposure-chart'
        download_id = 'national-flood-exposure-relative-download' if measurement_type == 'relative' else 'national-flood-exposure-download'
        
        # Create note text based on measurement type
        if measurement_type == 'relative':
            note_text = [
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
            ]
        else:
            note_text = [
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
            ]
        
        return html.Div([
            # Filters
            html.Div(filters, style={'display': 'flex', 'flex-wrap': 'wrap', 'gap': '1rem'}),
            
            # Chart
            dcc.Graph(id=chart_id),
            
            # Data source note
            html.Div([
                html.P(note_text, className="indicator-note"),
                html.Div([
                    create_download_trigger_button(download_id),
                    create_methodological_note_button()
                ], className="buttons-container")
            ], className="indicator-note-container")
        ], className="chart-container")
    
    @app.callback(
        Output('flood-exposure-content', 'children'),
        Input('flood-exposure-subtabs', 'active_tab'),
        prevent_initial_call=False
    )
    def render_flood_exposure_chart(active_subtab):
        """Render the appropriate flood exposure visualization"""
        
        if active_subtab == 'national-flood-exposure-buildup':
            # Default to absolute view on initial load
            return create_buildup_tab_content('absolute')
        
        elif active_subtab == 'national-flood-exposure-population':
            return html.Div([
                # Flood type selector
                create_flood_type_selector('flood-type-selector-population'),
                
                # Chart
                dcc.Graph(id="national-flood-exposure-population-chart"),
                
                # Data source note
                html.Div([
                    html.P([
                        html.B("Data Source: "), 
                        "Fathom3 flood maps (2020) and GHSL Population (2023).",
                        html.Br(),
                        html.B("Note: "), 
                        "This chart shows the total population exposed to flooding for different return periods. "
                        "A 1-in-100 year flood has a 1% probability of occurring in any given year and typically affects "
                        "larger areas than more frequent floods. ",
                        html.A("Learn more about flood return periods", 
                               href="https://www.gfdrr.org/en/100-year-flood", 
                               target="_blank",
                               style={'color': '#295e84', 'text-decoration': 'underline'}),
                        "."
                    ], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('national-flood-exposure-population-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        
        elif active_subtab == 'national-flood-exposure-population-relative':
            return html.Div([
                # Flood type selector
                create_flood_type_selector('flood-type-selector-population-relative'),
                
                # Return period selector
                create_return_period_selector('flood-return-period-selector-population-relative'),
                
                # Combined benchmark selector
                create_combined_benchmark_selector(
                    dropdown_id='flood-combined-benchmark-selector-population',
                    default_regional_codes=[]
                ),
                
                # Chart
                dcc.Graph(id="national-flood-exposure-population-relative-chart"),
                
                # Data source note
                html.Div([
                    html.P([
                        html.B("Data Source: "), 
                        "Fathom3 flood maps (2020) and GHSL Population (2023).",
                        html.Br(),
                        html.B("Note: "), 
                        "This chart shows the percentage of total population exposed to flooding for different return periods. "
                        "Values represent the proportion of a country's population that falls within flood-prone zones. ",
                        html.A("Learn more about flood return periods", 
                               href="https://www.gfdrr.org/en/100-year-flood", 
                               target="_blank",
                               style={'color': '#295e84', 'text-decoration': 'underline'}),
                        "."
                    ], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('national-flood-exposure-population-relative-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        
        return html.Div("Select a subtab to view flood exposure data")
    
    @app.callback(
        Output('flood-exposure-content', 'children', allow_duplicate=True),
        Input('flood-measurement-type-selector', 'value'),
        prevent_initial_call=True
    )
    def update_buildup_measurement_type(measurement_type):
        """Update built-up tab content when measurement type changes"""
        return create_buildup_tab_content(measurement_type or 'absolute')
