"""
Callbacks for Cities Flood Exposure visualization
Multi-line chart showing flood exposure at city level for all cities across SSA
"""

from dash import Input, Output, State, html
import plotly.graph_objects as go
import dash_leaflet as dl

from ...utils.flood_data_loader import load_city_flood_exposure_data
from ...utils.flood_ui_helpers import get_city_colors
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from ...utils.data_loader import load_africapolis_centroids
from config.settings import CHART_STYLES


def register_cities_flood_exposure_callbacks(app):
    """Register callbacks for Cities Flood Exposure chart"""
    
    # Load static data once at registration time for performance
    data = load_city_flood_exposure_data()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    city_colors = get_city_colors()
    
    @app.callback(
        [Output('cities-flood-exposure-chart', 'figure'),
         Output('cities-flood-exposure-chart', 'style'),
         Output('cities-flood-exposure-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('cities-flood-return-period-selector', 'value'),
         Input('cities-flood-exposure-type-selector', 'value'),
         Input('cities-flood-measurement-type-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_cities_flood_exposure_chart(selected_country, return_period, exposure_type, measurement_type):
        """
        Generate multi-line chart showing flood exposure over time for all cities in selected country
        
        Args:
            selected_country: ISO3 country code
            return_period: Return period ('1in5', '1in10', '1in100')
            exposure_type: 'built_s' (built-up area) or 'pop' (population)
            measurement_type: 'absolute' or 'relative'
            
        Returns:
            Plotly figure object
        """
        try:
            # Set defaults
            return_period = return_period or '1in100'
            exposure_type = exposure_type or 'built_s'
            measurement_type = measurement_type or 'absolute'
            
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Filter data for selected country
            country_data = data[data['ISO3'] == selected_country].copy()
            
            if country_data.empty:
                raise Exception(f"No city flood exposure data available for selected country")
            
            # Get country name for title
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Determine which column to plot based on exposure type, measurement type, and return period
            if exposure_type == 'built_s':
                if measurement_type == 'absolute':
                    column_map = {
                        '1in5': 'BU_1in5',
                        '1in10': 'BU_1in10',
                        '1in100': 'BU_1in100'
                    }
                    yaxis_title = 'Built-up Area Exposed (km²)'
                    chart_title_suffix = 'Built-up Area'
                else:  # relative
                    column_map = {
                        '1in5': 'BU_1in5_pct',
                        '1in10': 'BU_1in10_pct',
                        '1in100': 'BU_1in100_pct'
                    }
                    yaxis_title = 'Built-up Area Exposed (%)'
                    chart_title_suffix = 'Built-up Area (%)'
            else:  # pop
                if measurement_type == 'absolute':
                    column_map = {
                        '1in5': 'POP_1in5',
                        '1in10': 'POP_1in10',
                        '1in100': 'POP_1in100'
                    }
                    yaxis_title = 'Population Exposed'
                    chart_title_suffix = 'Population'
                else:  # relative
                    column_map = {
                        '1in5': 'POP_1in5_pct',
                        '1in10': 'POP_1in10_pct',
                        '1in100': 'POP_1in100_pct'
                    }
                    yaxis_title = 'Population Exposed (%)'
                    chart_title_suffix = 'Population (%)'
            
            value_column = column_map[return_period]
            
            # Return period labels for subtitle
            return_period_labels = {
                '1in5': '1-in-5 year',
                '1in10': '1-in-10 year',
                '1in100': '1-in-100 year'
            }
            
            # Create figure
            fig = go.Figure()
            
            # Get unique cities and assign colors
            cities = country_data.sort_values('agglosName')['agglosName'].unique()
            
            # Add line for each city
            for idx, city_name in enumerate(cities):
                city_data = country_data[country_data['agglosName'] == city_name].sort_values('ghsl_year')
                
                # Use modulo to cycle through colors if more than 10 cities
                color = city_colors[idx % len(city_colors)]
                
                # Format hover template based on measurement type
                if measurement_type == 'absolute':
                    if exposure_type == 'built_s':
                        hover_template = f'<b>{city_name}</b><br>Built-up Area: %{{y:.2f}} km²<extra></extra>'
                    else:
                        hover_template = f'<b>{city_name}</b><br>Population: %{{y:,.0f}}<extra></extra>'
                else:
                    hover_template = f'<b>{city_name}</b><br>Percentage: %{{y:.2f}}%<extra></extra>'
                
                fig.add_trace(go.Scatter(
                    x=city_data['ghsl_year'],
                    y=city_data[value_column],
                    mode='lines+markers',
                    name=city_name,
                    line=dict(color=color, width=2.5),
                    marker=dict(size=8),
                    hovertemplate=hover_template
                ))
            
            # Create separate title
            title_text = html.H6([html.B(country_name), f' | Cities Flood Exposure - {chart_title_suffix}'], 
                                className='chart-title')
            
            # Update layout
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title=yaxis_title,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                hovermode='x unified',
                legend=dict(
                    title='City',
                    orientation='v',
                    yanchor='top',
                    y=1,
                    xanchor='left',
                    x=1.02,
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='#e5e7eb',
                    borderwidth=0
                ),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    dtick=5  # Show every 5 years
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    rangemode='tozero',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='#e5e7eb',
                    # tickformat='.2f' if measurement_type == 'relative' else None,
                    ticksuffix='%' if measurement_type == 'relative' else None
                )
            )
            
            return fig, {'display': 'block'}, title_text
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback
    create_simple_download_callback(
        app,
        'cities-flood-exposure-download',
        lambda: data,
        'cities_flood_exposure'
    )
    
    @app.callback(
        Output('cities-flood-map-modal', 'is_open'),
        [Input('cities-flood-map-button', 'n_clicks'),
         Input('close-cities-flood-map-button', 'n_clicks')],
        [State('cities-flood-map-modal', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_cities_flood_map_modal(open_clicks, close_clicks, is_open):
        """Toggle the city map modal open/closed"""
        return not is_open
    
    @app.callback(
        Output('cities-flood-map-container', 'children'),
        [Input('cities-flood-map-modal', 'is_open'),
         Input('main-country-filter', 'value')],
        prevent_initial_call=True
    )
    def update_cities_flood_map(is_open, selected_country):
        """Generate Leaflet map showing locations of all cities in the chart"""
        if not is_open or not selected_country:
            return []
        
        try:
            # Load centroids data
            centroids = load_africapolis_centroids()
            
            # Filter data for cities in the selected country
            country_data = data[data['ISO3'] == selected_country].copy()
            
            if country_data.empty:
                return []
            
            # Get unique city names (agglosName)
            city_names = country_data['agglosName'].unique()
            
            # Filter centroids for these cities
            city_centroids = centroids[centroids['agglosName'].isin(city_names)].copy()
            
            if city_centroids.empty:
                return []
            
            # Create markers for each city
            markers = []
            for _, row in city_centroids.iterrows():
                marker = dl.Marker(
                    position=[row['Latitude'], row['Longitude']],
                    children=[
                        dl.Tooltip(row['agglosName']),
                        dl.Popup(f"<b>{row['agglosName']}</b><br>Country: {row['ISO3']}")
                    ]
                )
                markers.append(marker)
            
            # Calculate map center and zoom
            if len(city_centroids) > 0:
                center_lat = city_centroids['Latitude'].mean()
                center_lon = city_centroids['Longitude'].mean()
                
                # Calculate zoom based on city spread
                lat_range = city_centroids['Latitude'].max() - city_centroids['Latitude'].min()
                lon_range = city_centroids['Longitude'].max() - city_centroids['Longitude'].min()
                max_range = max(lat_range, lon_range)
                
                if max_range < 1:
                    zoom = 9
                elif max_range < 3:
                    zoom = 8
                elif max_range < 5:
                    zoom = 7
                elif max_range < 10:
                    zoom = 6
                else:
                    zoom = 5
            else:
                center_lat, center_lon, zoom = 0, 20, 4
            
            # Create map
            map_children = [
                dl.TileLayer(),
                dl.LayerGroup(children=markers)
            ]
            
            return dl.Map(
                children=map_children,
                center=[center_lat, center_lon],
                zoom=zoom,
                style={'width': '100%', 'height': '100%'}
            )
            
        except Exception as e:
            print(f"Error generating cities flood map: {str(e)}")
            return []
