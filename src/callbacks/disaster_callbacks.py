"""
Callbacks for historical disasters functionality
"""

from dash import Input, Output, callback, dcc, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ..utils.data_loader import load_emdat_data
    from ..utils.country_utils import load_subsaharan_countries_dict
    from ..utils.color_utils import get_disaster_color, DISASTER_COLORS
    from config.settings import DATA_CONFIG
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.data_loader import load_emdat_data
    from src.utils.country_utils import load_subsaharan_countries_dict
    from src.utils.color_utils import get_disaster_color, DISASTER_COLORS
    from config.settings import DATA_CONFIG


def register_callbacks(app):
    """Register all disaster-related callbacks"""
    
    @app.callback(
        Output('disaster-chart-container', 'children'),
        [Input('disaster-subtabs', 'active_tab'),
         Input('main-country-filter', 'value')]
    )
    def render_disaster_chart(active_subtab, selected_country):
        """Render different disaster charts based on selected subtab"""
        if active_subtab == 'disaster-frequency':
            return html.Div([
                dcc.Graph(id="disaster-frequency-chart")
            ], style={
                'background': 'white',
                'padding': '1.5rem',
                'border-radius': '0.5rem',
                'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                'border': '1px solid #e5e7eb'
            })
        elif active_subtab == 'disaster-timeline':
            return html.Div([
                dcc.Graph(id="disaster-timeline-chart")
            ], style={
                'background': 'white',
                'padding': '1.5rem',
                'border-radius': '0.5rem',
                'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                'border': '1px solid #e5e7eb'
            })
        elif active_subtab == 'disaster-affected':
            return html.Div([
                dcc.Graph(id="disaster-affected-chart")
            ], style={
                'background': 'white',
                'padding': '1.5rem',
                'border-radius': '0.5rem',
                'box-shadow': '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
                'border': '1px solid #e5e7eb'
            })
        else:
            return html.Div("Select a chart type above")
    
    @app.callback(
        Output('disaster-frequency-chart', 'figure'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def update_disaster_frequency_chart(selected_country):
        """Create bar chart showing frequency of historical disasters by disaster type since configured start year"""
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
            marker_line_color='#295e84',
            marker_line_width=1,
            hovertemplate='<b>%{x}</b><br>Events: %{y}<extra></extra>'
        )
        
        return fig
    
    @app.callback(
        Output('disaster-timeline-chart', 'figure'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def update_disaster_timeline_chart(selected_country):
        """Create stacked bar chart showing disasters by 5-year intervals since configured start year"""
        try:
            # Load real EM-DAT data
            emdat_data = load_emdat_data()
            
            # Load country mapping for ISO code to full name conversion
            countries_dict = load_subsaharan_countries_dict()
            
            # Filter data based on country input only
            if selected_country and 'ISO' in emdat_data.columns:
                emdat_data = emdat_data[emdat_data['ISO'] == selected_country]
            
            # Create 5-year intervals starting from 1975
            if emdat_data.empty:
                # Create empty data structure
                timeline_data = pd.DataFrame({
                    'Year_Interval': ['1975-1979'],
                    'Disaster Type': ['No Data'],
                    'Event Count': [0]
                })
                title_suffix = "No data available for selected country"
            else:
                # Create 5-year interval bins starting from configured year
                start_year = DATA_CONFIG['emdat_start_year']
                emdat_data['Year_Interval'] = pd.cut(
                    emdat_data['Year'],
                    bins=range(start_year, 2030, 5),
                    labels=[f"{year}-{year+4}" for year in range(start_year, 2025, 5)],
                    include_lowest=True,
                    right=False
                )
                
                # Group by interval and disaster type
                timeline_data = emdat_data.groupby(['Year_Interval', 'Disaster Type']).size().reset_index(name='Event Count')
                
                # Convert interval to string for plotting
                timeline_data['Year_Interval'] = timeline_data['Year_Interval'].astype(str)
                
                # Map ISO code to full country name
                if selected_country:
                    country_name = countries_dict.get(selected_country, selected_country)
                    title_suffix = f"{country_name}"
                else:
                    raise ValueError("No country selected")
                    
        except Exception as e:
            # Return empty data on error
            timeline_data = pd.DataFrame({
                'Year_Interval': ['1975-1979'],
                'Disaster Type': ['Error'],
                'Event Count': [0]
            })
            title_suffix = f"Error loading data"
        
        # Create stacked bar chart with disaster type colors
        fig = px.bar(
            timeline_data,
            x='Year_Interval',
            y='Event Count',
            color='Disaster Type',
            title=f'<b>{title_suffix}</b> | Historical Disasters by 5-Year Intervals ({DATA_CONFIG["analysis_period"]})<br><sub>Data Source: EM-DAT</sub>',
            labels={'Event Count': 'Number of Events', 'Year_Interval': '5-Year Interval'},
            color_discrete_map=DISASTER_COLORS
        )
        
        # Update layout styling
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            xaxis=dict(
                showgrid=False,
                gridwidth=0,
                gridcolor='#e5e7eb',
                tickmode='array',
                tickvals=timeline_data['Year_Interval'].unique(),
                ticktext=[interval.replace('-', ' -<br>') for interval in timeline_data['Year_Interval'].unique()],
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                dtick=1 if timeline_data['Event Count'].max() <= 10 else None,
                rangemode='tozero',
                showgrid=True,
                gridwidth=1,
                gridcolor='#e5e7eb',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='#e5e7eb'
            ),
            margin=dict(b=100, r=150)  # Extra margin for legend
        )
        
        # Update bar styling
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            hovertemplate='<b>%{fullData.name}</b><br>Period: %{x}<br>Events: %{y}<extra></extra>'
        )
        
        return fig
    
    @app.callback(
        Output('disaster-affected-chart', 'figure'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def update_disaster_affected_chart(selected_country):
        """Create stacked bar chart showing total affected population by 5-year intervals since configured start year"""
        try:
            # Load real EM-DAT data
            emdat_data = load_emdat_data()
            
            # Load country mapping for ISO code to full name conversion
            countries_dict = load_subsaharan_countries_dict()
            
            # Filter data based on country input only
            if selected_country and 'ISO' in emdat_data.columns:
                emdat_data = emdat_data[emdat_data['ISO'] == selected_country]
            
            # Create 5-year intervals starting from configured year
            if emdat_data.empty:
                # Create empty data structure
                affected_data = pd.DataFrame({
                    'Year_Interval': ['1975-1979'],
                    'Disaster Type': ['No Data'],
                    'Total Affected': [0]
                })
                title_suffix = "No data available for selected country"
            else:
                # Create 5-year interval bins starting from configured year
                start_year = DATA_CONFIG['emdat_start_year']
                emdat_data['Year_Interval'] = pd.cut(
                    emdat_data['Year'],
                    bins=range(start_year, 2030, 5),
                    labels=[f"{year}-{year+4}" for year in range(start_year, 2025, 5)],
                    include_lowest=True,
                    right=False
                )
                
                # Group by interval and disaster type, sum affected population
                affected_data = emdat_data.groupby(['Year_Interval', 'Disaster Type'])['Total Affected'].sum().reset_index()
                
                # Convert interval to string for plotting
                affected_data['Year_Interval'] = affected_data['Year_Interval'].astype(str)
                
                # Map ISO code to full country name
                if selected_country:
                    country_name = countries_dict.get(selected_country, selected_country)
                    title_suffix = f"{country_name}"
                else:
                    raise ValueError("No country selected")
                    
        except Exception as e:
            # Return empty data on error
            affected_data = pd.DataFrame({
                'Year_Interval': ['1975-1979'],
                'Disaster Type': ['Error'],
                'Total Affected': [0]
            })
            title_suffix = f"Error loading data"
        
        # Create stacked bar chart with disaster type colors
        fig = px.bar(
            affected_data,
            x='Year_Interval',
            y='Total Affected',
            color='Disaster Type',
            title=f'<b>{title_suffix}</b> | Total Affected Population by 5-Year Intervals ({DATA_CONFIG["analysis_period"]})<br><sub>Data Source: EM-DAT</sub>',
            labels={'Total Affected': 'Total Affected Population', 'Year_Interval': '5-Year Interval'},
            color_discrete_map=DISASTER_COLORS
        )
        
        # Update layout styling
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            xaxis=dict(
                showgrid=False,
                gridwidth=0,
                gridcolor='#e5e7eb',
                tickmode='array',
                tickvals=affected_data['Year_Interval'].unique(),
                ticktext=[interval.replace('-', ' -<br>') for interval in affected_data['Year_Interval'].unique()],
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                dtick=1 if affected_data['Total Affected'].max() <= 10 else None,
                rangemode='tozero',
                showgrid=True,
                gridwidth=1,
                gridcolor='#e5e7eb',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='#e5e7eb'
            ),
            margin=dict(b=100, r=150)  # Extra margin for legend
        )
        
        # Update bar styling
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            hovertemplate='<b>%{fullData.name}</b><br>Period: %{x}<br>Affected: %{y:,.0f}<extra></extra>'
        )
        
        return fig