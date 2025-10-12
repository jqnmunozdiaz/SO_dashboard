"""
Main callback controller that handles tab switching and content rendering
"""

from dash import Input, Output, html, clientside_callback, ClientsideFunction
from src.layouts.world_bank_layout import (
    create_world_bank_disaster_tab_content,
    create_world_bank_urbanization_tab_content,
    create_world_bank_flood_risk_tab_content
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
            return create_world_bank_disaster_tab_content()
        elif active_tab == 'urbanization':
            return create_world_bank_urbanization_tab_content()
        elif active_tab == 'flood_risk':
            return create_world_bank_flood_risk_tab_content()
        elif active_tab == 'comparison':
            return create_comparison_tab_content()
        else:
            return html.Div([
                html.H3("Welcome to the Sub-Saharan Africa DRM Dashboard"),
                html.P("Select a tab above to begin exploring the data.")
            ])


def create_comparison_tab_content():
    """Create World Bank-styled content for the Country Comparison tab matching Review_CatDDOs"""
    import dash_bootstrap_components as dbc
    from dash import dcc, html
    
    return html.Div([
        html.Div([
            # Filter controls section
            html.Div([
                html.H3(
                    "Comparison Settings",
                    style={
                        'font-size': '1.125rem',
                        'font-weight': '600',
                        'color': '#374151',
                        'margin-bottom': '1rem'
                    }
                ),
                html.P(
                    "Use the main country filter above to select the primary country for comparison.",
                    style={
                        'font-size': '0.875rem',
                        'color': '#6b7280',
                        'margin-bottom': '1.5rem'
                    }
                ),
                html.Div([
                    html.Label(
                        "Additional Countries for Comparison:",
                        style={
                            'display': 'block',
                            'font-size': '0.875rem',
                            'font-weight': '500',
                            'color': '#374151',
                            'margin-bottom': '0.5rem'
                        }
                    ),
                    dcc.Dropdown(
                        id="comparison-additional-countries",
                        multi=True,
                        placeholder="Select additional countries to compare...",
                        maxItems=4,
                        style={'margin-bottom': '1.5rem'}
                    ),
                    html.Label(
                        "Comparison Metrics:",
                        style={
                            'display': 'block',
                            'font-size': '0.875rem',
                            'font-weight': '500',
                            'color': '#374151',
                            'margin-bottom': '0.5rem'
                        }
                    ),
                    dcc.Checklist(
                        id="comparison-metrics",
                        options=[
                            {'label': 'Disaster Frequency', 'value': 'disaster_freq'},
                            {'label': 'Population at Risk', 'value': 'pop_risk'},
                            {'label': 'Economic Impact', 'value': 'economic_impact'},
                            {'label': 'Urban Growth Rate', 'value': 'urban_growth'},
                            {'label': 'Flood Risk Level', 'value': 'flood_risk'}
                        ],
                        value=['disaster_freq', 'pop_risk', 'flood_risk'],
                        style={'margin-bottom': '1.5rem'}
                    ),
                    html.Label(
                        "Chart Type:",
                        style={
                            'display': 'block',
                            'font-size': '0.875rem',
                            'font-weight': '500',
                            'color': '#374151',
                            'margin-bottom': '0.5rem'
                        }
                    ),
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
            ], style={
                'background': 'white',
                'padding': '1.5rem',
                'border-radius': '0.5rem',
                'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                'border': '1px solid #e5e7eb',
                'margin-bottom': '1.5rem'
            }),
            
            # Charts section
            html.Div([
                # Main comparison chart
                html.Div([
                    dcc.Graph(id="comparison-main-chart")
                ], style={
                    'background': 'white',
                    'padding': '1.5rem',
                    'border-radius': '0.5rem',
                    'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                    'border': '1px solid #e5e7eb',
                    'margin-bottom': '1.5rem'
                }),
                
                # Summary table
                html.Div([
                    html.Div(id="comparison-summary-table")
                ], style={
                    'background': 'white',
                    'padding': '1.5rem',
                    'border-radius': '0.5rem',
                    'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                    'border': '1px solid #e5e7eb'
                })
            ])
        ], style={
            'max-width': '80rem',
            'margin': '0 auto',
            'padding': '1.5rem'
        })
    ], style={
        'background': '#f9fafb',
        'min-height': 'calc(100vh - 300px)'
    })