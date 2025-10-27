"""
Orchestrator for flood exposure callbacks
"""

from dash import Input, Output, State, html, dcc, no_update
import dash_bootstrap_components as dbc
from .flood.National_Flood_Exposure_callbacks import register_national_flood_exposure_callbacks
from .flood.National_Flood_Exposure_Relative_callbacks import register_national_flood_exposure_relative_callbacks
from .flood.National_Flood_Exposure_Population_callbacks import register_national_flood_exposure_population_callbacks
from .flood.National_Flood_Exposure_Population_Relative_callbacks import register_national_flood_exposure_population_relative_callbacks
from .flood.Cities_Flood_Exposure_callbacks import register_cities_flood_exposure_callbacks
from .flood.Precipitation_callbacks import register_precipitation_callbacks
from .country_benchmark_callbacks import register_combined_benchmark_options_callback

try:
    from ..utils.flood_ui_helpers import (create_return_period_selector, 
                                           create_measurement_type_selector, create_exposure_type_selector,
                                           create_city_return_period_selector)
    from ..utils.ui_helpers import create_combined_benchmark_selector, create_download_trigger_button, create_methodological_note_button
    from ..utils.country_utils import get_subsaharan_countries
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.flood_ui_helpers import (create_return_period_selector, 
                                             create_measurement_type_selector, create_exposure_type_selector,
                                             create_city_return_period_selector)
    from src.utils.ui_helpers import create_combined_benchmark_selector, create_download_trigger_button, create_methodological_note_button
    from src.utils.country_utils import get_subsaharan_countries


def register_callbacks(app):
    """Register all flood exposure callbacks"""
    
    # Callback to filter country dropdown options based on active flood subtab
    @app.callback(
        Output('main-country-filter', 'options', allow_duplicate=True),
        Input('flood-exposure-subtabs', 'active_tab'),
        prevent_initial_call=True
    )
    def update_country_filter_options_flood(flood_subtab):
        """Update country filter options for flood tabs - hide regional aggregates for Cities Flood Exposure"""
        try:
            # Get individual countries (without regional aggregates)
            countries = get_subsaharan_countries()
            
            # Sort countries alphabetically by name
            countries = sorted(countries, key=lambda x: x['name'])
            
            # For Cities Flood Exposure, only show individual countries
            if flood_subtab == 'cities-flood-exposure':
                return [{'label': country['name'], 'value': country['code']} for country in countries]
            else:
                # For National Flood Exposure, include regional aggregates
                regional_options = [
                    {'label': 'Sub-Saharan Africa', 'value': 'SSA'},
                    {'label': 'Eastern & Southern Africa', 'value': 'AFE'},
                    {'label': 'Western & Central Africa', 'value': 'AFW'}
                ]
                all_options = [{'label': country['name'], 'value': country['code']} for country in countries]
                all_options.extend(regional_options)
                return all_options
                
        except Exception as e:
            print(f"Error updating country filter options for flood: {str(e)}")
            # Fallback to individual countries only
            countries = get_subsaharan_countries()
            countries = sorted(countries, key=lambda x: x['name'])
            return [{'label': country['name'], 'value': country['code']} for country in countries]
    
    # Register individual chart callbacks
    register_national_flood_exposure_callbacks(app)
    register_national_flood_exposure_relative_callbacks(app)
    register_national_flood_exposure_population_callbacks(app)
    register_national_flood_exposure_population_relative_callbacks(app)
    register_cities_flood_exposure_callbacks(app)
    register_precipitation_callbacks(app)
    
    # Register combined benchmark dropdown callbacks
    register_combined_benchmark_options_callback(app, 'flood-combined-benchmark-selector')
    
    def create_flood_exposure_tab_content(exposure_type='built_s', measurement_type='absolute', benchmark_selections=None):
        """Helper function to create flood exposure tab content based on exposure and measurement type"""
        
        # Create 2x2 grid layout for filters # Top row: Exposure type (left) and Measurement type (right)
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
    
    def create_cities_flood_exposure_tab_content():
        """Helper function to create cities flood exposure tab content"""
        
        # Create filters layout - simpler than national (no benchmarks)
        # Top row: Exposure type (left) and Measurement type (right)
        top_row = html.Div([
            html.Div(
                create_exposure_type_selector('cities-flood-exposure-type-selector', default_value='built_s'),
                style={'flex': '1', 'min-width': '300px'}
            ),
            html.Div(
                create_measurement_type_selector('cities-flood-measurement-type-selector', default_value='absolute'),
                style={'flex': '1', 'min-width': '300px'}
            )
        ], style={'display': 'flex', 'gap': '1rem', 'flex-wrap': 'wrap'})
        
        # Bottom row: Return period selector (left) and map button (right)
        bottom_row = html.Div([
            html.Div(
                create_city_return_period_selector('cities-flood-return-period-selector'),
                style={'flex': '1', 'min-width': '300px'}
            ),
            html.Div(
                dbc.Button("📍 Where are these cities?", id="cities-flood-map-button", color="info", className="download-data-button"),
                style={'display': 'flex', 'align-items': 'flex-end', 'padding-bottom': '0.5rem'}
            )
        ], style={'display': 'flex', 'gap': '1rem', 'flex-wrap': 'wrap', 'justify-content': 'space-between'})
        
        filters_container = html.Div([
            top_row, 
            bottom_row
        ], style={'display': 'flex', 'flex-direction': 'column', 'gap': '1rem'})
        
        # Chart and download IDs
        chart_id = 'cities-flood-exposure-chart'
        download_id = 'cities-flood-exposure-download'
        
        # Data source note
        data_source = "Fathom3 flood maps (2020), GHSL Built-up Surface and Population (2023), and Africapolis city boundaries."
        note_prefix = "This chart shows flood exposure over time for cities in the selected country. Each line represents a different city. "
        
        note_text = [
            html.B("Data Source: "), 
            data_source,
            html.Br(),
            html.B("Note: "), 
            note_prefix,
            "The data includes up to 5 major cities per country. ",
            "A 1-in-100 year flood has a 1% probability of occurring in any given year. ",
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
            ], className="indicator-note-container"),
            
            # City Map Modal
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("City Locations")),
                dbc.ModalBody([
                    html.Div(id="cities-flood-map-container", style={'height': '70vh'})
                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-cities-flood-map-button", className="ml-auto")
                )
            ], id="cities-flood-map-modal", size="xl", is_open=False)
        ], className="chart-container")
    
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
                value=[5, 10, 100],  # Both selected by default
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
        
        elif active_subtab == 'cities-flood-exposure':
            # Cities flood exposure tab - no benchmarks
            return create_cities_flood_exposure_tab_content()
        
        return html.Div("Select a subtab to view flood exposure data")
    
    @app.callback(
        Output('flood-projections-content', 'children'),
        Input('flood-projections-subtabs', 'active_tab'),
        prevent_initial_call=False
    )
    def render_flood_projections_chart(active_subtab):
        """Render the appropriate flood projections visualization"""
        
        if active_subtab == 'precipitation':
            # Precipitation patterns tab
            return create_precipitation_tab_content()
        
        return html.Div("Select a subtab to view flood projection data")
    
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

