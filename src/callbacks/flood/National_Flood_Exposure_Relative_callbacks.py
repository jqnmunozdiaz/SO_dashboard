"""
Callbacks for National Flood Exposure (Built-up, Relative) visualization
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.flood_data_loader import load_flood_exposure_data, filter_flood_data
from ...utils.flood_ui_helpers import get_return_period_labels
from ...utils.benchmark_config import get_benchmark_colors, get_benchmark_names
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from ...utils.color_utils import get_benchmark_country_color
from config.settings import CHART_STYLES


def register_national_flood_exposure_relative_callbacks(app):
    """Register callbacks for National Flood Exposure (Built-up, Relative) chart"""
    
    # Load static data once at registration time for performance
    flood_data = load_flood_exposure_data('built_s')
    countries_dict = load_subsaharan_countries_and_regions_dict()
    benchmark_colors_dict = get_benchmark_colors()

    @app.callback(
        [Output('national-flood-exposure-relative-chart', 'figure'),
         Output('national-flood-exposure-relative-chart', 'style'),
         Output('national-flood-exposure-relative-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('flood-return-period-selector', 'value'),
         Input('flood-combined-benchmark-selector', 'value'),
         Input('flood-measurement-type-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_national_flood_exposure_relative_chart(selected_country, selected_return_periods, combined_benchmarks, measurement_type):
        """
        Generate line chart showing relative flood exposure over time by return period
        
        Args:
            selected_country: ISO3 country code
            selected_return_periods: List of return periods to display
            combined_benchmarks: List of combined benchmark codes (countries and regions)
            
        Returns:
            Plotly figure object
        """
        try:
            # Hardcoded to Fluvial & Pluvial (Defended)
            selected_flood_type = 'FLUVIAL_PLUVIAL_DEFENDED'
            # Ensure measurement_type default
            measurement_type = measurement_type or 'relative'
            
            # Split combined benchmarks into regions and countries
            regional_benchmarks = [b for b in (combined_benchmarks or []) if b in benchmark_colors_dict]
            benchmark_countries = [b for b in (combined_benchmarks or []) if b not in benchmark_colors_dict]
            
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Handle no return periods selected
            if not selected_return_periods:
                raise Exception("Please select at least one return period")
            
            # Get color and label mappings
            labels = get_return_period_labels()
            benchmark_colors = get_benchmark_colors()
            benchmark_names = get_benchmark_names()
            
            # Define line types for each return period
            return_period_line_types = {
                '1in100': 'solid',
                '1in10': 'dash',
                '1in5': 'dot'
            }
            
            # Create figure
            fig = go.Figure()
            
            # Custom order: 1in100, 1in10, 1in5 (most severe to least severe)
            return_period_order = ['1in100', '1in10', '1in5']
            
            # Plot main country
            country_data = filter_flood_data(flood_data, selected_country, selected_flood_type)
            
            if country_data.empty:
                raise Exception(f"No flood exposure data available for selected country and flood type")
            
            country_name = countries_dict.get(selected_country, selected_country)
            available_periods = country_data['return_period'].unique()
            # Filter return periods based on both availability and user selection
            return_periods = [rp for rp in return_period_order if rp in available_periods and rp in selected_return_periods]
            
            for rp in return_periods:
                rp_data = country_data[country_data['return_period'] == rp].sort_values('ghsl_year')
                
                fig.add_trace(go.Scatter(
                    x=rp_data['ghsl_year'],
                    y=rp_data['relative_exposure_pct'],
                    mode='lines+markers',
                    name=f"{labels.get(rp, rp)} - {country_name}",
                    line=dict(color="#0a83d9", width=2.5, dash=return_period_line_types.get(rp, 'solid')),
                    marker=dict(size=8),
                    hovertemplate=f'<b>{country_name}</b><br>Return Period: {labels.get(rp, rp)}<br>Exposure: %{{y:.2f}}%<extra></extra>'
                ))
            
            # Plot regional benchmarks
            if regional_benchmarks:
                for region_code in regional_benchmarks:
                    region_data = filter_flood_data(flood_data, region_code, selected_flood_type)
                    
                    if not region_data.empty:
                        region_name = benchmark_names.get(region_code, region_code)
                        region_color = benchmark_colors.get(region_code, '#666666')
                        
                        for rp in return_periods:
                            rp_data = region_data[region_data['return_period'] == rp].sort_values('ghsl_year')
                            
                            if not rp_data.empty:
                                fig.add_trace(go.Scatter(
                                    x=rp_data['ghsl_year'],
                                    y=rp_data['relative_exposure_pct'],
                                    mode='lines+markers',
                                    name=f"{labels.get(rp, rp)} - {region_name}",
                                    line=dict(color=region_color, width=2, dash=return_period_line_types.get(rp, 'solid')),
                                    marker=dict(size=6, symbol='x'),
                                    hovertemplate=f'<b>{region_name}</b><br>Return Period: {labels.get(rp, rp)}<br>Exposure: %{{y:.2f}}%<extra></extra>',
                                    opacity=0.7
                                ))
            
            # Plot benchmark countries
            if benchmark_countries:
                for idx, benchmark_iso in enumerate(benchmark_countries):
                    benchmark_data = filter_flood_data(flood_data, benchmark_iso, selected_flood_type)
                    
                    if not benchmark_data.empty:
                        benchmark_name = countries_dict.get(benchmark_iso, benchmark_iso)
                        # Assign a unique color to each benchmark country
                        benchmark_color = get_benchmark_country_color(idx)
                        
                        for rp in return_periods:
                            rp_data = benchmark_data[benchmark_data['return_period'] == rp].sort_values('ghsl_year')
                            
                            if not rp_data.empty:
                                fig.add_trace(go.Scatter(
                                    x=rp_data['ghsl_year'],
                                    y=rp_data['relative_exposure_pct'],
                                    mode='lines+markers',
                                    name=f"{labels.get(rp, rp)} - {benchmark_name}",
                                    line=dict(color=benchmark_color, width=2, dash=return_period_line_types.get(rp, 'solid')),
                                    marker=dict(size=6, symbol='diamond'),
                                    hovertemplate=f'<b>{benchmark_name}</b><br>Return Period: {labels.get(rp, rp)}<br>Exposure: %{{y:.2f}}%<extra></extra>',
                                    opacity=0.7
                                ))
            
            # Create separate title
            chart_title = html.H6([html.B(country_name), ' | National Flood Exposure - Built-up Area (Relative)'], 
                                 style={'marginBottom': '1rem', 'color': '#2c3e50'})
            
            # Update layout (flood type is hardcoded to Fluvial & Pluvial (Defended))
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Exposed Built-up Area (% of Total)',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                hovermode='x unified',
                legend=dict(
                    title='Return Period',
                    orientation='v',
                    yanchor='middle',
                    y=0.5,
                    xanchor='left',
                    x=1.02,
                    bgcolor='rgba(255, 255, 255, 0.8)',
                    bordercolor='#e5e7eb',
                    borderwidth=0
                ),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    dtick=5  # Show every 5 years
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    rangemode='tozero',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='#e5e7eb',
                    ticksuffix='%'
                )
            )
            
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback
    create_simple_download_callback(
        app,
        'national-flood-exposure-relative-download',
        lambda: flood_data,
        'national_flood_exposure_built_up_relative'
    )
