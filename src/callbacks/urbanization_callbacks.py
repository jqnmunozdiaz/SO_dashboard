"""
Main urbanization callbacks orchestrator
Coordinates all urbanization-related visualization callbacks
"""

from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

# Import individual callback modules
from .urbanization.Urban_Population_Living_in_Slums_callbacks import register_urban_population_living_in_slums_callbacks
from .urbanization.Access_to_Drinking_Water_callbacks import register_access_to_drinking_water_callbacks
from .urbanization.Access_to_Sanitation_callbacks import register_access_to_sanitation_callbacks
from .urbanization.Access_to_Electricity_Urban_callbacks import register_access_to_electricity_urban_callbacks
from .urbanization.Urban_Population_Projections_callbacks import register_urban_population_projections_callbacks
from .urbanization.Urbanization_Rate_callbacks import register_urbanization_rate_callbacks
from .urbanization.GDP_vs_Urbanization_callbacks import register_gdp_vs_urbanization_callbacks
from .urbanization.Cities_Distribution_callbacks import register_cities_distribution_callbacks
from .urbanization.Cities_Evolution_callbacks import register_cities_evolution_callbacks
from .urbanization.Urban_Density_callbacks import register_urban_density_callbacks
from .urbanization.Cities_Growth_Rate_callbacks import register_cities_growth_rate_callbacks
from .urbanization.Cities_Growth_callbacks import register_cities_growth_callbacks
from .country_benchmark_callbacks import register_country_benchmark_options_callback, register_combined_benchmark_options_callback

from ..utils.data_loader import load_urbanization_indicators_notes_dict
from ..utils.ui_helpers import create_benchmark_selectors, create_combined_benchmark_selector, create_download_trigger_button, create_methodological_note_button
from ..utils.country_utils import get_subsaharan_countries


