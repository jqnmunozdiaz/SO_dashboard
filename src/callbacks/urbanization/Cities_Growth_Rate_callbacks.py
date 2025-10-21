"""
Callbacks for Cities Growth Rate scatterplot visualization
Shows population growth rate vs built-up area growth rate for cities (2000-2020)
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd

try:
    from ...utils.data_loader import load_cities_growth_rate
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_error_chart
    from ...utils.download_helpers import prepare_csv_download
    from ...utils.color_utils import CITY_SIZE_COLORS
    from config.settings import CHART_STYLES
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_cities_growth_rate
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from src.utils.download_helpers import prepare_csv_download
    from src.utils.color_utils import CITY_SIZE_COLORS
    from config.settings import CHART_STYLES

def register_cities_growth_rate_callbacks(app):
    """Register callbacks for Cities Growth Rate scatterplot chart"""
    
    # Load static data once at registration time for performance
    data = load_cities_growth_rate()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        Output('cities-growth-rate-chart', 'figure'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def generate_cities_growth_rate_chart(selected_country):
        try:
            # Load data (pre-loaded)
            
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Filter for selected country
            filtered_data = data[data['ISO3'] == selected_country].copy()
            
            if filtered_data.empty:
                raise Exception(f"No data available for {countries_dict.get(selected_country, selected_country)}")
            
            # Convert CAGR from decimal to percentage
            filtered_data['pop_cagr_pct'] = filtered_data['pop_cagr'] * 100
            filtered_data['built_up_cagr_pct'] = filtered_data['built_up_cagr'] * 100
            
            # Define size categories in order (for legend consistency)
            size_categories_ordered = [
                '10 million or more',
                '5 to 10 million',
                '1 to 5 million',
                '500 000 to 1 million',
                '300 000 to 500 000',
                'Fewer than 300 000'
            ]
            
            # Create figure
            fig = go.Figure()
            
            # Add scatter traces for each size category
            for category in size_categories_ordered:
                category_data = filtered_data[filtered_data['size_category'] == category]
                
                if not category_data.empty:
                    # Calculate marker sizes based on 2020 population (logarithmic scaling)
                    # Scale from ~4 to ~28 pixels based on population size for better visual distinction
                    min_size = 4
                    max_size = 28
                    pop_min = filtered_data['pop_2020'].min()
                    pop_max = filtered_data['pop_2020'].max()
                    
                    if pop_max > pop_min:
                        # Logarithmic scaling to handle wide range of population sizes
                        sizes = []
                        for pop in category_data['pop_2020']:
                            # Use log scale, but ensure minimum size for small cities
                            log_size = min_size + (max_size - min_size) * (pop - pop_min) / (pop_max - pop_min)
                            sizes.append(max(min_size, min(max_size, log_size)))
                    else:
                        sizes = [12] * len(category_data)  # Default size if all same
                    
                    # Create hover text
                    hover_texts = []
                    for _, row in category_data.iterrows():
                        hover_texts.append(
                            f"<b>{row['agglosName']}</b><br>" +
                            f"Population 2020: {row['pop_2020']:,.0f}<br>" +
                            f"Population Growth Rate: {row['pop_cagr_pct']:.2f}%<br>" +
                            f"Built-up Growth Rate: {row['built_up_cagr_pct']:.2f}%<br>" +
                            f"Size Category: {row['size_category']}<br>"
                        )
                    
                    fig.add_trace(go.Scatter(
                        x=category_data['pop_cagr_pct'],
                        y=category_data['built_up_cagr_pct'],
                        mode='markers',
                        name=category,
                        marker=dict(
                            size=sizes,
                            color=CITY_SIZE_COLORS.get(category, '#95a5a6'),
                            line=dict(width=1, color='white'),
                            sizemode='diameter',
                            opacity=0.8
                        ),
                        text=hover_texts,
                        hoverinfo='text',
                        showlegend=True
                    ))
            
            # Add diagonal reference line (y=x) where population and built-up growth are equal
            x_range = [filtered_data['pop_cagr_pct'].min() - 1, filtered_data['pop_cagr_pct'].max() + 1]
            y_range = [filtered_data['built_up_cagr_pct'].min() - 1, filtered_data['built_up_cagr_pct'].max() + 1]
            
            # Find the common range for the diagonal line
            min_val = min(x_range[0], y_range[0])
            max_val = max(x_range[1], y_range[1])
            
            fig.add_trace(go.Scatter(
                x=[min_val, max_val],
                y=[min_val, max_val],
                mode='lines',
                name='Equal Growth (y=x)',
                line=dict(color='gray', width=1, dash='dash'),
                showlegend=True,
                hoverinfo='skip'
            ))
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            fig.update_layout(
                title=f'<b>{country_name}</b> | Built-up and Population Growth Rate in Cities (2000-2020)',
                xaxis=dict(
                    title='Population Growth Rate (%)',
                    showgrid=True,
                    gridcolor='#e2e8f0',
                    zeroline=True,
                    zerolinecolor='#374151',
                    zerolinewidth=1,
                    ticksuffix='%'
                ),
                yaxis=dict(
                    title='Built-up Area Growth Rate (%)',
                    showgrid=True,
                    gridcolor='#e2e8f0',
                    zeroline=True,
                    zerolinecolor='#374151',
                    zerolinewidth=1,
                    ticksuffix='%'
                ),
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
                    borderwidth=0
                ),
                height=600,
                hovermode='closest'
            )
            
            return fig
            
        except Exception as e:
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='scatter',
                xaxis_title='Population Growth Rate (%)',
                yaxis_title='Built-up Area Growth Rate (%)',
                title='Built-up and Urbanization Growth Rate in Cities (2000-2020)'
            )
    
    @app.callback(
        Output('cities-growth-rate-download', 'data'),
        Input('cities-growth-rate-download-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_cities_growth_rate_data(n_clicks):
        """Download cities growth rate data as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            # Load full dataset (pre-loaded)
            
            filename = "africapolis_ghsl2023_cagr_2000_2020"
            
            return prepare_csv_download(data, filename)
        
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None
