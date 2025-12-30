"""
Callbacks for Urbanization Level visualization
Shows line chart of urban population percentage over time for selected country with regional benchmarks
Based on UN DESA World Urbanization Prospects 2025 (WUP2025) National Definitions data
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.data_loader import load_wup2025_national_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.benchmark_config import get_benchmark_colors, get_benchmark_names
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def register_urbanization_rate_callbacks(app):
    """Register callbacks for Urbanization Rate chart"""
    
    # Load static data once at registration time for performance
    wup_data = load_wup2025_national_data()
    countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
    benchmark_colors_dict = get_benchmark_colors()
    benchmark_names = get_benchmark_names()
    
    @app.callback(
        [Output('urbanization-rate-chart', 'figure'),
         Output('urbanization-rate-chart', 'style'),
         Output('urbanization-rate-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('urbanization-rate-combined-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_urbanization_rate_chart(selected_country, combined_benchmarks):
        """Generate line chart showing urbanization rate over time"""
        try:
            # Split combined benchmarks into regions and countries
            benchmark_regions = [b for b in (combined_benchmarks or []) if b in benchmark_colors_dict]
            benchmark_countries = [b for b in (combined_benchmarks or []) if b not in benchmark_colors_dict]

            # Load country and region mapping for ISO code to full name conversion (pre-loaded)            
            if wup_data.empty:
                return create_simple_error_message("No data available")
            
            # Create the figure
            fig = go.Figure()
            
            # Get country data
            if selected_country and selected_country in wup_data['ISO3_Code'].values:
                country_data = wup_data[wup_data['ISO3_Code'] == selected_country].copy()
                country_data = country_data.sort_values('Year')
                
                if not country_data.empty:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    
                    # Split data for historical (<=2025) and projections (>=2025)
                    hist_data = country_data[country_data['Year'] <= 2025]
                    proj_data = country_data[country_data['Year'] >= 2025]

                    # Add historical (solid line)
                    if not hist_data.empty:
                        fig.add_trace(go.Scatter(
                            x=hist_data['Year'],
                            y=hist_data['Urbanization_Rate'] * 100,
                            mode='lines',
                            name=country_name,
                            line=dict(color='#295e84', width=3),
                            hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Urbanization Level: %{{y:.1f}}%<extra></extra>',
                            showlegend=True
                        ))

                    # Add projections (dashed line)
                    if not proj_data.empty:
                        fig.add_trace(go.Scatter(
                            x=proj_data['Year'],
                            y=proj_data['Urbanization_Rate'] * 100,
                            mode='lines',
                            name=country_name,
                            line=dict(color='#295e84', width=3, dash='dash'),
                            hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Urbanization Level: %{{y:.1f}}%<extra></extra>',
                            showlegend=False
                        ))

                    title_suffix = f"{country_name}"
                else:
                    raise Exception("No country selected")
            else:
                raise Exception("No country selected")
            
            # Add benchmark regions if selected
            
            if benchmark_regions:
                for region in benchmark_regions:
                    if region in wup_data['ISO3_Code'].values:
                        region_data = wup_data[wup_data['ISO3_Code'] == region].copy()
                        region_data = region_data.sort_values('Year')
                        
                        if not region_data.empty:
                            region_name = benchmark_names.get(region, region)
                            region_color = benchmark_colors_dict.get(region, '#95a5a6')
                            
                            # Split data for historical (<=2025) and projections (>=2025)
                            region_hist = region_data[region_data['Year'] <= 2025]
                            region_proj = region_data[region_data['Year'] >= 2025]
                            
                            # Add historical (solid line)
                            if not region_hist.empty:
                                fig.add_trace(go.Scatter(
                                    x=region_hist['Year'],
                                    y=region_hist['Urbanization_Rate'] * 100,
                                    mode='lines',
                                    name=region_name,
                                    line=dict(color=region_color, width=2),
                                    hovertemplate=f'<b>{region_name}</b><br>Year: %{{x}}<br>Urbanization Level: %{{y:.1f}}%<extra></extra>',
                                    showlegend=True
                                ))
                            
                            # Add projections (dashed line)
                            if not region_proj.empty:
                                fig.add_trace(go.Scatter(
                                    x=region_proj['Year'],
                                    y=region_proj['Urbanization_Rate'] * 100,
                                    mode='lines',
                                    name=region_name,
                                    line=dict(color=region_color, width=2, dash='dash'),
                                    hovertemplate=f'<b>{region_name}</b><br>Year: %{{x}}<br>Urbanization Level: %{{y:.1f}}%<extra></extra>',
                                    showlegend=False
                                ))
            
            # Add country benchmarks if selected
            if benchmark_countries:
                # Define colors for benchmark countries (using a color palette)
                country_colors = ['#e74c3c', '#f39c12', '#27ae60', '#3498db', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
                
                for i, country_iso in enumerate(benchmark_countries):
                    if country_iso in wup_data['ISO3_Code'].values:
                        country_benchmark_data = wup_data[wup_data['ISO3_Code'] == country_iso].copy()
                        country_benchmark_data = country_benchmark_data.sort_values('Year')
                        
                        if not country_benchmark_data.empty:
                            country_name = countries_and_regions_dict.get(country_iso, country_iso)
                            # Cycle through colors
                            color = country_colors[i % len(country_colors)]
                            
                            # Split data for historical (<=2025) and projections (>=2025)
                            country_hist = country_benchmark_data[country_benchmark_data['Year'] <= 2025]
                            country_proj = country_benchmark_data[country_benchmark_data['Year'] >= 2025]
                            
                            # Add historical (solid line with markers)
                            if not country_hist.empty:
                                fig.add_trace(go.Scatter(
                                    x=country_hist['Year'],
                                    y=country_hist['Urbanization_Rate'] * 100,
                                    mode='lines',
                                    name=country_name,
                                    line=dict(color=color, width=2),
                                    marker=dict(size=4, color=color),
                                    hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Urbanization Level: %{{y:.1f}}%<extra></extra>',
                                    showlegend=True
                                ))
                            
                            # Add projections (dashed line with markers)
                            if not country_proj.empty:
                                fig.add_trace(go.Scatter(
                                    x=country_proj['Year'],
                                    y=country_proj['Urbanization_Rate'] * 100,
                                    mode='lines',
                                    name=country_name,
                                    line=dict(color=color, width=2, dash='dot'),
                                    marker=dict(size=4, color=color),
                                    hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Urbanization Level: %{{y:.1f}}%<extra></extra>',
                                    showlegend=False
                                ))
            
            # Create separate title
            chart_title = html.H6([html.B(title_suffix), ' | Urbanization Level'], 
                                 className='chart-title')
            
            # Update layout (without title)
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Urban Population<br>(% of Total Population)',
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
            
            # Add vertical line at 2025 to separate historical from projections
            fig.add_vline(x=2025, line_dash="dash", line_color="gray", opacity=0.5)

            # Add annotations for Historical and Projections
            fig.add_annotation(
                x=2024,
                y=1,
                yref="paper",
                text="Historical",
                showarrow=False,
                font=dict(size=12, color="gray"),
                yanchor="top",
                xanchor="right"
            )
            fig.add_annotation(
                x=2026,
                y=1,
                yref="paper",
                text="Projections",
                showarrow=False,
                font=dict(size=12, color="gray"),
                yanchor="top",
                xanchor="left"
            )
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'urbanization-rate-download',
        lambda: wup_data
    )
