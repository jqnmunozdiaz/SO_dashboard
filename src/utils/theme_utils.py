"""
Theme utilities for the dashboard
Provides theme-aware styling configurations for charts and components
"""

def get_chart_theme(is_dark=False):
    """
    Get plotly chart theme configuration based on dark/light mode
    
    Args:
        is_dark (bool): Whether to use dark theme
        
    Returns:
        dict: Plotly layout configuration
    """
    if is_dark:
        return {
            'paper_bgcolor': '#2d3748',
            'plot_bgcolor': '#374151',
            'font': {'color': '#f8f9fa', 'family': 'Arial, sans-serif'},
            'title': {'font': {'color': '#f8f9fa', 'size': 16}},
            'xaxis': {
                'gridcolor': '#4a5568',
                'zerolinecolor': '#4a5568',
                'color': '#f8f9fa',
                'tickfont': {'color': '#f8f9fa'},
                'titlefont': {'color': '#f8f9fa'}
            },
            'yaxis': {
                'gridcolor': '#4a5568',
                'zerolinecolor': '#4a5568', 
                'color': '#f8f9fa',
                'tickfont': {'color': '#f8f9fa'},
                'titlefont': {'color': '#f8f9fa'}
            },
            'colorway': [
                '#63b3ed', '#4fd1c7', '#f093fb', '#f6e05e', 
                '#fc8181', '#a78bfa', '#68d391', '#fbb6ce',
                '#90cdf4', '#81e6d9', '#c6f6d5', '#fed7d7'
            ],
            'legend': {'font': {'color': '#f8f9fa'}},
            'hoverlabel': {
                'bgcolor': '#374151',
                'bordercolor': '#4a5568',
                'font': {'color': '#f8f9fa'}
            }
        }
    else:
        return {
            'paper_bgcolor': 'white',
            'plot_bgcolor': 'white',
            'font': {'color': '#2c3e50', 'family': 'Arial, sans-serif'},
            'title': {'font': {'color': '#2c3e50', 'size': 16}},
            'xaxis': {
                'gridcolor': '#e2e8f0',
                'zerolinecolor': '#e2e8f0',
                'color': '#2c3e50',
                'tickfont': {'color': '#2c3e50'},
                'titlefont': {'color': '#2c3e50'}
            },
            'yaxis': {
                'gridcolor': '#e2e8f0',
                'zerolinecolor': '#e2e8f0',
                'color': '#2c3e50',
                'tickfont': {'color': '#2c3e50'},
                'titlefont': {'color': '#2c3e50'}
            },
            'colorway': [
                '#3498db', '#2ecc71', '#e74c3c', '#f39c12',
                '#9b59b6', '#1abc9c', '#34495e', '#e67e22',
                '#95a5a6', '#f1c40f', '#e67e22', '#8e44ad'
            ],
            'legend': {'font': {'color': '#2c3e50'}},
            'hoverlabel': {
                'bgcolor': 'white',
                'bordercolor': '#bdc3c7',
                'font': {'color': '#2c3e50'}
            }
        }


def get_map_theme(is_dark=False):
    """
    Get map-specific theme configuration
    
    Args:
        is_dark (bool): Whether to use dark theme
        
    Returns:
        dict: Map styling configuration
    """
    if is_dark:
        return {
            'style': 'carto-darkmatter',
            'paper_bgcolor': '#2d3748',
            'geo': {
                'bgcolor': '#374151',
                'showframe': False,
                'showcoastlines': True,
                'coastlinecolor': '#4a5568',
                'projection': {'type': 'natural earth'}
            }
        }
    else:
        return {
            'style': 'carto-positron',
            'paper_bgcolor': 'white',
            'geo': {
                'bgcolor': 'white',
                'showframe': False,
                'showcoastlines': True,
                'coastlinecolor': '#bdc3c7',
                'projection': {'type': 'natural earth'}
            }
        }


def get_card_style(is_dark=False):
    """
    Get card styling based on theme
    
    Args:
        is_dark (bool): Whether to use dark theme
        
    Returns:
        dict: CSS style dict for cards
    """
    if is_dark:
        return {
            'backgroundColor': '#2d3748',
            'borderColor': '#4a5568',
            'color': '#f8f9fa'
        }
    else:
        return {
            'backgroundColor': 'white',
            'borderColor': '#bdc3c7',
            'color': '#2c3e50'
        }


def get_input_style(is_dark=False):
    """
    Get input/dropdown styling based on theme
    
    Args:
        is_dark (bool): Whether to use dark theme
        
    Returns:
        dict: CSS style dict for inputs
    """
    if is_dark:
        return {
            'backgroundColor': '#374151',
            'borderColor': '#4a5568',
            'color': '#f8f9fa'
        }
    else:
        return {
            'backgroundColor': 'white',
            'borderColor': '#bdc3c7',
            'color': '#2c3e50'
        }


def merge_chart_theme(figure_dict, is_dark=False):
    """
    Merge theme configuration into existing figure dictionary
    
    Args:
        figure_dict (dict): Existing plotly figure dict
        is_dark (bool): Whether to use dark theme
        
    Returns:
        dict: Updated figure dict with theme applied
    """
    theme_config = get_chart_theme(is_dark)
    
    if 'layout' not in figure_dict:
        figure_dict['layout'] = {}
    
    # Merge theme config with existing layout
    for key, value in theme_config.items():
        if key in ['xaxis', 'yaxis'] and key in figure_dict['layout']:
            # Merge axis configs
            figure_dict['layout'][key].update(value)
        else:
            figure_dict['layout'][key] = value
    
    return figure_dict


# Common color palettes for different themes
DISASTER_COLORS_LIGHT = {
    'Drought': '#e74c3c',
    'Flood': '#3498db', 
    'Storm': '#9b59b6',
    'Earthquake': '#f39c12',
    'Wildfire': '#e67e22',
    'Epidemic': '#2ecc71',
    'Other': '#95a5a6'
}

DISASTER_COLORS_DARK = {
    'Drought': '#fc8181',
    'Flood': '#63b3ed',
    'Storm': '#a78bfa', 
    'Earthquake': '#f6e05e',
    'Wildfire': '#fbb6ce',
    'Epidemic': '#68d391',
    'Other': '#a0aec0'
}

def get_disaster_colors(is_dark=False):
    """Get disaster type color mapping based on theme"""
    return DISASTER_COLORS_DARK if is_dark else DISASTER_COLORS_LIGHT