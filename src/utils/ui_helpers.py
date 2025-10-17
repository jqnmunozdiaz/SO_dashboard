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