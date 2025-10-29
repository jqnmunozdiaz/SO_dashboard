"""
Callbacks for National Flood Exposure (Population, Absolute) visualization
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.flood_data_loader import load_flood_exposure_data, filter_flood_data
from ...utils.flood_ui_helpers import get_return_period_colors, get_return_period_labels
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def register_national_flood_exposure_population_callbacks(app):
    """Register callbacks for National Flood Exposure (Population, Absolute) chart"""
    
    # Load static data once at registration time for performance
    data = load_flood_exposure_data('pop')
    countries_dict = load_subsaharan_countries_and_regions_dict()
    colors = get_return_period_colors()
    labels = get_return_period_labels()
    
    @app.callback(
        [Output('national-flood-exposure-population-chart', 'figure'),
         Output('national-flood-exposure-population-chart', 'style'),
         Output('national-flood-exposure-population-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('flood-return-period-selector', 'value'),
         Input('flood-measurement-type-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_national_flood_exposure_population_chart(selected_country, selected_return_periods, measurement_type):
        """
        Generate line chart showing population flood exposure over time by return period
        
        Args:
            selected_country: ISO3 country code
            selected_return_periods: List of return periods to display
            measurement_type: Measurement type (absolute or relative)
            
        Returns:
            Plotly figure object
        """
        try:
            # Hardcoded to Fluvial & Pluvial (Defended)
            selected_flood_type = 'FLUVIAL_PLUVIAL_DEFENDED'
            measurement_type = measurement_type or 'absolute'
            
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Filter data
            country_data = filter_flood_data(data, selected_country, selected_flood_type)
            
            if country_data.empty:
                raise Exception(f"No flood exposure data available for selected country and flood type")
            
            # Get country name for title
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Create figure
            fig = go.Figure()
            
            # Add line for each return period
            # Custom order: 1in100, 1in10, 1in5 (most severe to least severe)
            return_period_order = ['1in100', '1in10', '1in5']
            available_periods = country_data['return_period'].unique()
            # If the user selected specific return periods, respect that selection
            if selected_return_periods:
                selected_set = set(selected_return_periods)
                return_periods = [rp for rp in return_period_order if rp in available_periods and rp in selected_set]
            else:
                return_periods = [rp for rp in return_period_order if rp in available_periods]
            
            for rp in return_periods:
                rp_data = country_data[country_data['return_period'] == rp].sort_values('ghsl_year')
                
                fig.add_trace(go.Scatter(
                    x=rp_data['ghsl_year'],
                    y=rp_data['ftm3_ghsl_total_pop_#'],
                    mode='lines+markers',
                    name=labels.get(rp, rp),
                    line=dict(color=colors.get(rp, '#666666'), width=2.5),
                    marker=dict(size=8),
                    hovertemplate=f'<b>{country_name}</b><br>Return Period: {labels.get(rp, rp)}<br>Population: %{{y:,.0f}}<extra></extra>'
                ))
            
            # Create separate title
            chart_title = html.H6([html.B(country_name), ' | National Flood Exposure - Population'], 
                                 style={'marginBottom': '1rem', 'color': '#2c3e50'})
            
            # Update layout (flood type is hardcoded to Fluvial & Pluvial (Defended))
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Population (persons)',
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
                    zerolinecolor='#e5e7eb'
                )
            )
            
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback
    create_simple_download_callback(
        app,
        'national-flood-exposure-population-download',
        lambda: data,
        'national_flood_exposure_population'
    )
