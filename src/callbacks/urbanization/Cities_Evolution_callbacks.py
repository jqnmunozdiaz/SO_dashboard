"""
Callbacks for Cities Evolution stacked bar chart visualization
Shows evolution of urban population across city size categories over time
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd

try:
    from ...utils.data_loader import load_city_size_distribution, load_city_agglomeration_counts
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_error_chart
    from ...utils.color_utils import CITY_SIZE_COLORS
    from config.settings import CHART_STYLES
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_city_size_distribution, load_city_agglomeration_counts
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from src.utils.color_utils import CITY_SIZE_COLORS
    from config.settings import CHART_STYLES

def register_cities_evolution_callbacks(app):
    """Register callbacks for Cities Evolution stacked bar chart"""
    
    @app.callback(
        Output('cities-evolution-chart', 'figure'),
        [Input('main-country-filter', 'value')],
        prevent_initial_call=False
    )
    def generate_cities_evolution_chart(selected_country):
        try:
            # Load data
            data = load_city_size_distribution()
            agglom_counts = load_city_agglomeration_counts()
            countries_dict = load_subsaharan_countries_and_regions_dict()
            
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Filter for selected country
            filtered_data = data[data['Country Code'] == selected_country]
            filtered_agglom = agglom_counts[agglom_counts['Country Code'] == selected_country]
            
            if filtered_data.empty:
                raise Exception(f"No data available for {countries_dict.get(selected_country, selected_country)}")
            
            # Group by year and size category, sum populations
            grouped = filtered_data.groupby(['Year', 'Size Category'])['Population'].sum().reset_index()
            
            # Define size categories in order (smallest to largest for bottom-to-top stacking)
            size_categories_ordered = [
                'Fewer than 300 000',
                '300 000 to 500 000',
                '500 000 to 1 million',
                '1 to 5 million',
                '5 to 10 million',
                '10 million or more'
            ]
            
            # Get unique years and sort them
            years = sorted(grouped['Year'].unique())
            
            # Calculate total max population to determine if we should use millions
            max_population = 0
            for year in years:
                year_total = grouped[grouped['Year'] == year]['Population'].sum() * 1000
                if year_total > max_population:
                    max_population = year_total
            
            # Determine if we should display in millions
            use_millions = max_population >= 1000000
            population_divisor = 1000000 if use_millions else 1
            yaxis_title = 'Urban Population (Millions)' if use_millions else 'Urban Population'
            yaxis_suffix = 'M' if use_millions else ''
            
            # Create stacked bar chart
            fig = go.Figure()
            
            # Add a bar for each size category (smallest first for bottom of stack)
            for category in size_categories_ordered:
                category_data = grouped[grouped['Size Category'] == category]
                
                # Create a list of populations for each year, 0 if no data
                populations = []
                for year in years:
                    year_data = category_data[category_data['Year'] == year]
                    if not year_data.empty:
                        # Convert from thousands to actual population, then to millions if needed
                        pop_value = year_data['Population'].values[0] * 1000 / population_divisor
                        populations.append(pop_value)
                    else:
                        populations.append(0)
                
                # Format hover template based on whether we're using millions
                if use_millions:
                    hover_format = 'Population: %{y:.2f}M<br>'
                else:
                    hover_format = 'Population: %{y:,.0f}<br>'
                
                fig.add_trace(go.Bar(
                    name=category,
                    x=years,
                    y=populations,
                    marker_color=CITY_SIZE_COLORS.get(category, '#95a5a6'),
                    hovertemplate='<b>%{fullData.name}</b><br>' +
                                  hover_format +
                                  '<extra></extra>'
                ))
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Add text annotations showing number of agglomerations
            for year in years:
                cumulative_height = 0
                for category in size_categories_ordered:
                    # Get population for this category and year
                    category_data = grouped[(grouped['Size Category'] == category) & (grouped['Year'] == year)]
                    if not category_data.empty:
                        pop_value = category_data['Population'].values[0] * 1000 / population_divisor
                        
                        # Get agglomeration count for this category and year
                        agglom_data = filtered_agglom[
                            (filtered_agglom['Size Category'] == category) & 
                            (filtered_agglom['Year'] == year)
                        ]
                        
                        if not agglom_data.empty:
                            count = int(agglom_data['Number of Agglomerations'].values[0])
                            
                            # Only show annotation if count > 0
                            if count > 0:
                                # Position text in the middle of this bar segment
                                text_y = cumulative_height + (pop_value / 2)
                                
                                # Format text: "1 city" or "N cities"
                                count_text = f"{count} city" if count == 1 else f"{count} cities"
                                
                                fig.add_annotation(
                                    x=year,
                                    y=text_y,
                                    text=count_text,
                                    showarrow=False,
                                    font=dict(size=10, color='white', family='Arial Black')
                                )
                        
                        cumulative_height += pop_value
            
            fig.update_layout(
                title=f'<b>{country_name}</b> | Urban Population Evolution by City Size',
                xaxis_title='Year',
                yaxis_title=yaxis_title,
                barmode='stack',
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
                margin=dict(r=250, l=80, t=80, b=80),
                xaxis=dict(
                    showgrid=False,
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    tickmode='linear',
                    dtick=5
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    tickformat=',.1f' if use_millions else ',',
                    ticksuffix=yaxis_suffix
                )
            )
            
            return fig
            
        except Exception as e:
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='bar',
                title='Urban Population Evolution by City Size',
                xaxis_title='Year',
                yaxis_title='Urban Population'
            )
