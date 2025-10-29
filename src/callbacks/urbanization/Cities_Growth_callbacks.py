"""
Callbacks for Cities Growth (Built-up Expansion) visualization
Shows 2020 absolute values and 2000-2020 CAGR for selected cities
"""

from dash import Input, Output, State, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_leaflet as dl

from ...utils.data_loader import load_africapolis_ghsl_simple, load_africapolis_centroids
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def register_cities_growth_callbacks(app):
    """Register callbacks for Cities Growth chart"""
    
    # Load static data once at registration time for performance
    data = load_africapolis_ghsl_simple()
    centroids_data = load_africapolis_centroids()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        Output('cities-growth-city-selector', 'options'),
        Output('cities-growth-city-selector', 'value'),
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
            country_data_sorted = country_data.sort_values('POP_2020', ascending=False)
            
            # Create options for all cities sorted alphabetically
            country_data_alpha = country_data.sort_values('agglosName')
            options = [
                {'label': row['agglosName'], 'value': row['agglosName']}
                for _, row in country_data_alpha.iterrows()
            ]
            
            # Pre-select top 5 cities by population
            top_5_cities = country_data_sorted.head(5)['agglosName'].tolist()
            
            return options, top_5_cities
            
        except Exception as e:
            print(f"Error updating city options: {str(e)}")
            return [], []
    
    @app.callback(
        [Output('cities-growth-chart', 'figure'),
         Output('cities-growth-chart', 'style')],
        [Input('main-country-filter', 'value'),
         Input('cities-growth-metric-selector', 'value'),
         Input('cities-growth-city-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_cities_growth_chart(selected_country, selected_metric, selected_cities):
        """
        Generate side-by-side horizontal bar charts showing 2020 values and CAGR
        
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
                (data['agglosName'].isin(selected_cities))
            ].copy()
            
            if filtered_data.empty:
                raise Exception(f"No data available for selected cities")
            
            # Sort by 2020 population (descending) to maintain consistent ordering
            filtered_data = filtered_data.sort_values('POP_2020', ascending=True)
            
            # Determine which columns to use based on metric
            if selected_metric == 'BU':
                col_2020 = 'BU_2020'
                col_cagr = 'BU_CAGR_2000_2020'
                metric_name = 'Built-up'
                unit_2020 = 'sq. km'
                unit_cagr = '%'
                title_suffix = 'Built-up Area'
            else:  # POP
                col_2020 = 'POP_2020'
                col_cagr = 'POP_CAGR_2000_2020'
                metric_name = 'Population'
                unit_2020 = ''
                unit_cagr = '%'
                title_suffix = 'Population'
            
            # Create subplots: 2 columns, 1 row
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=(
                    f'2020',
                    f'2000-2020'
                ),
                horizontal_spacing=0.15,
                specs=[[{"type": "bar"}, {"type": "bar"}]]
            )
            
            # Define orange color for bars
            bar_color = '#e67e22'  # Orange color
            
            # Left chart: 2020 absolute values
            fig.add_trace(
                go.Bar(
                    y=filtered_data['agglosName'],
                    x=filtered_data[col_2020],
                    orientation='h',
                    marker=dict(color=bar_color),
                    text=filtered_data[col_2020].apply(lambda x: f'{x:.0f}' if selected_metric == 'BU' else f'{x:,.0f}'),
                    textposition='auto',
                    textfont=dict(size=10),
                    hovertemplate='<b>%{y}</b><br>' + f'{metric_name}: %{{x:,.2f}} {unit_2020}<extra></extra>',
                    showlegend=False
                ),
                row=1, col=1
            )
            
            # Right chart: CAGR values
            fig.add_trace(
                go.Bar(
                    y=filtered_data['agglosName'],
                    x=filtered_data[col_cagr],
                    orientation='h',
                    marker=dict(color=bar_color),
                    text=filtered_data[col_cagr].apply(lambda x: f'{x:.1f}%'),
                    textposition='auto',
                    textfont=dict(size=10),
                    hovertemplate='<b>%{y}</b><br>' + f'Annual growth rate: %{{x:,.2f}}{unit_cagr}<extra></extra>',
                    showlegend=False
                ),
                row=1, col=2
            )
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Update layout
            fig.update_layout(
                title=f'<b>{country_name}</b> | {title_suffix} Expansion',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                height=max(400, len(selected_cities) * 60),  # Dynamic height based on number of cities
                showlegend=False,
                margin=dict(l=150, r=150, t=100, b=50)
            )
            
            # Update x-axes
            fig.update_xaxes(
                title_text=f'Total {metric_name} ({unit_2020})' if unit_2020 else f'Total {metric_name}',
                showgrid=True,
                gridcolor='#e5e7eb',
                row=1, col=1
            )
            
            fig.update_xaxes(
                title_text=f'Annual growth rate ({unit_cagr})',
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
            
            return fig, {'display': 'block'}
            
        except Exception as e:
            return create_simple_error_message(str(e))
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'cities-growth-download',
        lambda: data,
        'cities_built_up_growth'
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
                (centroids_data['agglosName'].isin(selected_cities))
            ].copy()
            
            if filtered_centroids.empty:
                return html.Div("No location data available for selected cities")
            
            # Calculate map center and zoom
            center_lat = filtered_centroids['Latitude'].mean()
            center_lon = filtered_centroids['Longitude'].mean()
            
            # Calculate appropriate zoom level based on city spread
            lat_range = filtered_centroids['Latitude'].max() - filtered_centroids['Latitude'].min()
            lon_range = filtered_centroids['Longitude'].max() - filtered_centroids['Longitude'].min()
            max_range = max(lat_range, lon_range)
            
            # Determine zoom level
            if max_range > 10:
                zoom = 5
            elif max_range > 5:
                zoom = 6
            elif max_range > 2:
                zoom = 7
            elif max_range > 1:
                zoom = 8
            else:
                zoom = 9
            
            # Create markers for each city
            markers = []
            for _, row in filtered_centroids.iterrows():
                marker = dl.Marker(
                    position=[row['Latitude'], row['Longitude']],
                    children=[
                        dl.Tooltip(row['agglosName']),
                        dl.Popup([
                            html.H6(row['agglosName'], style={'marginBottom': '5px'}),
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
