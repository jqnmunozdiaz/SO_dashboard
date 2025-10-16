"""
Utility functions for error handling in callbacks
"""

import pandas as pd
from functools import wraps

# Use the shared error/chart helper to keep UI consistent
from .component_helpers import create_error_chart


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
                # Use the centralized create_error_chart so all callbacks show
                # errors with the same look-and-feel.
                err_msg = f"{default_title} - {str(e)[:200]}"
                return create_error_chart(error_message=err_msg, chart_type='line', title=default_title)
        return wrapper
    return decorator


def safe_filter_data(data, countries=None, disaster_types=None):
    """
    Safely filter EM-DAT data using actual column names
    
    Args:
        data: DataFrame with EM-DAT structure (ISO, Disaster Type, Year, Total Deaths, Total Affected)
        countries: List of ISO country codes (e.g., ['NGA', 'KEN'])
        disaster_types: List of disaster types (e.g., ['Flood', 'Storm'])
    """
    if data is None or data.empty:
        return pd.DataFrame()
    
    filtered_data = data.copy()
    
    # Filter by countries using actual ISO column
    if countries and len(countries) > 0 and 'ISO' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['ISO'].isin(countries)]
    
    # Filter by disaster types using actual Disaster Type column
    if disaster_types and len(disaster_types) > 0 and 'Disaster Type' in filtered_data.columns:
        filtered_data = filtered_data[filtered_data['Disaster Type'].isin(disaster_types)]
    
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
    Safely aggregate EM-DAT data with error handling
    
    Args:
        data: DataFrame with EM-DAT structure
        group_by: List of columns to group by (e.g., ['Disaster Type'], ['ISO', 'Year'])
        agg_dict: Dict of aggregations (e.g., {'Total Deaths': 'sum', 'Total Affected': 'sum'})
    """
    try:
        if data.empty:
            return pd.DataFrame()
        
        # Check if all group_by columns exist in EM-DAT data
        missing_cols = [col for col in group_by if col not in data.columns]
        if missing_cols:
            return pd.DataFrame()
        
        # Check if all aggregation columns exist in EM-DAT data
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