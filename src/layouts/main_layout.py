"""
Main layout for the Sub-Saharan Africa DRM Dashboard
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.data_loader import get_subsaharan_countries

def create_main_layout():
    """Create the main dashboard layout"""
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        html.H1(
                            "Sub-Saharan Africa Disaster Risk Management Dashboard",
                            className="text-center mb-4",
                            style={'color': '#2c3e50', 'font-weight': 'bold'}
                        ),
                    ], width=12),

                ]),
                html.Hr(),
            ], width=12)
        ]),
        
        # Main country filter (applies to all tabs)
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Label("Select Country:", className="fw-bold", style={'color': '#2c3e50'}),
                            ], width=3),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="main-country-filter",
                                    options=[
                                        {'label': country['name'], 'value': country['code']}
                                        for country in get_subsaharan_countries()
                                    ],
                                    value=get_subsaharan_countries()[0]['code'],  # Default to first country
                                    placeholder="Select a country...",
                                    className="mb-0"
                                )
                            ], width=9)
                        ], align="center")
                    ])
                ], className="mb-3", style={'backgroundColor': '#f8f9fa', 'border': '1px solid #dee2e6'})
            ], width=12)
        ]),
        
        # Navigation tabs
        dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(label="Historical Disasters", tab_id="disasters"),
                    dbc.Tab(label="Urbanization Trends", tab_id="urbanization"),
                    dbc.Tab(label="Flood Risk Assessment", tab_id="flood_risk"),
                    dbc.Tab(label="Country Comparison", tab_id="comparison"),
                ], id="main-tabs", active_tab="disasters"),
            ], width=12)
        ], className="mb-4"),
        
        # Main content area
        dbc.Row([
            dbc.Col([
                html.Div(id="tab-content")
            ], width=12)
        ]),
        
        # Footer
        dbc.Row([
            dbc.Col([
                html.Hr(),
                html.P(
                    "World Bank Disaster Risk Management - Sub-Saharan Africa Dashboard",
                    className="text-center text-muted small"
                )
            ], width=12)
        ], className="mt-5")
        
    ], fluid=True)


def create_disaster_tab_content():
    """Create content for the Historical Disasters tab"""
    return dbc.Container([
        dbc.Row([
            # Filters
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Filters", className="card-title"),
                        html.Label("Disaster Type:"),
                        dcc.Dropdown(
                            id="disaster-type-dropdown",
                            multi=True,
                            placeholder="Select disaster types..."
                        ),
                        html.Br(),
                        html.Label("Year Range:"),
                        dcc.RangeSlider(
                            id="disaster-year-slider",
                            marks={i: str(i) for i in range(1975, 2030, 10)},
                            min=1975,
                            max=2025,
                            step=1,
                            value=[2000, 2025]
                        )
                    ])
                ])
            ], width=3),
            
            # Main visualizations
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="disaster-timeline-chart")
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="disaster-map")
                    ], width=8),
                    dbc.Col([
                        dcc.Graph(id="disaster-impact-chart")
                    ], width=4)
                ])
            ], width=9)
        ])
    ])


def create_urbanization_tab_content():
    """Create content for the Urbanization Trends tab"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Urban Development Indicators", className="card-title"),
                        html.Label("Select Indicator:"),
                        dcc.Dropdown(
                            id="urban-indicator-dropdown",
                            options=[
                                {'label': 'Urban Population %', 'value': 'urban_pop_pct'},
                                {'label': 'Urban Growth Rate', 'value': 'urban_growth'},
                                {'label': 'Population Density', 'value': 'pop_density'},
                            ],
                            value='urban_pop_pct'
                        )
                    ])
                ])
            ], width=3),
            
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="urbanization-trend-chart")
                    ], width=12)
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="urbanization-map")
                    ], width=12)
                ])
            ], width=9)
        ])
    ])


def create_flood_risk_tab_content():
    """Create content for the Flood Risk Assessment tab"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Flood Risk Parameters", className="card-title"),
                        html.Label("Risk Level:"),
                        dcc.Dropdown(
                            id="flood-risk-level",
                            options=[
                                {'label': 'Low', 'value': 'low'},
                                {'label': 'Medium', 'value': 'medium'},
                                {'label': 'High', 'value': 'high'},
                                {'label': 'Very High', 'value': 'very_high'}
                            ],
                            multi=True,
                            value=['medium', 'high', 'very_high']
                        ),
                        html.Br(),
                        html.Label("Scenario:"),
                        dcc.RadioItems(
                            id="flood-scenario",
                            options=[
                                {'label': 'Current', 'value': 'current'},
                                {'label': '2030 Projection', 'value': '2030'},
                                {'label': '2050 Projection', 'value': '2050'}
                            ],
                            value='current'
                        )
                    ])
                ])
            ], width=3),
            
            dbc.Col([
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="flood-risk-map")
                    ], width=8),
                    dbc.Col([
                        dcc.Graph(id="flood-risk-stats")
                    ], width=4)
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(id="flood-vulnerability-chart")
                    ], width=12)
                ])
            ], width=9)
        ])
    ])