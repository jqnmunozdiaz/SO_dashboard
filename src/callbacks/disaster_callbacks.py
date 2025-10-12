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
    
    @app.callback(
        Output('disaster-frequency-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('disaster-type-dropdown', 'value')],
        prevent_initial_call=False
    )
    def update_disaster_frequency_chart(selected_country, disaster_types):
        """Create bar chart showing frequency of historical disasters by disaster type since 1975"""
        try:
            # Load real EM-DAT data
            emdat_data = load_emdat_data()
            
            # Filter data based on inputs using actual column names
            if selected_country and 'ISO' in emdat_data.columns:
                emdat_data = emdat_data[emdat_data['ISO'] == selected_country]
            if disaster_types and len(disaster_types) > 0 and 'Disaster Type' in emdat_data.columns:
                emdat_data = emdat_data[emdat_data['Disaster Type'].isin(disaster_types)]
            
            # Count frequency by disaster type
            if emdat_data.empty:
                frequency_data = pd.DataFrame({
                    'Disaster Type': ['No Data'],
                    'Event Count': [0]
                })
                title_suffix = "No data available for selected filters"
            else:
                frequency_data = emdat_data.groupby('Disaster Type').size().reset_index(name='Event Count')
                frequency_data = frequency_data.sort_values('Event Count', ascending=False)
                
                # Create title with country info
                if selected_country:
                    country_name = selected_country  # You could map this to full country name if needed
                    title_suffix = f"for {country_name} since 1975"
                else:
                    title_suffix = "for Sub-Saharan Africa since 1975"
                
        except Exception as e:
            # Return empty data on error
            frequency_data = pd.DataFrame({
                'Disaster Type': ['Error'],
                'Event Count': [0]
            })
            title_suffix = f"Error loading data: {str(e)[:50]}"
        
        # Create bar chart
        fig = px.bar(
            frequency_data,
            x='Disaster Type',
            y='Event Count',
            title=f'Frequency of Historical Events by Disaster Type<br><sub>{title_suffix} | Data Source: EM-DAT</sub>',
            labels={'Event Count': 'Number of Events', 'Disaster Type': 'Disaster Type'},
            color='Event Count',
            color_continuous_scale='Reds'
        )
        
        # Update layout styling
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
            xaxis_tickangle=-45,
            showlegend=False,
            coloraxis_showscale=False,
            yaxis=dict(
                dtick=1 if frequency_data['Event Count'].max() <= 10 else None,
                rangemode='tozero'
            )
        )
        
        # Update bar styling
        fig.update_traces(
            marker_line_color='#295e84',
            marker_line_width=1,
            hovertemplate='<b>%{x}</b><br>Events: %{y}<extra></extra>'
        )
        
        return fig