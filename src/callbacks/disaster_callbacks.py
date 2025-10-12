"""
Callbacks for historical disasters functionality
"""

from dash import Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

try:
    from ..utils.data_loader import load_emdat_data
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.data_loader import load_emdat_data


def register_callbacks(app):
    """Register all disaster-related callbacks"""
    
    @app.callback(
        Output('disaster-type-dropdown', 'options'),
        Input('main-tabs', 'active_tab')
    )
    def update_disaster_type_options(active_tab):
        """Update disaster type dropdown options"""
        if active_tab == 'disasters':
            try:
                # Load real disaster data to get available disaster types
                disaster_data = load_emdat_data()
                if 'Disaster Type' in disaster_data.columns:
                    # Get unique disaster types from real data (already human-readable)
                    unique_types = disaster_data['Disaster Type'].dropna().unique()
                    
                    # Create dropdown options using the disaster types as-is
                    disaster_types = [
                        {'label': dtype, 'value': dtype}
                        for dtype in unique_types
                        if dtype and str(dtype) != 'nan'
                    ]
                    
                    # Sort by label
                    disaster_types = sorted(disaster_types, key=lambda x: x['label'])
                    return disaster_types
                else:
                    raise ValueError("disaster_type column not found")
            except Exception as e:
                # Raise error instead of providing fallback data
                raise Exception(f"Failed to load disaster type options: {str(e)}")
        return []
    
    # Additional callbacks for charts will be added here as needed