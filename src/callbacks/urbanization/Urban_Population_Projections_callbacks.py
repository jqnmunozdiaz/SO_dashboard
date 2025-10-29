"""
Callbacks for Urban Population Projections visualization
Shows urban and rural population trends with uncertainty bands for selected country
Based on UN DESA World Population Prospects and World Urbanization Prospects data
"""

from dash import Input, Output, html
import plotly.graph_objects as go
import pandas as pd

from ...utils.data_loader import load_undesa_urban_projections, load_undesa_urban_growth_rates
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES

def register_urban_population_projections_callbacks(app):
    """Register callbacks for Urban Population Projections chart"""
    
    # Load static data once at registration time for performance
    undesa_projections = load_undesa_urban_projections()
    undesa_growth_rates = load_undesa_urban_growth_rates()
    countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        [Output('urban-population-projections-chart', 'figure'),
         Output('urban-population-projections-chart', 'style'),
         Output('urban-population-projections-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('urban-population-projections-mode', 'value')],
        prevent_initial_call=False
    )
    def generate_urban_population_projections_chart(selected_country, display_mode):
        """Generate urban and rural population projections chart with uncertainty bands"""
        # Default to absolute values if mode not specified
        if display_mode is None:
            display_mode = 'absolute'
        
        try:
            # Load country and region mapping for ISO code to full name conversion (pre-loaded)
            
            if selected_country:
                country_name = countries_and_regions_dict.get(selected_country, selected_country)
            else:
                raise Exception("No country selected")

            # Load appropriate data based on display mode (pre-loaded)
            if display_mode == 'growth_rate':
                # Use pre-loaded growth rates
                undesa_data = undesa_growth_rates
            else:
                # Use pre-loaded absolute population values
                undesa_data = undesa_projections
               
            # Filter data for selected country
            country_data = undesa_data[undesa_data['ISO3'] == selected_country].copy()
            
            # Pivot data for easier access
            country_pivot = country_data.pivot(index='year', columns='indicator', values='value')
            
            # Define year ranges - ensure 2025 is in both to connect the lines
            past_years = list(range(1950, 2030, 5))  # Includes 2025
            future_years = list(range(2025, 2055, 5))  # Also includes 2025
            
            # Create figure
            fig = go.Figure()
            
            # Get colors from CHART_STYLES
            colors = {'urban': CHART_STYLES['colors']['urban'], 'rural': CHART_STYLES['colors']['rural']}
            
            # Add data for both urban and rural
            for aoi in ['urban', 'rural']:
                # Determine which columns to use based on display mode
                if display_mode == 'growth_rate':
                    lower95_col = f'{aoi}_lower95_growth_rate'
                    upper95_col = f'{aoi}_upper95_growth_rate'
                    lower80_col = f'{aoi}_lower80_growth_rate'
                    upper80_col = f'{aoi}_upper80_growth_rate'
                    median_col = f'{aoi}_median_growth_rate'
                    historical_col = f'{aoi}_growth_rate'
                else:
                    lower95_col = f'{aoi}_pop_lower95'
                    upper95_col = f'{aoi}_pop_upper95'
                    lower80_col = f'{aoi}_pop_lower80'
                    upper80_col = f'{aoi}_pop_upper80'
                    median_col = f'{aoi}_pop_median'
                    historical_col = f'wup_{aoi}_pop'
                
                # Add uncertainty bands for future projections (95% confidence interval)
                if lower95_col in country_pivot.columns and upper95_col in country_pivot.columns:
                    # Get data for uncertainty bands
                    years_with_data = [year for year in future_years if year in country_pivot.index 
                                     and pd.notna(country_pivot.loc[year, lower95_col]) 
                                     and pd.notna(country_pivot.loc[year, upper95_col])]
                    
                    if years_with_data:
                        lower95_values = [country_pivot.loc[year, lower95_col] for year in years_with_data]
                        upper95_values = [country_pivot.loc[year, upper95_col] for year in years_with_data]
                        
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
                if lower80_col in country_pivot.columns and upper80_col in country_pivot.columns:
                    # Get data for uncertainty bands
                    years_with_data = [year for year in future_years if year in country_pivot.index 
                                     and pd.notna(country_pivot.loc[year, lower80_col]) 
                                     and pd.notna(country_pivot.loc[year, upper80_col])]
                    
                    if years_with_data:
                        lower80_values = [country_pivot.loc[year, lower80_col] for year in years_with_data]
                        upper80_values = [country_pivot.loc[year, upper80_col] for year in years_with_data]
                        
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
                
                # Add historical data (solid line) - includes up to 2025
                if historical_col in country_pivot.columns:
                    past_years_with_data = [year for year in past_years if year in country_pivot.index 
                                          and pd.notna(country_pivot.loc[year, historical_col])]
                    if past_years_with_data:
                        past_values = [country_pivot.loc[year, historical_col] for year in past_years_with_data]
                        
                        # Set hover template based on display mode
                        if display_mode == 'growth_rate':
                            hover_template = f'<b>{aoi.title()} Growth Rate</b><br>Growth Rate: %{{y:.2f}}%<br><extra></extra>'
                        else:
                            hover_template = f'<b>{aoi.title()} Population</b><br>Population: %{{y:.1f}} million<br><extra></extra>'
                        
                        fig.add_trace(go.Scatter(
                            x=past_years_with_data,
                            y=past_values,
                            mode='lines+markers',
                            name=f'{aoi.title()} (Historical)',
                            line=dict(color=colors[aoi], width=3),
                            marker=dict(size=6),
                            hovertemplate=hover_template,
                            connectgaps=False
                        ))
                
                # Add future projections (dashed line) - starts at 2025 to connect with historical
                if median_col in country_pivot.columns:
                    future_years_with_data = [year for year in future_years if year in country_pivot.index 
                                            and pd.notna(country_pivot.loc[year, median_col])]
                    if future_years_with_data:
                        future_values = [country_pivot.loc[year, median_col] for year in future_years_with_data]
                        
                        # Set hover template based on display mode
                        if display_mode == 'growth_rate':
                            hover_template = f'<b>{aoi.title()} Growth Rate (Projected)</b><br>Growth Rate: %{{y:.2f}}%<br><extra></extra>'
                        else:
                            hover_template = f'<b>{aoi.title()} Population (Projected)</b><br>Population: %{{y:.1f}} million<br><extra></extra>'
                        
                        fig.add_trace(go.Scatter(
                            x=future_years_with_data,
                            y=future_values,
                            mode='lines+markers',
                            name=f'{aoi.title()} (Projected)',
                            line=dict(color=colors[aoi], width=3, dash='dash'),
                            marker=dict(size=6),
                            hovertemplate=hover_template,
                            connectgaps=False
                        ))
            
            # Update layout with appropriate y-axis title and formatting
            if display_mode == 'growth_rate':
                yaxis_title = 'Population Growth Rate (%)'
                chart_title = html.H6([
                    html.B(country_name),
                    ' | Urban and Rural Population Growth Rate'
                ], style={'marginBottom': '1rem', 'color': '#2c3e50'})
                yaxis_config = dict(
                    title=yaxis_title,
                    tickformat='0.0f',  # Format as decimal with 1 place
                    ticksuffix='%'  # Add % suffix to each tick
                )
            else:
                yaxis_title = 'Population (millions)'
                chart_title = html.H6([
                    html.B(country_name),
                    ' | Urban and Rural Population Projections'
                ], style={'marginBottom': '1rem', 'color': '#2c3e50'})
                yaxis_config = dict(
                    title=yaxis_title,
                    tickformat=None
                )
            
            fig.update_layout(
                xaxis_title='Year',
                yaxis=yaxis_config,
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
                margin=dict(l=60, r=20, t=80, b=60),
                height=500
            )
            
            # Add vertical line at 2025 to separate historical from projections
            fig.add_vline(x=2025, line_dash="dash", line_color="gray", opacity=0.5)
            
            # Add annotations on either side of the line
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
            
            # Add zero line for growth rate mode
            if display_mode == 'growth_rate':
                fig.add_hline(y=0, line_dash="dot", line_color="gray", opacity=0.5)
            
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'urban-population-projections-download',
        lambda: undesa_projections,
        'undesa_urban_population_projections'
    )