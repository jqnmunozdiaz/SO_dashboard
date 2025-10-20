"""
World Bank-styled layout for the Sub-Saharan Africa DRM Dashboard
"""

from dash import html, dcc
import dash_bootstrap_components as dbc
from src.utils.data_loader import get_subsaharan_countries
from src.utils.country_utils import get_countries_with_regions
from src.utils.ui_helpers import (
    create_city_platform_button,
    create_download_component,
    create_methodological_note_button,
)


def create_world_bank_layout():
    """Create the World Bank-styled main dashboard layout"""

    return html.Div([
        # Header
        html.Div([
            html.Div([
                html.Div([
                    html.H2(
                        id="dynamic-header-title",
                        children="Sub-Saharan Africa DRM Dashboard",
                        className="header-title",
                    )
                ], className="header-title-container"),

                html.Div(className="header-spacer"),

                html.Div([
                    html.Img(
                        src="/assets/images/wb-full-logo.png",
                        className="header-logo header-logo-wb",
                        alt="World Bank Logo",
                    ),
                    html.Img(
                        src="/assets/images/gfdrr-logo.png",
                        className="header-logo",
                        alt="GFDRR Logo",
                    ),
                ], className="header-logos"),
            ], className="header-inner"),
        ], className="header-container"),

        # Main content
        html.Div([
            # Hero
            html.Div([
                html.Div([
                    html.Div([
                        html.H1("Disaster Risk & Urbanization Analytics Dashboard", className="hero-title"),
                        html.P("Sub-Saharan Africa", className="hero-subtitle"),
                        html.P(
                            "An interactive platform for analyzing historical disaster patterns, urbanization trends, and resilience indicators across Sub-Saharan Africa. This tool informs decision making for disaster preparedness and long-term risk reduction strategies.",
                            className="hero-description",
                        ),
                        html.P("Select a country, explore the tabs, and interact with the dynamic figures. For city-level information, visit the dedicated platform.", className="hero-description",
                        ),
                    ], className="hero-content"),

                    html.Div([
                        html.Div(className="hero-map-image"),
                        # City-level platform button positioned over the hero map
                        html.Div(
                            create_city_platform_button("https://www.google.com"), className="hero-map-action"
                        ),
                    ], className="hero-map"),
                ], className="hero-inner"),
            ], className="hero-section"),

            # Filters
            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Label("Select Country or Region:", className="filter-label"),
                            html.Div([
                                dcc.Dropdown(
                                    id="main-country-filter",
                                    options=[
                                        {"label": country["name"], "value": country["code"]}
                                        for country in get_countries_with_regions()
                                    ],
                                    value=get_subsaharan_countries()[0]["code"],
                                    placeholder="Select a country...",
                                )
                            ], className="filter-dropdown-container"),
                        ], className="filter-control-group"),
                    ], className="filter-card"),
                ], className="filter-inner"),
            ], className="filter-section"),

            # Navigation
            html.Div([
                html.Div([
                    dbc.Tabs(
                        [
                            dbc.Tab(label="Historical Disasters", tab_id="disasters"),
                            dbc.Tab(label="Urbanization Trends", tab_id="urbanization"),
                            dbc.Tab(label="Exposure to Flood Hazard", tab_id="flood-exposure"),
                            dbc.Tab(label="Projections of Flood Risk", tab_id="flood-projections"),
                        ],
                        id="main-tabs",
                        active_tab="disasters",
                        className="main-nav-tabs main-tabs-container",
                    )
                ], className="nav-inner"),
            ], className="nav-section"),

            # Content area (callbacks populate this)
            html.Div(id="tab-content", className="content-area"),

            # Hidden download components (available app-wide)
            html.Div([
                create_download_component("disaster-frequency-download"),
                create_download_component("disaster-timeline-download"),
                create_download_component("disaster-affected-download"),
                create_download_component("disaster-deaths-download"),
                create_download_component("urban-population-projections-download"),
                create_download_component("urbanization-rate-download"),
                create_download_component("urban-population-slums-download"),
                create_download_component("access-to-electricity-urban-download"),
                create_download_component("gdp-vs-urbanization-download"),
                create_download_component("cities-distribution-download"),
                create_download_component("cities-evolution-download"),
            ], style={"display": "none"}),
        ], className="main-content"),
    ], className="dashboard-container")


def create_world_bank_disaster_tab_content():
    return html.Div([
        html.Div([
            html.Div([
                dbc.Tabs(
                    [
                        dbc.Tab(label="Overview of Disasters", tab_id="disaster-frequency"),
                        dbc.Tab(label="Disasters by Year", tab_id="disaster-timeline"),
                        dbc.Tab(label="Total Affected Population", tab_id="disaster-affected"),
                        dbc.Tab(label="Total Deaths", tab_id="disaster-deaths"),
                    ],
                    id="disaster-subtabs",
                    active_tab="disaster-frequency",
                    className="sub-nav-tabs subtabs-container",
                )
            ]),
            html.Div([html.Div(id="disaster-chart-container")])
        ], className="tab-content-inner"),
    ], className="tab-content-container")


def create_world_bank_urbanization_tab_content():
    return html.Div([
        html.Div([
            html.Div([
                dbc.Tabs(
                    [
                        dbc.Tab(label="Urban Population", tab_id="urban-population-projections"),
                        dbc.Tab(label="Urbanization Rate", tab_id="urbanization-rate"),
                        dbc.Tab(label="Population Living in Slums", tab_id="urban-population-slums"),
                        dbc.Tab(label="Access to Electricity", tab_id="access-to-electricity-urban"),
                        dbc.Tab(label="GDP vs Urbanization", tab_id="gdp-vs-urbanization"),
                        dbc.Tab(label="Cities Distribution", tab_id="cities-distribution"),
                        dbc.Tab(label="Cities Evolution", tab_id="cities-evolution"),
                    ],
                    id="urbanization-subtabs",
                    active_tab="urban-population-projections",
                    className="sub-nav-tabs subtabs-container",
                )
            ]),
            html.Div([html.Div(id="urbanization-chart-container")])
        ], className="tab-content-inner"),
    ], className="tab-content-container")


def create_world_bank_flood_exposure_tab_content():
    return html.Div([
        html.Div([
            dbc.Tabs(
                id="flood-exposure-subtabs",
                active_tab="national-flood-exposure",
                className="sub-nav-tabs subtabs-container",
                children=[
                    dbc.Tab(label="National Flood Exposure (Built-up, Absolute)", tab_id="national-flood-exposure"),
                    dbc.Tab(label="National Flood Exposure (Built-up, Relative)", tab_id="national-flood-exposure-relative"),
                    dbc.Tab(label="National Flood Exposure (Population, Absolute)", tab_id="national-flood-exposure-population"),
                    dbc.Tab(label="National Flood Exposure (Population, Relative)", tab_id="national-flood-exposure-population-relative"),
                ],
            ),
            html.Div(id="flood-exposure-content"),
        ], className="tab-content-inner"),
    ], className="tab-content-container")


def create_world_bank_flood_projections_tab_content():
    return html.Div([
        html.Div([
            html.Div([html.P("...", className="coming-soon-text")], className="coming-soon-card")
        ], className="tab-content-inner"),
    ], className="tab-content-container")

