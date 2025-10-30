"""
Callbacks for Access to Electricity, Urban visualization
Shows line chart of urban electricity access percentage over time for selected country with regional benchmarks
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.data_loader import load_wdi_data, load_urbanization_indicators_dict
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.benchmark_config import get_benchmark_names, get_benchmark_colors
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def register_access_to_electricity_urban_callbacks(app):
    """Register callbacks for Access to Electricity, Urban chart"""
    
    # Load static data once at registration time for performance
    electricity_data = load_wdi_data('EG.ELC.ACCS.UR.ZS')
    indicators_dict = load_urbanization_indicators_dict()
    countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
    benchmark_colors_dict = get_benchmark_colors()
    benchmark_names = get_benchmark_names()
    
    @app.callback(
        [Output('access-to-electricity-urban-chart', 'figure'),
         Output('access-to-electricity-urban-chart', 'style'),
         Output('access-to-electricity-urban-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('electricity-combined-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_access_to_electricity_urban_chart(selected_country, combined_benchmarks):
        """Generate line chart showing access to electricity in urban areas over time"""
        try:
            # Split combined benchmarks into regions and countries
            benchmark_regions = [b for b in (combined_benchmarks or []) if b in benchmark_colors_dict]
            benchmark_countries = [b for b in (combined_benchmarks or []) if b not in benchmark_colors_dict]

            # Load indicators dictionary for title (pre-loaded)
            chart_title = indicators_dict.get('EG.ELC.ACCS.UR.ZS', 'Access to Electricity, Urban')
            
            if electricity_data.empty:
                raise Exception("No data available for selected country")
            
            # Create the figure
            fig = go.Figure()
            
            # Get country data for selected country
            if selected_country and selected_country in electricity_data['Country Code'].values:
                country_data = electricity_data[electricity_data['Country Code'] == selected_country].copy()
                country_data = country_data.sort_values('Year')
                if not country_data.empty:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    fig.add_trace(go.Scatter(
                        x=country_data['Year'],
                        y=country_data['Value'],
                        mode='lines+markers',
                        name=country_name,
                        line=dict(color='#295e84', width=3),
                        marker=dict(size=6, color='#295e84'),
                        hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Electricity Access: %{{y:.1f}}%<extra></extra>'
                    ))
                    title_suffix = f"{country_name}"
                else:
                    raise Exception("No country selected")
            else:
                raise Exception("No country selected")
            
            # Add country benchmarks if selected
            if benchmark_countries:
                for iso in benchmark_countries:
                    if iso in electricity_data['Country Code'].values:
                        bench_data = electricity_data[electricity_data['Country Code'] == iso].copy()
                        bench_data = bench_data.sort_values('Year')
                        if not bench_data.empty:
                            bench_name = countries_and_regions_dict.get(iso, iso)
                            fig.add_trace(go.Scatter(
                                x=bench_data['Year'],
                                y=bench_data['Value'],
                                mode='lines',
                                name=bench_name,
                                line=dict(width=2, dash='dot'),
                                hovertemplate=f'<b>{bench_name}</b><br>Year: %{{x}}<br>Electricity Access: %{{y:.1f}}%<extra></extra>'
                            ))
            
            # Add benchmark regions if selected
            if benchmark_regions:
                for region in benchmark_regions:
                    if region in electricity_data['Country Code'].values:
                        region_data = electricity_data[electricity_data['Country Code'] == region].copy()
                        region_data = region_data.sort_values('Year')
                        
                        if not region_data.empty:
                            fig.add_trace(go.Scatter(
                                x=region_data['Year'],
                                y=region_data['Value'],
                                mode='lines',
                                name=benchmark_names.get(region, region),
                                line=dict(color=benchmark_colors_dict.get(region, '#95a5a6'), width=2, dash='dash'),
                                hovertemplate=f'<b>{benchmark_names.get(region, region)}</b><br>Year: %{{x}}<br>Electricity Access: %{{y:.1f}}%<extra></extra>'
                            ))
            
            # Create separate title
            title_text = html.H6([html.B(title_suffix), f' | {chart_title}'], 
                                className='chart-title')
            
            # Update layout (without title)
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Access to Electricity<br>(% of Urban Population)',
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
                margin=dict(b=0, t=60)
            )

            return fig, {'display': 'block'}, title_text
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'access-to-electricity-urban-download',
        lambda: electricity_data,
        'access_to_electricity_urban'
    )