"""
Main disaster callbacks orchestrator
Coordinates all disaster-related visualization callbacks organized in disaster subfolder
"""

from dash import Input, Output, dcc, html

# Import individual callback modules from disaster subfolder with clear naming
from .disaster.Frequency_by_Type_callbacks import setup_frequency_by_type_callbacks
from .disaster.Disasters_by_Year_callbacks import setup_disasters_by_year_callbacks
from .disaster.Total_Affected_Population_callbacks import setup_total_affected_population_callbacks
from .disaster.Total_Deaths_callbacks import setup_total_deaths_callbacks


def register_callbacks(app):
    """Register all disaster-related callbacks with organized structure"""
    
    # Register individual callback modules using clear function names
    setup_frequency_by_type_callbacks(app)
    setup_disasters_by_year_callbacks(app)
    setup_total_affected_population_callbacks(app)
    setup_total_deaths_callbacks(app)
    
    # Main chart container callback (orchestrates which chart to show based on subtab selection)
    @app.callback(
        Output('disaster-chart-container', 'children'),
        [Input('disaster-subtabs', 'active_tab'),
         Input('main-country-filter', 'value')]
    )
    def render_disaster_chart_by_subtab(active_subtab, selected_country):
        """Render different disaster charts based on selected subtab with clear chart mapping"""
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
        elif active_subtab == 'disaster-deaths':
            return html.Div([
                dcc.Graph(id="disaster-deaths-chart")
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")