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
    from ..utils.data_loader import load_urbanization_indicators_notes_dict, get_subsaharan_countries
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.benchmark_config import get_benchmark_options
    from src.utils.data_loader import load_urbanization_indicators_notes_dict, get_subsaharan_countries
    from src.utils.country_utils import load_subsaharan_countries_dict


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
                    html.P("Urban and rural population projections from UN DESA World Population Prospects and World Urbanization Prospects. Uncertainty bands show 95% and 80% confidence intervals for future projections.", className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'urbanization-rate':
            return html.Div([
                # Benchmark selection checkboxes
                html.Div([
                    html.Label("Regional Benchmarks:", className="checkbox-label"),
                    html.Div([
                        dcc.Checklist(
                            id='urbanization-rate-benchmark-selector',
                            options=get_benchmark_options(),
                            value=[],  # No benchmarks selected by default
                            className="benchmark-checkboxes",
                            inline=True
                        )
                    ], className="checkbox-group")
                ], className="benchmark-selector-container"),
                # Country benchmark selection dropdown
                html.Div([
                    html.Label("Country Benchmarks:", className="dropdown-label"),
                    html.Div([
                        dcc.Dropdown(
                            id='urbanization-rate-country-benchmark-selector',
                            options=[],  # Will be populated by callback
                            value=[],
                            multi=True,
                            placeholder="Select countries to compare...",
                            className="country-benchmark-dropdown"
                        )
                    ], className="dropdown-group")
                ], className="country-benchmark-selector-container"),
                # Chart
                dcc.Graph(id="urbanization-rate-chart"),
                # Indicator note
                html.Div([
                    html.P("Percentage of population living in urban areas from UN DESA World Urbanization Prospects. Shows historical trends and future projections of urbanization levels.", className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'urban-population-slums':
            slums_note = notes_dict.get('EN.POP.SLUM.UR.ZS', '')
            return html.Div([
                # Benchmark selection checkboxes
                html.Div([
                    html.Label("Regional Benchmarks:", className="checkbox-label"),
                    html.Div([
                        dcc.Checklist(
                            id='slums-benchmark-selector',
                            options=get_benchmark_options(),
                            value=[],  # No benchmarks selected by default
                            className="benchmark-checkboxes",
                            inline=True
                        )
                    ], className="checkbox-group")
                ], className="benchmark-selector-container"),
                # Country benchmark selection dropdown
                html.Div([
                    html.Label("Country Benchmarks:", className="dropdown-label"),
                    html.Div([
                        dcc.Dropdown(
                            id='slums-country-benchmark-selector',
                            options=[],  # Will be populated by callback
                            value=[],
                            multi=True,
                            placeholder="Select countries to compare...",
                            className="country-benchmark-dropdown"
                        )
                    ], className="dropdown-group")
                ], className="country-benchmark-selector-container"),
                # Chart
                dcc.Graph(id="urban-population-slums-chart"),
                # Indicator note
                html.Div([
                    html.P(slums_note, className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'access-to-electricity-urban':
            electricity_note = notes_dict.get('EG.ELC.ACCS.UR.ZS', '')
            return html.Div([
                # Benchmark selection checkboxes
                html.Div([
                    html.Label("Regional Benchmarks:", className="checkbox-label"),
                    html.Div([
                        dcc.Checklist(
                            id='electricity-benchmark-selector',
                            options=get_benchmark_options(),
                            value=[],  # No benchmarks selected by default
                            className="benchmark-checkboxes",
                            inline=True
                        )
                    ], className="checkbox-group")
                ], className="benchmark-selector-container"),
                # Country benchmark selection dropdown
                html.Div([
                    html.Label("Country Benchmarks:", className="dropdown-label"),
                    html.Div([
                        dcc.Dropdown(
                            id='electricity-country-benchmark-selector',
                            options=[],  # Will be populated by callback
                            value=[],
                            multi=True,
                            placeholder="Select countries to compare...",
                            className="country-benchmark-dropdown"
                        )
                    ], className="dropdown-group")
                ], className="country-benchmark-selector-container"),
                # Chart
                dcc.Graph(id="access-to-electricity-urban-chart"),
                # Indicator note
                html.Div([
                    html.P(electricity_note, className="indicator-note")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'gdp-vs-urbanization':
            return html.Div([
                # Country benchmark selection dropdown
                html.Div([
                    html.Label("Country Benchmarks:", className="dropdown-label"),
                    html.Div([
                        dcc.Dropdown(
                            id='gdp-vs-urbanization-country-benchmark-selector',
                            options=[],  # Will be populated by callback
                            value=[],
                            multi=True,
                            placeholder="Select countries to compare...",
                            className="country-benchmark-dropdown"
                        )
                    ], className="dropdown-group")
                ], className="country-benchmark-selector-container"),
                # Chart
                dcc.Graph(id="gdp-vs-urbanization-chart"),
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")