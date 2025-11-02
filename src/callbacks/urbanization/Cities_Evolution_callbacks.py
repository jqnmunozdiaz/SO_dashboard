"""
Callbacks for Cities Evolution stacked bar chart visualization
Shows evolution of urban population across city size categories over time
"""

from dash import Input, Output, html
import plotly.express as px

from ...utils.data_loader import load_city_size_distribution
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from ...utils.color_utils import CITY_SIZE_COLORS, CITY_SIZE_CATEGORIES_ORDERED
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

            # Prepare data for Plotly Express
            filtered_data = filtered_data.copy()
            
            # Calculate total max population to determine if we should use millions
            max_population = (filtered_data['Population'].sum() * 1000)
            use_millions = max_population >= 1e6
            population_divisor = 1e6 if use_millions else 1
            yaxis_title = 'Urban Population (Millions)' if use_millions else 'Urban Population'
            
            # Add display population column
            filtered_data['Population_Display'] = filtered_data['Population'] * 1000 / population_divisor
            
            # For stacking order: In Plotly Express, category_orders determines trace order
            # First category in category_orders list = BOTTOM of stack
            # Last category in category_orders list = TOP of stack
            # We want: Gray at bottom, Red at top
            # So category_orders should be: Gray -> Green -> Blue -> Yellow -> Orange -> Red
            
            # Sort data by population ASCENDING within each category
            # In stacked bars, first rows in DataFrame = bottom of segment, last rows = top of segment
            # So population ascending means smallest cities render first (bottom), largest render last (top)
            filtered_data = filtered_data.sort_values(
                ['Year', 'Size Category', 'Population'], 
                ascending=[True, True, True]  # Population ascending = largest cities render last (on top within category)
            )
            
            # Create stacked bar chart with Plotly Express
            fig = px.bar(
                filtered_data,
                x='Year',
                y='Population_Display',
                color='Size Category',
                hover_data={
                    'City Name': True,
                    'Size Category': True,
                    'Population_Display': False,  # We'll format this manually
                    'Year': False
                },
                color_discrete_map=CITY_SIZE_COLORS,
                # category_orders controls stacking: first item = bottom, last item = top
                # Use normal order (smallest to largest) so Red (10M+) is at top
                category_orders={'Size Category': CITY_SIZE_CATEGORIES_ORDERED}
            )
            
            # Reverse the legend order to show Red at top, Gray at bottom
            fig.update_layout(legend={'traceorder': 'reversed'})
            
            # Customize hover template with properly formatted population
            if use_millions:
                # Format as millions with 2 decimal places, no rounding
                hover_template = (
                    '<b>%{customdata[0]}</b><br>' +
                    'Size: %{customdata[1]}<br>' +
                    'Population: %{y:.2f}M<br>' +
                    '<extra></extra>'
                )
            else:
                # Format with thousands separator
                hover_template = (
                    '<b>%{customdata[0]}</b><br>' +
                    'Size: %{customdata[1]}<br>' +
                    'Population: %{y:,.0f}<br>' +
                    '<extra></extra>'
                )
            
            fig.update_traces(hovertemplate=hover_template)
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Create separate title
            chart_title = html.H6([html.B(country_name), ' | Evolution of Urban Population over Time across Cities'], 
                                 className='chart-title')
            
            # Update layout to match World Bank styling
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
                    dtick=5,
                    type='linear'  # Ensure years are treated as continuous
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
