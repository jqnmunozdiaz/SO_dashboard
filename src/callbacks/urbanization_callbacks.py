"""
Main urbanization callbacks orchestrator
Coordinates all urbanization-related visualization callbacks
"""

from dash import Input, Output, dcc, html

# Import individual callback modules
from .urbanization.Urban_Population_Living_in_Slums_callbacks import register_urban_population_living_in_slums_callbacks
from .urbanization.Access_to_Electricity_Urban_callbacks import register_access_to_electricity_urban_callbacks
from .urbanization.Urban_Population_Projections_callbacks import register_urban_population_projections_callbacks
from .urbanization.Urbanization_Rate_callbacks import register_urbanization_rate_callbacks
from .urbanization.GDP_vs_Urbanization_callbacks import register_gdp_vs_urbanization_callbacks
from .urbanization.Cities_Distribution_callbacks import register_cities_distribution_callbacks
from .urbanization.Cities_Evolution_callbacks import register_cities_evolution_callbacks
from .country_benchmark_callbacks import register_country_benchmark_options_callback, register_combined_benchmark_options_callback

try:
    from ..utils.benchmark_config import get_benchmark_options
    from ..utils.data_loader import load_urbanization_indicators_notes_dict
    from ..utils.ui_helpers import create_benchmark_selectors, create_combined_benchmark_selector, create_download_button, create_methodological_note_button
    from ..utils.country_utils import get_subsaharan_countries
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.benchmark_config import get_benchmark_options
    from src.utils.data_loader import load_urbanization_indicators_notes_dict
    from src.utils.ui_helpers import create_benchmark_selectors, create_combined_benchmark_selector, create_download_button, create_methodological_note_button
    from src.utils.country_utils import get_subsaharan_countries


def register_callbacks(app):
    """Register all urbanization-related callbacks"""
    
    # Register individual callback modules
    register_urban_population_living_in_slums_callbacks(app)
    register_access_to_electricity_urban_callbacks(app)
    register_urban_population_projections_callbacks(app)
    register_urbanization_rate_callbacks(app)
    register_gdp_vs_urbanization_callbacks(app)
    register_cities_distribution_callbacks(app)
    register_cities_evolution_callbacks(app)
    
    # Register combined benchmark dropdown callbacks (countries + regions in one dropdown)
    register_combined_benchmark_options_callback(app, 'slums-combined-benchmark-selector')
    register_combined_benchmark_options_callback(app, 'urbanization-rate-combined-benchmark-selector')
    register_combined_benchmark_options_callback(app, 'electricity-combined-benchmark-selector')
    
    # Register separate country benchmark callback for GDP vs Urbanization
    register_country_benchmark_options_callback(app, 'gdp-vs-urbanization-country-benchmark-selector')
    
    # Callback to filter country dropdown options based on active subtab
    @app.callback(
        Output('main-country-filter', 'options'),
        Input('urbanization-subtabs', 'active_tab')
    )
    def update_country_filter_options(active_subtab):
        """Update country filter options - hide regional aggregates for Cities Distribution/Evolution"""
        try:
            # Get individual countries (without regional aggregates)
            countries = get_subsaharan_countries()
            
            # Sort countries alphabetically by name
            countries = sorted(countries, key=lambda x: x['name'])
            
            # For Cities Distribution and Cities Evolution, only show individual countries
            if active_subtab in ['cities-distribution', 'cities-evolution']:
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
            print(f"Error updating country filter options: {str(e)}")
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
                # Chart
                dcc.Graph(id="urban-population-projections-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "UN DESA (World Population Prospects & World Urbanization Prospects).", html.Br(), html.B("Note:"), " Uncertainty bands show 95% and 80% confidence intervals for future projections."], className="indicator-note"),
                    html.Div([
                        create_download_button('urban-population-projections-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'urbanization-rate':
            return html.Div([
                # Combined benchmark selector
                create_combined_benchmark_selector(
                    dropdown_id='urbanization-rate-combined-benchmark-selector',
                    default_regional_codes=[]
                ),
                # Chart
                dcc.Graph(id="urbanization-rate-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "UN DESA World Urbanization Prospects.", html.Br(), html.B("Note:"), " Percentage of population living in urban areas. Shows historical trends and future projections of urbanization levels."], className="indicator-note"),
                    html.Div([
                        create_download_button('urbanization-rate-download'),
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
                        create_download_button('urban-population-slums-download'),
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
                        create_download_button('access-to-electricity-urban-download'),
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
                    html.P([html.B("Data Source: "), "World Bank World Development Indicators.", html.Br(), html.B("Note:"), " Urban population refers to people living in urban areas as defined by national statistical offices. The data are collected by the UN Population Division. Aggregation of urban and rural population may not add up to total population because of different country coverage. There is no consistent and universally accepted standard for distinguishing urban from rural areas. Therefore, cross-country comparisons should be made with caution. Gross domestic product (GDP) is expressed in constant international dollars, converted by purchasing power parities (PPPs). PPPs account for the different price levels across countries and thus PPP-based comparisons of economic output are more appropriate for comparing the output of economies and the average material well-being of their inhabitants than exchange-rate based comparisons."], className="indicator-note"),
                    html.Div([
                        create_download_button('gdp-vs-urbanization-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'cities-distribution':
            return html.Div([
                # Year filter (radio buttons)
                html.Div([
                    html.Label("Year:", className="filter-label"),
                    dcc.RadioItems(
                        id='cities-distribution-year-filter',
                        options=[
                            {'label': '2020', 'value': 2020},
                            {'label': '2025', 'value': 2025},
                            {'label': '2030', 'value': 2030},
                            {'label': '2035', 'value': 2035}
                        ],
                        value=2025,
                        inline=True,
                        className="year-radio-buttons"
                    )
                ], className="year-filter-container"),
                # Chart
                dcc.Graph(id="cities-distribution-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "UN DESA World Urbanization Prospects 2018.", html.Br(), html.B("Note:"), " Distribution of urban population across city size categories for selected year."], className="indicator-note"),
                    html.Div([
                        create_download_button('cities-distribution-download'),
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
                        create_download_button('cities-evolution-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")