"""
Callbacks for disaster frequency visualization - "Frequency by Type" subtab
Shows bar chart of disaster event counts grouped by disaster type for selected country
"""

from dash import Input, Output
import plotly.express as px
import pandas as pd
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ...utils.data_loader import load_emdat_data
    from ...utils.country_utils import load_subsaharan_countries_dict
    from ...utils.color_utils import get_disaster_color, DISASTER_COLORS
    from config.settings import DATA_CONFIG
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_emdat_data
    from src.utils.country_utils import load_subsaharan_countries_dict
    from src.utils.color_utils import get_disaster_color, DISASTER_COLORS
    from config.settings import DATA_CONFIG


def setup_frequency_by_type_callbacks(app):
    """Setup callbacks for the 'Frequency by Type' disaster chart"""
    
    @app.callback(
        Output('disaster-frequency-chart', 'figure'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def generate_disaster_frequency_by_type_chart(selected_country):
        """Generate bar chart showing frequency of historical disasters by disaster type since configured start year"""
        try:
            # Load real EM-DAT data
            emdat_data = load_emdat_data()
            
            # Load country mapping for ISO code to full name conversion
            countries_dict = load_subsaharan_countries_dict()
            
            # Filter data based on country input only
            if selected_country and 'ISO' in emdat_data.columns:
                emdat_data = emdat_data[emdat_data['ISO'] == selected_country]
            
            # Count frequency by disaster type
            if emdat_data.empty:
                frequency_data = pd.DataFrame({
                    'Disaster Type': ['No Data'],
                    'Event Count': [0]
                })
                title_suffix = "No data available for selected country"
            else:
                frequency_data = emdat_data.groupby('Disaster Type').size().reset_index(name='Event Count')
                frequency_data = frequency_data.sort_values('Event Count', ascending=False)
                
                # Add colors for each disaster type
                frequency_data['Color'] = frequency_data['Disaster Type'].apply(
                    lambda x: get_disaster_color(x, DISASTER_COLORS)
                )
                
                # Create title with country info - map ISO code to full country name
                if selected_country:
                    country_name = countries_dict.get(selected_country, selected_country)
                    title_suffix = f"{country_name}"
                else:
                    raise ValueError("No country selected for disaster frequency analysis")
                
        except Exception as e:
            # Return empty data on error
            frequency_data = pd.DataFrame({
                'Disaster Type': ['Error'],
                'Event Count': [0],
                'Color': ['#e74c3c']
            })
            title_suffix = f"Error loading data: {str(e)[:50]}"
        
        # Create bar chart with custom colors
        fig = px.bar(
            frequency_data,
            x='Disaster Type',
            y='Event Count',
            title=f'<b>{title_suffix}</b> | Frequency of Historical Events by Disaster Type ({DATA_CONFIG["analysis_period"]})<br><sub>Data Source: EM-DAT</sub>',
            labels={'Event Count': 'Number of Events', 'Disaster Type': 'Disaster Type'},
            color='Disaster Type',
            color_discrete_map={
            row['Disaster Type']: row['Color'] 
            for _, row in frequency_data.iterrows()
            }
        )
        
        # Update layout styling
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
            xaxis_tickangle=0,
            showlegend=False,
            yaxis=dict(
                dtick=1 if frequency_data['Event Count'].max() <= 10 else None,
                rangemode='tozero',
                showgrid=True,
                gridwidth=1,
                gridcolor='#e5e7eb',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='#e5e7eb'
            ),
            margin=dict(b=80)
        )
        
        # Update bar styling
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            hovertemplate='<b>%{x}</b><br>Events: %{y}<extra></extra>'
        )
        
        return fig