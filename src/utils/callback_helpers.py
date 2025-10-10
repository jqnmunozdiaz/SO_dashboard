"""
Utility functions for error handling in callbacks
"""

import plotly.graph_objects as go
import pandas as pd
from functools import wraps


def handle_callback_errors(default_title="No Data Available"):
    """
    Decorator to handle callback errors gracefully
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                # Return empty figure with error message
                fig = go.Figure()
                fig.update_layout(
                    title=f"{default_title} - Error: {str(e)[:100]}",
                    xaxis_title="",
                    yaxis_title="",
                    showlegend=False,
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font={'color': '#2c3e50'}
                )
                return fig
        return wrapper
    return decorator


def safe_filter_data(data, countries=None, disaster_types=None, year_range=None):
    """
    Safely filter data with None checks
    """
    if data is None or data.empty:
        return pd.DataFrame()
    
    filtered_data = data.copy()
    
    # Filter by countries
    if countries and len(countries) > 0:
        if 'country_code' in filtered_data.columns:
            filtered_data = filtered_data[filtered_data['country_code'].isin(countries)]
        elif 'country' in filtered_data.columns:
            # Convert country codes to names if needed
            country_code_to_name = {
                'NGA': 'Nigeria', 'KEN': 'Kenya', 'ETH': 'Ethiopia',
                'GHA': 'Ghana', 'TZA': 'Tanzania', 'UGA': 'Uganda',
                'MOZ': 'Mozambique', 'MDG': 'Madagascar', 'CMR': 'Cameroon',
                'MLI': 'Mali', 'RWA': 'Rwanda', 'SEN': 'Senegal',
                'BFA': 'Burkina Faso', 'CIV': 'Ivory Coast'
            }
            country_names = [country_code_to_name.get(code, code) for code in countries]
            filtered_data = filtered_data[filtered_data['country'].isin(country_names)]
    
    # Filter by disaster types
    if disaster_types and len(disaster_types) > 0 and 'disaster_type' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['disaster_type'].isin(disaster_types)]
    
    # Filter by year range
    if year_range and len(year_range) == 2 and 'year' in filtered_data.columns:
        filtered_data = filtered_data[
            (filtered_data['year'] >= year_range[0]) & 
            (filtered_data['year'] <= year_range[1])
        ]
    
    return filtered_data


def create_empty_figure(title="No Data Available", subtitle=""):
    """
    Create an empty figure with a message
    """
    fig = go.Figure()
    fig.update_layout(
        title=f"{title}<br><span style='font-size:12px'>{subtitle}</span>",
        xaxis_title="",
        yaxis_title="",
        showlegend=False,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': '#2c3e50'},
        title_font_size=16
    )
    return fig


def safe_aggregate_data(data, group_by, agg_dict):
    """
    Safely aggregate data with error handling
    """
    try:
        if data.empty:
            return pd.DataFrame()
        
        # Check if all group_by columns exist
        missing_cols = [col for col in group_by if col not in data.columns]
        if missing_cols:
            return pd.DataFrame()
        
        # Check if all aggregation columns exist
        missing_agg_cols = [col for col in agg_dict.keys() if col not in data.columns]
        if missing_agg_cols:
            # Remove missing columns from aggregation
            agg_dict = {k: v for k, v in agg_dict.items() if k not in missing_agg_cols}
        
        if not agg_dict:
            return pd.DataFrame()
        
        return data.groupby(group_by).agg(agg_dict).reset_index()
    
    except Exception as e:
        return pd.DataFrame()


def validate_inputs(*args):
    """
    Validate callback inputs and return safe values
    """
    safe_args = []
    for arg in args:
        if arg is None:
            safe_args.append([])
        elif isinstance(arg, (list, tuple)):
            safe_args.append(list(arg))
        else:
            safe_args.append(arg)
    return safe_args