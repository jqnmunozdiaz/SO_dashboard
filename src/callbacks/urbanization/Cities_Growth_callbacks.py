"""
Callbacks for Cities Growth (Built-up Expansion) visualization
Shows year2 absolute values and year1-year2 CAGR for selected cities
"""

from dash import Input, Output, State, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_leaflet as dl

from ...utils.data_loader import load_africapolis_centroids, load_cities_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message, calculate_map_zoom
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES

'''
KeyError: 'worldpop_built_km2_2025'
Cities Growth: 
Population : Africapolis
built-up: World pop (romain a deja evnoye les donnees, mais dois rajouter worldpop_built_cagr_2015_2020 pour 2020-2025) avec les AOIs actualisees
'''

def register_cities_growth_callbacks(app):
    """Register callbacks for Cities Growth chart"""
    
    # Load static data once at registration time for performance
    data_or = load_cities_data()

    centroids_data = load_africapolis_centroids()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    pop_year1 = 2020   
    pop_year2 = 2025

    bu_year1 = 2015
    bu_year2 = 2020
    
    data = data_or.copy()
    
    data[f'BU_{bu_year1}'] = data[f'worldpop_built_km2_{bu_year1}'] 
    data[f'BU_{bu_year2}'] = data[f'worldpop_built_km2_{bu_year2}']
    data[f'BU_CAGR_{bu_year1}_{bu_year2}'] = data[f'worldpop_built_cagr_{bu_year1}_{bu_year2}'] * 100
    
    data[f'POP_{pop_year1}'] = data[f'africapolis_pop_{pop_year1}']
    data[f'POP_{pop_year2}'] = data[f'africapolis_pop_{pop_year2}']
    data[f'POP_CAGR_{pop_year1}_{pop_year2}'] = data[f'africapolis_pop_cagr_{pop_year1}_{pop_year2}'] * 100
    
    @app.callback(
        Output('cities-growth-city-selector', 'options'),
        Output('cities-growth-city-selector', 'value'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def update_city_options(selected_country):
        """Populate city dropdown based on selected country, sorted by year2 population"""
        try:
            if not selected_country:
                return [], []
            
            # Filter for selected country
            country_data = data[data['ISO3'] == selected_country].copy()
            
            if country_data.empty:
                return [], []
            
            # Sort by year2 population (descending) for getting top 5
            country_data_sorted = country_data.sort_values(f'POP_{pop_year2}', ascending=False)
            
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
        [Output('cities-growth-chart', 'figure'),
         Output('cities-growth-chart', 'style'),
         Output('cities-growth-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('cities-growth-metric-selector', 'value'),
         Input('cities-growth-city-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_cities_growth_chart(selected_country, selected_metric, selected_cities):
        """
        Generate side-by-side horizontal bar charts showing year2 values and CAGR
        
        Args:
            selected_country: ISO3 country code
            selected_metric: 'BU' for Built-up or 'POP' for Population
            selected_cities: List of selected city names
            
        Returns:
            Plotly figure with two subplots
        """
        try:
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Handle no cities selected
            if not selected_cities or len(selected_cities) == 0:
                raise Exception("Please select at least one city from the dropdown")
            
            # Filter for selected country and cities
            filtered_data = data[
                (data['ISO3'] == selected_country) & 
                (data['Agglomeration_Name'].isin(selected_cities))
            ].copy()
            
            if filtered_data.empty:
                raise Exception(f"No data available for selected cities")
            
            # Sort by year2 population (descending) to maintain consistent ordering
            filtered_data = filtered_data.sort_values(f'POP_{pop_year2}', ascending=True)
            
            # Determine which columns to use based on metric
            if selected_metric == 'BU':
                col_year2 = f'BU_{bu_year2}'
                col_cagr = f'BU_CAGR_{bu_year1}_{bu_year2}'
                metric_name = 'Built-up'
                unit_year2 = 'km²'
                unit_cagr = '%'
                title_suffix = 'Built-up Area'
                year2_label = f'{bu_year2}'
                year_range_label = f'{bu_year1}-{bu_year2}'
            else:  # POP
                col_year2 = f'POP_{pop_year2}'
                col_cagr = f'POP_CAGR_{pop_year1}_{pop_year2}'
                metric_name = 'Population'
                unit_year2 = ''
                unit_cagr = '%'
                title_suffix = 'Population'
                year2_label = f'{pop_year2}'
                year_range_label = f'{pop_year1}-{pop_year2}'
            
            # Create subplots: 2 columns, 1 row
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=(
                    year2_label,
                    year_range_label
                ),
                horizontal_spacing=0.15,
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Define orange color for bars
            bar_color = '#e67e22'  # Orange color
            
            # Left chart: year2 absolute values
            fig.add_trace(
                go.Bar(
                    y=filtered_data['Agglomeration_Name'],
                    x=filtered_data[col_year2],
                    orientation='h',
                    marker=dict(color=bar_color),
                    text=filtered_data[col_year2].apply(lambda x: f'{x:,.1f}' if selected_metric == 'BU' else f'{x:,.0f}'),
                    textposition='auto',
                    textfont=dict(size=10),
                    hoverinfo='skip',
                    showlegend=False
                ),
                row=1, col=1
            )
            
            # Right chart: CAGR values
            fig.add_trace(
                go.Bar(
                    y=filtered_data['Agglomeration_Name'],
                    x=filtered_data[col_cagr],
                    orientation='h',
                    marker=dict(color=bar_color),
                    text=filtered_data[col_cagr].apply(lambda x: f'{x:.1f}%'),
                    textposition='auto',
                    textfont=dict(size=10),
                    hoverinfo='skip',
                    showlegend=False
                ),
                row=1, col=2
            )
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Create title separately
            chart_title = html.H6([
                html.B(country_name),
                f' | {title_suffix} Expansion'
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
                title_text=f'Total {metric_name} ({unit_year2})<br>{year2_label}' if unit_year2 else f'Total {metric_name}<br>{year2_label}',
                showgrid=True,
                gridcolor='#e5e7eb',
                row=1, col=1
            )
            
            fig.update_xaxes(
                title_text=f'Annual Growth Rate ({unit_cagr})<br>{year_range_label}',
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
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'cities-growth-download',
        lambda: data
    )
    
    @app.callback(
        Output('city-map-modal', 'is_open'),
        [Input('show-city-map-button', 'n_clicks'),
         Input('close-city-map-button', 'n_clicks')],
        [State('city-map-modal', 'is_open')],
        prevent_initial_call=True
    )
    def toggle_map_modal(show_clicks, close_clicks, is_open):
        """Toggle the city map modal visibility"""
        return not is_open
    
    @app.callback(
        Output('city-map-container', 'children'),
        [Input('city-map-modal', 'is_open')],
        [State('main-country-filter', 'value'),
         State('cities-growth-city-selector', 'value')],
        prevent_initial_call=True
    )
    def update_city_map(is_open, selected_country, selected_cities):
        """Generate Leaflet map with selected cities"""
        if not is_open or not selected_country or not selected_cities:
            return html.Div("No cities selected")
        
        try:
            # Filter centroids for selected country and cities
            filtered_centroids = centroids_data[
                (centroids_data['ISO3'] == selected_country) & 
                (centroids_data['Agglomeration_Name'].isin(selected_cities))
            ].copy()
            
            if filtered_centroids.empty:
                return html.Div("No location data available for selected cities")
            
            # Calculate map center and zoom
            center_lat = filtered_centroids['Latitude'].mean()
            center_lon = filtered_centroids['Longitude'].mean()
            
            # Calculate appropriate zoom level based on city spread
            lat_range = filtered_centroids['Latitude'].max() - filtered_centroids['Latitude'].min()
            lon_range = filtered_centroids['Longitude'].max() - filtered_centroids['Longitude'].min()
            zoom = calculate_map_zoom(lat_range, lon_range)
            
            # Create markers for each city
            markers = []
            for _, row in filtered_centroids.iterrows():
                marker = dl.Marker(
                    position=[row['Latitude'], row['Longitude']],
                    children=[
                        dl.Tooltip(row['Agglomeration_Name']),
                        dl.Popup([
                            html.H6(row['Agglomeration_Name'], style={'marginBottom': '5px'}),
                            html.P(f"Country: {countries_dict.get(row['ISO3'], row['ISO3'])}", 
                                   style={'marginBottom': '0px', 'fontSize': '12px'})
                        ])
                    ]
                )
                markers.append(marker)
            
            # Create map
            city_map = dl.Map(
                children=[
                    dl.TileLayer(url='https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
                                attribution='&copy; OpenStreetMap contributors'),
                    dl.LayerGroup(markers)
                ],
                center=[center_lat, center_lon],
                zoom=zoom,
                style={'width': '100%', 'height': '70vh'}
            )
            
            return city_map
            
        except Exception as e:
            return html.Div(f"Error loading map: {str(e)}", style={'color': 'red'})
            return None
