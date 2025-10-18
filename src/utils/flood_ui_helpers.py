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
            className='year-radio-buttons',
            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
        )
    ], className='year-filter-container')


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
                {'label': ' 1-in-100 year', 'value': '1in100'},
                {'label': ' 1-in-10 year', 'value': '1in10'},
                {'label': ' 1-in-5 year', 'value': '1in5'}
            ],
            value=['1in100', '1in10', '1in5'],  # All selected by default
            className='benchmark-checkboxes',
            inline=True,
            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
        )
    ], className='year-filter-container')
