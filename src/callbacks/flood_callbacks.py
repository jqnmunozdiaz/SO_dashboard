"""
Orchestrator for flood exposure callbacks
"""

from dash import Input, Output, State, html, dcc, ctx, MATCH, ALL, no_update
from .flood.National_Flood_Exposure_callbacks import register_national_flood_exposure_callbacks
from .flood.National_Flood_Exposure_Relative_callbacks import register_national_flood_exposure_relative_callbacks
from .flood.National_Flood_Exposure_Population_callbacks import register_national_flood_exposure_population_callbacks
from .flood.National_Flood_Exposure_Population_Relative_callbacks import register_national_flood_exposure_population_relative_callbacks
from .country_benchmark_callbacks import register_country_benchmark_options_callback, register_combined_benchmark_options_callback

try:
    from ..utils.flood_ui_helpers import create_flood_type_selector, create_return_period_selector, create_measurement_type_selector, create_exposure_type_selector
    from ..utils.ui_helpers import create_benchmark_selectors, create_combined_benchmark_selector, create_download_trigger_button, create_methodological_note_button
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.flood_ui_helpers import create_flood_type_selector, create_return_period_selector, create_measurement_type_selector, create_exposure_type_selector
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
    
    def create_flood_exposure_tab_content(exposure_type='built_s', measurement_type='absolute', benchmark_selections=None):
        """Helper function to create flood exposure tab content based on exposure and measurement type"""
        
        # Create 2x2 grid layout for filters
        # Top row: Exposure type (left) and Measurement type (right)
        top_row = html.Div([
            html.Div(
                create_exposure_type_selector('flood-exposure-type-selector', default_value=exposure_type),
                style={'flex': '1', 'min-width': '300px'}
            ),
            html.Div(
                create_measurement_type_selector('flood-measurement-type-selector', default_value=measurement_type),
                style={'flex': '1', 'min-width': '300px'}
            )
        ], style={'display': 'flex', 'gap': '1rem', 'flex-wrap': 'wrap'})
        
        # Bottom row: Return periods (left) and Benchmark selector (right, conditional)
        bottom_left = html.Div(
            create_return_period_selector('flood-return-period-selector'),
            style={'flex': '1', 'min-width': '300px'}
        )
        
        if measurement_type == 'relative':
            # Relative view: show benchmarks selector on bottom right
            # Preserve benchmark selections if provided, otherwise use empty list
            default_benchmarks = benchmark_selections if benchmark_selections is not None else []
            bottom_right = html.Div(
                create_combined_benchmark_selector(
                    dropdown_id='flood-combined-benchmark-selector',
                    default_regional_codes=default_benchmarks
                ),
                style={'flex': '1', 'min-width': '300px'}
            )
            bottom_row = html.Div([bottom_left, bottom_right], 
                                 style={'display': 'flex', 'gap': '1rem', 'flex-wrap': 'wrap'})
        else:
            # Absolute view: only return periods, no benchmarks
            bottom_row = html.Div([bottom_left], 
                                 style={'display': 'flex', 'gap': '1rem', 'flex-wrap': 'wrap'})
        
        # Store is now in the main layout, not recreated here
        filters_container = html.Div([
            top_row, 
            bottom_row
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '1rem'})
        
        # Determine which chart to render and download button based on exposure and measurement type
        if exposure_type == 'built_s' and measurement_type == 'absolute':
            chart_id = 'national-flood-exposure-chart'
            download_id = 'national-flood-exposure-download'
            data_source = "Fathom3 flood maps (2020) and GHSL Built-up Surface (2023)."
            note_prefix = "This chart shows the total built-up area exposed to flooding for different return periods. "
        elif exposure_type == 'built_s' and measurement_type == 'relative':
            chart_id = 'national-flood-exposure-relative-chart'
            download_id = 'national-flood-exposure-relative-download'
            data_source = "Fathom3 flood maps (2020) and GHSL Built-up Surface (2023)."
            note_prefix = "This chart shows the percentage of total built-up area exposed to flooding for different return periods. Values represent the proportion of a country's built-up area that falls within flood-prone zones. "
        elif exposure_type == 'pop' and measurement_type == 'absolute':
            chart_id = 'national-flood-exposure-population-chart'
            download_id = 'national-flood-exposure-population-download'
            data_source = "Fathom3 flood maps (2020) and GHSL Population (2023)."
            note_prefix = "This chart shows the total population exposed to flooding for different return periods. "
        else:  # pop + relative
            chart_id = 'national-flood-exposure-population-relative-chart'
            download_id = 'national-flood-exposure-population-relative-download'
            data_source = "Fathom3 flood maps (2020) and GHSL Population (2023)."
            note_prefix = "This chart shows the percentage of total population exposed to flooding for different return periods. Values represent the proportion of a country's population that falls within flood-prone zones. "
        
        # Create note text
        note_text = [
            html.B("Data Source: "), 
            data_source,
            html.Br(),
            html.B("Note: "), 
            note_prefix,
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
            filters_container,
            
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
        
        if active_subtab == 'national-flood-exposure':
            # Default to built-up area, absolute view on initial load
            return create_flood_exposure_tab_content('built_s', 'absolute')
        
        return html.Div("Select a subtab to view flood exposure data")
    
    @app.callback(
        [Output('flood-exposure-content', 'children', allow_duplicate=True),
         Output('flood-benchmark-store', 'data', allow_duplicate=True)],
        [Input('flood-exposure-type-selector', 'value'),
         Input('flood-measurement-type-selector', 'value')],
        [State('flood-benchmark-store', 'data')],
        prevent_initial_call=True
    )
    def update_flood_exposure_content(exposure_type, measurement_type, stored_benchmarks):
        """Update content when exposure type or measurement type changes"""
        # Use stored benchmark selections if available
        content = create_flood_exposure_tab_content(
            exposure_type or 'built_s', 
            measurement_type or 'absolute',
            stored_benchmarks
        )
        # Return content and keep the stored benchmarks unchanged
        return content, stored_benchmarks
    
    @app.callback(
        Output('flood-benchmark-store', 'data', allow_duplicate=True),
        Input('flood-combined-benchmark-selector', 'value'),
        State('flood-benchmark-store', 'data'),
        prevent_initial_call=True
    )
    def save_benchmark_selections(benchmark_value, current_stored):
        """Save benchmark selections to store when they change"""
        print(f"DEBUG save_benchmark_selections: benchmark_value={benchmark_value}, current_stored={current_stored}")
        
        # If the incoming value matches what we stored, it's just the component initializing
        # with the default we gave it - don't update anything
        if benchmark_value == current_stored:
            return no_update
        
        # If we have a real user change (value is not None and differs from stored)
        if benchmark_value is not None:
            return benchmark_value
        
        # If value is None (shouldn't happen but just in case), no update
        return no_update

