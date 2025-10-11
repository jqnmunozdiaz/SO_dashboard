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
        # Header with gradient background
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1(
                        "Sub-Saharan Africa Disaster Risk Management Dashboard",
                        className="text-center mb-3",
                        style={
                            'color': 'white', 
                            'font-weight': '700',
                            'font-size': '2.5rem',
                            'text-shadow': '2px 2px 4px rgba(0,0,0,0.3)',
                            'margin': '0'
                        }
                    ),
                    html.P(
                        "Real-time insights and analytics for disaster preparedness and response",
                        className="text-center mb-0",
                        style={
                            'color': 'rgba(255,255,255,0.9)',
                            'font-size': '1.1rem',
                            'font-weight': '300'
                        }
                    )
                ], style={
                    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    'padding': '3rem 2rem',
                    'border-radius': '15px',
                    'margin-bottom': '2rem',
                    'box-shadow': '0 10px 30px rgba(0,0,0,0.1)'
                }),
            ], width=12)
        ]),
        
        # Main country filter with enhanced styling
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                html.Div([
                                    html.I(className="fas fa-globe-africa me-2", style={'color': '#667eea'}),
                                    html.Label("Select Country:", className="fw-bold mb-0", 
                                               style={'color': '#2c3e50', 'font-size': '1.1rem'})
                                ], className="d-flex align-items-center")
                            ], width=3),
                            dbc.Col([
                                dcc.Dropdown(
                                    id="main-country-filter",
                                    options=[
                                        {'label': country['name'], 'value': country['code']}
                                        for country in get_subsaharan_countries()
                                    ],
                                    value=get_subsaharan_countries()[0]['code'],
                                    placeholder="Select a country...",
                                    style={
                                        'border-radius': '8px',
                                        'box-shadow': '0 2px 4px rgba(0,0,0,0.1)'
                                    }
                                )
                            ], width=9)
                        ], align="center")
                    ], style={'padding': '1.5rem'})
                ], style={
                    'background': 'linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%)',
                    'border': 'none',
                    'border-radius': '12px',
                    'box-shadow': '0 8px 25px rgba(0,0,0,0.1)',
                    'margin-bottom': '2rem'
                })
            ], width=12)
        ]),
        
        # Navigation tabs with enhanced styling
        dbc.Row([
            dbc.Col([
                dbc.Tabs([
                    dbc.Tab(
                        label="📊 Historical Disasters",
                        tab_id="disasters",
                        tab_style={
                            'border-radius': '12px 12px 0 0',
                            'border': 'none',
                            'background': 'rgba(255, 255, 255, 0.7)',
                            'margin-right': '0.5rem',
                            'padding': '1rem 1.5rem'
                        },
                        active_tab_style={
                            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                            'color': 'white',
                            'border': 'none',
                            'font-weight': 'bold',
                            'box-shadow': '0 8px 25px rgba(102, 126, 234, 0.3)'
                        }
                    ),
                    dbc.Tab(
                        label="🏙️ Urbanization Trends",
                        tab_id="urbanization",
                        tab_style={
                            'border-radius': '12px 12px 0 0',
                            'border': 'none',
                            'background': 'rgba(255, 255, 255, 0.7)',
                            'margin-right': '0.5rem',
                            'padding': '1rem 1.5rem'
                        },
                        active_tab_style={
                            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                            'color': 'white',
                            'border': 'none',
                            'font-weight': 'bold',
                            'box-shadow': '0 8px 25px rgba(102, 126, 234, 0.3)'
                        }
                    ),
                    dbc.Tab(
                        label="💧 Flood Risk Assessment",
                        tab_id="flood_risk",
                        tab_style={
                            'border-radius': '12px 12px 0 0',
                            'border': 'none',
                            'background': 'rgba(255, 255, 255, 0.7)',
                            'margin-right': '0.5rem',
                            'padding': '1rem 1.5rem'
                        },
                        active_tab_style={
                            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                            'color': 'white',
                            'border': 'none',
                            'font-weight': 'bold',
                            'box-shadow': '0 8px 25px rgba(102, 126, 234, 0.3)'
                        }
                    ),
                    dbc.Tab(
                        label="⚖️ Country Comparison",
                        tab_id="comparison",
                        tab_style={
                            'border-radius': '12px 12px 0 0',
                            'border': 'none',
                            'background': 'rgba(255, 255, 255, 0.7)',
                            'margin-right': '0.5rem',
                            'padding': '1rem 1.5rem'
                        },
                        active_tab_style={
                            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                            'color': 'white',
                            'border': 'none',
                            'font-weight': 'bold',
                            'box-shadow': '0 8px 25px rgba(102, 126, 234, 0.3)'
                        }
                    ),
                ], id="main-tabs", active_tab="disasters"),
            ], width=12)
        ], className="mb-4"),
        
        # Main content area
        dbc.Row([
            dbc.Col([
                html.Div(id="tab-content")
            ], width=12)
        ]),
        
        # Footer with enhanced styling
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.P(
                        "World Bank Disaster Risk Management - Sub-Saharan Africa Dashboard",
                        className="text-center mb-2",
                        style={'color': 'rgba(255,255,255,0.9)', 'font-weight': '300'}
                    ),
                    html.P(
                        "Powered by real-time data analytics and machine learning",
                        className="text-center mb-0",
                        style={'color': 'rgba(255,255,255,0.7)', 'font-size': '0.9rem'}
                    )
                ], style={
                    'background': 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
                    'padding': '2rem',
                    'border-radius': '12px',
                    'margin-top': '3rem'
                })
            ], width=12)
        ])
        
    ], fluid=True, style={
        'background': 'transparent',
        'min-height': '100vh'
    })


