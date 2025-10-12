"""
World Bank-styled layout for the Sub-Saharan Africa DRM Dashboard
Inspired by the Review_CatDDOs dashboard design
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.data_loader import get_subsaharan_countries

def create_world_bank_layout():
    """Create the World Bank-styled main dashboard layout matching Review_CatDDOs structure"""
    
    # This matches the Review_CatDDOs layout: flex h-screen bg-gray-50 overflow-hidden
    return html.Div([
        # Main content area (equivalent to MainContent from Review_CatDDOs)
        html.Div([
            # Hero Section matching DashboardHero.tsx structure
            html.Div([
                html.Div([
                    # Left content section
                    html.Div([
                        html.H1(
                            "Sub-Saharan Africa DRM Dashboard",
                            style={
                                'font-size': '2.25rem',
                                'font-weight': '700',
                                'line-height': '2.5rem',
                                'color': '#295e84',
                                'margin-bottom': '1.5rem'
                            }
                        ),
                        html.P(
                            "An interactive platform for analyzing disaster risk patterns, vulnerability assessments, and resilience indicators across Sub-Saharan Africa. This tool enables evidence-based decision making for disaster preparedness, response planning, and long-term risk reduction strategies.",
                            style={
                                'font-size': '1rem',
                                'line-height': '1.75rem',
                                'color': '#6b7280',
                                'margin-bottom': '1.5rem'
                            }
                        ),
                        html.P(
                            "Explore comprehensive datasets on historical disasters, urban development patterns, flood risk projections, and comparative country profiles to strengthen disaster risk management initiatives and inform policy development.",
                            style={
                                'font-size': '1rem',
                                'line-height': '1.75rem',
                                'color': '#6b7280'
                            }
                        )
                    ], style={
                        'flex': '1 1 0%',
                        'padding-right': '3rem'
                    }),
                    
                    # Right map section
                    html.Div([
                        html.Div(
                            style={
                                'width': '100%',
                                'height': '300px',
                                'background-image': 'url("/assets/images/world-map-dashboard.png")',
                                'background-size': 'contain',
                                'background-repeat': 'no-repeat',
                                'background-position': 'center',
                                'opacity': '0.8'
                            }
                        )
                    ], style={
                        'flex': '1 1 0%'
                    })
                ], style={
                    'display': 'flex',
                    'align-items': 'center',
                    'gap': '2rem'
                })
            ], style={
                'padding': '4rem 1.5rem',
                'max-width': '80rem',
                'margin': '0 auto'
            }),
            
            # Filter section
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label(
                                "Select Country:",
                                style={
                                    'font-size': '0.875rem',
                                    'font-weight': '500',
                                    'color': '#374151',
                                    'margin-right': '1rem',
                                    'margin-bottom': '0',
                                    'align-self': 'center'
                                }
                            ),
                            html.Div([
                                dcc.Dropdown(
                                    id="main-country-filter",
                                    options=[
                                        {'label': country['name'], 'value': country['code']}
                                        for country in get_subsaharan_countries()
                                    ],
                                    value=get_subsaharan_countries()[0]['code'],
                                    placeholder="Select a country..."
                                )
                            ], style={
                                'width': '300px'
                            })
                        ], style={
                            'display': 'flex',
                            'align-items': 'center',
                            'gap': '1rem'
                        })
                    ], style={
                        'background': 'white',
                        'padding': '1.5rem',
                        'border-radius': '0.5rem',
                        'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                        'border': '1px solid #e5e7eb'
                    })
                ], style={
                    'max-width': '80rem',
                    'margin': '0 auto',
                    'padding': '0 1.5rem'
                })
            ], style={
                'background': '#f9fafb',
                'padding': '2rem 0'
            }),
            
            # Navigation tabs
            html.Div([
                html.Div([
                    dbc.Tabs([
                        dbc.Tab(
                            label="Historical Disasters",
                            tab_id="disasters",
                            tab_style={
                                'border': 'none',
                                'background': 'transparent',
                                'padding': '0.75rem 1.5rem',
                                'margin-right': '0.5rem',
                                'border-radius': '9999px',
                                'color': '#6b7280',
                                'font-weight': '500',
                                'font-size': '0.875rem'
                            },
                            active_tab_style={
                                'background': '#f3f4f6',
                                'color': '#374151',
                                'border': 'none',
                                'font-weight': '600'
                            }
                        )
                    ], id="main-tabs", active_tab="disasters", style={'border': 'none'})
                ], style={
                    'max-width': '80rem',
                    'margin': '0 auto',
                    'padding': '0 1.5rem'
                })
            ], style={
                'background': 'white',
                'padding': '1rem 0',
                'border-bottom': '1px solid #e5e7eb'
            }),
            
            # Content area
            html.Div(id="tab-content", style={
                'flex': '1 1 0%'
            })
            
        ], style={
            'flex': '1 1 0%',
            'overflow-y': 'auto'
        })
        
    ], style={
        'display': 'flex',
        'height': '100vh',
        'background': '#f9fafb',
        'overflow': 'hidden'
    })


def create_world_bank_disaster_tab_content():
    """Create World Bank-styled content for the Historical Disasters tab matching Review_CatDDOs"""
    return html.Div([
        html.Div([
            # Filter controls section
            html.Div([
                html.H3(
                    "Filters",
                    style={
                        'font-size': '1.125rem',
                        'font-weight': '600',
                        'color': '#374151',
                        'margin-bottom': '1rem'
                    }
                ),
                html.Div([
                    html.Label(
                        "Disaster Type:",
                        style={
                            'display': 'block',
                            'font-size': '0.875rem',
                            'font-weight': '500',
                            'color': '#374151',
                            'margin-bottom': '0.5rem'
                        }
                    ),
                    dcc.Dropdown(
                        id="disaster-type-dropdown",
                        multi=True,
                        placeholder="Select disaster types...",
                        style={'margin-bottom': '1.5rem'}
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
            
            # Charts container
            html.Div([
                # Disaster frequency bar chart
                html.Div([
                    dcc.Graph(id="disaster-frequency-chart")
                ], style={
                    'background': 'white',
                    'padding': '1.5rem',
                    'border-radius': '0.5rem',
                    'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                    'border': '1px solid #e5e7eb'
                })
            ], id="charts-container")
        ], style={
            'max-width': '80rem',
            'margin': '0 auto',
            'padding': '1.5rem'
        })
    ], style={
        'background': '#f9fafb',
        'min-height': 'calc(100vh - 300px)'
    })

