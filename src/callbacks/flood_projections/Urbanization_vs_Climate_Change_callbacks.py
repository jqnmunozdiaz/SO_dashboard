"""
Callbacks for Urbanization vs Climate Change visualization
Shows built-up exposure to flooding under different demographic and climate scenarios
"""

from dash import Input, Output, html
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ...utils.data_loader import load_flood_projections_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def register_urbanization_vs_climate_change_callbacks(app):
    """Register callbacks for Urbanization vs Climate Change chart"""
    
    @app.callback(
        [Output('urbanization-vs-climate-change-chart', 'figure'),
         Output('urbanization-vs-climate-change-chart', 'style'),
         Output('urbanization-vs-climate-change-title', 'children')],
        Input('main-country-filter', 'value'),
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
                raise Exception("No country selected")
            
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
                    range=[-0.5, 11.5],
                    row=row, col=1
                )
                
                # Update y-axis for this subplot
                fig.update_yaxes(
                    title_text='Built-up exposed to floods (km²)',
                    gridcolor='rgba(128, 128, 128, 0.2)',
                    row=row, col=1
                )
            
            # Create title separately
            chart_title = html.H6([
                html.B(country_name),
                ' | Built-up Flood Exposure: Urbanization vs Climate Change'
            ], className='chart-title')
            
            # Update overall layout
            fig.update_layout(
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=False,  # Remove legend to match matplotlib version
                height=800,
                margin=dict(t=100, b=140, l=80, r=40),
                hovermode='closest'
            )
            
            # Add annotations for scenario group labels (below bottom subplot)
            annotations = list(fig.layout.annotations)  # Preserve subplot titles
            annotations.extend([
                dict(
                    text='Current<br>conditions',
                    xref='x2', yref='paper',
                    x=0, y=-0.07,
                    xanchor='center', yanchor='top',
                    showarrow=False,
                    font=dict(size=11),
                    xshift=0
                ),
                dict(
                    text='Demographic<br>scenarios',
                    xref='x2', yref='paper',
                    x=4, y=-0.07,
                    xanchor='center', yanchor='top',
                    showarrow=False,
                    font=dict(size=11),
                    xshift=0
                ),
                dict(
                    text='Climate change<br>scenarios',
                    xref='x2', yref='paper',
                    x=9.5, y=-0.07,
                    xanchor='center', yanchor='top',
                    showarrow=False,
                    font=dict(size=11),
                    xshift=0
                )
            ])
            
            fig.update_layout(annotations=annotations)
            
            # Remove gridlines from x-axis, keep only y-axis
            fig.update_xaxes(showgrid=False)
            
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Create download callback
    create_simple_download_callback(
        app,
        'urbanization-vs-climate-change-download',
        lambda: load_flood_projections_data(),
        'urbanization_vs_climate_flood_exposure'
    )
