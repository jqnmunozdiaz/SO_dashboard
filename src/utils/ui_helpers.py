"""
UI component helpers for creating reusable dashboard components
"""

from dash import dcc, html
import dash_bootstrap_components as dbc

try:
    from .benchmark_config import get_benchmark_options
    from .GLOBAL_BENCHMARK_CONFIG import get_global_benchmark_dropdown_options, get_all_global_benchmark_codes
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.benchmark_config import get_benchmark_options
    from src.utils.GLOBAL_BENCHMARK_CONFIG import get_global_benchmark_dropdown_options, get_all_global_benchmark_codes


def create_benchmark_selectors(
    regional_id, 
    country_id, 
    include_regional=True, 
    include_country=True, 
    global_id=None, 
    include_global=False,
    exclude_from_default=None
):
    """
    Create benchmark selection UI components for regional, country, and global benchmarks

    Args:
        regional_id (str): ID for the regional benchmark checklist
        country_id (str): ID for the country benchmark dropdown
        include_regional (bool): Whether to include regional benchmark selector
        include_country (bool): Whether to include country benchmark selector
        global_id (str): ID for the global benchmark dropdown
        include_global (bool): Whether to include global benchmark selector
        exclude_from_default (list): List of benchmark codes to exclude from default selection (e.g., ['AFE', 'AFW'])

    Returns:
        list: List of HTML components for benchmark selection
    """
    components = []

    if include_global:
        # Global benchmark selection dropdown
        # Apply dynamic exclusions from default selection
        all_codes = get_all_global_benchmark_codes()
        if exclude_from_default:
            default_codes = [code for code in all_codes if code not in exclude_from_default]
        else:
            default_codes = all_codes
        
        components.append(html.Div([
            html.Label("Regional Benchmarks:", className="dropdown-label"),
            html.Div([
                dcc.Dropdown(
                    id=global_id,
                    options=get_global_benchmark_dropdown_options(),
                    value=default_codes,
                    multi=True,
                    placeholder="Select regions to compare...",
                    className="country-benchmark-dropdown"
                )
            ], className="dropdown-group")
        ], className="country-benchmark-selector-container"))

    if include_regional:
        # Regional benchmark selection checkboxes
        components.append(html.Div([
            html.Label("Regional Benchmarks:", className="checkbox-label"),
            html.Div([
                dcc.Checklist(
                    id=regional_id,
                    options=get_benchmark_options(),
                    value=[],  # No benchmarks selected by default
                    className="benchmark-checkboxes",
                    inline=True
                )
            ], className="checkbox-group")
        ], className="benchmark-selector-container"))

    if include_country:
        # Country benchmark selection dropdown
        components.append(html.Div([
            html.Label("Country Benchmarks:", className="dropdown-label"),
            html.Div([
                dcc.Dropdown(
                    id=country_id,
                    options=[],  # Will be populated by callback
                    value=[],
                    multi=True,
                    placeholder="Select countries to compare...",
                    className="country-benchmark-dropdown"
                )
            ], className="dropdown-group")
        ], className="country-benchmark-selector-container"))

    return components


def create_combined_benchmark_selector(dropdown_id, default_regional_codes=None):
    """
    Create a combined benchmark selector that includes both countries and regions in a single dropdown.
    Countries are listed first alphabetically, followed by regional benchmarks at the end.
    
    Args:
        dropdown_id (str): ID for the combined benchmark dropdown
        default_regional_codes (list): List of regional codes to select by default (e.g., ['SSA']) - now handled by callback
        
    Returns:
        html.Div: Combined benchmark selector component
    """
    return html.Div([
        html.Label("Benchmarks:", className="dropdown-label"),
        html.Div([
            dcc.Dropdown(
                id=dropdown_id,
                options=[],  # Will be populated by callback with countries + regions
                value=[],    # Will be set by callback
                multi=True,
                placeholder="Select countries or regions to compare...",
                className="country-benchmark-dropdown"
            )
        ], className="dropdown-group")
    ], className="country-benchmark-selector-container")


def create_download_button(download_id):
    """
    Create a download data button component
    
    Args:
        download_id (str): Unique ID for the download component (e.g., 'urban-pop-projections-download')
        
    Returns:
        html.Div: Download button component with dcc.Download
    """
    return html.Div([
        dbc.Button(
            [html.I(className="fas fa-download me-2"), "Download Data"],
            id=f"{download_id}-button",
            color="primary",
            size="sm",
            className="download-data-button",
            n_clicks=0
        ),
        dcc.Download(id=download_id)
    ], className="download-button-container")


def create_download_trigger_button(download_id):
    """
    Create only the visible download trigger button (no dcc.Download component).

    Args:
        download_id (str): Base download id (e.g., 'urban-population-projections-download')

    Returns:
        dbc.Button: Button element with id `{download_id}-button`.
    """
    return dbc.Button(
        [html.I(className="fas fa-download me-2"), "Download Data"],
        id=f"{download_id}-button",
        color="primary",
        size="sm",
        className="download-data-button",
        n_clicks=0
    )


def create_download_component(download_id):
    """
    Create only the dcc.Download component for a given download id.

    Args:
        download_id (str): ID for the dcc.Download component.

    Returns:
        dcc.Download: Download component with the given id.
    """
    return dcc.Download(id=download_id)


def create_methodological_note_button():
    """
    Create a methodological note download button component
    
    Returns:
        html.A: Methodological note button as a download link
    """
    return html.A([
        dbc.Button(
            [html.I(className="fas fa-file-alt me-2"), "Methodological Note"],
            color="primary",
            size="sm",
            className="download-data-button",
        )
    ], 
    href="/assets/documents/SSA DRM Dashboard - Methodological Note.docx",
    download="SSA_DRM_Dashboard_Methodological_Note.docx",
    className="download-button-container"
    )


def create_city_platform_button(href: str = "https://www.google.com"):
    """
    Create a styled action button that links to an external city-level platform.

    Args:
        href (str): URL to navigate to when the button is clicked.

    Returns:
        html.A: Anchor-wrapped button linking to the provided href.
    """
    return html.A([
        dbc.Button(
            [html.I(className="fas fa-city me-2"), "City-level Platform"],
            color="primary",
            size="sm",
            className="download-data-button",
        )
    ], href=href, target="_blank", rel="noopener noreferrer", className="download-button-container")


def create_absolute_relative_selector(radio_id):
    """
    Create radio button selector for Absolute vs Relative view
    
    Args:
        radio_id (str): Unique ID for the radio button component
        
    Returns:
        html.Div: Radio button selector component
    """
    return html.Div([
        html.Label("Display Mode:", className="filter-label"),
        dcc.RadioItems(
            id=radio_id,
            options=[
                {'label': ' Absolute', 'value': 'absolute'},
                {'label': ' Relative (% of population)', 'value': 'relative'}
            ],
            value='absolute',
            className="radio-buttons",
            inline=True
        )
    ], className="filter-container")