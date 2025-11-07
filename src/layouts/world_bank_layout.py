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
)
import os


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
                    html.Button(
                        "Disclaimer",
                        id="disclaimer-button",
                        className="contact-us-button",
                        n_clicks=0
                    ),
                    html.Button(
                        "Contact Form",
                        id="contact-us-button",
                        className="contact-us-button",
                        n_clicks=0
                    ),
                    # Placeholder for logos - currently commented out
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

        # Contact Us Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Contact Form")),
            dbc.ModalBody([
                html.P("You can leave a message for questions, comments, feedback, or any other inquiries.", 
                       className="contact-intro-message"),
                html.Div([
                    html.Label("Name:", className="contact-form-label"),
                    dbc.Input(
                        id="contact-name",
                        type="text",
                        placeholder="Enter your name",
                        className="contact-form-input"
                    ),
                ], className="contact-form-group"),
                html.Div([
                    html.Label("Email (optional):", className="contact-form-label"),
                    dbc.Input(
                        id="contact-email",
                        type="email",
                        placeholder="Enter your email (optional)",
                        className="contact-form-input"
                    ),
                ], className="contact-form-group"),
                html.Div([
                    html.Label("Message:", className="contact-form-label"),
                    dbc.Textarea(
                        id="contact-message",
                        placeholder="Enter your message or feedback",
                        className="contact-form-textarea",
                        style={"minHeight": "150px"}
                    ),
                ], className="contact-form-group"),
                html.Div(id="contact-form-feedback", className="contact-form-feedback"),
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    "Send",
                    id="contact-submit-button",
                    className="contact-submit-button",
                    n_clicks=0
                ),
                dbc.Button(
                    "Close",
                    id="contact-close-button",
                    className="contact-close-button",
                    n_clicks=0
                ),
            ]),
        ],
        id="contact-modal",
        is_open=False,
        size="lg",
        backdrop=True,
        centered=True),

        # Disclaimer Modal
        dbc.Modal([
            dbc.ModalHeader(dbc.ModalTitle("Disclaimer")),
            dbc.ModalBody([
                html.P(
                    "This work is a product of the staff of The World Bank with external contributions. "
                    "The findings, interpretations, and conclusions expressed in this work do not necessarily "
                    "reflect the views of The World Bank, its Board of Executive Directors, or the governments "
                    "they represent. The World Bank does not guarantee the accuracy of the data included in this work. "
                    "The boundaries, colors, denominations, and other information shown on any map in this work do not "
                    "imply any judgment on the part of The World Bank concerning the legal status of any territory or "
                    "the endorsement or acceptance of such boundaries.",
                    style={'textAlign': 'justify', 'lineHeight': '1.6'}
                )
            ]),
            dbc.ModalFooter([
                dbc.Button(
                    "Close",
                    id="disclaimer-close-button",
                    className="contact-close-button",
                    n_clicks=0
                ),
            ]),
        ],
        id="disclaimer-modal",
        is_open=True,
        size="lg",
        backdrop=True,
        centered=True),

        # Main content
        html.Div([
            # Hero
            html.Div([
                html.Div([
                    html.Div([
                        html.H1("Disaster Risk & Urbanization Analytics Dashboard", className="hero-title"),
                        html.P("Sub-Saharan Africa", className="hero-subtitle"),
                        html.P([
                            html.B("This platform enables users to analyze disaster risk and urbanization trends across Sub-Saharan Africa. "),
                            "Combining historical disaster data with urban growth projections and climate scenarios, it supports evidence-based "
                            "planning for disaster risk reduction and sustainable urban development."
                        ], className="hero-description"),
                        html.P([
                            html.B("Explore country-level trends in disaster impacts, urbanization patterns, flood exposure, and future climate risks. "),
                            "The interactive visualizations enable to identify priorities "
                            "and inform decisions for building resilient cities."
                        ], className="hero-description"),
                        html.P([
                            "For detailed subnational analysis and city-specific data, visit the ",
                            html.A("city-level platform", href="https://urban-risk-observatory.web.app/", target="_blank", style={'color': "#358EDD", 'text-decoration': 'none', 'font-weight': 'bold'}),
                            "."
                        ], className="hero-description"),
                    ], className="hero-content"),

                    html.Div([
                        html.Div(className="hero-map-image"),
                        # City-level platform button removed from here - moved to filter section
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
                    create_city_platform_button("https://urban-risk-observatory.web.app/"),
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
                            dbc.Tab(label="Future Precipitation Extremes and Flood Exposure", tab_id="flood-projections"),
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
                create_download_component("access-to-drinking-water-download"),
                create_download_component("access-to-sanitation-download"),
                create_download_component("access-to-electricity-urban-download"),
                create_download_component("gdp-vs-urbanization-download"),
                create_download_component("cities-distribution-download"),
                create_download_component("cities-evolution-download"),
                create_download_component("cities-growth-rate-download"),
                create_download_component("cities-growth-download"),
                create_download_component("urban-density-download"),
                create_download_component("population-economic-activity-download"),
                create_download_component("national-flood-exposure-download"),
                create_download_component("national-flood-exposure-relative-download"),
                create_download_component("national-flood-exposure-population-download"),
                create_download_component("national-flood-exposure-population-relative-download"),
                create_download_component("cities-flood-exposure-download"),
                create_download_component("precipitation-download"),
                create_download_component("urbanization-vs-climate-change-download"),
                # Store for flood benchmark selections
                dcc.Store(id='flood-benchmark-store', data=[]),
                # Store for contact form submission status
                dcc.Store(id='contact-form-store', data={}),
                # Store to track if disclaimer was shown this session
                dcc.Store(id='disclaimer-session-store', data=None, storage_type='session'),
            ], style={"display": "none"}),
        ], className="main-content"),
    ], className="dashboard-container")


def create_world_bank_disaster_tab_content():
    return html.Div([
        html.Div([
            html.Div([
                dbc.Tabs(
                    [
                        dbc.Tab(label="Overview of Disasters", tab_id="disaster-frequency", label_class_name="tab-blue"),
                        dbc.Tab(label="Disasters by Year", tab_id="disaster-timeline", label_class_name="tab-blue"),
                        dbc.Tab(label="Total Affected Population", tab_id="disaster-affected", label_class_name="tab-blue"),
                        dbc.Tab(label="Total Deaths", tab_id="disaster-deaths", label_class_name="tab-blue"),
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
                        dbc.Tab(label="Population", tab_id="urban-population-projections", label_class_name="tab-blue"),
                        dbc.Tab(label="Urbanization Level", tab_id="urbanization-rate", label_class_name="tab-blue"),
                        dbc.Tab(label="GDP vs Urbanization", tab_id="gdp-vs-urbanization", label_class_name="tab-blue"),
                        dbc.Tab(label="Population Living in Slums", tab_id="urban-population-slums", label_class_name="tab-blue"),
                        dbc.Tab(label="Access to Drinking Water", tab_id="access-to-drinking-water", label_class_name="tab-green"),
                        dbc.Tab(label="Access to Sanitation", tab_id="access-to-sanitation", label_class_name="tab-green"),
                        dbc.Tab(label="Access to Electricity", tab_id="access-to-electricity-urban", label_class_name="tab-green"),
                        dbc.Tab(label="Cities Distribution", tab_id="cities-distribution", label_class_name="tab-orange"),
                        dbc.Tab(label="Cities Evolution", tab_id="cities-evolution", label_class_name="tab-orange"),
                        dbc.Tab(label="Built-up and Population Growth Rate in Cities", tab_id="cities-growth-rate", label_class_name="tab-orange"),
                        dbc.Tab(label="Cities Growth", tab_id="cities-growth", label_class_name="tab-orange"),
                        dbc.Tab(label="Built-up per capita in Cities", tab_id="urban-density", label_class_name="tab-orange"),
                        dbc.Tab(label="Population & Economic Activity", tab_id="population-economic-activity", label_class_name="tab-orange"),
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
                    dbc.Tab(label="National Flood Exposure", tab_id="national-flood-exposure", label_class_name="tab-blue"),
                    dbc.Tab(label="Cities Flood Exposure", tab_id="cities-flood-exposure", label_class_name="tab-orange"),
                ],
            ),
            html.Div(id="flood-exposure-content"),
        ], className="tab-content-inner"),
    ], className="tab-content-container")


def create_world_bank_flood_projections_tab_content():
    return html.Div([
        html.Div([
            dbc.Tabs(
                id="flood-projections-subtabs",
                active_tab="overview",
                className="sub-nav-tabs subtabs-container",
                children=[
                    dbc.Tab(label="Overview", tab_id="overview", label_class_name="tab-gray"),
                    dbc.Tab(label="Changes in Extreme Precipitation", tab_id="precipitation", label_class_name="tab-blue"),
                    dbc.Tab(label="Urbanization and Climate Change", tab_id="urbanization-vs-climate", label_class_name="tab-blue"),
                ],
            ),
            html.Div(id="flood-projections-content"),
        ], className="tab-content-inner"),
    ], className="tab-content-container")

