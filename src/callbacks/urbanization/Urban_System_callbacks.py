"""
Callbacks for Urban System visualization
Shows time series of population distribution across Cities, Towns, and Rural areas
"""

from dash import Input, Output, html
import plotly.graph_objects as go

from ...utils.data_loader import load_wup2025_level1_data
from ...utils.country_utils import (
    load_subsaharan_countries_and_regions_dict,
)
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def register_urban_system_callbacks(app):
    """Register callbacks for Urban System chart"""

    # Load data once at startup
    urban_system_data_cache = load_wup2025_level1_data()
    countries_dict = load_subsaharan_countries_and_regions_dict()

    # Define colors for each category
    category_colors = {
        'Cities': '#2563eb',  # Blue
        'Towns': '#f59e0b',   # Orange
        'Rural': '#10b981'    # Green
    }

    @app.callback(
        [Output('urban-system-chart', 'figure'),
         Output('urban-system-chart', 'style'),
         Output('urban-system-title', 'children')],
        [
            Input('main-country-filter', 'value'),
            Input('urban-system-mode', 'value'),
        ],
        prevent_initial_call=False,
    )
    def generate_urban_system_chart(selected_country, display_mode):
        try:
            if not selected_country:
                raise Exception("No country selected")

            country_name = countries_dict.get(selected_country, selected_country)

            # Filter data for selected country
            country_data = urban_system_data_cache[
                urban_system_data_cache['ISO3_Code'] == selected_country
            ].copy()

            if country_data.empty:
                raise Exception(f"No urban system data available for {country_name}")

            # Sort by year
            country_data = country_data.sort_values('Year')

            # Create figure based on display mode
            if display_mode == 'relative_2':
                # Create stacked bar chart showing percentage distribution
                # Pivot data to get one row per year with columns for each category
                pivot_data = country_data.pivot(index='Year', columns='Category', values='Pop_rel').reset_index()
                
                # Ensure all categories exist
                if 'Cities' not in pivot_data.columns or 'Towns' not in pivot_data.columns or 'Rural' not in pivot_data.columns:
                    raise Exception(f"Missing category data for {country_name}")
                
                # Convert to percentages (multiply by 100)
                pivot_data['Cities_pct'] = pivot_data['Cities'] * 100
                pivot_data['Towns_pct'] = pivot_data['Towns'] * 100
                pivot_data['Rural_pct'] = pivot_data['Rural'] * 100
                
                # Create stacked area chart
                fig = go.Figure()
                
                # Add area traces for each category (in reverse order so Rural is at bottom)
                fig.add_trace(go.Scatter(
                    x=pivot_data['Year'],
                    y=pivot_data['Rural_pct'],
                    name='Rural',
                    mode='lines',
                    line=dict(width=0.5, color=category_colors['Rural']),
                    fillcolor=category_colors['Rural'],
                    fill='tonexty',
                    stackgroup='one',
                    hovertemplate='<b>Rural</b><br>Year: %{x}<br>Share: %{y:.1f}%<extra></extra>'
                ))
                
                fig.add_trace(go.Scatter(
                    x=pivot_data['Year'],
                    y=pivot_data['Towns_pct'],
                    name='Towns',
                    mode='lines',
                    line=dict(width=0.5, color=category_colors['Towns']),
                    fillcolor=category_colors['Towns'],
                    fill='tonexty',
                    stackgroup='one',
                    hovertemplate='<b>Towns</b><br>Year: %{x}<br>Share: %{y:.1f}%<extra></extra>'
                ))
                
                fig.add_trace(go.Scatter(
                    x=pivot_data['Year'],
                    y=pivot_data['Cities_pct'],
                    name='Cities',
                    mode='lines',
                    line=dict(width=0.5, color=category_colors['Cities']),
                    fillcolor=category_colors['Cities'],
                    fill='tonexty',
                    stackgroup='one',
                    hovertemplate='<b>Cities</b><br>Year: %{x}<br>Share: %{y:.1f}%<extra></extra>'
                ))
                
                chart_subtitle = 'Pattern of Urbanization'
                chart_title = html.H6([html.B(country_name), f' | {chart_subtitle}'], 
                                     className='chart-title')
                
                # Update layout for stacked area chart
                fig.update_layout(
                    xaxis=dict(
                        title='Year',
                        showgrid=True,
                        gridcolor='#e2e8f0',
                        zeroline=False,
                    ),
                    yaxis=dict(
                        title='Population Share (%)',
                        showgrid=True,
                        gridcolor='#e2e8f0',
                        zeroline=True,
                        zerolinecolor='#e2e8f0',
                        range=[0, 100],
                        ticksuffix='%'
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font={'color': CHART_STYLES['colors']['primary']},
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=-0.2,
                        xanchor='center',
                        x=0.5,
                        bgcolor='rgba(255,255,255,0.8)',
                    ),
                    margin=dict(t=40, b=80, l=80, r=80),
                    hovermode='x unified',
                    height=600,
                )
                
                # Add vertical line at 2025 to separate historical from projections
                fig.add_vline(x=2025, line_dash="dash", line_color="gray", opacity=0.5)
                
                # Add annotations on either side of the line
                fig.add_annotation(
                    x=2024,
                    y=0,
                    yref="paper",
                    text="Historical",
                    showarrow=False,
                    font=dict(size=12, color="gray"),
                    yanchor="bottom",
                    xanchor="right"
                )
                
                fig.add_annotation(
                    x=2026,
                    y=0,
                    yref="paper", 
                    text="Projections",
                    showarrow=False,
                    font=dict(size=12, color="gray"),
                    yanchor="bottom",
                    xanchor="left"
                )
                
            else:
                # Original line chart for absolute and relative_1 modes
                fig = go.Figure()
                
                # Determine which column to use based on display mode
                if display_mode == 'absolute':
                    value_column = 'Pop'
                    yaxis_title = 'Population'
                    chart_subtitle = 'Urban System (Absolute Population)'
                    hover_template = '<b>%{fullData.name}</b><br>Population: %{y:,.0f}<extra></extra>'
                else:  # relative_1
                    value_column = 'Pop_rel'
                    yaxis_title = 'Population Share (%)'
                    chart_subtitle = 'Urban System (Relative Distribution)'
                    hover_template = '<b>%{fullData.name}</b><br>Share: %{y:.1%}<extra></extra>'

                # Plot each category as a separate line
                for category in ['Cities', 'Towns', 'Rural']:
                    category_data = country_data[country_data['Category'] == category]
                    
                    if not category_data.empty:
                        # Split data for historical (<=2025) and projections (>=2025)
                        hist_data = category_data[category_data['Year'] <= 2025]
                        proj_data = category_data[category_data['Year'] >= 2025]
                        
                        # Add historical (solid line)
                        if not hist_data.empty:
                            fig.add_trace(
                                go.Scatter(
                                    x=hist_data['Year'],
                                    y=hist_data[value_column],
                                    mode='lines',
                                    name=category,
                                    line=dict(color=category_colors[category], width=3),
                                    marker=dict(size=6),
                                    hovertemplate=hover_template,
                                    showlegend=True
                                )
                            )
                        
                        # Add projections (dashed line)
                        if not proj_data.empty:
                            fig.add_trace(
                                go.Scatter(
                                    x=proj_data['Year'],
                                    y=proj_data[value_column],
                                    mode='lines',
                                    name=category,
                                    line=dict(color=category_colors[category], width=3, dash='dash'),
                                    marker=dict(size=6),
                                    hovertemplate=hover_template,
                                    showlegend=False
                                )
                            )

                # Create title
                chart_title = html.H6([html.B(country_name), f' | {chart_subtitle}'], 
                                     className='chart-title')

                # Update layout
                fig.update_layout(
                    xaxis=dict(
                        title='Year',
                        showgrid=True,
                        gridcolor='#e2e8f0',
                        zeroline=False,
                    ),
                    yaxis=dict(
                        title=yaxis_title,
                        showgrid=True,
                        gridcolor='#e2e8f0',
                        zeroline=True,
                        zerolinecolor='#e2e8f0',
                        range=[0, None],
                    ),
                    plot_bgcolor='white',
                    paper_bgcolor='white',
                    font={'color': CHART_STYLES['colors']['primary']},
                    legend=dict(
                        orientation='h',
                        yanchor='bottom',
                        y=-0.2,
                        xanchor='center',
                        x=0.5,
                        bgcolor='rgba(255,255,255,0.8)',
                    ),
                    margin=dict(t=40, b=80, l=80, r=80),
                    hovermode='x unified',
                    height=600,
                )

                # For relative mode, format as percentage
                if display_mode == 'relative_1':
                    fig.update_yaxes(tickformat='.0%')

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

            return fig, {'display': 'block'}, chart_title

        except Exception as e:
            # Print error to console for debugging
            print(f"ERROR in Urban System chart (Pattern of Urbanization): {str(e)}")
            import traceback
            traceback.print_exc()
            
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""

    # Register download callback
    create_simple_download_callback(
        app,
        'urban-system-download',
        lambda: urban_system_data_cache
    )
