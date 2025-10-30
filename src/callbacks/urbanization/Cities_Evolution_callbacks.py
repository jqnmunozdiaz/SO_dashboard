"""
Callbacks for Cities Evolution stacked bar chart visualization
Shows evolution of urban population across city size categories over time
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.data_loader import load_city_size_distribution
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from ...utils.color_utils import CITY_SIZE_COLORS
from config.settings import CHART_STYLES

def register_cities_evolution_callbacks(app):
    """Register callbacks for Cities Evolution stacked bar chart"""
    
    # Load static data once at registration time for performance
    data = load_city_size_distribution()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        [Output('cities-evolution-chart', 'figure'),
         Output('cities-evolution-chart', 'style'),
         Output('cities-evolution-title', 'children')],
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def generate_cities_evolution_chart(selected_country):
        try:
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Filter for selected country
            filtered_data = data[data['Country Code'] == selected_country]
            
            if filtered_data.empty:
                raise Exception(f"No data available for {countries_dict.get(selected_country, selected_country)}")

            # Get unique years and sort them
            years = sorted(filtered_data['Year'].unique())
            
            # Calculate total max population to determine if we should use millions
            max_population = 0
            for year in years:
                year_total = filtered_data[filtered_data['Year'] == year]['Population'].sum() * 1000
                if year_total > max_population:
                    max_population = year_total
            
            # Determine if we should display in millions
            use_millions = max_population >= 1000000
            population_divisor = 1000000 if use_millions else 1
            yaxis_title = 'Urban Population (Millions)' if use_millions else 'Urban Population'
            
            # Define size categories in order (smallest to largest for bottom-to-top stacking)
            size_categories_ordered = [
                'Fewer than 300 000',
                '300 000 to 500 000',
                '500 000 to 1 million',
                '1 to 5 million',
                '5 to 10 million',
                '10 million or more'
            ]
            
            # Create stacked bar chart - bars ordered by size category for each year
            fig = go.Figure()
                       
            # For each year, we need to add cities in order by size category
            for year in years:
                year_data = filtered_data[filtered_data['Year'] == year]
                
                # Sort cities by size category for this year, then by population within category
                cities_by_category_this_year = {}
                for category in size_categories_ordered:
                    category_data = year_data[year_data['Size Category'] == category]
                    # Sort by population (ascending) within this category so largest cities are on top
                    category_data_sorted = category_data.sort_values('Population', ascending=True)
                    cities_in_category = category_data_sorted['City Name'].tolist()
                    cities_by_category_this_year[category] = cities_in_category
                
                # Add bars for this year, ordered by size category (then by population within category)
                for size_category in size_categories_ordered:
                    for city_name in cities_by_category_this_year[size_category]:
                        city_data = year_data[year_data['City Name'] == city_name]
                        
                        if not city_data.empty:
                            pop_value = city_data.iloc[0]['Population'] * 1000 / population_divisor
                            year_size_category = city_data.iloc[0]['Size Category']
                            color = CITY_SIZE_COLORS.get(year_size_category, '#95a5a6')
                            
                            # Format hover text
                            if use_millions:
                                pop_text = f'{pop_value:.2f}M'
                            else:
                                pop_text = f'{pop_value:,.0f}'
                            
                            hover_text = (
                                f'<b>{city_name}</b><br>' +
                                f'Size: {year_size_category}<br>' +
                                f'Population: {pop_text}<br>' +
                                '<extra></extra>'
                            )
                            
                            fig.add_trace(go.Bar(
                                name=city_name,
                                x=[year],
                                y=[pop_value],
                                marker_color=color,
                                hovertemplate=hover_text,
                                legendgroup=year_size_category,
                                showlegend=False
                            ))
            
            # Add invisible traces for legend (one for each size category in order)
            for category in reversed(size_categories_ordered):
                fig.add_trace(go.Bar(
                    name=category,
                    x=[None],
                    y=[None],
                    marker_color=CITY_SIZE_COLORS.get(category, '#95a5a6'),
                    showlegend=True,
                    legendgroup=category
                ))
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Create separate title
            chart_title = html.H6([html.B(country_name), ' | Urban Population by Individual Cities'], 
                                 className='chart-title')
            
            fig.update_layout(
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
                    borderwidth=0
                ),
                height=600,
                margin=dict(r=250, l=80, t=50, b=0),
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
                    tickformat=',.1f' if use_millions else ','
                )
            )
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'cities-evolution-download',
        lambda: data,
        'cities_individual_evolution'
    )
