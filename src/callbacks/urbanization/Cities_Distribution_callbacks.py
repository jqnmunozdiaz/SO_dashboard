"""
Callbacks for Cities Distribution treemap visualization
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
    """Register callbacks for Cities Distribution treemap chart"""
    
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
            ].copy()
            
            if filtered_data.empty:
                raise Exception(f"No data available for {countries_dict.get(selected_country, selected_country)} in {selected_year}")
            
            # Define size categories in order (for consistent grouping) Order from largest to smallest for visual hierarchy in pie chart
            size_categories_ordered = [
                '10 million or more',
                '5 to 10 million',
                '1 to 5 million',
                '500 000 to 1 million',
                '300 000 to 500 000',
                'Fewer than 300 000'
            ]
            
            # Create sorting keys to ensure "Other cities" always appear at the end of each category
            category_order = {cat: i for i, cat in enumerate(size_categories_ordered)}
            filtered_data['category_sort_order'] = filtered_data['Size Category'].map(category_order)
            filtered_data['is_other_cities'] = filtered_data['City Name'].str.startswith('Other cities').astype(int)
            
            # Sort by: 1) size category, 2) named cities before "Other cities", 3) population descending
            sorted_data = filtered_data.sort_values(
                ['category_sort_order', 'is_other_cities', 'Population'], 
                ascending=[True, True, False]
            ).reset_index(drop=True)
            
            # Get city names, populations, and size categories in sorted order
            city_names = sorted_data['City Name'].tolist()
            populations = sorted_data['Population'].tolist()
            size_categories = sorted_data['Size Category'].tolist()
            
            # Scale populations to actual numbers (from thousands)
            scaled_populations = [p * 1000 for p in populations]
            
            # Calculate total population for percentage calculation
            total_population = sum(scaled_populations)
            
            # Assign colors based on size category
            colors = [CITY_SIZE_COLORS.get(category, '#95a5a6') for category in size_categories]
            
            # Check if there's any data
            if sum(populations) == 0:
                raise Exception(f"No city size data available for {countries_dict.get(selected_country, selected_country)} in {selected_year}")
            
            # Calculate percentage for each city relative to total
            percentages = [(val / total_population * 100) for val in scaled_populations]
            
            # Create custom hover text with correct percentages
            hover_texts = []
            for i, (name, val, pct) in enumerate(zip(city_names, scaled_populations, percentages)):
                hover_texts.append(
                    f'<b>{name}</b><br>' +
                    f'Population: {val:,.0f}<br>' +
                    f'Percentage: {pct:.1f}%<br>'
                )
            
            # Create treemap with flat structure (no hierarchy)
            # Use sort=False to maintain the order we defined (categories from largest to smallest)
            fig = go.Figure(go.Treemap(
                labels=[f"{name}<br>{pct:.1f}%" for name, pct in zip(city_names, percentages)],
                parents=[''] * len(city_names),
                values=scaled_populations,
                textposition='middle center',
                marker=dict(
                    colors=colors,
                    line=dict(width=2, color='white')
                ),
                hovertext=hover_texts,
                hoverinfo='text',
                pathbar=dict(visible=False),
                sort=False  # Preserve the order we sorted by category
            ))
            
            # Add invisible traces for legend (one for each size category)
            for category in size_categories_ordered:
                fig.add_trace(go.Scatter(
                    x=[None],
                    y=[None],
                    mode='markers',
                    marker=dict(size=12, color=CITY_SIZE_COLORS.get(category, '#95a5a6')),
                    name=category,
                    showlegend=True
                ))
            
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
                margin=dict(l=10, r=10, t=80, b=10)
            )
            
            # Hide axes (even though treemap doesn't use them)
            fig.update_xaxes(visible=False)
            fig.update_yaxes(visible=False)
            
            return fig
            
        except Exception as e:
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='treemap',
                title='Urban Population Distribution by City Size'
            )
    
    @app.callback(
        Output('cities-distribution-download', 'data'),
        Input('cities-distribution-download-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_cities_distribution_data(n_clicks):
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
