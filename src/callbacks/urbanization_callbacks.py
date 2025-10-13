"""
Main urbanization callbacks orchestrator
Coordinates all urbanization-related visualization callbacks
"""

from dash import Input, Output, dcc, html

# Import individual callback modules
from .urbanization.Urban_Population_Living_in_Slums_callbacks import register_urban_population_living_in_slums_callbacks
from .urbanization.Access_to_Electricity_Urban_callbacks import register_access_to_electricity_urban_callbacks

try:
    from ..utils.benchmark_config import get_benchmark_options
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.benchmark_config import get_benchmark_options


def register_callbacks(app):
    """Register all urbanization-related callbacks"""
    
    # Register individual callback modules
    register_urban_population_living_in_slums_callbacks(app)
    register_access_to_electricity_urban_callbacks(app)
    
    # Main chart container callback (orchestrates which chart to show)
    @app.callback(
        Output('urbanization-chart-container', 'children'),
        [Input('urbanization-subtabs', 'active_tab'),
         Input('main-country-filter', 'value')]
    )
    def render_urbanization_chart(active_subtab, selected_country):
        """Render different urbanization charts based on selected subtab"""
        if active_subtab == 'urban-population-slums':
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
                # Chart
                dcc.Graph(id="urban-population-slums-chart")
            ], className="chart-container")
        elif active_subtab == 'access-to-electricity-urban':
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
                # Chart
                dcc.Graph(id="access-to-electricity-urban-chart")
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")