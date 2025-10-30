"""
Callbacks for National Flood Exposure visualization (Consolidated)
Handles all combinations: built-up/population × absolute/relative in a single callback
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.flood_data_loader import load_flood_exposure_data, filter_flood_data
from ...utils.flood_ui_helpers import get_return_period_colors, get_return_period_labels
from ...utils.benchmark_config import get_benchmark_colors, get_benchmark_names
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from ...utils.color_utils import get_benchmark_country_color
from config.settings import CHART_STYLES


def register_national_flood_exposure_consolidated_callbacks(app):
    """Register consolidated callbacks for all National Flood Exposure variations"""
    
    # Load static data once at registration time for performance
    built_s_data = load_flood_exposure_data('built_s')
    pop_data = load_flood_exposure_data('pop')
    countries_dict = load_subsaharan_countries_and_regions_dict()
    return_period_colors = get_return_period_colors()
    return_period_labels = get_return_period_labels()
    benchmark_colors_dict = get_benchmark_colors()
    benchmark_names = get_benchmark_names()
    
    # Define line types for each return period (used in relative view)
    return_period_line_types = {
        '1in100': 'solid',
        '1in10': 'dash',
        '1in5': 'dot'
    }
    
    @app.callback(
        [Output('national-flood-exposure-chart', 'figure'),
         Output('national-flood-exposure-chart', 'style'),
         Output('national-flood-exposure-title', 'children'),
         Output('national-flood-exposure-relative-chart', 'figure'),
         Output('national-flood-exposure-relative-chart', 'style'),
         Output('national-flood-exposure-relative-title', 'children'),
         Output('national-flood-exposure-population-chart', 'figure'),
         Output('national-flood-exposure-population-chart', 'style'),
         Output('national-flood-exposure-population-title', 'children'),
         Output('national-flood-exposure-population-relative-chart', 'figure'),
         Output('national-flood-exposure-population-relative-chart', 'style'),
         Output('national-flood-exposure-population-relative-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('flood-return-period-selector', 'value'),
         Input('flood-exposure-type-selector', 'value'),
         Input('flood-measurement-type-selector', 'value'),
         Input('flood-combined-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_national_flood_exposure_chart(selected_country, selected_return_periods, exposure_type, measurement_type, combined_benchmarks):
        """
        Generate appropriate flood exposure chart based on exposure type and measurement type
        
        Args:
            selected_country: ISO3 country code
            selected_return_periods: List of return periods to display
            exposure_type: 'built_s' or 'pop'
            measurement_type: 'absolute' or 'relative'
            combined_benchmarks: List of benchmark codes (only used for relative view)
            
        Returns:
            Multiple outputs (figure, style, title) for all 4 chart variations
        """
        # Set defaults
        exposure_type = exposure_type or 'built_s'
        measurement_type = measurement_type or 'absolute'
        selected_flood_type = 'FLUVIAL_PLUVIAL_DEFENDED'
        
        # Determine which chart to render
        is_built_s = (exposure_type == 'built_s')
        is_absolute = (measurement_type == 'absolute')
        
        # Initialize all outputs as empty
        empty_fig, empty_style = create_simple_error_message("")
        outputs = [empty_fig, {'display': 'none'}, ""] * 4
        
        try:
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Select appropriate data source
            data = built_s_data if is_built_s else pop_data
            
            # Filter data for selected country
            country_data = filter_flood_data(data, selected_country, selected_flood_type)
            
            if country_data.empty:
                raise Exception(f"No flood exposure data available for selected country")
            
            # Custom order: 1in100, 1in10, 1in5 (most severe to least severe)
            return_period_order = ['1in100', '1in10', '1in5']
            available_periods = country_data['return_period'].unique()
            
            # Filter return periods based on selection
            if selected_return_periods:
                selected_set = set(selected_return_periods)
                return_periods = [rp for rp in return_period_order if rp in available_periods and rp in selected_set]
            else:
                return_periods = [rp for rp in return_period_order if rp in available_periods]
            
            # Create figure
            fig = go.Figure()
            
            if is_absolute:
                # ABSOLUTE VIEW - Simple lines by return period
                for rp in return_periods:
                    rp_data = country_data[country_data['return_period'] == rp].sort_values('ghsl_year')
                    
                    # Determine value column and hover template
                    if is_built_s:
                        y_values = rp_data['ftm3_ghsl_total_built_s_km2']
                        hover_template = f'<b>{country_name}</b><br>Return Period: {return_period_labels.get(rp, rp)}<br>Built-up Area: %{{y:.2f}} km²<extra></extra>'
                        yaxis_title = 'Built-up Area (km²)'
                        chart_title_suffix = 'Built-up Area'
                    else:
                        y_values = rp_data['ftm3_ghsl_total_pop_#']
                        hover_template = f'<b>{country_name}</b><br>Return Period: {return_period_labels.get(rp, rp)}<br>Population: %{{y:,.0f}}<extra></extra>'
                        yaxis_title = 'Population (persons)'
                        chart_title_suffix = 'Population'
                    
                    fig.add_trace(go.Scatter(
                        x=rp_data['ghsl_year'],
                        y=y_values,
                        mode='lines+markers',
                        name=return_period_labels.get(rp, rp),
                        line=dict(color=return_period_colors.get(rp, '#666666'), width=2.5),
                        marker=dict(size=8),
                        hovertemplate=hover_template
                    ))
                
                chart_title = html.H6([html.B(country_name), f' | National Flood Exposure - {chart_title_suffix}'], 
                                     className='chart-title')
                
                fig.update_layout(
                    xaxis_title='Year',
                    yaxis_title=yaxis_title,
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
                        dtick=5
                    ),
                    yaxis=dict(
                        showgrid=True,
                        gridwidth=1,
                        gridcolor='#e5e7eb',
                        rangemode='tozero',
                        zeroline=True,
                        zerolinewidth=1,
                        zerolinecolor='#e5e7eb'
                    ),
                    margin=dict(t=40, b=80, l=80, r=150)
                )
                
            else:
                # RELATIVE VIEW - Include benchmarks
                # Check if return periods selected (required for relative view)
                if not return_periods:
                    raise Exception("Please select at least one return period")
                
                # Split combined benchmarks into regions and countries
                regional_benchmarks = [b for b in (combined_benchmarks or []) if b in benchmark_colors_dict]
                benchmark_countries = [b for b in (combined_benchmarks or []) if b not in benchmark_colors_dict]
                
                # Plot main country with different line types per return period
                for rp in return_periods:
                    rp_data = country_data[country_data['return_period'] == rp].sort_values('ghsl_year')
                    
                    fig.add_trace(go.Scatter(
                        x=rp_data['ghsl_year'],
                        y=rp_data['relative_exposure_pct'],
                        mode='lines+markers',
                        name=f"{return_period_labels.get(rp, rp)} - {country_name}",
                        line=dict(color="#0a83d9", width=2.5, dash=return_period_line_types.get(rp, 'solid')),
                        marker=dict(size=8),
                        hovertemplate=f'<b>{country_name}</b><br>Return Period: {return_period_labels.get(rp, rp)}<br>Exposure: %{{y:.2f}}%<extra></extra>'
                    ))
                
                # Plot regional benchmarks
                if regional_benchmarks:
                    for region_code in regional_benchmarks:
                        region_data = filter_flood_data(data, region_code, selected_flood_type)
                        
                        if not region_data.empty:
                            region_name = benchmark_names.get(region_code, region_code)
                            region_color = benchmark_colors_dict.get(region_code, '#666666')
                            
                            for rp in return_periods:
                                rp_data = region_data[region_data['return_period'] == rp].sort_values('ghsl_year')
                                
                                if not rp_data.empty:
                                    fig.add_trace(go.Scatter(
                                        x=rp_data['ghsl_year'],
                                        y=rp_data['relative_exposure_pct'],
                                        mode='lines+markers',
                                        name=f"{return_period_labels.get(rp, rp)} - {region_name}",
                                        line=dict(color=region_color, width=2, dash=return_period_line_types.get(rp, 'solid')),
                                        marker=dict(size=6, symbol='x'),
                                        hovertemplate=f'<b>{region_name}</b><br>Return Period: {return_period_labels.get(rp, rp)}<br>Exposure: %{{y:.2f}}%<extra></extra>',
                                        opacity=0.7
                                    ))
                
                # Plot benchmark countries
                if benchmark_countries:
                    for idx, benchmark_iso in enumerate(benchmark_countries):
                        benchmark_data = filter_flood_data(data, benchmark_iso, selected_flood_type)
                        
                        if not benchmark_data.empty:
                            benchmark_name = countries_dict.get(benchmark_iso, benchmark_iso)
                            benchmark_color = get_benchmark_country_color(idx)
                            
                            for rp in return_periods:
                                rp_data = benchmark_data[benchmark_data['return_period'] == rp].sort_values('ghsl_year')
                                
                                if not rp_data.empty:
                                    fig.add_trace(go.Scatter(
                                        x=rp_data['ghsl_year'],
                                        y=rp_data['relative_exposure_pct'],
                                        mode='lines+markers',
                                        name=f"{return_period_labels.get(rp, rp)} - {benchmark_name}",
                                        line=dict(color=benchmark_color, width=2, dash=return_period_line_types.get(rp, 'solid')),
                                        marker=dict(size=6, symbol='diamond'),
                                        hovertemplate=f'<b>{benchmark_name}</b><br>Return Period: {return_period_labels.get(rp, rp)}<br>Exposure: %{{y:.2f}}%<extra></extra>',
                                        opacity=0.7
                                    ))
                
                # Set title and yaxis based on exposure type
                if is_built_s:
                    chart_title_suffix = 'Built-up Area (Relative)'
                    yaxis_title = 'Exposed Built-up Area (% of Total)'
                else:
                    chart_title_suffix = 'Population (Relative)'
                    yaxis_title = 'Exposed Population (% of Total)'
                
                chart_title = html.H6([html.B(country_name), f' | National Flood Exposure - {chart_title_suffix}'], 
                                     className='chart-title')
                
                fig.update_layout(
                    xaxis_title='Year',
                    yaxis_title=yaxis_title,
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
                        dtick=5
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
                    ),
                    margin=dict(t=40, b=80, l=80, r=150)
                )
            
            # Determine which output index to populate (0=built_s absolute, 1=built_s relative, 2=pop absolute, 3=pop relative)
            if is_built_s and is_absolute:
                output_idx = 0
            elif is_built_s and not is_absolute:
                output_idx = 1
            elif not is_built_s and is_absolute:
                output_idx = 2
            else:  # pop relative
                output_idx = 3
            
            # Update the appropriate output
            outputs[output_idx * 3] = fig
            outputs[output_idx * 3 + 1] = {'display': 'block'}
            outputs[output_idx * 3 + 2] = chart_title
            
            return outputs
            
        except Exception as e:
            error_fig, error_style = create_simple_error_message(str(e))
            
            # Determine which chart to show error in
            if is_built_s and is_absolute:
                output_idx = 0
            elif is_built_s and not is_absolute:
                output_idx = 1
            elif not is_built_s and is_absolute:
                output_idx = 2
            else:
                output_idx = 3
            
            outputs[output_idx * 3] = error_fig
            outputs[output_idx * 3 + 1] = error_style
            outputs[output_idx * 3 + 2] = ""
            
            return outputs
    
    # Register download callbacks for all variations
    create_simple_download_callback(
        app,
        'national-flood-exposure-download',
        lambda: built_s_data,
        'national_flood_exposure_built_up'
    )
    
    create_simple_download_callback(
        app,
        'national-flood-exposure-relative-download',
        lambda: built_s_data,
        'national_flood_exposure_built_up_relative'
    )
    
    create_simple_download_callback(
        app,
        'national-flood-exposure-population-download',
        lambda: pop_data,
        'national_flood_exposure_population'
    )
    
    create_simple_download_callback(
        app,
        'national-flood-exposure-population-relative-download',
        lambda: pop_data,
        'national_flood_exposure_population_relative'
    )
