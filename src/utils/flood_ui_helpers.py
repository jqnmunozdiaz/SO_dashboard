"""
Reusable helper functions for creating flood exposure UI components
"""

from dash import html, dcc


def create_flood_type_selector(component_id, default_value=None):
    """
    Create a radio button selector for flood types
    
    Args:
        component_id: Unique ID for the component
        default_value: Default flood type to select (optional)
        
    Returns:
        html.Div containing the flood type selector
    """
    from ..utils.flood_data_loader import get_flood_types
    
    flood_types = get_flood_types()
    default = default_value or flood_types[0]
    
    # Create human-readable labels
    labels = {
        'COASTAL_DEFENDED': 'Coastal (Defended)',
        'FLUVIAL_PLUVIAL_DEFENDED': 'Fluvial & Pluvial (Defended)',
        'COASTAL_UNDEFENDED': 'Coastal (Undefended)',
        'FLUVIAL_PLUVIAL_UNDEFENDED': 'Fluvial & Pluvial (Undefended)'
    }
    
    options = [
        {'label': labels.get(ft, ft), 'value': ft} 
        for ft in flood_types
    ]
    
    return html.Div([
        html.Label('Flood Type:', className='filter-label'),
        dcc.RadioItems(
            id=component_id,
            options=options,
            value=default,
            className='radio-buttons',
            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
        )
    ], className='filter-container')


def get_return_period_colors():
    """
    Get consistent color mapping for return periods
    
    Returns:
        Dictionary mapping return period to color
    """
    return {
        '1in5': '#3b82f6',    # Blue - most frequent
        '1in10': '#f59e0b',   # Orange - medium
        '1in100': '#ef4444'   # Red - least frequent (most severe)
    }


def get_return_period_labels():
    """
    Get human-readable labels for return periods
    
    Returns:
        Dictionary mapping return period codes to labels
    """
    return {
        '1in5': '1-in-5 year',
        '1in10': '1-in-10 year',
        '1in100': '1-in-100 year'
    }


def create_return_period_selector(component_id):
    """
    Create a checkbox selector for return periods
    
    Args:
        component_id: Unique ID for the component
        
    Returns:
        html.Div containing the return period selector
    """
    return html.Div([
        html.Label('Return Periods:', className='filter-label'),
        dcc.Checklist(
            id=component_id,
            options=[
                {'label': ' 1-in-5 year', 'value': '1in5'},
                {'label': ' 1-in-10 year', 'value': '1in10'},
                {'label': ' 1-in-100 year', 'value': '1in100'}
            ],
            value=['1in100', '1in10', '1in5'],  # All selected by default
            className='benchmark-checkboxes',
            inline=True,
            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
        )
    ], className='filter-container')


def create_measurement_type_selector(component_id, default_value='absolute'):
    """
    Create a radio button selector for measurement type (absolute vs relative)
    
    Args:
        component_id: Unique ID for the component
        default_value: Default measurement type ('absolute' or 'relative')
        
    Returns:
        html.Div containing the measurement type selector
    """
    return html.Div([
        html.Label('Measurement Type:', className='filter-label'),
        dcc.RadioItems(
            id=component_id,
            options=[
                {'label': 'Absolute', 'value': 'absolute'},
                {'label': 'Relative (%)', 'value': 'relative'}
            ],
            value=default_value,
            className='radio-buttons',
            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
        )
    ], className='filter-container')


def create_exposure_type_selector(component_id, default_value='built_s'):
    """
    Create a radio button selector for exposure type (Built-up vs Population)
    
    Args:
        component_id: Unique ID for the component
        default_value: Default exposure type ('built_s' or 'pop')
        
    Returns:
        html.Div containing the exposure type selector
    """
    return html.Div([
        html.Label('Exposure Type:', className='filter-label'),
        dcc.RadioItems(
            id=component_id,
            options=[
                {'label': 'Built-up Area', 'value': 'built_s'},
                {'label': 'Population', 'value': 'pop'}
            ],
            value=default_value,
            className='radio-buttons',
            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
        )
    ], className='filter-container')


def get_city_colors():
    """
    Get a list of distinct colors for differentiating cities in charts
    Uses a qualitative color palette suitable for multiple categories
    
    Returns:
        List of color hex codes
    """
    return [
        '#1f77b4',  # Blue
        '#ff7f0e',  # Orange
        '#2ca02c',  # Green
        '#d62728',  # Red
        '#9467bd',  # Purple
        '#8c564b',  # Brown
        '#e377c2',  # Pink
        '#7f7f7f',  # Gray
        '#bcbd22',  # Olive
        '#17becf',  # Cyan
    ]


def create_city_return_period_selector(component_id):
    """
    Create a radio button selector for return periods (single selection)
    Used for city-level flood exposure where only one return period displays at a time
    
    Args:
        component_id: Unique ID for the component
        
    Returns:
        html.Div containing the return period radio selector
    """
    return html.Div([
        html.Label('Return Period:', className='filter-label'),
        dcc.RadioItems(
            id=component_id,
            options=[
                {'label': ' 1-in-5 year', 'value': '1in5'},
                {'label': ' 1-in-10 year', 'value': '1in10'},
                {'label': ' 1-in-100 year', 'value': '1in100'}
            ],
            value='1in100',  # Default to 1-in-100 year
            className='radio-buttons',
            inline=True,
            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
        )
    ], className='filter-container')
