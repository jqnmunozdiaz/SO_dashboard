"""
World Bank-styled layout for the Sub-Saharan Africa DRM Dashboard
Inspired by the Review_CatDDOs dashboard design
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.data_loader import get_subsaharan_countries

# Shared tab styles - modify these to change all tabs at once
TAB_STYLE_INACTIVE = {
    'border': '0px solid #e5e7eb',
    'background': 'transparent',
    'padding': '0.875rem 1.75rem',
    'margin-right': '0.5rem',
    'border-radius': '8px',
    'color': "#08387b",
    'font-weight': '500',
    'font-size': '0.875rem',
    'cursor': 'pointer'
}

TAB_STYLE_ACTIVE = {
    'border': '0px solid #295e84',
    'background': 'transparent',
    'color': '#295e84',
    'font-weight': '600'
}

def create_world_bank_layout():
    """Create the World Bank-styled main dashboard layout matching Review_CatDDOs structure"""
    
    # This matches the Review_CatDDOs layout: flex h-screen bg-gray-50 overflow-hidden
    return html.Div([
        # Header with title and logos - always visible at top
        html.Div([
            html.Div([
                # Title on the left - now dynamic based on country selection
                html.Div([
                    html.H2(
                        id="dynamic-header-title",
                        children="Sub-Saharan Africa DRM Dashboard",
                        style={
                            'font-size': '1.25rem',
                            'font-weight': '600',
                            'color': '#295e84',
                            'margin': '0'
                        }
                    )
                ], style={
                    'display': 'flex',
                    'align-items': 'center'
                }),
                
                # Spacer div to push logos to the right
                html.Div(style={'flex': '1'}),
                
                # Logos container on the right
                html.Div([
                    html.Img(
                        src="/assets/images/wb-full-logo.png",
                        style={
                            'height': '40px',
                            'margin-right': '1rem',
                            'filter': 'brightness(0.8)'
                        },
                        alt="World Bank Logo"
                    ),
                    html.Img(
                        src="/assets/images/gfdrr-logo.png",
                        style={
                            'height': '40px',
                            'filter': 'brightness(0.8)'
                        },
                        alt="GFDRR Logo"
                    )
                ], style={
                    'display': 'flex',
                    'align-items': 'center'
                })
            ], style={
                'display': 'flex',
                'align-items': 'center',
                'max-width': '80rem',
                'margin': '0 auto',
                'padding': '0 1.5rem'
            })
        ], style={
            'background': 'white',
            'padding': '1rem 0',
            'border-bottom': '1px solid #e5e7eb',
            'position': 'sticky',
            'top': '0',
            'z-index': '50',
            'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1)'
        }),
        
        # Main content area
        html.Div([
            # Hero Section
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
                            "An interactive platform for analyzing historical disaster patterns, urbanization trends, and resilience indicators across Sub-Saharan Africa. This tool enables evidence-based decision making for disaster preparedness, response planning, and long-term risk reduction strategies.",
                            style={
                                'font-size': '1rem',
                                'line-height': '1.75rem',
                                'color': '#6b7280',
                                'margin-bottom': '1.5rem'
                            }
                        ),
                        html.P(
                            "Select a country and interact with the dynamic figures.",
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
                                'width': '150px'  # Reduced from 300px to half
                            }),
                            # Methodological Note download button
                            html.A([
                                html.Button(
                                    "📄 Methodological Note",
                                    style={
                                        'background-color': '#295e84',
                                        'color': 'white',
                                        'border': 'none',
                                        'padding': '0.5rem 1rem',
                                        'border-radius': '0.375rem',
                                        'font-size': '0.875rem',
                                        'font-weight': '500',
                                        'cursor': 'pointer',
                                        'transition': 'all 0.2s ease'
                                    }
                                )
                            ], 
                            href="/assets/documents/SSA DRM Dashboard - Methodological Note.docx",
                            download="SSA_DRM_Dashboard_Methodological_Note.docx",
                            style={'margin-left': '1rem'}
                            )
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
                            tab_style=TAB_STYLE_INACTIVE,
                            active_tab_style=TAB_STYLE_ACTIVE
                        ),
                        dbc.Tab(
                            label="Historical Urbanization",
                            tab_id="urbanization",
                            tab_style=TAB_STYLE_INACTIVE,
                            active_tab_style=TAB_STYLE_ACTIVE
                        ),
                        dbc.Tab(
                            label="Exposure to Flood Hazard",
                            tab_id="flood-exposure",
                            tab_style=TAB_STYLE_INACTIVE,
                            active_tab_style=TAB_STYLE_ACTIVE
                        ),
                        dbc.Tab(
                            label="Projections of Flood Risk",
                            tab_id="flood-projections",
                            tab_style=TAB_STYLE_INACTIVE,
                            active_tab_style=TAB_STYLE_ACTIVE
                        )
                    ], id="main-tabs", active_tab="disasters", style={
                        'border': 'none',
                        'display': 'flex',
                        'justify-content': 'center',
                        'flex-wrap': 'wrap',
                        'gap': '0.5rem',
                        'padding': '0.75rem'
                    })
                ], style={
                    'max-width': '80rem',
                    'margin': '0 auto',
                    'padding': '0 1.5rem',
                    'width': '100%'
                })
            ], style={
                'background': 'transparent',
                'padding': '1.5rem 0',
                'border-bottom': 'none'
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
        'flex-direction': 'column',
        'height': '100vh',
        'background': '#f9fafb',
        'overflow': 'hidden'
    })


def create_world_bank_disaster_tab_content():
    """Create World Bank-styled content for the Historical Disasters tab with subtabs"""
    return html.Div([
        html.Div([
            # Subtabs for different disaster visualizations
            html.Div([
                dbc.Tabs([
                    dbc.Tab(
                        label="Frequency by Type",
                        tab_id="disaster-frequency",
                        tab_style={
                            'border': '1px solid #e5e7eb',
                            'background': 'transparent',
                            'padding': '0.5rem 1rem',
                            'margin-right': '0.25rem',
                            'border-radius': '4px',
                            'color': '#64748b',
                            'font-weight': '500',
                            'font-size': '0.8rem'
                        },
                        active_tab_style={
                            'border': '1px solid #295e84',
                            'background': 'transparent',
                            'color': '#295e84',
                            'font-weight': '600'
                        }
                    ),
                    dbc.Tab(
                        label="Disasters by Year",
                        tab_id="disaster-timeline",
                        tab_style={
                            'border': '1px solid #e5e7eb',
                            'background': 'transparent',
                            'padding': '0.5rem 1rem',
                            'margin-right': '0.25rem',
                            'border-radius': '4px',
                            'color': '#64748b',
                            'font-weight': '500',
                            'font-size': '0.8rem'
                        },
                        active_tab_style={
                            'border': '1px solid #295e84',
                            'background': 'transparent',
                            'color': '#295e84',
                            'font-weight': '600'
                        }
                    ),
                    dbc.Tab(
                        label="Total Affected Population",
                        tab_id="disaster-affected",
                        tab_style={
                            'border': '1px solid #e5e7eb',
                            'background': 'transparent',
                            'padding': '0.5rem 1rem',
                            'margin-right': '0.25rem',
                            'border-radius': '4px',
                            'color': '#64748b',
                            'font-weight': '500',
                            'font-size': '0.8rem'
                        },
                        active_tab_style={
                            'border': '1px solid #295e84',
                            'background': 'transparent',
                            'color': '#295e84',
                            'font-weight': '600'
                        }
                    )
                ], id="disaster-subtabs", active_tab="disaster-frequency", style={
                    'border': 'none',
                    'margin-bottom': '1.5rem'
                })
            ]),
            
            # Charts container
            html.Div([
                html.Div(id="disaster-chart-container")
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


def create_world_bank_urbanization_tab_content():
    """Create World Bank-styled content for the Historical Urbanization tab"""
    return html.Div([
        html.Div([
            html.H3(
                "Historical Urbanization Analysis",
                style={
                    'font-size': '1.5rem',
                    'font-weight': '600',
                    'color': '#374151',
                    'margin-bottom': '1rem'
                }
            ),
            html.P(
                "This section will contain historical urbanization trends, population growth data, and urban development indicators for Sub-Saharan African countries.",
                style={
                    'font-size': '1rem',
                    'line-height': '1.75rem',
                    'color': '#6b7280',
                    'margin-bottom': '2rem'
                }
            ),
            html.Div([
                html.P(
                    "Historical urbanization content coming soon...",
                    style={
                        'font-size': '1.125rem',
                        'color': '#9ca3af',
                        'text-align': 'center',
                        'padding': '2rem'
                    }
                )
            ], style={
                'background': 'white',
                'padding': '2rem',
                'border-radius': '0.5rem',
                'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                'border': '1px solid #e5e7eb',
                'text-align': 'center'
            })
        ], style={
            'max-width': '80rem',
            'margin': '0 auto',
            'padding': '1.5rem'
        })
    ], style={
        'background': '#f9fafb',
        'min-height': 'calc(100vh - 300px)'
    })


def create_world_bank_flood_exposure_tab_content():
    """Create World Bank-styled content for the Exposure to Flood Hazard tab"""
    return html.Div([
        html.Div([
            html.H3(
                "Exposure to Flood Hazard",
                style={
                    'font-size': '1.5rem',
                    'font-weight': '600',
                    'color': '#374151',
                    'margin-bottom': '1rem'
                }
            ),
            html.P(
                "This section will contain current flood hazard exposure data, vulnerable population mapping, and infrastructure at risk assessments for Sub-Saharan African countries.",
                style={
                    'font-size': '1rem',
                    'line-height': '1.75rem',
                    'color': '#6b7280',
                    'margin-bottom': '2rem'
                }
            ),
            html.Div([
                html.P(
                    "Flood exposure analysis coming soon...",
                    style={
                        'font-size': '1.125rem',
                        'color': '#9ca3af',
                        'text-align': 'center',
                        'padding': '2rem'
                    }
                )
            ], style={
                'background': 'white',
                'padding': '2rem',
                'border-radius': '0.5rem',
                'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                'border': '1px solid #e5e7eb',
                'text-align': 'center'
            })
        ], style={
            'max-width': '80rem',
            'margin': '0 auto',
            'padding': '1.5rem'
        })
    ], style={
        'background': '#f9fafb',
        'min-height': 'calc(100vh - 300px)'
    })


def create_world_bank_flood_projections_tab_content():
    """Create World Bank-styled content for the Projections of Flood Risk tab"""
    return html.Div([
        html.Div([
            html.H3(
                "Projections of Flood Risk",
                style={
                    'font-size': '1.5rem',
                    'font-weight': '600',
                    'color': '#374151',
                    'margin-bottom': '1rem'
                }
            ),
            html.P(
                "This section will contain future flood risk projections, climate change impact scenarios, and long-term risk assessments for Sub-Saharan African countries.",
                style={
                    'font-size': '1rem',
                    'line-height': '1.75rem',
                    'color': '#6b7280',
                    'margin-bottom': '2rem'
                }
            ),
            html.Div([
                html.P(
                    "Flood risk projections coming soon...",
                    style={
                        'font-size': '1.125rem',
                        'color': '#9ca3af',
                        'text-align': 'center',
                        'padding': '2rem'
                    }
                )
            ], style={
                'background': 'white',
                'padding': '2rem',
                'border-radius': '0.5rem',
                'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                'border': '1px solid #e5e7eb',
                'text-align': 'center'
            })
        ], style={
            'max-width': '80rem',
            'margin': '0 auto',
            'padding': '1.5rem'
        })
    ], style={
        'background': '#f9fafb',
        'min-height': 'calc(100vh - 300px)'
    })

