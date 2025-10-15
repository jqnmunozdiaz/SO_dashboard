"""
UI component helpers for creating reusable dashboard components
"""

from dash import dcc, html

try:
    from .benchmark_config import get_benchmark_options
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.benchmark_config import get_benchmark_options


def create_benchmark_selectors(regional_id, country_id, include_regional=True, include_country=True):
    """
    Create benchmark selection UI components for regional and country benchmarks

    Args:
        regional_id (str): ID for the regional benchmark checklist
        country_id (str): ID for the country benchmark dropdown
        include_regional (bool): Whether to include regional benchmark selector
        include_country (bool): Whether to include country benchmark selector

    Returns:
        list: List of HTML components for benchmark selection
    """
    components = []

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