def register_callbacks(app):
    """Register all urbanization-related callbacks"""
    
    # Register individual callback modules
    register_urban_population_living_in_slums_callbacks(app)
    register_access_to_drinking_water_callbacks(app)
    register_access_to_sanitation_callbacks(app)
    register_access_to_electricity_urban_callbacks(app)
    register_urban_population_projections_callbacks(app)
    register_urbanization_rate_callbacks(app)
    register_urban_density_callbacks(app)
    register_gdp_vs_urbanization_callbacks(app)
    register_cities_distribution_callbacks(app)
    register_cities_evolution_callbacks(app)
    register_cities_growth_rate_callbacks(app)
    register_cities_growth_callbacks(app)
    
    # Register combined benchmark dropdown callbacks (countries + regions in one dropdown)
    register_combined_benchmark_options_callback(app, 'slums-combined-benchmark-selector', default_regional_codes=['SSA'])
    register_combined_benchmark_options_callback(app, 'urbanization-rate-combined-benchmark-selector', default_regional_codes=['SSA'])
    register_combined_benchmark_options_callback(app, 'urban-density-combined-benchmark-selector', default_regional_codes=['SSA'])
    register_combined_benchmark_options_callback(app, 'electricity-combined-benchmark-selector', default_regional_codes=['SSA'])
    
    # Register separate country benchmark callback for GDP vs Urbanization
    register_country_benchmark_options_callback(app, 'gdp-vs-urbanization-country-benchmark-selector')
    
    
    # Callback to filter country dropdown options based on active subtab
    @app.callback(
        Output('main-country-filter', 'options', allow_duplicate=True),
        Input('urbanization-subtabs', 'active_tab'),
        prevent_initial_call=True
    )
    def update_country_filter_options_urbanization(urbanization_subtab):
        """Update country filter options for urbanization tabs - hide regional aggregates for Cities Distribution/Evolution/Growth Rate"""
        try:
            # Get individual countries (without regional aggregates)
            countries = get_subsaharan_countries()
            
            # Sort countries alphabetically by name
            countries = sorted(countries, key=lambda x: x['name'])
            
            # For Cities Distribution, Cities Evolution, Cities Growth Rate, and Cities Growth, only show individual countries
            if urbanization_subtab in ['cities-distribution', 'cities-evolution', 'cities-growth-rate', 'cities-growth']:
                return [{'label': country['name'], 'value': country['code']} for country in countries]
            else:
                # For other subtabs, include regional aggregates
                regional_options = [
                    {'label': 'Sub-Saharan Africa', 'value': 'SSA'},
                    {'label': 'Eastern & Southern Africa', 'value': 'AFE'},
                    {'label': 'Western & Central Africa', 'value': 'AFW'}
                ]
                all_options = [{'label': country['name'], 'value': country['code']} for country in countries]
                all_options.extend(regional_options)
                return all_options
                
        except Exception as e:
            print(f"Error updating country filter options for urbanization: {str(e)}")
            # Fallback to individual countries only
            countries = get_subsaharan_countries()
            countries = sorted(countries, key=lambda x: x['name'])
            return [{'label': country['name'], 'value': country['code']} for country in countries]
    
    # Main chart container callback (orchestrates which chart to show)
    @app.callback(
        Output('urbanization-chart-container', 'children'),
        [Input('urbanization-subtabs', 'active_tab'),
         Input('main-country-filter', 'value')]
    )
    def render_urbanization_chart(active_subtab, selected_country):
        """Render different urbanization charts based on selected subtab"""
        
        # Load indicator notes
        notes_dict = load_urbanization_indicators_notes_dict()
        
        if active_subtab == 'urban-population-projections':
            return html.Div([
                # Radio button to toggle between absolute values and growth rate
                html.Div([
                    html.Label('Display Mode:', className='filter-label'),
                    dcc.RadioItems(
                        id='urban-population-projections-mode',
                        options=[
                            {'label': 'Absolute Values', 'value': 'absolute'},
                            {'label': 'Growth Rate', 'value': 'growth_rate'}
                        ],
                        value='absolute',
                        className='radio-buttons',
                        labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
                    )
                ], className='filter-container'),
                # Chart
                dcc.Graph(id="urban-population-projections-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "UN DESA (World Population Prospects & World Urbanization Prospects).", html.Br(), html.B("Note:"), " Uncertainty bands show 95% and 80% confidence intervals for future projections. The 2025 value corresponds to an estimate based on UN DESA datasets."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('urban-population-projections-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'urbanization-rate':
            return html.Div([
                # Combined benchmark selector
                create_combined_benchmark_selector(
                    dropdown_id='urbanization-rate-combined-benchmark-selector',
                    default_regional_codes=['SSA']
                ),
                # Chart
                dcc.Graph(id="urbanization-rate-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "UN DESA World Urbanization Prospects.", html.Br(), html.B("Note:"), " Percentage of population living in urban areas. Shows historical trends and future projections of urbanization levels. The 2025 value corresponds to an estimate based on UN DESA datasets."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('urbanization-rate-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'urban-density':
            return html.Div([
                # Combined benchmark selector
                create_combined_benchmark_selector(
                    dropdown_id='urban-density-combined-benchmark-selector',
                    default_regional_codes=['SSA']
                ),
                # Chart
                dcc.Graph(id="urban-density-chart"),
                # Indicator note
                html.Div([
                    html.P([
                        html.B("Data Source: "), "Africapolis & GHSL 2023 (processed).",
                        html.Br(),
                        html.B("Note:"), " Computed as total built-up area divided by population in cities as defined by Africapolis. Regional benchmarks aggregate populations and built-up areas before calculating per capita values."
                    ], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('urban-density-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'urban-population-slums':
            slums_note = notes_dict.get('EN.POP.SLUM.UR.ZS', '')
            return html.Div([
                # Combined benchmark selector
                create_combined_benchmark_selector(
                    dropdown_id='slums-combined-benchmark-selector',
                    default_regional_codes=[]
                ),
                # Chart
                dcc.Graph(id="urban-population-slums-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "World Bank World Development Indicators (WDI).", html.Br(), html.B("Note:"), f" {slums_note}"], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('urban-population-slums-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'access-to-drinking-water':
            return html.Div([
                # Chart
                dcc.Graph(id="access-to-drinking-water-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "WHO/UNICEF Joint Monitoring Programme (JMP) for Water Supply, Sanitation and Hygiene.", html.Br(), html.B("Note:"),
                            html.Br(), html.B("At Least Basic: "), "Drinking water from an improved source (piped water, boreholes or tubewells, protected dug wells, protected springs, rainwater, and packaged or delivered water), that is accessible on premises, available when needed and free from faecal and priority chemical contamination, or can be collected within 30 minutes.",
                            html.Br(), html.B("Limited: "), "Drinking water from an improved source, for which collection time exceeds 30 minutes for a round trip, including queuing.",
                            html.Br(), html.B("Unimproved: "), "Drinking water from an unprotected dug well or unprotected spring.",
                            html.Br(), html.B("Surface Water: "), "Drinking water directly from a river, dam, lake, pond, stream, canal or irrigation canal."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('access-to-drinking-water-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'access-to-sanitation':
            return html.Div([
                # Chart
                dcc.Graph(id="access-to-sanitation-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "WHO/UNICEF Joint Monitoring Programme (JMP) for Water Supply, Sanitation and Hygiene.", html.Br(), html.B("Note:"),
                            html.Br(), html.B("At Least Basic: "), "Use of improved facilities that are not shared with other households.",
                            html.Br(), html.B("Limited: "), "Use of improved facilities shared between two or more households.",
                            html.Br(), html.B("Unimproved: "), "Use of pit latrines without a slab or platform, hanging latrines or bucket latrines.",
                            html.Br(), html.B("Open Defecation: "), "Disposal of human faeces in fields, forests, bushes, open bodies of water, beaches and other open spaces or with solid waste."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('access-to-sanitation-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'access-to-electricity-urban':
            electricity_note = notes_dict.get('EG.ELC.ACCS.UR.ZS', '')
            return html.Div([
                # Combined benchmark selector
                create_combined_benchmark_selector(
                    dropdown_id='electricity-combined-benchmark-selector',
                    default_regional_codes=[]
                ),
                # Chart
                dcc.Graph(id="access-to-electricity-urban-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "World Bank World Development Indicators (WDI).", html.Br(), html.B("Note:"), f" {electricity_note}"], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('access-to-electricity-urban-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'gdp-vs-urbanization':
            return html.Div([
                # Benchmark selectors (global and country benchmarks)
                *create_benchmark_selectors(
                    regional_id='gdp-vs-urbanization-benchmark-selector',
                    country_id='gdp-vs-urbanization-country-benchmark-selector',
                    global_id='gdp-vs-urbanization-global-benchmark-selector',
                    include_regional=False,
                    include_country=True,
                    include_global=True,
                    exclude_from_default=['AFE', 'AFW']  # Exclude subregions from default selection
                ),
                # Chart
                dcc.Graph(id="gdp-vs-urbanization-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "World Bank World Development Indicators.", html.Br(), html.B("Note:"), " Urban population refers to people living in urban areas as defined by national statistical offices. The data are collected by the UN Population Division. Cross-country comparisons should be made with caution since this data does not rely on an internationally harmonized definition of urban areas. Aggregation of urban and rural population may not add up to total population because of different country coverage. Gross domestic product (GDP) is expressed in constant international dollars, converted by purchasing power parities (PPPs). PPPs account for the different price levels across countries and thus PPP-based comparisons of economic output are more appropriate for comparing the output of economies and the average material well-being of their inhabitants than exchange-rate based comparisons."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('gdp-vs-urbanization-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'cities-distribution':
            return html.Div([
                # Year filter (slider)
                html.Div([
                    html.Label("Year:", className="filter-label"),
                    dcc.Slider(
                        id='cities-distribution-year-filter',
                        min=2020,
                        max=2035,
                        step=5,
                        value=2025,
                        marks={
                            2020: {'label': '2020', 'style': {'color': '#374151'}},
                            2025: {'label': '2025', 'style': {'color': '#374151'}},
                            2030: {'label': '2030', 'style': {'color': '#374151'}},
                            2035: {'label': '2035', 'style': {'color': '#374151'}}
                        }
                    )
                ], className="filter-container"),
                # Plotly treemap chart
                dcc.Graph(id="cities-distribution-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "UN DESA World Urbanization Prospects 2018.", html.Br(), html.B("Note:"), " Distribution of urban population across city size categories for selected year."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('cities-distribution-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'cities-evolution':
            return html.Div([
                # Chart
                dcc.Graph(id="cities-evolution-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "UN DESA World Urbanization Prospects 2018.", html.Br(), html.B("Note:"), " Urban population evolution showing individual cities stacked and colored by size category."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('cities-evolution-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'cities-growth-rate':
            return html.Div([
                # Chart
                dcc.Graph(id="cities-growth-rate-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "Africapolis & GHSL 2023.", html.Br(), html.B("Note:"), " Scatterplot showing the relationship between population CAGR (Compound Annual Growth Rate) and built-up area CAGR for cities between 2000 and 2020. Points above the diagonal line (y=x) indicate cities where built-up area expanded faster than population, while points below indicate population growth outpaced built-up growth rate."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('cities-growth-rate-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'cities-growth':
            return html.Div([
                # Metric selector (Built-up vs Population)
                html.Div([
                    html.Div([
                        html.Label('Metric:', className='filter-label'),
                        dcc.RadioItems(
                            id='cities-growth-metric-selector',
                            options=[
                                {'label': 'Built-up', 'value': 'BU'},
                                {'label': 'Population', 'value': 'POP'}
                            ],
                            value='BU',
                            className='radio-buttons',
                            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
                        )
                    ], className='cities-growth-metric-group'),
                    dbc.Button("📍 Where are these cities?", id="show-city-map-button", color="info", className="download-data-button")
                ], className='cities-growth-metric-container'),
                # City selector
                html.Div([
                    html.Label('Cities:', className='dropdown-label'),
                    html.Div([
                        dcc.Dropdown(
                            id='cities-growth-city-selector',
                            options=[],
                            value=[],
                            multi=True,
                            placeholder='Select cities...',
                            className='city-dropdown'
                        )
                    ], className='dropdown-group')
                ], className='city-selector-container'),
                # Chart
                dcc.Graph(id="cities-growth-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "Africapolis & GHSL 2023.", html.Br(), html.B("Note:"), " Shows absolute values in 2020 and Compound Annual Growth Rate (CAGR) between 2000 and 2020 for selected cities."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('cities-growth-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container"),
                # City Map Modal
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("City Locations")),
                    dbc.ModalBody([
                        html.Div(id="city-map-container", style={'height': '70vh'})
                    ]),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close-city-map-button", className="ml-auto")
                    )
                ], id="city-map-modal", size="xl", is_open=False)
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")