"""
Callbacks for Urbanization Rate visualization
Shows line chart of urban population percentage over time for selected country with regional benchmarks
Based on UN DESA World Urbanization Prospects data
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ...utils.data_loader import load_undesa_urban_projections
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.benchmark_config import get_benchmark_colors, get_benchmark_names
    from ...utils.component_helpers import create_error_chart
    from ...utils.download_helpers import prepare_csv_download
    from config.settings import CHART_STYLES
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_undesa_urban_projections
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.benchmark_config import get_benchmark_colors, get_benchmark_names
    from src.utils.component_helpers import create_error_chart
    from src.utils.download_helpers import prepare_csv_download
    from config.settings import CHART_STYLES


def register_urbanization_rate_callbacks(app):
    """Register callbacks for Urbanization Rate chart"""
    
    @app.callback(
        Output('urbanization-rate-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('urbanization-rate-benchmark-selector', 'value'),
         Input('urbanization-rate-country-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_urbanization_rate_chart(selected_country, benchmark_regions, benchmark_countries):
        """Generate line chart showing urbanization rate over time"""
        try:
            # Load UNDESA urban projections data
            undesa_data = load_undesa_urban_projections()
            
            # Load country and region mapping for ISO code to full name conversion
            countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
            
            if undesa_data.empty:
                # Return empty chart if no data
                return create_error_chart(
                    error_message="No data available",
                    chart_type='line',
                    xaxis_title='Year',
                    yaxis_title='Urban Population (% of Total Population)',
                    yaxis_range=[0, 100],
                    title='Urbanization Rate'
                )
            
            # Filter for urban proportion data only
            urban_prop_data = undesa_data[undesa_data['indicator'] == 'wup_urban_prop'].copy()
            
            # Create the figure
            fig = go.Figure()
            
            # Get country data
            if selected_country and selected_country in urban_prop_data['ISO3'].values:
                country_data = urban_prop_data[urban_prop_data['ISO3'] == selected_country].copy()
                country_data = country_data.sort_values('year')
                
                if not country_data.empty:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    
                    # Split data for historical (<=2025) and projections (>2025)
                    hist_data = country_data[country_data['year'] <= 2025]
                    proj_data = country_data[country_data['year'] > 2025]

                    # Add historical (solid line)
                    if not hist_data.empty:
                        fig.add_trace(go.Scatter(
                            x=hist_data['year'],
                            y=hist_data['value'] * 100,
                            mode='lines',
                            name=f'{country_name} (Historical)',
                            line=dict(color='#295e84', width=3),
                            hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Urbanization Rate: %{{y:.1f}}%<extra></extra>'
                        ))

                    # Add projections (dashed line)
                    if not proj_data.empty:
                        fig.add_trace(go.Scatter(
                            x=proj_data['year'],
                            y=proj_data['value'] * 100,
                            mode='lines',
                            name=f'{country_name} (Projections)',
                            line=dict(color='#295e84', width=3, dash='dash'),
                            hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Urbanization Rate: %{{y:.1f}}%<extra></extra>'
                        ))

                    title_suffix = f"{country_name}"
                else:
                    raise Exception("No country selected")
            else:
                raise Exception("No country selected")
            
            # Add benchmark regions if selected
            benchmark_colors = get_benchmark_colors()
            benchmark_names = get_benchmark_names()
            
            if benchmark_regions:
                for region in benchmark_regions:
                    if region in urban_prop_data['ISO3'].values:
                        region_data = urban_prop_data[urban_prop_data['ISO3'] == region].copy()
                        region_data = region_data.sort_values('year')
                        
                        if not region_data.empty:
                            fig.add_trace(go.Scatter(
                                x=region_data['year'],
                                y=region_data['value'] * 100,  # Convert to percentage
                                mode='lines',
                                name=benchmark_names.get(region, region),
                                line=dict(color=benchmark_colors.get(region, '#95a5a6'), width=2, dash='dash'),
                                hovertemplate=f'<b>{benchmark_names.get(region, region)}</b><br>Year: %{{x}}<br>Urbanization Rate: %{{y:.1f}}%<extra></extra>'
                            ))
            
            # Add country benchmarks if selected
            if benchmark_countries:
                # Define colors for benchmark countries (using a color palette)
                country_colors = ['#e74c3c', '#f39c12', '#27ae60', '#3498db', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
                
                for i, country_iso in enumerate(benchmark_countries):
                    if country_iso in urban_prop_data['ISO3'].values:
                        country_benchmark_data = urban_prop_data[urban_prop_data['ISO3'] == country_iso].copy()
                        country_benchmark_data = country_benchmark_data.sort_values('year')
                        
                        if not country_benchmark_data.empty:
                            country_name = countries_and_regions_dict.get(country_iso, country_iso)
                            # Cycle through colors
                            color = country_colors[i % len(country_colors)]
                            
                            fig.add_trace(go.Scatter(
                                x=country_benchmark_data['year'],
                                y=country_benchmark_data['value'] * 100,  # Convert to percentage
                                mode='lines+markers',
                                name=country_name,
                                line=dict(color=color, width=2, dash='dot'),
                                marker=dict(size=4, color=color),
                                hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Urbanization Rate: %{{y:.1f}}%<extra></extra>'
                            ))
            
            # Update layout
            fig.update_layout(
                title=f'<b>{title_suffix}</b> | Urbanization Rate',
                xaxis_title='Year',
                yaxis_title='Urban Population (% of Total Population)',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                title_font_size=16,
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
            return fig
            
        except Exception as e:
            # Return error chart
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='line',
                xaxis_title='Year',
                yaxis_title='Urban Population (% of Total Population)',
                yaxis_range=[0, 100],
                title='Urbanization Rate'
            )
    
    @app.callback(
        Output('urbanization-rate-download', 'data'),
        [Input('urbanization-rate-download-button', 'n_clicks'),
         Input('main-country-filter', 'value')],
        prevent_initial_call=True
    )
    def download_urbanization_rate_data(n_clicks, selected_country):
        """Download UN DESA urbanization rate data as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            # Load full dataset (raw data, no filtering)
            undesa_data = load_undesa_urban_projections()
            
            filename = "urbanization_rate"
            
            return prepare_csv_download(undesa_data, filename)
        
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None
