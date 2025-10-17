"""
Callbacks for Urban Population Projections visualization
Shows urban and rural population trends with uncertainty bands for selected country
Based on UN DESA World Population Prospects and World Urbanization Prospects data
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
    from src.utils.component_helpers import create_error_chart
    from src.utils.download_helpers import prepare_csv_download
    from config.settings import CHART_STYLES


def register_urban_population_projections_callbacks(app):
    """Register callbacks for Urban Population Projections chart"""
    
    @app.callback(
        Output('urban-population-projections-chart', 'figure'),
        [Input('main-country-filter', 'value')],
        prevent_initial_call=False
    )
    def generate_urban_population_projections_chart(selected_country):
        """Generate urban and rural population projections chart with uncertainty bands"""
        try:
            # Load country and region mapping for ISO code to full name conversion
            countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
            
            if selected_country:
                country_name = countries_and_regions_dict.get(selected_country, selected_country)
            else:
                raise Exception("No country selected")

            # Load UNDESA urban projections data
            undesa_data = load_undesa_urban_projections()
            

            
            # Filter data for selected country
            country_data = undesa_data[undesa_data['ISO3'] == selected_country].copy()
            
            # Pivot data for easier access
            country_pivot = country_data.pivot(index='year', columns='indicator', values='value')
            
            # Define year ranges
            past_years = list(range(1950, 2030, 5))
            future_years = list(range(2025, 2055, 5))
            
            # Create figure
            fig = go.Figure()
            
            # Get colors from CHART_STYLES
            colors = {'urban': CHART_STYLES['colors']['urban'], 'rural': CHART_STYLES['colors']['rural']}
            
            # Add data for both urban and rural
            for aoi in ['urban', 'rural']:
                # Add uncertainty bands for future projections (95% confidence interval)
                if f'{aoi}_pop_lower95' in country_pivot.columns and f'{aoi}_pop_upper95' in country_pivot.columns:
                    # Get data for uncertainty bands
                    years_with_data = [year for year in future_years if year in country_pivot.index 
                                     and pd.notna(country_pivot.loc[year, f'{aoi}_pop_lower95']) 
                                     and pd.notna(country_pivot.loc[year, f'{aoi}_pop_upper95'])]
                    
                    if years_with_data:
                        lower95_values = [country_pivot.loc[year, f'{aoi}_pop_lower95'] for year in years_with_data]
                        upper95_values = [country_pivot.loc[year, f'{aoi}_pop_upper95'] for year in years_with_data]
                        
                        # Add 95% confidence interval
                        # Convert hex to rgba with 20% opacity
                        if aoi == 'urban':
                            fill_color = 'rgba(31, 119, 180, 0.2)'  # Blue with 20% opacity
                        else:
                            fill_color = 'rgba(44, 160, 44, 0.2)'   # Green with 20% opacity
                        
                        fig.add_trace(go.Scatter(
                            x=years_with_data + years_with_data[::-1],
                            y=upper95_values + lower95_values[::-1],
                            fill='toself',
                            fillcolor=fill_color,
                            line=dict(color='rgba(255,255,255,0)'),
                            hoverinfo="skip",
                            showlegend=False,
                            name=f'{aoi.title()} 95% CI'
                        ))
                
                # Add uncertainty bands for future projections (80% confidence interval)
                if f'{aoi}_pop_lower80' in country_pivot.columns and f'{aoi}_pop_upper80' in country_pivot.columns:
                    # Get data for uncertainty bands
                    years_with_data = [year for year in future_years if year in country_pivot.index 
                                     and pd.notna(country_pivot.loc[year, f'{aoi}_pop_lower80']) 
                                     and pd.notna(country_pivot.loc[year, f'{aoi}_pop_upper80'])]
                    
                    if years_with_data:
                        lower80_values = [country_pivot.loc[year, f'{aoi}_pop_lower80'] for year in years_with_data]
                        upper80_values = [country_pivot.loc[year, f'{aoi}_pop_upper80'] for year in years_with_data]
                        
                        # Add 80% confidence interval
                        # Convert hex to rgba with 40% opacity
                        if aoi == 'urban':
                            fill_color = 'rgba(31, 119, 180, 0.4)'  # Blue with 40% opacity
                        else:
                            fill_color = 'rgba(44, 160, 44, 0.4)'   # Green with 40% opacity
                        
                        fig.add_trace(go.Scatter(
                            x=years_with_data + years_with_data[::-1],
                            y=upper80_values + lower80_values[::-1],
                            fill='toself',
                            fillcolor=fill_color,
                            line=dict(color='rgba(255,255,255,0)'),
                            hoverinfo="skip",
                            showlegend=False,
                            name=f'{aoi.title()} 80% CI'
                        ))
                
                # Add historical data (solid line)
                if f'wup_{aoi}_pop' in country_pivot.columns:
                    past_years_with_data = [year for year in past_years if year in country_pivot.index 
                                          and pd.notna(country_pivot.loc[year, f'wup_{aoi}_pop'])]
                    if past_years_with_data:
                        past_values = [country_pivot.loc[year, f'wup_{aoi}_pop'] for year in past_years_with_data]
                        
                        fig.add_trace(go.Scatter(
                            x=past_years_with_data,
                            y=past_values,
                            mode='lines+markers',
                            name=f'{aoi.title()} (Historical)',
                            line=dict(color=colors[aoi], width=3),
                            marker=dict(size=6),
                            hovertemplate=f'<b>{aoi.title()} Population</b><br>' +
                                        'Year: %{x}<br>' +
                                        'Population: %{y:.1f} million<br>' +
                                        '<extra></extra>'
                        ))
                
                # Add future projections (dashed line)
                if f'{aoi}_pop_median' in country_pivot.columns:
                    future_years_with_data = [year for year in future_years if year in country_pivot.index 
                                            and pd.notna(country_pivot.loc[year, f'{aoi}_pop_median'])]
                    if future_years_with_data:
                        future_values = [country_pivot.loc[year, f'{aoi}_pop_median'] for year in future_years_with_data]
                        
                        fig.add_trace(go.Scatter(
                            x=future_years_with_data,
                            y=future_values,
                            mode='lines+markers',
                            name=f'{aoi.title()} (Projected)',
                            line=dict(color=colors[aoi], width=3, dash='dash'),
                            marker=dict(size=6),
                            hovertemplate=f'<b>{aoi.title()} Population (Projected)</b><br>' +
                                        'Year: %{x}<br>' +
                                        'Population: %{y:.1f} million<br>' +
                                        '<extra></extra>'
                        ))
            
            # Update layout
            fig.update_layout(
                title=f'<b>{country_name}</b> | Urban and Rural Population Projections',
                xaxis_title='Year',
                yaxis_title='Population (millions)',
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                template='plotly_white',
                font={'color': CHART_STYLES['colors']['primary']},
                title_font=dict(size=16, color=CHART_STYLES['font']['color']),
                margin=dict(l=60, r=20, t=80, b=60),
                height=500
            )
            
            # Add vertical line at 2025 to separate historical from projections
            fig.add_vline(x=2025, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add annotations on either side of the line
            fig.add_annotation(
                x=2024,  # Midpoint of historical period (1950-2025)
                y=1,
                yref="paper",
                text="Historical",
                showarrow=False,
                font=dict(size=12, color="gray"),
                yanchor="top",
                xanchor="right"
            )
            
            fig.add_annotation(
                x=2026,  # Midpoint of projection period (2025-2055)
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
            # Return error chart using shared utility
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='scatter',
                xaxis_title='Year',
                yaxis_title='Population (millions)',
                title='Urban and Rural Population Projections'
            )
    
    @app.callback(
        Output('urban-population-projections-download', 'data'),
        Input('urban-population-projections-download-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_urban_population_projections_data(n_clicks):
        """Download urban population projections data as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            # Load full dataset (raw data, no filtering)
            undesa_data = load_undesa_urban_projections()
            
            filename = "urban_population_projections"
            
            return prepare_csv_download(undesa_data, filename)
        
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None