"""
Main disaster callbacks orchestrator
Coordinates all disaster-related visualization callbacks
"""

from dash import Input, Output, dcc, html

# Import individual callback modules
from .disaster_frequency_callbacks import register_disaster_frequency_callbacks
from .disaster_timeline_callbacks import register_disaster_timeline_callbacks
from .disaster_affected_callbacks import register_disaster_affected_callbacks


def register_callbacks(app):
    """Register all disaster-related callbacks"""
    
    # Register individual callback modules
    register_disaster_frequency_callbacks(app)
    register_disaster_timeline_callbacks(app)
    register_disaster_affected_callbacks(app)
    
    # Main chart container callback (orchestrates which chart to show)
    @app.callback(
        Output('disaster-chart-container', 'children'),
        [Input('disaster-subtabs', 'active_tab'),
         Input('main-country-filter', 'value')]
    )
    def render_disaster_chart(active_subtab, selected_country):
        """Render different disaster charts based on selected subtab"""
        if active_subtab == 'disaster-frequency':
            return html.Div([
                dcc.Graph(id="disaster-frequency-chart")
            ], className="chart-container")
        elif active_subtab == 'disaster-timeline':
            return html.Div([
                dcc.Graph(id="disaster-timeline-chart")
            ], className="chart-container")
        elif active_subtab == 'disaster-affected':
            return html.Div([
                dcc.Graph(id="disaster-affected-chart")
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")