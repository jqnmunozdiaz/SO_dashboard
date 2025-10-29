"""
Callbacks for Urban Population Living in Slums visualization
Shows line chart of slums population percentage over time for selected country with regional benchmarks
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.data_loader import load_wdi_data, load_urbanization_indicators_dict
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.benchmark_config import get_benchmark_colors, get_benchmark_names
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def register_urban_population_living_in_slums_callbacks(app):
    """Register callbacks for Urban Population Living in Slums chart"""
    
    # Load static data once at registration time for performance
    slums_data = load_wdi_data('EN.POP.SLUM.UR.ZS')
    indicators_dict = load_urbanization_indicators_dict()
    countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
    benchmark_colors_dict = get_benchmark_colors()
    benchmark_names = get_benchmark_names()
    
    @app.callback(
        [Output('urban-population-slums-chart', 'figure'),
         Output('urban-population-slums-chart', 'style'),
         Output('urban-population-slums-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('slums-combined-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_urban_population_slums_chart(selected_country, combined_benchmarks):
        """Generate line chart showing urban population living in slums over time"""
        try:
            # Split combined benchmarks into regions and countries
            benchmark_regions = [b for b in (combined_benchmarks or []) if b in benchmark_colors_dict]
            benchmark_countries = [b for b in (combined_benchmarks or []) if b not in benchmark_colors_dict]
            # Load slums data (pre-loaded)
            
            # Load indicators dictionary for title (pre-loaded)
            chart_title = indicators_dict.get('EN.POP.SLUM.UR.ZS', 'Urban Population Living in Slums')
            
            # Create the figure
            fig = go.Figure()
            
            # Get country data
            if selected_country and selected_country in slums_data['Country Code'].values:
                country_data = slums_data[slums_data['Country Code'] == selected_country].copy()
                country_data = country_data.sort_values('Year')
                
                if not country_data.empty:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    
                    # Add country line
                    fig.add_trace(go.Scatter(
                        x=country_data['Year'],
                        y=country_data['Value'],
                        mode='lines+markers',
                        name=country_name,
                        line=dict(color='#295e84', width=3),
                        marker=dict(size=6, color='#295e84'),
                        hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Slums Population: %{{y:.1f}}%<extra></extra>'
                    ))
                    
                    title_suffix = f"{country_name}"
                else:
                    raise Exception("No country selected")
            else:
                raise Exception("No country selected")
            
            # Add benchmark regions if selected
            
            if benchmark_regions:
                for region in benchmark_regions:
                    if region in slums_data['Country Code'].values:
                        region_data = slums_data[slums_data['Country Code'] == region].copy()
                        region_data = region_data.sort_values('Year')
                        
                        if not region_data.empty:
                            fig.add_trace(go.Scatter(
                                x=region_data['Year'],
                                y=region_data['Value'],
                                mode='lines',
                                name=benchmark_names.get(region, region),
                                line=dict(color=benchmark_colors_dict.get(region, '#95a5a6'), width=2, dash='dash'),
                                hovertemplate=f'<b>{benchmark_names.get(region, region)}</b><br>Year: %{{x}}<br>Slums Population: %{{y:.1f}}%<extra></extra>'
                            ))
            
            # Add country benchmarks if selected
            if benchmark_countries:
                # Define colors for benchmark countries (using a color palette)
                country_colors = ['#e74c3c', '#f39c12', '#27ae60', '#3498db', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
                
                for i, country_iso in enumerate(benchmark_countries):
                    if country_iso in slums_data['Country Code'].values:
                        country_benchmark_data = slums_data[slums_data['Country Code'] == country_iso].copy()
                        country_benchmark_data = country_benchmark_data.sort_values('Year')
                        
                        if not country_benchmark_data.empty:
                            country_name = countries_and_regions_dict.get(country_iso, country_iso)
                            # Cycle through colors
                            color = country_colors[i % len(country_colors)]
                            
                            fig.add_trace(go.Scatter(
                                x=country_benchmark_data['Year'],
                                y=country_benchmark_data['Value'],
                                mode='lines+markers',
                                name=country_name,
                                line=dict(color=color, width=2, dash='dot'),
                                marker=dict(size=4, color=color),
                                hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Slums Population: %{{y:.1f}}%<extra></extra>'
                            ))
            
            # Create separate title
            title_text = html.H6([html.B(title_suffix), f' | {chart_title}'], 
                                style={'marginBottom': '1rem', 'color': '#2c3e50'})
            
            # Update layout (without title)
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Population Living in Slums<br>(% of Urban Population)',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                yaxis=dict(
                    range=[0, 100],  # Y-axis from 0% to 100%
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='#e5e7eb',
                    ticksuffix='%'
                ),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                margin=dict(b=80, t=100)
            )

            return fig, {'display': 'block'}, title_text
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'urban-population-slums-download',
        lambda: slums_data,
        'urban_population_slums'
    )