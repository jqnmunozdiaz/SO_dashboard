"""
Callbacks for Future Precipitation Patterns visualization
"""

from dash import Input, Output
import plotly.graph_objects as go

try:
    from ...utils.data_loader import load_precipitation_data
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_error_chart
    from ...utils.download_helpers import prepare_csv_download
    from ...utils.precipitation_config import SSP_COLORS
    from config.settings import CHART_STYLES
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_precipitation_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from src.utils.download_helpers import prepare_csv_download
    from src.utils.precipitation_config import SSP_COLORS
    from config.settings import CHART_STYLES


def register_precipitation_callbacks(app):
    """Register callbacks for Future Precipitation Patterns chart"""
    
    # Load static data once at registration time for performance
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        Output('precipitation-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('precipitation-rp-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_precipitation_chart(selected_country, selected_return_periods):
        """
        Generate precipitation patterns chart showing future changes in return periods
        
        Args:
            selected_country: ISO3 country code
            selected_return_periods: List of return periods to show (e.g., [10, 100])
            
        Returns:
            Plotly figure object
        """
        try:
            # Load data
            fyear = 2050
            var_name = '1day'
            data = load_precipitation_data(var_name)
            
            # Handle no country selected
            if not selected_country:
                raise Exception("Please select a country to view precipitation patterns")
            
            # Filter data for selected country and year
            country_data = data[(data['ISO3'] == selected_country) & (data['year'] == fyear)]
            
            if country_data.empty:
                raise Exception(f"No precipitation data available for selected country")
            
            # Filter by selected return periods
            if selected_return_periods:
                country_data = country_data[country_data['RP'].isin(selected_return_periods)]
            
            if country_data.empty:
                raise Exception("No data for selected return periods")
            
            # Get country name for title
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Get unique return periods and sort them
            return_periods = sorted(country_data['RP'].unique())
            
            # Pre-calculate y positions for annotations (before creating figure)
            n_rows = len(return_periods)
            v_spacing = 0.15
            available_height = 1.0 - (n_rows - 1) * v_spacing
            row_height = available_height / n_rows
            
            # Create figure with subplots (one row per return period)
            from plotly.subplots import make_subplots
            fig = make_subplots(
                rows=len(return_periods), 
                cols=1,
                vertical_spacing=0.15,
                row_heights=[1] * len(return_periods)
            )
            
            # Add subtitles to the left of each subplot
            for idx, rp in enumerate(return_periods):
                row = idx + 1
                # Position annotation at y=0 in the subplot's data coordinates
                # This aligns with the scatter points which are all at y=0
                fig.add_annotation(
                    text=f'<b>{int(rp)}-year</b>',
                    xref='paper',
                    yref=f'y{row}' if row > 1 else 'y',  # Reference the specific subplot's y-axis
                    x=-0.12,  # Position to the left of the plot
                    y=0,  # Same height as the data points
                    showarrow=False,
                    font=dict(size=12, color=CHART_STYLES['colors']['primary']),
                    align='right'
                )
            
            # Process each return period
            xfin = country_data['mult'].max()                 # Calculate range for x-axis

            for idx, rp in enumerate(return_periods):
                row = idx + 1
                rp_data = country_data[country_data['RP'] == rp].copy()
                rp_data = rp_data.set_index('SSP')
                
                ep = 1/rp  # Current exceedance probability
                                
                # Add range line (grey horizontal line)
                fig.add_trace(
                    go.Scatter(
                        x=[min(rp_data['Future_EP']), max(rp_data['Future_EP'])],
                        y=[0, 0],
                        mode='lines+markers',
                        line=dict(color='#DEDEDE', width=2),
                        marker=dict(symbol='line-ns', size=10, color='#DEDEDE'),
                        showlegend=False,
                        hoverinfo='skip'
                    ),
                    row=row, col=1
                )
                
                # Add "Today" marker
                fig.add_trace(
                    go.Scatter(
                        x=[ep],
                        y=[0],
                        mode='markers',
                        marker=dict(symbol='x', size=12, color='black', line=dict(width=2)),
                        name='Today' if idx == 0 else None,
                        showlegend=(idx == 0),
                        legendgroup='today',
                        hovertemplate=f'<b>Today</b><br>Probability: {ep*100:.1f}%<extra></extra>'
                    ),
                    row=row, col=1
                )
                
                # Add SSP markers
                for i, ssp in enumerate(sorted(rp_data.index)):
                    future_ep = rp_data.at[ssp, 'Future_EP']
                    color = SSP_COLORS.get(ssp, '#666666')
                    
                    fig.add_trace(
                        go.Scatter(
                            x=[future_ep],
                            y=[0],
                            mode='markers',
                            marker=dict(symbol='circle', size=12, color=color),
                            name=ssp if idx == 0 else None,
                            showlegend=(idx == 0),
                            legendgroup=ssp,
                            hovertemplate=f'<b>{ssp}</b><br>Probability: {future_ep*100:.1f}%<extra></extra>'
                        ),
                        row=row, col=1
                    )
                
                # Calculate tick positions ensuring ep is included as the first tick
                # Create 6 positions starting from ep
                tick_positions = [ep + i * (ep*xfin - ep) / 5 for i in range(6)]
                
                # Update axes for this subplot
                fig.update_xaxes(
                    range=[ep * 0.98, ep*xfin*1.02],  # Start slightly before ep to make X cross fully visible
                    tickformat='.1%',
                    tickvals=tick_positions,  # Explicitly set 6 tick positions starting from ep
                    showgrid=True,  # Add gridlines
                    gridcolor='lightgray',  # Make gridlines visible
                    showline=False,
                    zeroline=False,
                    row=row, col=1
                )
                
                fig.update_yaxes(
                    range=[-0.3, 0.5],
                    showticklabels=False,
                    showgrid=False,
                    showline=False,
                    zeroline=False,
                    row=row, col=1
                )
            
            fig.update_xaxes(
                title_text='Annual exceedance probability',
                title_font=dict(size=11),
                # title_standoff=25,  # Increase space between ticks and title
                row=len(return_periods), col=1
            )
                        
            # Update layout
            fig.update_layout(
                title=dict(
                    text=f'<b>{country_name}</b> | Future Precipitation Patterns',
                    font=dict(size=16, color=CHART_STYLES['colors']['primary'])
                ),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(color=CHART_STYLES['colors']['primary']),
                # Add extra height for legend space
                showlegend=True,
                legend=dict(
                    orientation='v',
                    yanchor='top',
                    y=1,
                    xanchor='left',
                    x=1.02,
                    font=dict(size=10)
                ),
                margin=dict(l=140, r=120, t=80, b=80),  # Adjust right margin for legend space, reduce bottom margin
                hovermode='closest'
            )

            return fig
            
        except Exception as e:
            return create_error_chart(
                error_message=f"Error loading precipitation data: {str(e)}",
                chart_type='scatter',
                title='Future Precipitation Patterns'
            )
    
    @app.callback(
        Output('precipitation-download', 'data'),
        Input('precipitation-download-button', 'n_clicks'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=True
    )
    def download_precipitation_data(n_clicks, selected_country):
        """Download precipitation data as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            # Load full dataset
            data = load_precipitation_data('1day')  
            filename = f"precipitation_patterns"    
            return prepare_csv_download(data, filename)
            
        except Exception as e:
            print(f"Error preparing precipitation download: {str(e)}")
            return None
