"""
Callbacks for Urbanization vs Climate Change visualization
Shows built-up exposure to flooding under different demographic and climate scenarios
"""

from dash import Input, Output
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

try:
    from ...utils.data_loader import load_flood_projections_data
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_error_chart
    from ...utils.download_helpers import prepare_csv_download
    from config.settings import CHART_STYLES
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_flood_projections_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from src.utils.download_helpers import prepare_csv_download
    from config.settings import CHART_STYLES


def register_urbanization_vs_climate_change_callbacks(app):
    """Register callbacks for Urbanization vs Climate Change chart"""
    
    @app.callback(
        Output('urbanization-vs-climate-change-chart', 'figure'),
        [Input('main-country-filter', 'value')],
        prevent_initial_call=False
    )
    def generate_urbanization_vs_climate_change_chart(selected_country):
        """
        Generate grouped bar chart comparing demographic vs climate scenarios
        Shows 2 subplots (one for each return period: 10-year and 100-year)
        """
        try:
            # Load data
            dff = load_flood_projections_data()
            countries_dict = load_subsaharan_countries_and_regions_dict()
            
            # Validate country selection
            if not selected_country:
                raise Exception("Please select a country to view flood projections")
            
            # Get country name for title
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Check if country exists in data
            if country_name not in dff.index:
                raise Exception(f"No flood projection data available for {country_name}")
            
            # Return periods and titles
            RPs = [10, 100]
            titles = ['Recurrent floods (10-year return period)', 'Extreme floods (100-year return period)']
            fyear = 2050
            
            # Create subplots - 2 rows, 1 column
            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=titles,
                vertical_spacing=0.15,
                specs=[[{"type": "bar"}], [{"type": "bar"}]]
            )
            
            # Color scheme
            colors = {
                'current': 'orange',
                'demographic': {
                    'lower95': '#3ac3d6',
                    'lower80': '#17bac7',
                    'median': '#0cafbd',
                    'upper80': '#00a9ae',
                    'upper95': '#329f9c'
                },
                'climate': {
                    'SSP1_2.6': '#edcc6f',
                    'SSP2_4.5': '#d2ebff',
                    'SSP3_7.0': '#88cafc',
                    'SSP5_8.5': '#404066'
                }
            }
            
            # Generate chart for each return period
            for i, RP in enumerate(RPs):
                row = i + 1
                
                # Get current condition value (2020 baseline)
                val_2020 = dff.at[country_name, f'2020_{RP}']
                
                # X-axis positions for grouped bars
                x_positions = {
                    'current': [0],
                    'demographic': [2, 3, 4, 5, 6],
                    'climate': [8, 9, 10, 11]
                }
                
                # Add 2020 baseline bar
                fig.add_trace(
                    go.Bar(
                        x=x_positions['current'],
                        y=[val_2020],
                        marker_color=colors['current'],
                        name='2020 Baseline' if i == 0 else None,
                        showlegend=(i == 0),
                        hovertemplate='<b>2020 Baseline</b><br>Exposed: %{y:.2f} km²<extra></extra>',
                        width=0.8
                    ),
                    row=row, col=1
                )
                
                # Add demographic scenario bars
                demo_labels = ['low\n95', 'low\n80', 'Mdn.', 'high\n80', 'high\n95']
                demo_keys = ['lower95', 'lower80', 'median', 'upper80', 'upper95']
                
                for j, (label, key) in enumerate(zip(demo_labels, demo_keys)):
                    value = max(val_2020, dff.at[country_name, f'bupsc1_{key}_{RP}'])
                    fig.add_trace(
                        go.Bar(
                            x=[x_positions['demographic'][j]],
                            y=[value],
                            marker_color=colors['demographic'][key],
                            name=f'Demo: {label.replace(chr(10), " ")}' if i == 0 else None,
                            showlegend=(i == 0),
                            hovertemplate=f'<b>Demographic: {label.replace(chr(10), " ")}</b><br>Exposed: %{{y:.2f}} km²<extra></extra>',
                            width=0.8
                        ),
                        row=row, col=1
                    )
                
                # Add climate scenario bars
                climate_labels = ['SSP1\n2.6', 'SSP2\n4.5', 'SSP3\n7.0', 'SSP5\n8.5']
                climate_keys = ['SSP1_2.6', 'SSP2_4.5', 'SSP3_7.0', 'SSP5_8.5']
                
                for j, (label, key) in enumerate(zip(climate_labels, climate_keys)):
                    value = max(val_2020, dff.at[country_name, f'{fyear}-{key}_{RP}'])
                    fig.add_trace(
                        go.Bar(
                            x=[x_positions['climate'][j]],
                            y=[value],
                            marker_color=colors['climate'][key],
                            name=f'Climate: {label.replace(chr(10), " ")}' if i == 0 else None,
                            showlegend=(i == 0),
                            hovertemplate=f'<b>Climate: {label.replace(chr(10), " ")}</b><br>Exposed: %{{y:.2f}} km²<extra></extra>',
                            width=0.8
                        ),
                        row=row, col=1
                    )
                
                # Add horizontal reference line at 2020 level
                fig.add_hline(
                    y=val_2020,
                    line_dash="dash",
                    line_color="gray",
                    line_width=1,
                    opacity=0.5,
                    row=row, col=1
                )
                
                # Update x-axis for this subplot
                fig.update_xaxes(
                    tickmode='array',
                    tickvals=list(range(0, 12)),
                    ticktext=['2020', '', 'low\n95', 'low\n80', 'Mdn.', 'high\n80', 'high\n95', '', 
                             'SSP1\n2.6', 'SSP2\n4.5', 'SSP3\n7.0', 'SSP5\n8.5'],
                    tickfont=dict(size=10),
                    row=row, col=1
                )
                
                # Update y-axis for this subplot
                fig.update_yaxes(
                    title_text='Built-up exposed to floods (km²)',
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    row=row, col=1
                )
            
            # Update overall layout
            fig.update_layout(
                title=f'<b>{country_name}</b> | Built-up Flood Exposure: Urbanization vs Climate Change',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=False,  # Remove legend to match matplotlib version
                height=800,
                margin=dict(t=100, b=80, l=80, r=40),
                hovermode='closest'
            )
            
            # Add annotations for scenario group labels (only on top subplot)
            annotations = [
                dict(
                    text='Current<br>conditions',
                    xref='x', yref='paper',
                    x=0, y=1.12,
                    xanchor='center', yanchor='bottom',
                    showarrow=False,
                    font=dict(size=11)
                ),
                dict(
                    text='Demographic<br>scenarios',
                    xref='x', yref='paper',
                    x=4, y=1.12,
                    xanchor='center', yanchor='bottom',
                    showarrow=False,
                    font=dict(size=11)
                ),
                dict(
                    text='Climate change<br>scenarios',
                    xref='x', yref='paper',
                    x=9.5, y=1.12,
                    xanchor='center', yanchor='bottom',
                    showarrow=False,
                    font=dict(size=11)
                )
            ]
            
            fig.update_layout(annotations=annotations)
            
            # Remove gridlines from x-axis, keep only y-axis
            fig.update_xaxes(showgrid=False)
            
            return fig
            
        except Exception as e:
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='bar',
                title='Built-up Flood Exposure: Urbanization vs Climate Change',
                xaxis_title='Scenarios',
                yaxis_title='Built-up exposed to floods (km²)'
            )
    
    @app.callback(
        Output('urbanization-vs-climate-change-download', 'data'),
        [Input('urbanization-vs-climate-change-download-button', 'n_clicks'),
         Input('main-country-filter', 'value')],
        prevent_initial_call=True
    )
    def download_urbanization_vs_climate_change_data(n_clicks, selected_country):
        """Download flood projections data for selected country"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            data = load_flood_projections_data()
            filename = "flood_projections_all_countries"            
            return prepare_csv_download(data, filename)
            
        except Exception as e:
            print(f"Error downloading urbanization vs climate change data: {str(e)}")
            return None
