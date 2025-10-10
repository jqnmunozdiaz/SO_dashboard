"""
Callbacks for historical disasters functionality
"""

from dash import Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from ..utils.data_loader import load_disaster_data
from ..utils.chart_helpers import create_disaster_timeline, create_disaster_map


def register_callbacks(app):
    """Register all disaster-related callbacks"""
    
    @app.callback(
        Output('disaster-country-dropdown', 'options'),
        Input('main-tabs', 'active_tab')
    )
    def update_disaster_country_options(active_tab):
        """Update country dropdown options for disaster tab"""
        if active_tab == 'disasters':
            # Load available countries from disaster data
            countries = [
                {'label': 'Nigeria', 'value': 'NGA'},
                {'label': 'Kenya', 'value': 'KEN'},
                {'label': 'Ethiopia', 'value': 'ETH'},
                {'label': 'Ghana', 'value': 'GHA'},
                {'label': 'Tanzania', 'value': 'TZA'},
                {'label': 'Uganda', 'value': 'UGA'},
                {'label': 'Mozambique', 'value': 'MOZ'},
                {'label': 'Madagascar', 'value': 'MDG'},
                {'label': 'Cameroon', 'value': 'CMR'},
                {'label': 'Mali', 'value': 'MLI'},
            ]
            return countries
        return []
    
    @app.callback(
        Output('disaster-type-dropdown', 'options'),
        Input('main-tabs', 'active_tab')
    )
    def update_disaster_type_options(active_tab):
        """Update disaster type dropdown options"""
        if active_tab == 'disasters':
            disaster_types = [
                {'label': 'Flood', 'value': 'flood'},
                {'label': 'Drought', 'value': 'drought'},
                {'label': 'Storm', 'value': 'storm'},
                {'label': 'Earthquake', 'value': 'earthquake'},
                {'label': 'Wildfire', 'value': 'wildfire'},
                {'label': 'Epidemic', 'value': 'epidemic'},
                {'label': 'Volcanic Activity', 'value': 'volcanic'},
            ]
            return disaster_types
        return []
    
    @app.callback(
        Output('disaster-timeline-chart', 'figure'),
        [Input('disaster-country-dropdown', 'value'),
         Input('disaster-type-dropdown', 'value'),
         Input('disaster-year-slider', 'value')]
    )
    def update_disaster_timeline(countries, disaster_types, year_range):
        """Update disaster timeline chart"""
        # Placeholder data - replace with actual data loading
        sample_data = pd.DataFrame({
            'year': [2020, 2021, 2022, 2023] * 3,
            'country': ['Nigeria', 'Nigeria', 'Nigeria', 'Nigeria',
                       'Kenya', 'Kenya', 'Kenya', 'Kenya',
                       'Ethiopia', 'Ethiopia', 'Ethiopia', 'Ethiopia'],
            'disaster_count': [15, 12, 18, 20, 8, 10, 12, 14, 10, 8, 15, 17],
            'affected_population': [1000000, 800000, 1200000, 1500000,
                                  500000, 600000, 700000, 800000,
                                  600000, 400000, 900000, 1100000]
        })
        
        fig = px.line(
            sample_data, 
            x='year', 
            y='disaster_count', 
            color='country',
            title='Historical Disaster Trends',
            labels={'disaster_count': 'Number of Disasters', 'year': 'Year'}
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16
        )
        
        return fig
    
    @app.callback(
        Output('disaster-map', 'figure'),
        [Input('disaster-country-dropdown', 'value'),
         Input('disaster-type-dropdown', 'value'),
         Input('disaster-year-slider', 'value')]
    )
    def update_disaster_map(countries, disaster_types, year_range):
        """Update disaster map visualization"""
        # Placeholder choropleth map
        sample_countries = ['NGA', 'KEN', 'ETH', 'GHA', 'TZA']
        sample_values = [25, 18, 22, 12, 16]
        
        fig = go.Figure(data=go.Choropleth(
            locations=sample_countries,
            z=sample_values,
            locationmode='ISO-3',
            colorscale='Reds',
            text=[f'{val} disasters' for val in sample_values],
            colorbar_title="Disaster Count"
        ))
        
        fig.update_layout(
            title_text='Disaster Distribution Map',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                scope='africa'
            ),
            title_font_size=16
        )
        
        return fig
    
    @app.callback(
        Output('disaster-impact-chart', 'figure'),
        [Input('disaster-country-dropdown', 'value'),
         Input('disaster-type-dropdown', 'value'),
         Input('disaster-year-slider', 'value')]
    )
    def update_disaster_impact_chart(countries, disaster_types, year_range):
        """Update disaster impact statistics chart"""
        # Placeholder data
        impact_data = pd.DataFrame({
            'disaster_type': ['Flood', 'Drought', 'Storm', 'Earthquake'],
            'affected_population': [5000000, 3500000, 2000000, 800000],
            'economic_damage': [2500, 1800, 1200, 900]  # in millions USD
        })
        
        fig = px.bar(
            impact_data,
            x='disaster_type',
            y='affected_population',
            title='Impact by Disaster Type',
            labels={'affected_population': 'Affected Population', 'disaster_type': 'Disaster Type'}
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=14
        )
        
        return fig