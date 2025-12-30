"""
Callbacks for Cities Growth Rate scatterplot visualization
Shows population growth rate vs built-up area growth rate for cities (2015-2020)
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.data_loader import load_cities_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES

def register_cities_growth_rate_callbacks(app):
    """Register callbacks for Cities Growth Rate scatterplot chart"""
    
    # Load static data once at registration time for performance
    data = load_cities_data()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    year = 2025

    @app.callback(
        [Output('cities-growth-rate-chart', 'figure'),
         Output('cities-growth-rate-chart', 'style'),
         Output('cities-growth-rate-title', 'children')],
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def generate_cities_growth_rate_chart(selected_country):
        try:
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Filter for selected country
            filtered_data = data[data['ISO3'] == selected_country].copy()
            
            if filtered_data.empty:
                raise Exception(f"No data available for {countries_dict.get(selected_country, selected_country)}")
            
            # Create figure
            fig = go.Figure()
                
            # Create hover text
            hover_texts = []
            for _, row in filtered_data.iterrows():
                hover_texts.append(
                    f"<b>{row['Agglomeration_Name']}</b><br>" +
                    f"Population ({year}): {int(row[f'africapolis_pop_{year}']):,}<br>" +
                    f"Built-up ({year}): {row[f'worldpop_built_km2_{year}']:.1f} km²<br>"
                    f"Built-up per capita: {row[f'buppercapita_{year}']:.1f} m²/person<br>"
                )
            
            fig.add_trace(go.Scatter(
                x=filtered_data[f'africapolis_pop_{year}'],
                y=filtered_data[f'buppercapita_{year}'],
                mode='markers',
                marker=dict(
                    size=12,
                    color='#95a5a6',
                    line=dict(width=1, color='white'),
                    sizemode='diameter',
                    opacity=0.8
                ),
                text=hover_texts,
                hoverinfo='text',
                showlegend=False
            ))
            
            # Set x-axis to start at 0
            fig.update_xaxes(range=[4, None])
            # Add vertical line at x=10^4 (start of plot)
            fig.add_shape(
                type='line',
                x0=10**4, x1=10**4,
                y0=0, y1=1,
                yref='paper',
                line=dict(color='#374151', width=1),
                layer='below'
            )
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Create separate title
            chart_title = html.H6([html.B(country_name), f' | Built-up per capita in Cities ({year})'], 
                                 className='chart-title')
            
            fig.update_layout(
                xaxis=dict(
                    title='Population (log scale)',
                    showgrid=True,
                    gridcolor='#e2e8f0',
                    zeroline=True,
                    zerolinecolor='#374151',
                    zerolinewidth=1,
                    type='log',
                    range=[4, None]
                ),
                
                yaxis=dict(
                    title='Built-up Area per Capita (m² per person)',
                    showgrid=True,
                    gridcolor='#e2e8f0',
                    zeroline=True,
                    zerolinecolor='#374151',
                    zerolinewidth=1,
                    ticksuffix='',
                    range=[0, None]
                ),
                
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=False,
                margin=dict(t=40, b=80, l=80, r=150),
                height=600,
                hovermode='closest'
            )

            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'cities-growth-rate-download',
        lambda: data
    )
