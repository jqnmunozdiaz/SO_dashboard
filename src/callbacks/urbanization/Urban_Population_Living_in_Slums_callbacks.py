"""
Callbacks for Urban Population Living in Slums visualization
Shows line chart of slums population percentage over time for selected country with regional benchmarks
"""

from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ...utils.data_loader import load_wdi_data, load_urbanization_indicators_dict
    from ...utils.country_utils import load_subsaharan_countries_dict
    from config.settings import CHART_STYLES
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_wdi_data, load_urbanization_indicators_dict
    from src.utils.country_utils import load_subsaharan_countries_dict
    from config.settings import CHART_STYLES


def register_urban_population_living_in_slums_callbacks(app):
    """Register callbacks for Urban Population Living in Slums chart"""
    
    @app.callback(
        Output('urban-population-slums-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('slums-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_urban_population_slums_chart(selected_country, benchmark_regions):
        """Generate line chart showing urban population living in slums over time"""
        try:
            # Load slums data
            slums_data = load_wdi_data('EN.POP.SLUM.UR.ZS')
            
            # Load indicators dictionary for title
            indicators_dict = load_urbanization_indicators_dict()
            chart_title = indicators_dict.get('EN.POP.SLUM.UR.ZS', 'Urban Population Living in Slums')
            
            # Load country mapping for ISO code to full name conversion
            countries_dict = load_subsaharan_countries_dict()
            
            if slums_data.empty:
                # Return empty chart if no data
                fig = create_empty_chart("No data available")
                return fig
            
            # Create the figure
            fig = go.Figure()
            
            # Get country data
            if selected_country and selected_country in slums_data['Country Code'].values:
                country_data = slums_data[slums_data['Country Code'] == selected_country].copy()
                country_data = country_data.sort_values('Year')
                
                if not country_data.empty:
                    country_name = countries_dict.get(selected_country, selected_country)
                    
                    # Add country line
                    fig.add_trace(go.Scatter(
                        x=country_data['Year'],
                        y=country_data['Value'],
                        mode='lines+markers',
                        name=country_name,
                        line=dict(color='#295e84', width=3),
                        marker=dict(size=6, color='#295e84'),
                        hovertemplate=f'<b>{country_name}</b><br>Year: %{{x}}<br>Slums Population: %{{y:.1f}}%<extra></extra>'
                    ))
                    
                    title_suffix = f"{country_name}"
                else:
                    title_suffix = f"{countries_dict.get(selected_country, selected_country)} - No data available"
            else:
                title_suffix = "No country selected"
            
            # Add benchmark regions if selected
            benchmark_colors = {
                'SSA': '#e74c3c',  # Red
                'AFE': '#f39c12',  # Orange
                'AFW': '#27ae60'   # Green
            }
            
            benchmark_names = {
                'SSA': 'Sub-Saharan Africa',
                'AFE': 'Africa Eastern and Southern',
                'AFW': 'Africa Western and Central'
            }
            
            if benchmark_regions:
                for region in benchmark_regions:
                    if region in slums_data['Country Code'].values:
                        region_data = slums_data[slums_data['Country Code'] == region].copy()
                        region_data = region_data.sort_values('Year')
                        
                        if not region_data.empty:
                            fig.add_trace(go.Scatter(
                                x=region_data['Year'],
                                y=region_data['Value'],
                                mode='lines',
                                name=benchmark_names.get(region, region),
                                line=dict(color=benchmark_colors.get(region, '#95a5a6'), width=2, dash='dash'),
                                hovertemplate=f'<b>{benchmark_names.get(region, region)}</b><br>Year: %{{x}}<br>Slums Population: %{{y:.1f}}%<extra></extra>'
                            ))
            
            # Update layout
            fig.update_layout(
                title=f'<b>{title_suffix}</b> | {chart_title}<br><sub>Data Source: World Development Indicators (World Bank)</sub>',
                xaxis_title='Year',
                yaxis_title='Population Living in Slums (% of Urban Population)',
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
            
            return fig
            
        except Exception as e:
            # Return error chart
            return create_empty_chart(f"Error loading data: {str(e)[:50]}")


def create_empty_chart(message):
    """Create an empty chart with error message"""
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        xanchor='center', yanchor='middle',
        showarrow=False,
        font=dict(size=16, color="gray")
    )
    fig.update_layout(
        title='Urban Population Living in Slums',
        xaxis_title='Year',
        yaxis_title='Population Living in Slums (% of Urban Population)',
        plot_bgcolor='white',
        paper_bgcolor='white',
        yaxis=dict(range=[0, 100]),
        showlegend=False
    )
    return fig