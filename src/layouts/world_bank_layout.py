"""
World Bank-styled layout for the Sub-Saharan Africa DRM Dashboard
Inspired by the Review_CatDDOs dashboard design
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.data_loader import get_subsaharan_countries
from src.utils.country_utils import get_countries_with_regions

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
                        className="header-title"
                    )
                ], className="header-title-container"),
                
                # Spacer div to push logos to the right
                html.Div(className="header-spacer"),
                
                # Logos container on the right
                html.Div([
                    html.Img(
                        src="/assets/images/wb-full-logo.png",
                        className="header-logo header-logo-wb",
                        alt="World Bank Logo"
                    ),
                    html.Img(
                        src="/assets/images/gfdrr-logo.png",
                        className="header-logo",
                        alt="GFDRR Logo"
                    )
                ], className="header-logos")
            ], className="header-inner")
        ], className="header-container"),
        
        # Main content area
        html.Div([
            # Hero Section
            html.Div([
                html.Div([
                    # Left content section
                    html.Div([
                        html.H1([
                            "Disaster Risk & Urbanization Analytics Dashboard"
                        ], className="hero-title"),
                        html.P(
                            "Sub-Saharan Africa",
                            className="hero-subtitle"
                        ),
                        html.P(
                            "An interactive platform for analyzing historical disaster patterns, urbanization trends, and resilience indicators across Sub-Saharan Africa. This tool enables evidence-based decision making for disaster preparedness, response planning, and long-term risk reduction strategies.",
                            className="hero-description"
                        ),
                        html.P(
                            "Select a country and interact with the dynamic figures.",
                            className="hero-description"
                        )
                    ], className="hero-content"),
                    # Right map section
                    html.Div([
                        html.Div(className="hero-map-image")
                    ], className="hero-map")
                ], className="hero-inner")
            ], className="hero-section"),
            
            # Filter section
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label(
                                "Select Country or Region:",
                                className="filter-label"
                            ),
                            html.Div([
                                dcc.Dropdown(
                                    id="main-country-filter",
                                    options=[
                                        {'label': country['name'], 'value': country['code']}
                                        for country in get_countries_with_regions()
                                    ],
                                    value=get_subsaharan_countries()[0]['code'],
                                    placeholder="Select a country..."
                                )
                            ], className="filter-dropdown-container")
                        ], className="filter-control-group"),
                    ], className="filter-card")
                ], className="filter-inner")
            ], className="filter-section"),
            
            # Navigation tabs
            html.Div([
                html.Div([
                    dbc.Tabs([
                        dbc.Tab(
                            label="Historical Disasters",
                            tab_id="disasters"
                        ),
                        dbc.Tab(
                            label="Urbanization Trends",
                            tab_id="urbanization"
                        ),
                        dbc.Tab(
                            label="Exposure to Flood Hazard",
                            tab_id="flood-exposure"
                        ),
                        dbc.Tab(
                            label="Projections of Flood Risk",
                            tab_id="flood-projections"
                        )
                    ], id="main-tabs", active_tab="disasters", 
                    className="main-nav-tabs main-tabs-container")
                ], className="nav-inner")
            ], className="nav-section"),
            
            # Content area
            html.Div(id="tab-content", className="content-area")
            
        ], className="main-content")
        
    ], className="dashboard-container")


def create_world_bank_disaster_tab_content():
    """Create World Bank-styled content for the Historical Disasters tab with subtabs"""
    return html.Div([
        html.Div([
            # Subtabs for different disaster visualizations
            html.Div([
                dbc.Tabs([
                    dbc.Tab(
                        label="Overview of Disasters",
                        tab_id="disaster-frequency"
                    ),
                    dbc.Tab(
                        label="Disasters by Year",
                        tab_id="disaster-timeline"
                    ),
                    dbc.Tab(
                        label="Total Affected Population",
                        tab_id="disaster-affected"
                    ),
                    dbc.Tab(
                        label="Total Deaths",
                        tab_id="disaster-deaths"
                    )
                ], id="disaster-subtabs", active_tab="disaster-frequency", 
                className="sub-nav-tabs subtabs-container")
            ]),
            
            # Charts container
            html.Div([
                html.Div(id="disaster-chart-container")
            ])
        ], className="tab-content-inner")
    ], className="tab-content-container")


def create_world_bank_urbanization_tab_content():
    """Create World Bank-styled content for the Historical Urbanization tab with subtabs"""
    return html.Div([
        html.Div([
            # Subtabs for different urbanization visualizations
            html.Div([
                dbc.Tabs([
                    dbc.Tab(
                        label="Urban Population",
                        tab_id="urban-population-projections"
                    ),
                    dbc.Tab(
                        label="Urbanization Rate",
                        tab_id="urbanization-rate"
                    ),
                    dbc.Tab(
                        label="Population Living in Slums",
                        tab_id="urban-population-slums"
                    ),
                    dbc.Tab(
                        label="Access to Electricity",
                        tab_id="access-to-electricity-urban"
                    ),
                    dbc.Tab(
                        label="GDP vs Urbanization",
                        tab_id="gdp-vs-urbanization"
                    ),
                    dbc.Tab(
                        label="Cities Distribution",
                        tab_id="cities-distribution"
                    ),
                    dbc.Tab(
                        label="Cities Evolution",
                        tab_id="cities-evolution"
                    )
                ], id="urbanization-subtabs", active_tab="urban-population-projections", 
                className="sub-nav-tabs subtabs-container")
            ]),
            
            # Charts container
            html.Div([
                html.Div(id="urbanization-chart-container")
            ])
        ], className="tab-content-inner")
    ], className="tab-content-container")


def create_world_bank_flood_exposure_tab_content():
    """Create World Bank-styled content for the Exposure to Flood Hazard tab"""
    return html.Div([
        html.Div([
            html.H3(
                "Exposure to Flood Hazard",
                className="tab-title"
            ),
            html.P(
                "This section will contain current flood hazard exposure data, vulnerable population mapping, and infrastructure at risk assessments for Sub-Saharan African countries.",
                className="tab-description"
            ),
            html.Div([
                html.P(
                    "Flood exposure analysis coming soon...",
                    className="coming-soon-text"
                )
            ], className="coming-soon-card")
        ], className="tab-content-inner")
    ], className="tab-content-container")


def create_world_bank_flood_projections_tab_content():
    """Create World Bank-styled content for the Projections of Flood Risk tab"""
    return html.Div([
        html.Div([
            html.H3(
                "Projections of Flood Risk",
                className="tab-title"
            ),
            html.P(
                "This section will contain future flood risk projections, climate change impact scenarios, and long-term risk assessments for Sub-Saharan African countries.",
                className="tab-description"
            ),
            html.Div([
                html.P(
                    "Flood risk projections coming soon...",
                    className="coming-soon-text"
                )
            ], className="coming-soon-card")
        ], className="tab-content-inner")
    ], className="tab-content-container")

