"""
Callbacks for urbanization trends functionality
"""

from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def register_callbacks(app):
    """Register all urbanization-related callbacks"""
    
    @app.callback(
        Output('urban-country-dropdown', 'options'),
        Input('main-tabs', 'active_tab')
    )
    def update_urban_country_options(active_tab):
        """Update country dropdown options for urbanization tab"""
        if active_tab == 'urbanization':
            countries = [
                {'label': 'Nigeria', 'value': 'NGA'},
                {'label': 'Kenya', 'value': 'KEN'},
                {'label': 'Ethiopia', 'value': 'ETH'},
                {'label': 'Ghana', 'value': 'GHA'},
                {'label': 'Tanzania', 'value': 'TZA'},
                {'label': 'Uganda', 'value': 'UGA'},
                {'label': 'Rwanda', 'value': 'RWA'},
                {'label': 'Senegal', 'value': 'SEN'},
                {'label': 'Burkina Faso', 'value': 'BFA'},
                {'label': 'Ivory Coast', 'value': 'CIV'},
            ]
            return countries
        return []
    
    @app.callback(
        Output('urbanization-trend-chart', 'figure'),
        [Input('urban-indicator-dropdown', 'value'),
         Input('urban-country-dropdown', 'value')]
    )
    def update_urbanization_trend(indicator, countries):
        """Update urbanization trend chart"""
        # Sample data for urbanization trends
        years = list(range(2000, 2024))
        
        # Sample data for different countries
        sample_data = pd.DataFrame({
            'year': years * 3,
            'country': ['Nigeria'] * len(years) + ['Kenya'] * len(years) + ['Ethiopia'] * len(years),
            'urban_pop_pct': (
                [35 + i * 0.8 for i in range(len(years))] +
                [25 + i * 1.2 for i in range(len(years))] +
                [15 + i * 0.9 for i in range(len(years))]
            ),
            'urban_growth': (
                [3.5 + 0.1 * (i % 5) for i in range(len(years))] +
                [4.2 + 0.15 * (i % 4) for i in range(len(years))] +
                [5.1 + 0.12 * (i % 6) for i in range(len(years))]
            ),
            'pop_density': (
                [120 + i * 2.5 for i in range(len(years))] +
                [85 + i * 1.8 for i in range(len(years))] +
                [65 + i * 1.2 for i in range(len(years))]
            )
        })
        
        if countries:
            sample_data = sample_data[sample_data['country'].isin([
                'Nigeria' if 'NGA' in countries else None,
                'Kenya' if 'KEN' in countries else None,
                'Ethiopia' if 'ETH' in countries else None
            ].remove(None) if None in [
                'Nigeria' if 'NGA' in countries else None,
                'Kenya' if 'KEN' in countries else None,
                'Ethiopia' if 'ETH' in countries else None
            ] else [
                'Nigeria' if 'NGA' in countries else None,
                'Kenya' if 'KEN' in countries else None,
                'Ethiopia' if 'ETH' in countries else None
            ])]
        
        y_column = indicator or 'urban_pop_pct'
        title_map = {
            'urban_pop_pct': 'Urban Population Percentage Over Time',
            'urban_growth': 'Urban Growth Rate Over Time',
            'pop_density': 'Population Density Over Time'
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
         Input('urban-country-dropdown', 'value')]
    )
    def update_urbanization_map(indicator, countries):
        """Update urbanization map visualization"""
        # Sample data for map
        country_codes = ['NGA', 'KEN', 'ETH', 'GHA', 'TZA', 'UGA', 'RWA', 'SEN', 'BFA', 'CIV']
        
        # Sample values based on indicator
        if indicator == 'urban_pop_pct':
            values = [52, 28, 22, 57, 35, 25, 17, 48, 31, 52]
            title = 'Urban Population Percentage by Country'
            colorbar_title = 'Urban Pop %'
        elif indicator == 'urban_growth':
            values = [4.2, 4.8, 5.6, 3.8, 5.2, 5.8, 3.2, 4.1, 6.1, 4.5]
            title = 'Urban Growth Rate by Country'
            colorbar_title = 'Growth Rate %'
        else:  # pop_density
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