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
    
    # Theme toggle callback
    @app.callback(
        Output('theme-store', 'data'),
        Input('theme-toggle', 'value')
    )
    def toggle_theme(dark_mode):
        """Toggle between light and dark themes"""
        return {'theme': 'dark' if dark_mode else 'light'}
    
    # Apply theme styles callback
    @app.callback(
        [
            Output('main-container', 'className'),
            Output('main-title', 'style'),
            Output('header-hr', 'style'),
            Output('footer-hr', 'style'),
            Output('footer-text', 'className')
        ],
        Input('theme-store', 'data')
    )
    def apply_theme_styles(theme_data):
        """Apply theme-specific styles to main elements"""
        is_dark = theme_data.get('theme') == 'dark'
        
        if is_dark:
            return (
                'dark-theme',
                {'color': '#f8f9fa', 'font-weight': 'bold'},
                {'border-color': '#495057'},
                {'border-color': '#495057'},
                'text-center text-light small'
            )
        else:
            return (
                '',
                {'color': '#2c3e50', 'font-weight': 'bold'},
                {},
                {},
                'text-center text-muted small'
            )
    
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
                        html.Label("Select Countries (max 5):"),
                        dcc.Dropdown(
                            id="comparison-country-dropdown",
                            multi=True,
                            placeholder="Select countries to compare...",
                            maxItems=5
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