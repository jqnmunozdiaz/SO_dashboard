"""
Callbacks for National Flood Exposure (Built-up, Absolute) visualization
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd

try:
    from ...utils.flood_data_loader import load_flood_exposure_data, filter_flood_data
    from ...utils.flood_ui_helpers import get_return_period_colors, get_return_period_labels
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_error_chart
    from ...utils.download_helpers import prepare_csv_download
    from config.settings import CHART_STYLES
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.flood_data_loader import load_flood_exposure_data, filter_flood_data
    from src.utils.flood_ui_helpers import get_return_period_colors, get_return_period_labels
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from src.utils.download_helpers import prepare_csv_download
    from config.settings import CHART_STYLES


def register_national_flood_exposure_callbacks(app):
    """Register callbacks for National Flood Exposure (Built-up, Absolute) chart"""
    
    # Load static data once at registration time for performance
    data = load_flood_exposure_data('built_s')
    countries_dict = load_subsaharan_countries_and_regions_dict()
    colors = get_return_period_colors()
    labels = get_return_period_labels()
    
    @app.callback(
        Output('national-flood-exposure-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('flood-return-period-selector', 'value'),
         Input('flood-measurement-type-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_national_flood_exposure_chart(selected_country, selected_return_periods, measurement_type):
        """
        Generate line chart showing flood exposure over time by return period
        
        Args:
            selected_country: ISO3 country code
            
        Returns:
            Plotly figure object
        """
        try:
            # Load data (pre-loaded)
            # Hardcoded to Fluvial & Pluvial (Defended)
            selected_flood_type = 'FLUVIAL_PLUVIAL_DEFENDED'
            # Ensure measurement_type has a default (not strictly needed here but keeps signature consistent)
            measurement_type = measurement_type or 'absolute'
            
            # Handle no country selected
            if not selected_country:
                raise Exception("Please select a country to view flood exposure data")
            
            # Filter data
            country_data = filter_flood_data(data, selected_country, selected_flood_type)
            
            if country_data.empty:
                raise Exception(f"No flood exposure data available for selected country and flood type")
            
            # Get country name for title
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Get color and label mappings (pre-loaded)
            
            # Create figure
            fig = go.Figure()
            
            # Add line for each return period
            # Custom order: 1in100, 1in10, 1in5 (most severe to least severe)
            return_period_order = ['1in100', '1in10', '1in5']
            available_periods = country_data['return_period'].unique()
            # If the user selected specific return periods (from the selector), respect that selection;
            # otherwise plot all available periods in the standard order.
            if selected_return_periods:
                # ensure selection is iterable
                selected_set = set(selected_return_periods)
                return_periods = [rp for rp in return_period_order if rp in available_periods and rp in selected_set]
            else:
                return_periods = [rp for rp in return_period_order if rp in available_periods]

            for rp in return_periods:
                rp_data = country_data[country_data['return_period'] == rp].sort_values('ghsl_year')
                
                fig.add_trace(go.Scatter(
                    x=rp_data['ghsl_year'],
                    y=rp_data['ftm3_ghsl_total_built_s_km2'],
                    mode='lines+markers',
                    name=labels.get(rp, rp),
                    line=dict(color=colors.get(rp, '#666666'), width=2.5),
                    marker=dict(size=8),
                    hovertemplate=f'<b>{country_name}</b><br>Built-up Area: %{{y:.2f}} km²<extra></extra>'
                ))
            
            # Update layout (flood type is hardcoded to Fluvial & Pluvial (Defended))
            fig.update_layout(
                title=f'<b>{country_name}</b> | National Flood Exposure - Built-up Area<br><sub>Fluvial & Pluvial (Defended)</sub>',
                xaxis_title='Year',
                yaxis_title='Built-up Area (km²)',
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
            
            return fig
            
        except Exception as e:
            return create_error_chart(
                error_message=f"Error loading flood exposure data: {str(e)}",
                chart_type='line',
                xaxis_title='Year',
                yaxis_title='Built-up Area (km²)',
                title='National Flood Exposure - Built-up Area'
            )
    
    @app.callback(
        Output('national-flood-exposure-download', 'data'),
        Input('national-flood-exposure-download-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_national_flood_exposure_data(n_clicks):
        """Download flood exposure data as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            return prepare_csv_download(data, "national_flood_exposure_built_up")
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None
