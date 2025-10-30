"""
Callbacks for Cities Distribution treemap visualization
Shows distribution of urban population across city size categories using Plotly treemap
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.data_loader import load_city_size_distribution
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.download_helpers import create_simple_download_callback
from ...utils.color_utils import CITY_SIZE_COLORS
from ...utils.component_helpers import create_simple_error_message
from config.settings import CHART_STYLES

def register_cities_distribution_callbacks(app):
    """Register callbacks for Cities Distribution Plotly treemap chart"""
    
    # Load static data once at registration time for performance
    data = load_city_size_distribution()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        [Output('cities-distribution-chart', 'figure'),
         Output('cities-distribution-chart', 'style'),
         Output('cities-distribution-title', 'children')],
        [
            Input('main-country-filter', 'value'),
            Input('cities-distribution-year-filter', 'value')
        ],
        prevent_initial_call=False
    )
    def generate_cities_distribution_chart(selected_country, selected_year):
        """Generate Plotly treemap for cities distribution"""
        try:
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Filter for selected country and year
            filtered_data = data[
                (data['Country Code'] == selected_country) & 
                (data['Year'] == selected_year)
            ].copy()
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            if filtered_data.empty:
                raise Exception(f'No data available for {country_name} in {selected_year}')
            
            # Define size categories in order (for legend display and sorting)
            size_categories_ordered = [
                '10 million or more',
                '5 to 10 million',
                '1 to 5 million',
                '500 000 to 1 million',
                '300 000 to 500 000',
                'Fewer than 300 000'
            ]
            
            # Prepare data for treemap
            filtered_data['Population_Actual'] = filtered_data['Population'] * 1000  # Convert from thousands
            
            # Calculate total population for percentage
            total_pop = filtered_data['Population_Actual'].sum()
            filtered_data['Percentage'] = (filtered_data['Population_Actual'] / total_pop * 100).round(1)
            
            # Create category order mapping for sorting
            category_order = {cat: i for i, cat in enumerate(size_categories_ordered)}
            filtered_data['Category_Order'] = filtered_data['Size Category'].map(category_order)
            
            # Sort by category order (largest first), then by population descending within each category
            filtered_data = filtered_data.sort_values(
                ['Category_Order', 'Population_Actual'], 
                ascending=[True, False]
            ).reset_index(drop=True)
            
            # Create custom hover text
            filtered_data['hover_text'] = (
                '<b>' + filtered_data['City Name'] + '</b><br>' +
                'Population: ' + filtered_data['Population_Actual'].apply(lambda x: f'{x:,.0f}') + '<br>' +
                'Percentage: ' + filtered_data['Percentage'].astype(str) + '%<br>' +
                'Category: ' + filtered_data['Size Category'] +
                '<extra></extra>'
            )
            
            # Map colors to each city based on size category
            filtered_data['Color'] = filtered_data['Size Category'].map(CITY_SIZE_COLORS)
            
            # Create treemap with custom data for legend
            fig = go.Figure(go.Treemap(
                labels=filtered_data['City Name'],
                parents=[''] * len(filtered_data),  # All cities are at root level
                values=filtered_data['Population_Actual'],
                text=filtered_data['Percentage'].apply(lambda x: f'{x}%'),
                textposition='middle center',
                hovertemplate=filtered_data['hover_text'],
                marker=dict(
                    colors=filtered_data['Color'],
                    line=dict(width=2, color='white')
                ),
                textfont=dict(
                    size=12,
                    color='black'
                ),
                customdata=filtered_data['Size Category'],
                sort=False
            ))
            
            # Add invisible scatter traces for legend (one per size category)
            for category in size_categories_ordered:
                if category in filtered_data['Size Category'].values:
                    fig.add_trace(go.Scatter(
                        x=[None],
                        y=[None],
                        mode='markers',
                        marker=dict(
                            size=10,
                            color=CITY_SIZE_COLORS[category]
                        ),
                        showlegend=True,
                        name=category,
                        hoverinfo='skip'
                    ))
            
            # Create title separately
            chart_title = html.H6([
                html.B(country_name),
                f' | Cities Distribution by Size ({selected_year})'
            ], className='chart-title')
            
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                height=600,
                margin=dict(t=0, l=20, r=20, b=0),
                showlegend=True,
                legend=dict(
                    title=dict(text='Size Categories'),
                    orientation='v',
                    yanchor='top',
                    y=1,
                    xanchor='left',
                    x=1.02,
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='rgba(0, 0, 0, 0)',
                    borderwidth=0
                ),
                xaxis=dict(visible=False),
                yaxis=dict(visible=False)
            )
            
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'cities-distribution-download',
        lambda: data,
        'cities_size_distribution'
    )
