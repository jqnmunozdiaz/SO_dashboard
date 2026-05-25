"""
Callbacks for Risk Estimates - PML by Sector line chart
"""

from dash import Input, Output, html
import plotly.express as px
import pandas as pd
from typing import Optional

from ...utils.data_loader import load_giri_processed_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from config.settings import CHART_STYLES


def setup_pml_by_sector_callbacks(app):
    """Setup callbacks for GIRI PML by Sector visualization"""
    
    @app.callback(
        [Output('pml-sector-chart', 'figure'),
         Output('pml-sector-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('pml-sector-hazard-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_pml_sector_chart(selected_country, selected_hazard):
        """Generate line chart of GIRI PML by sector vs Return Period (RP)"""
        try:
            if not selected_country or not selected_hazard:
                raise Exception("Selection missing")
                
            countries_dict = load_subsaharan_countries_and_regions_dict()
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Regional aggregation check
            if selected_country in ['SSA', 'AFE', 'AFW']:
                raise Exception("PML by sector analytics are only available for individual countries, not for regional groupings.")
                
            # Load complete processed GIRI dataset
            df = load_giri_processed_data()
            
            # Filter for selected country, selected hazard, and PML risk metric
            # Also exclude Combined hazard and Combined sector
            filtered_df = df[
                (df['iso3cd'] == selected_country) & 
                (df['hazard'] == selected_hazard) & 
                (df['risk_metric_abbr'] == 'PML') &
                (df['sector'] != 'Combined')
            ].copy()
            
            if filtered_df.empty:
                raise Exception(f"No GIRI PML by sector data available for {country_name} ({selected_hazard})")
                
            # Compute Loss in Million USD for visual readability
            filtered_df['Loss_MUSD'] = filtered_df['Loss'] / 1e6
            
            # Convert RP to numeric and sort for correct line paths
            filtered_df['RP'] = pd.to_numeric(filtered_df['RP'])
            
            # Filter to present only up to RP = 1000
            filtered_df = filtered_df[filtered_df['RP'] <= 1000]
            filtered_df = filtered_df.sort_values(by='RP')
            
            # Combine sector and subsector to label as "sector - subsector"
            filtered_df['sector_subsector'] = filtered_df['sector'] + ' - ' + filtered_df['subsector']
            
            # Sort the combined label to have alphabetical ordering in the legend and consistent lines
            filtered_df = filtered_df.sort_values(by=['sector_subsector', 'RP'])
            
            # Create the interactive scatter plot grouped and colored by subsector
            fig = px.scatter(
                filtered_df,
                x='RP',
                y='Loss_MUSD',
                color='sector_subsector',
                color_discrete_sequence=px.colors.qualitative.Alphabet,
                log_x=False,
                labels={
                    'RP': 'Return Period (Years)',
                    'Loss_MUSD': 'Probable Maximum Loss (Million USD)',
                    'sector_subsector': 'Sector - Subsector'
                },
                template='plotly_white'
            )
            
            # Update traces to show both lines and markers, with a premium hover template showing the full subsector trace name
            fig.update_traces(
                mode='lines+markers',
                hovertemplate="<b>%{fullData.name}</b><br>RP: %{x} Years<br>PML: %{y:,.2f} M USD<extra></extra>"
            )
            
            # Dynamic chart title children
            title_children = html.H6([
                html.B(country_name),
                f" | PML by Subsector - {selected_hazard}"
            ], className='chart-title')
            
            # Layout updates matching World Bank styling
            fig.update_layout(
                xaxis_title='Return Period (Years)',
                yaxis_title='Probable Maximum Loss (Million USD)',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=True,
                legend=dict(
                    title="Sectors & Subsectors",
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02,
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="#e2e8f0",
                    borderwidth=0
                ),
                height=550,
                margin=dict(r=280, l=80, t=40, b=50),  # Increased right margin for longer subsector legend labels
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    type='linear',  # Linear scale for return periods
                    tickvals=sorted(filtered_df['RP'].unique()),
                    ticktext=[str(int(val)) for val in sorted(filtered_df['RP'].unique())]
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    tickformat=',.1f'
                )
            )
            
            return fig, title_children
            
        except Exception as e:
            # Return an empty figure with the error message in title
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.update_layout(
                xaxis={'visible': False},
                yaxis={'visible': False},
                annotations=[{
                    'text': str(e),
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 12, 'color': '#ef4444'}
                }]
            )
            title_children = html.Div(style={'color': '#ef4444', 'fontWeight': 'bold'}, children=str(e))
            return fig, title_children
