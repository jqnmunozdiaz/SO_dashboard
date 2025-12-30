"""
Callbacks for Cities Flood Exposure visualization
Side-by-side bar charts showing 2020 flood exposure and 2015-2020 CAGR for cities
"""

from dash import Input, Output, State, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_leaflet as dl
import pandas as pd

from ...utils.flood_data_loader import load_city_flood_exposure_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message, calculate_map_zoom
from ...utils.download_helpers import create_simple_download_callback
from ...utils.data_loader import load_africapolis_centroids
from config.settings import CHART_STYLES

def register_cities_flood_exposure_callbacks(app):
    """Register callbacks for Cities Flood Exposure chart"""
    
    # Load static data once at registration time for performance
    data = load_city_flood_exposure_data()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        Output('cities-flood-exposure-city-selector', 'options'),
        Output('cities-flood-exposure-city-selector', 'value'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def update_city_options(selected_country):
        """Populate city dropdown based on selected country, sorted by 2020 population"""
        try:
            if not selected_country:
                return [], []
            
            # Filter for selected country
            country_data = data[data['ISO3'] == selected_country].copy()
            
            if country_data.empty:
                return [], []
            
            # Sort by 2020 population (descending) for getting top 5
            country_data_sorted = country_data.sort_values('africapolis_pop_2020', ascending=False)
            
            # Create options for all cities sorted alphabetically
            country_data_alpha = country_data.sort_values('Agglomeration_Name')
            options = [
                {'label': row['Agglomeration_Name'], 'value': row['Agglomeration_Name']}
                for _, row in country_data_alpha.iterrows()
            ]
            
            # Pre-select top 5 cities by population
            top_5_cities = country_data_sorted.head(5)['Agglomeration_Name'].tolist()
            
            return options, top_5_cities
            
        except Exception as e:
            print(f"Error updating city options: {str(e)}")
            return [], []
    
    @app.callback(
        [Output('cities-flood-exposure-chart', 'figure'),
         Output('cities-flood-exposure-chart', 'style'),
         Output('cities-flood-exposure-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('cities-flood-return-period-selector', 'value'),
         Input('cities-flood-exposure-type-selector', 'value'),
         Input('cities-flood-measurement-type-selector', 'value'),
         Input('cities-flood-exposure-city-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_cities_flood_exposure_chart(selected_country, return_period, exposure_type, measurement_type, selected_cities):
        """
        Generate side-by-side horizontal bar charts showing 2020 flood exposure and 2015-2020 CAGR
        
        Args:
            selected_country: ISO3 country code
            return_period: Return period ('10' or '100')
            exposure_type: 'pop' (population) or 'built' (built-up area)
            measurement_type: 'absolute' or 'relative'
            selected_cities: List of selected city names
            
        Returns:
            Plotly figure with two subplots
        """
        try:
            # Set defaults
            return_period = return_period or '100'
            exposure_type = exposure_type or 'built'
            measurement_type = measurement_type or 'absolute'
            
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Handle no cities selected
            if not selected_cities or len(selected_cities) == 0:
                raise Exception("Please select at least one city from the dropdown")
            
            # Filter data for selected country and cities
            filtered_data = data[
                (data['ISO3'] == selected_country) & 
                (data['Agglomeration_Name'].isin(selected_cities))
            ].copy()
            
            if filtered_data.empty:
                raise Exception(f"No data available for selected cities")
            
            # Sort by 2020 population (ascending for horizontal bars - largest at top)
            filtered_data = filtered_data.sort_values('africapolis_pop_2020', ascending=True)
            
            # Get country name for title
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Determine column names and labels based on exposure type and measurement type
            if exposure_type == 'pop':
                year1 = 2020
                year2 = 2025
                
                if measurement_type == 'absolute':
                    col_year2 = f'worldpop_population_ftm_total_rp{return_period}_{year2}'
                    title_suffix = 'Population Exposed to Floods'
                    left_title = f'Population Exposed<br>{year2}'
                    text_format = filtered_data[col_year2].apply(lambda x: f'{x:,.0f}')
                else:  # relative
                    col_year2 = f'worldpop_population_ftm_share_rp{return_period}_{year2}'
                    title_suffix = 'Population Exposed to Floods (%)'
                    left_title = f'Population Exposed (%)<br>{year2}'
                    text_format = (filtered_data[col_year2] * 100).apply(lambda x: f'{x:.1f}%')
                
                col_cagr = f'pop_ftm3_fluvial_pluvial_flood_rp{return_period}_cagr_{year1}_{year2}'
                right_title = f'Annual Growth Rate (%)<br>{year1}-{year2}'
            else:  # built
                year1 = 2015
                year2 = 2020
                
                if measurement_type == 'absolute':
                    col_year2 = f'worldpop_built_surface_ftm_km2_rp{return_period}_{year2}'
                    title_suffix = 'Built-up Area Exposed to Floods'
                    left_title = f'Built-up Area Exposed (km²)<br>{year2}'
                    text_format = filtered_data[col_year2].apply(lambda x: f'{x:.2f}')
                else:  # relative
                    col_year2 = f'worldpop_built_surface_ftm_share_rp{return_period}_{year2}'
                    title_suffix = 'Built-up Area Exposed to Floods (%)'
                    left_title = f'Built-up Area Exposed (%)<br>{year2}'
                    text_format = (filtered_data[col_year2] * 100).apply(lambda x: f'{x:.1f}%')
                
                col_cagr = f'built_ftm3_fluvial_pluvial_flood_rp{return_period}_cagr_{year1}_{year2}'
                right_title = f'Annual Growth Rate (%)<br>{year1}-{year2}'
            
            # Check if columns exist
            if col_year2 not in filtered_data.columns or col_cagr not in filtered_data.columns:
                raise Exception(f"Data not available for selected flood type and return period")
            
            # Handle missing CAGR values (convert from decimal to percentage)
            filtered_data['cagr_display'] = (filtered_data[col_cagr] * 100).apply(
                lambda x: 'N/A' if pd.isna(x) else f'{x:.1f}%'
            )
            
            # Create subplots: 2 columns, 1 row
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=(
                    f'{year2}',
                    f'{year1}-{year2}'
                ),
                horizontal_spacing=0.15,
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Define orange color for bars
            bar_color = '#e67e22'  # Orange color
            
            # Left chart: absolute or relative values
            # For relative values, multiply by 100 to convert to percentage
            x_values = filtered_data[col_year2] * 100 if measurement_type == 'relative' else filtered_data[col_year2]
            
            fig.add_trace(
                go.Bar(
                    y=filtered_data['Agglomeration_Name'],
                    x=x_values,
                    orientation='h',
                    marker=dict(color=bar_color),
                    text=text_format,
                    textposition='auto',
                    textfont=dict(size=10),
                    hoverinfo='skip',
                    showlegend=False
                ),
                row=1, col=1
            )
            
            # Right chart: CAGR values (convert from decimal to percentage)
            # Filter out N/A values for plotting, but show them in hover
            cagr_x_values = (filtered_data[col_cagr] * 100).fillna(0)  # Replace NaN with 0 for plotting
            
            fig.add_trace(
                go.Bar(
                    y=filtered_data['Agglomeration_Name'],
                    x=cagr_x_values,
                    orientation='h',
                    marker=dict(color=bar_color),
                    text=filtered_data['cagr_display'],
                    textposition='auto',
                    textfont=dict(size=10),
                    hoverinfo='skip',
                    showlegend=False
                ),
                row=1, col=2
            )
            
            # Create title separately
            chart_title = html.H6([
                html.B(country_name),
                f' | {title_suffix}'
            ], className='chart-title')
            
            # Update layout
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                height=max(400, len(selected_cities) * 60),  # Dynamic height based on number of cities
                showlegend=False,
                margin=dict(l=150, r=150, t=0, b=50)
            )
            
            # Update x-axes
            fig.update_xaxes(
                title_text=left_title,
                showgrid=True,
                gridcolor='#e5e7eb',
                ticksuffix='%' if measurement_type == 'relative' else None,
                row=1, col=1
            )
            
            fig.update_xaxes(
                title_text=right_title,
                showgrid=True,
                gridcolor='#e5e7eb',
                ticksuffix='%',
                row=1, col=2
            )
            
            # Update y-axes (hide y-axis titles, keep labels)
            fig.update_yaxes(
                title_text='',
                showgrid=False,
                row=1, col=1
            )
            
            fig.update_yaxes(
                title_text='',
                showgrid=False,
                showticklabels=False,  # Hide labels on right chart since they're duplicated
                row=1, col=2
            )
            
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback
    create_simple_download_callback(
        app,
        'cities-flood-exposure-download',
        lambda: data
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
         Input('main-country-filter', 'value'),
         Input('cities-flood-exposure-city-selector', 'value')],
        prevent_initial_call=True
    )
    def update_cities_flood_map(is_open, selected_country, selected_cities):
        """Generate Leaflet map showing locations of selected cities"""
        if not is_open or not selected_country or not selected_cities:
            return []
        
        try:
            # Load centroids data
            centroids = load_africapolis_centroids()
            
            # Filter data for selected cities only
            country_data = data[
                (data['ISO3'] == selected_country) & 
                (data['Agglomeration_Name'].isin(selected_cities))
            ].copy()
            
            if country_data.empty:
                return []
            
            # Get unique city names from selected cities
            city_names = country_data['Agglomeration_Name'].unique()
            
            # Filter centroids for these selected cities
            city_centroids = centroids[centroids['Agglomeration_Name'].isin(city_names)].copy()
            
            if city_centroids.empty:
                return []
            
            # Create markers for each city
            markers = []
            for _, row in city_centroids.iterrows():
                marker = dl.Marker(
                    position=[row['Latitude'], row['Longitude']],
                    children=[
                        dl.Tooltip(row['Agglomeration_Name']),
                        dl.Popup(f"<b>{row['Agglomeration_Name']}</b><br>Country: {row['ISO3']}")
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
                zoom = calculate_map_zoom(lat_range, lon_range)
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
