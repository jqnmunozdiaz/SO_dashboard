"""
Callbacks for urbanization trends functionality
"""

from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

try:
    from ..utils.data_loader import create_sample_urbanization_data
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.data_loader import create_sample_urbanization_data


def register_callbacks(app):
    """Register all urbanization-related callbacks"""
    

    
    @app.callback(
        Output('urbanization-trend-chart', 'figure'),
        [Input('urban-indicator-dropdown', 'value'),
         Input('main-country-filter', 'value')]
    )
    def update_urbanization_trend(indicator, selected_country):
        """Update urbanization trend chart"""
        try:
            # Load actual sample data
            sample_data = create_sample_urbanization_data()
            
            # Filter by selected country
            if selected_country:
                # Map country code to name for filtering
                country_code_to_name = {
                    'NGA': 'Nigeria', 'KEN': 'Kenya', 'ETH': 'Ethiopia',
                    'GHA': 'Ghana', 'TZA': 'Tanzania', 'UGA': 'Uganda',
                    'RWA': 'Rwanda', 'SEN': 'Senegal', 'BFA': 'Burkina Faso',
                    'CIV': 'Ivory Coast'
                }
                selected_country_name = country_code_to_name.get(selected_country, selected_country)
                sample_data = sample_data[sample_data['country'] == selected_country_name]
                
        except Exception as e:
            # Fallback data
            years = list(range(2000, 2024))
            sample_data = pd.DataFrame({
                'year': years * 3,
                'country': ['Nigeria'] * len(years) + ['Kenya'] * len(years) + ['Ethiopia'] * len(years),
                'urban_population_pct': (
                    [35 + i * 0.8 for i in range(len(years))] +
                    [25 + i * 1.2 for i in range(len(years))] +
                    [15 + i * 0.9 for i in range(len(years))]
                ),
                'urban_growth_rate': (
                    [3.5 + 0.1 * (i % 5) for i in range(len(years))] +
                    [4.2 + 0.15 * (i % 4) for i in range(len(years))] +
                    [5.1 + 0.12 * (i % 6) for i in range(len(years))]
                ),
                'population_density': (
                    [120 + i * 2.5 for i in range(len(years))] +
                    [85 + i * 1.8 for i in range(len(years))] +
                    [65 + i * 1.2 for i in range(len(years))]
                )
            })
        
        y_column = indicator or 'urban_population_pct'
        title_map = {
            'urban_population_pct': 'Urban Population Percentage Over Time',
            'urban_growth_rate': 'Urban Growth Rate Over Time',
            'population_density': 'Population Density Over Time'
        }
        
        fig = px.line(
            sample_data,
            x='year',
            y=y_column,
            color='country',
            title=title_map.get(y_column, 'Urbanization Trends'),
            markers=True
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
            xaxis_title='Year',
            yaxis_title=title_map.get(y_column, 'Value')
        )
        
        return fig
    
    @app.callback(
        Output('urbanization-map', 'figure'),
        [Input('urban-indicator-dropdown', 'value'),
         Input('main-country-filter', 'value')]
    )
    def update_urbanization_map(indicator, selected_country):
        """Update urbanization map visualization"""
        # Sample data for map
        country_codes = ['NGA', 'KEN', 'ETH', 'GHA', 'TZA', 'UGA', 'RWA', 'SEN', 'BFA', 'CIV']
        
        # Sample values based on indicator
        if indicator == 'urban_population_pct':
            values = [52, 28, 22, 57, 35, 25, 17, 48, 31, 52]
            title = 'Urban Population Percentage by Country'
            colorbar_title = 'Urban Pop %'
        elif indicator == 'urban_growth_rate':
            values = [4.2, 4.8, 5.6, 3.8, 5.2, 5.8, 3.2, 4.1, 6.1, 4.5]
            title = 'Urban Growth Rate by Country'
            colorbar_title = 'Growth Rate %'
        else:  # population_density
            values = [226, 95, 115, 137, 67, 228, 525, 87, 76, 83]
            title = 'Population Density by Country'
            colorbar_title = 'People/km²'
        
        fig = go.Figure(data=go.Choropleth(
            locations=country_codes,
            z=values,
            locationmode='ISO-3',
            colorscale='Blues',
            text=[f'{country}: {val}' for country, val in zip(country_codes, values)],
            colorbar_title=colorbar_title
        ))
        
        fig.update_layout(
            title_text=title,
            geo=dict(
                showframe=False,
                showcoastlines=True,
                scope='africa'
            ),
            title_font_size=16
        )
        
        return fig