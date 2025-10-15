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
from .country_benchmark_callbacks import register_country_benchmark_options_callback

try:
    from ..utils.benchmark_config import get_benchmark_options
    from ..utils.data_loader import load_urbanization_indicators_notes_dict
    from ..utils.ui_helpers import create_benchmark_selectors
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.benchmark_config import get_benchmark_options
    from src.utils.data_loader import load_urbanization_indicators_notes_dict
    from src.utils.ui_helpers import create_benchmark_selectors


def register_callbacks(app):
    """Register all urbanization-related callbacks"""
    
    # Register individual callback modules
    register_urban_population_living_in_slums_callbacks(app)
    register_access_to_electricity_urban_callbacks(app)
    register_urban_population_projections_callbacks(app)
    register_urbanization_rate_callbacks(app)
    register_gdp_vs_urbanization_callbacks(app)
    
    # Register country benchmark dropdown callbacks
    register_country_benchmark_options_callback(app, 'slums-country-benchmark-selector')
    register_country_benchmark_options_callback(app, 'urbanization-rate-country-benchmark-selector')
    register_country_benchmark_options_callback(app, 'electricity-country-benchmark-selector')
    register_country_benchmark_options_callback(app, 'gdp-vs-urbanization-country-benchmark-selector')
    
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
                    html.P([html.B("Data Source: "), "UN DESA (World Population Prospects & World Urbanization Prospects).", html.Br(), html.B("Note:"), " Uncertainty bands show 95% and 80% confidence intervals for future projections."], className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'urbanization-rate':
            return html.Div([
                # Benchmark selectors
                *create_benchmark_selectors(
                    regional_id='urbanization-rate-benchmark-selector',
                    country_id='urbanization-rate-country-benchmark-selector',
                    include_regional=True,
                    include_country=True
                ),
                # Chart
                dcc.Graph(id="urbanization-rate-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "UN DESA World Urbanization Prospects.", html.Br(), html.B("Note:"), " Percentage of population living in urban areas. Shows historical trends and future projections of urbanization levels."], className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'urban-population-slums':
            slums_note = notes_dict.get('EN.POP.SLUM.UR.ZS', '')
            return html.Div([
                # Benchmark selectors
                *create_benchmark_selectors(
                    regional_id='slums-benchmark-selector',
                    country_id='slums-country-benchmark-selector',
                    include_regional=True,
                    include_country=True
                ),
                # Chart
                dcc.Graph(id="urban-population-slums-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "World Bank World Development Indicators (EN.POP.SLUM.UR.ZS).", html.Br(), html.B("Note:"), f" {slums_note}"], className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'access-to-electricity-urban':
            electricity_note = notes_dict.get('EG.ELC.ACCS.UR.ZS', '')
            return html.Div([
                # Benchmark selectors
                *create_benchmark_selectors(
                    regional_id='electricity-benchmark-selector',
                    country_id='electricity-country-benchmark-selector',
                    include_regional=True,
                    include_country=True
                ),
                # Chart
                dcc.Graph(id="access-to-electricity-urban-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "World Bank World Development Indicators (EG.ELC.ACCS.UR.ZS).", html.Br(), html.B("Note:"), f" {electricity_note}"], className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'gdp-vs-urbanization':
            return html.Div([
                # Benchmark selectors (only country benchmarks for this chart)
                *create_benchmark_selectors(
                    regional_id='gdp-vs-urbanization-benchmark-selector',
                    country_id='gdp-vs-urbanization-country-benchmark-selector',
                    include_regional=False,  # This chart doesn't have regional benchmarks
                    include_country=True
                ),
                # Chart
                dcc.Graph(id="gdp-vs-urbanization-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "World Bank World Development Indicators.", html.Br(), html.B("Note:"), " Urban population refers to people living in urban areas as defined by national statistical offices. The data are collected by the UN Population Division. Aggregation of urban and rural population may not add up to total population because of different country coverage. There is no consistent and universally accepted standard for distinguishing urban from rural areas. Therefore, cross-country comparisons should be made with caution. Gross domestic product (GDP) is expressed in constant international dollars, converted by purchasing power parities (PPPs). PPPs account for the different price levels across countries and thus PPP-based comparisons of economic output are more appropriate for comparing the output of economies and the average material well-being of their inhabitants than exchange-rate based comparisons."], className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")