"""
Shared utility functions for creating consistent chart components
"""

import plotly.graph_objects as go
import pandas as pd


def create_empty_chart(chart_type='bar', title="No Data Available", xaxis_title="", yaxis_title="", yaxis_range=None):
    """
    Create an empty chart with consistent styling for error states

    Args:
        chart_type: Type of chart ('bar', 'line', 'scatter', etc.)
        title: Title to display
        xaxis_title: X-axis label
        yaxis_title: Y-axis label
        yaxis_range: Optional y-axis range [min, max]

    Returns:
        plotly.graph_objects.Figure: Empty figure with error styling
    """
    fig = go.Figure()

    # Add empty trace based on chart type
    if chart_type == 'bar':
        fig.add_trace(go.Bar(x=[], y=[], name="No Data"))
    elif chart_type == 'line':
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name="No Data"))
    elif chart_type == 'scatter':
        fig.add_trace(go.Scatter(x=[], y=[], mode='markers', name="No Data"))
    else:
        # Default empty trace
        fig.add_trace(go.Bar(x=[], y=[], name="No Data"))

    # Update layout with consistent styling
    layout_updates = {
        'title': title,
        'xaxis_title': xaxis_title,
        'yaxis_title': yaxis_title,
        'showlegend': False,
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {'color': '#2c3e50'},
        'title_font_size': 16,
        'xaxis': {
            'showgrid': False,
            'gridwidth': 0,
            'gridcolor': '#e5e7eb'
        },
        'yaxis': {
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': '#e5e7eb',
            'zeroline': True,
            'zerolinewidth': 1,
            'zerolinecolor': '#e5e7eb'
        }
    }

    if yaxis_range:
        layout_updates['yaxis']['range'] = yaxis_range

    fig.update_layout(**layout_updates)

    return fig


def create_error_chart(error_message, chart_type='line', xaxis_title="", yaxis_title="", yaxis_range=None, title=None):
    """
    Create a chart displaying an error message with annotation

    Args:
        error_message: Error message to display as annotation
        chart_type: Type of chart ('bar', 'line', 'scatter', etc.)
        xaxis_title: X-axis label
        yaxis_title: Y-axis label
        yaxis_range: Optional y-axis range [min, max]
        title: Optional custom title (defaults to error message)

    Returns:
        plotly.graph_objects.Figure: Figure with error message annotation
    """
    fig = go.Figure()

    # Add empty trace based on chart type
    if chart_type == 'bar':
        fig.add_trace(go.Bar(x=[], y=[], name="No Data"))
    elif chart_type == 'line':
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name="No Data"))
    elif chart_type == 'scatter':
        fig.add_trace(go.Scatter(x=[], y=[], mode='markers', name="No Data"))
    else:
        # Default empty trace
        fig.add_trace(go.Scatter(x=[], y=[], mode='lines', name="No Data"))

    # Add error message annotation
    fig.add_annotation(
        text=error_message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle',
        showarrow=False,
        font=dict(size=16, color="gray")
    )

    # Update layout with consistent styling
    layout_updates = {
        'title': title if title else error_message,
        'xaxis_title': xaxis_title,
        'yaxis_title': yaxis_title,
        'showlegend': False,
        'plot_bgcolor': 'white',
        'paper_bgcolor': 'white',
        'font': {'color': '#2c3e50'},
        'title_font_size': 16,
        'xaxis': {
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': '#e5e7eb'
        },
        'yaxis': {
            'showgrid': True,
            'gridwidth': 1,
            'gridcolor': '#e5e7eb',
            'zeroline': True,
            'zerolinewidth': 1,
            'zerolinecolor': '#e5e7eb'
        }
    }

    if yaxis_range:
        layout_updates['yaxis']['range'] = yaxis_range

    fig.update_layout(**layout_updates)

    return fig
