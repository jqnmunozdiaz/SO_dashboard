"""
Callbacks for Cities Distribution pie chart visualization
Shows distribution of urban population across city size categories
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd

try:
    from ...utils.data_loader import load_city_size_distribution
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_error_chart
    from ...utils.download_helpers import prepare_csv_download
    from ...utils.color_utils import CITY_SIZE_COLORS
    from config.settings import CHART_STYLES
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_city_size_distribution
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from src.utils.download_helpers import prepare_csv_download
    from src.utils.color_utils import CITY_SIZE_COLORS
    from config.settings import CHART_STYLES

def register_cities_distribution_callbacks(app):
    """Register callbacks for Cities Distribution pie chart"""
    
    @app.callback(
        Output('cities-distribution-chart', 'figure'),
        [
            Input('main-country-filter', 'value'),
            Input('cities-distribution-year-filter', 'value')
        ],
        prevent_initial_call=False
    )
    def generate_cities_distribution_chart(selected_country, selected_year):
        try:
            # Load data
            data = load_city_size_distribution()
            countries_dict = load_subsaharan_countries_and_regions_dict()
            
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Filter for selected country and year
            filtered_data = data[
                (data['Country Code'] == selected_country) & 
                (data['Year'] == selected_year)
            ]
            
            if filtered_data.empty:
                raise Exception(f"No data available for {countries_dict.get(selected_country, selected_country)} in {selected_year}")
            
            # Get city names, populations, and size categories
            city_names = filtered_data['City Name'].tolist()
            populations = filtered_data['Population'].tolist()
            size_categories = filtered_data['Size Category'].tolist()
            
            # Assign colors based on size category
            colors = [CITY_SIZE_COLORS.get(category, '#95a5a6') for category in size_categories]
            
            # Check if there's any data
            if sum(populations) == 0:
                raise Exception(f"No city size data available for {countries_dict.get(selected_country, selected_country)} in {selected_year}")
            
            # Create pie chart with individual cities
            fig = go.Figure(data=[go.Pie(
                labels=city_names,
                values=populations,
                marker=dict(colors=colors),
                textinfo='percent',
                textposition='inside',
                hovertemplate='<b>%{label}</b><br>' +
                              'Population: %{value:,.0f} thousand<br>' +
                              'Size Category: %{customdata}<br>' +
                              'Percentage: %{percent}<br>' +
                              '<extra></extra>',
                customdata=size_categories,
                showlegend=False  # Hide pie legend, we'll add custom legend
            )])
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            fig.update_layout(
                title=f'<b>{country_name}</b> | Cities Distribution by Size ({selected_year})',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=True,
                legend=dict(
                    title="Size Categories",
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02,
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="#e2e8f0",
                    borderwidth=1
                ),
                height=600,
                margin=dict(r=250, l=50, t=80, b=50),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            
            # Add visible traces for legend (one for each size category)
            for category, color in CITY_SIZE_COLORS.items():
                fig.add_trace(go.Scatter(
                    x=[None],
                    y=[None],
                    mode='markers',
                    marker=dict(size=12, color=color),
                    name=category,
                    showlegend=True
                ))
            
            return fig
            
        except Exception as e:
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='pie',
                title='Urban Population Distribution by City Size'
            )
    
    @app.callback(
        Output('cities-distribution-download', 'data'),
        [Input('cities-distribution-download-button', 'n_clicks'),
         Input('main-country-filter', 'value')],
        prevent_initial_call=True
    )
    def download_cities_distribution_data(n_clicks, selected_country):
        """Download city size distribution data as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            # Load full dataset (raw data, no filtering)
            cities_data = load_city_size_distribution()
            
            filename = "cities_individual"
            
            return prepare_csv_download(cities_data, filename)
        
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None
