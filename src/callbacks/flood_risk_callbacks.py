"""
Callbacks for flood risk assessment functionality
"""

from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

try:
    from ..utils.data_loader import create_sample_flood_risk_data
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.data_loader import create_sample_flood_risk_data


def register_callbacks(app):
    """Register all flood risk-related callbacks"""
    
    @app.callback(
        Output('flood-risk-map', 'figure'),
        [Input('flood-risk-level', 'value'),
         Input('flood-scenario', 'value'),
         Input('main-country-filter', 'value')]
    )
    def update_flood_risk_map(risk_levels, scenario, selected_country):
        """Update flood risk map"""
        try:
            # Load actual flood risk data
            flood_data = create_sample_flood_risk_data()
            scenario_data = flood_data[flood_data['scenario'] == scenario]
            
            country_codes = scenario_data['country_code'].tolist()
            country_names = scenario_data['country'].tolist()
            risk_values = scenario_data['flood_risk_level'].tolist()
            
        except Exception as e:
            # Return empty data for error handling
            country_codes = []
            country_names = []
            risk_values = []
        
        fig = go.Figure(data=go.Choropleth(
            locations=country_codes,
            z=risk_values,
            locationmode='ISO-3',
            colorscale='Reds',
            text=[f'{name}: Risk Level {val:.1f}' for name, val in zip(country_names, risk_values)],
            colorbar_title="Risk Level (1-10)",
            zmin=1,
            zmax=10
        ))
        
        scenario_titles = {
            'current': 'Current Flood Risk Assessment',
            '2030': 'Projected Flood Risk - 2030',
            '2050': 'Projected Flood Risk - 2050'
        }
        
        fig.update_layout(
            title_text=scenario_titles.get(scenario, 'Flood Risk Assessment'),
            geo=dict(
                showframe=False,
                showcoastlines=True,
                scope='africa'
            ),
            title_font_size=16
        )
        
        return fig
    
    @app.callback(
        Output('flood-risk-stats', 'figure'),
        [Input('flood-risk-level', 'value'),
         Input('flood-scenario', 'value'),
         Input('main-country-filter', 'value')]
    )
    def update_flood_risk_stats(risk_levels, scenario, selected_country):
        """Update flood risk statistics"""
        # Return empty pie chart for no data
        fig = go.Figure()
        fig.update_layout(
            title=f"No flood risk data available for {scenario.title()} scenario",
            annotations=[{
                'text': 'No data available',
                'showarrow': False,
                'font': {'size': 16, 'color': '#666'}
            }]
        )
        
        fig.update_layout(
            title_font_size=14,
            font={'color': '#2c3e50'}
        )
        
        return fig
    
    @app.callback(
        Output('flood-vulnerability-chart', 'figure'),
        [Input('flood-risk-level', 'value'),
         Input('flood-scenario', 'value'),
         Input('main-country-filter', 'value')]
    )
    def update_flood_vulnerability_chart(risk_levels, scenario, selected_country):
        """Update flood vulnerability analysis chart"""
        try:
            # Load actual flood risk data
            flood_data = create_sample_flood_risk_data()
            scenario_data = flood_data[flood_data['scenario'] == scenario]
            
            # Create vulnerability DataFrame
            vuln_data = scenario_data[['country', 'exposure', 'sensitivity', 'adaptive_capacity']].copy()
            
        except Exception as e:
            # Return empty data for error handling
            vuln_data = pd.DataFrame(columns=['country', 'exposure', 'sensitivity', 'adaptive_capacity'])
        
        # Sort by exposure (as a proxy for vulnerability)
        vuln_data = vuln_data.sort_values('exposure', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=vuln_data['country'],
            x=vuln_data['exposure'],
            name='Exposure',
            orientation='h',
            marker_color='#e74c3c'
        ))
        
        fig.add_trace(go.Bar(
            y=vuln_data['country'],
            x=vuln_data['sensitivity'],
            name='Sensitivity',
            orientation='h',
            marker_color='#f39c12'
        ))
        
        fig.add_trace(go.Bar(
            y=vuln_data['country'],
            x=vuln_data['adaptive_capacity'],
            name='Adaptive Capacity',
            orientation='h',
            marker_color='#2ecc71'
        ))
        
        fig.update_layout(
            title='Flood Vulnerability Components by Country',
            xaxis_title='Score (1-10)',
            yaxis_title='Country',
            barmode='group',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
            height=500
        )
        
        return fig