def create_disaster_tab_content():
    """Create content for the Historical Disasters tab"""
    return dbc.Container([
        dbc.Row([
            # Filters
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5([
                            html.I(className="fas fa-filter me-2", style={'color': '#667eea'}),
                            "Filters"
                        ], className="card-title", style={'color': '#2c3e50', 'font-weight': 'bold'}),
                        html.Label([
                            html.I(className="fas fa-exclamation-triangle me-2", style={'color': '#e74c3c'}),
                            "Disaster Type:"
                        ], className="fw-bold", style={'color': '#2c3e50', 'margin-top': '1rem'}),
                        dcc.Dropdown(
                            id="disaster-type-dropdown",
                            multi=True,
                            placeholder="Select disaster types...",
                            style={'margin-bottom': '1rem'}
                        ),
                        html.Label([
                            html.I(className="fas fa-calendar-alt me-2", style={'color': '#3498db'}),
                            "Year Range:"
                        ], className="fw-bold", style={'color': '#2c3e50'}),
                        dcc.RangeSlider(
                            id="disaster-year-slider",
                            marks={i: str(i) for i in range(1975, 2030, 10)},
                            min=1975,
                            max=2025,
                            step=1,
                            value=[2000, 2025],
                            tooltip={'placement': 'bottom', 'always_visible': True}
                        )
                    ], style={'padding': '1.5rem'})
                ], style={
                    'border': 'none',
                    'border-radius': '12px',
                    'box-shadow': '0 6px 20px rgba(0,0,0,0.1)',
                    'background': 'linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%)'
                })
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
                        html.H5([
                            html.I(className="fas fa-chart-area me-2", style={'color': '#667eea'}),
                            "Urban Development Indicators"
                        ], className="card-title", style={'color': '#2c3e50', 'font-weight': 'bold'}),
                        html.Label([
                            html.I(className="fas fa-chart-bar me-2", style={'color': '#2ecc71'}),
                            "Select Indicator:"
                        ], className="fw-bold", style={'color': '#2c3e50', 'margin-top': '1rem'}),
                        dcc.Dropdown(
                            id="urban-indicator-dropdown",
                            options=[
                                {'label': '🏙️ Urban Population %', 'value': 'urban_pop_pct'},
                                {'label': '📈 Urban Growth Rate', 'value': 'urban_growth'},
                                {'label': '👥 Population Density', 'value': 'pop_density'},
                            ],
                            value='urban_pop_pct',
                            style={'border-radius': '8px'}
                        )
                    ], style={'padding': '1.5rem'})
                ], style={
                    'border': 'none',
                    'border-radius': '12px',
                    'box-shadow': '0 6px 20px rgba(0,0,0,0.1)',
                    'background': 'linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%)'
                })
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
                        html.H5([
                            html.I(className="fas fa-tint me-2", style={'color': '#667eea'}),
                            "Flood Risk Parameters"
                        ], className="card-title", style={'color': '#2c3e50', 'font-weight': 'bold'}),
                        html.Label([
                            html.I(className="fas fa-thermometer-half me-2", style={'color': '#e74c3c'}),
                            "Risk Level:"
                        ], className="fw-bold", style={'color': '#2c3e50', 'margin-top': '1rem'}),
                        dcc.Dropdown(
                            id="flood-risk-level",
                            options=[
                                {'label': '🟢 Low Risk', 'value': 'low'},
                                {'label': '🟡 Medium Risk', 'value': 'medium'},
                                {'label': '🟠 High Risk', 'value': 'high'},
                                {'label': '🔴 Very High Risk', 'value': 'very_high'}
                            ],
                            multi=True,
                            value=['medium', 'high', 'very_high'],
                            style={'margin-bottom': '1.5rem'}
                        ),
                        html.Label([
                            html.I(className="fas fa-clock me-2", style={'color': '#9b59b6'}),
                            "Scenario:"
                        ], className="fw-bold", style={'color': '#2c3e50'}),
                        dbc.RadioItems(
                            id="flood-scenario",
                            options=[
                                {'label': '🌊 Current Conditions', 'value': 'current'},
                                {'label': '📊 2030 Projection', 'value': '2030'},
                                {'label': '🔮 2050 Projection', 'value': '2050'}
                            ],
                            value='current',
                            inline=False,
                            style={'margin-top': '1rem'}
                        )
                    ], style={'padding': '1.5rem'})
                ], style={
                    'border': 'none',
                    'border-radius': '12px',
                    'box-shadow': '0 6px 20px rgba(0,0,0,0.1)',
                    'background': 'linear-gradient(145deg, #ffffff 0%, #f8f9fa 100%)'
                })
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