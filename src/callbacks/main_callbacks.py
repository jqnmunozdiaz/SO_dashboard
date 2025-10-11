"""
Main callback controller that handles tab switching and content rendering
"""

from dash import Input, Output, html, clientside_callback, ClientsideFunction
from src.layouts.main_layout import (
    create_disaster_tab_content,
    create_urbanization_tab_content,
    create_flood_risk_tab_content
)


def register_main_callbacks(app):
    """Register main navigation callbacks"""
    
    @app.callback(
        Output('tab-content', 'children'),
        Input('main-tabs', 'active_tab')
    )
    def render_tab_content(active_tab):
        """Render content based on active tab"""
        
        if active_tab == 'disasters':
            return create_disaster_tab_content()
        elif active_tab == 'urbanization':
            return create_urbanization_tab_content()
        elif active_tab == 'flood_risk':
            return create_flood_risk_tab_content()
        elif active_tab == 'comparison':
            return create_comparison_tab_content()
        else:
            return html.Div([
                html.H3("Welcome to the Sub-Saharan Africa DRM Dashboard"),
                html.P("Select a tab above to begin exploring the data.")
            ])


def create_comparison_tab_content():
    """Create content for the Country Comparison tab"""
    import dash_bootstrap_components as dbc
    from dash import dcc, html
    
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Comparison Settings", className="card-title"),
                        html.P("Use the main country filter above to select the primary country for comparison.", 
                               className="text-muted small"),
                        html.Label("Additional Countries for Comparison:"),
                        dcc.Dropdown(
                            id="comparison-additional-countries",
                            multi=True,
                            placeholder="Select additional countries to compare...",
                            maxItems=4
                        ),
                        html.Br(),
                        html.Label("Comparison Metrics:"),
                        dcc.Checklist(
                            id="comparison-metrics",
                            options=[
                                {'label': 'Disaster Frequency', 'value': 'disaster_freq'},
                                {'label': 'Population at Risk', 'value': 'pop_risk'},
                                {'label': 'Economic Impact', 'value': 'economic_impact'},
                                {'label': 'Urban Growth Rate', 'value': 'urban_growth'},
                                {'label': 'Flood Risk Level', 'value': 'flood_risk'}
                            ],
                            value=['disaster_freq', 'pop_risk', 'flood_risk']
                        ),
                        html.Br(),
                        html.Label("Chart Type:"),
                        dcc.RadioItems(
                            id="comparison-chart-type",
                            options=[
                                {'label': 'Bar Chart', 'value': 'bar'},
                                {'label': 'Radar Chart', 'value': 'radar'},
                                {'label': 'Scatter Plot', 'value': 'scatter'}
                            ],
                            value='bar'
                        )
                    ])
                ])
            ], width=3),
            
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="comparison-main-chart")
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        html.Div(id="comparison-summary-table")
                    ], width=12)
                ])
            ], width=9)
        ])
    ])