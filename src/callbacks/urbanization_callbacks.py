"""
Main urbanization callbacks orchestrator
Coordinates all urbanization-related visualization callbacks
"""

from dash import Input, Output, dcc, html

# Import individual callback modules
from .urbanization.Urban_Population_Living_in_Slums_callbacks import register_urban_population_living_in_slums_callbacks


def register_callbacks(app):
    """Register all urbanization-related callbacks"""
    
    # Register individual callback modules
    register_urban_population_living_in_slums_callbacks(app)
    
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
                            options=[
                                {'label': 'Sub-Saharan Africa', 'value': 'SSA'},
                                {'label': 'Africa Eastern and Southern', 'value': 'AFE'},
                                {'label': 'Africa Western and Central', 'value': 'AFW'}
                            ],
                            value=[],  # No benchmarks selected by default
                            className="benchmark-checkboxes",
                            inline=True
                        )
                    ], className="checkbox-group")
                ], className="benchmark-selector-container"),
                # Chart
                dcc.Graph(id="urban-population-slums-chart")
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")