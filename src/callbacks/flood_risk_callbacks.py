"""
Callbacks for flood risk assessment functionality
"""

from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def register_callbacks(app):
    """Register all flood risk-related callbacks"""
    
    @app.callback(
        Output('flood-risk-map', 'figure'),
        [Input('flood-risk-level', 'value'),
         Input('flood-scenario', 'value')]
    )
    def update_flood_risk_map(risk_levels, scenario):
        """Update flood risk map"""
        # Sample flood risk data
        country_codes = ['NGA', 'KEN', 'ETH', 'GHA', 'TZA', 'UGA', 'MOZ', 'MDG', 'CMR', 'MLI']
        country_names = ['Nigeria', 'Kenya', 'Ethiopia', 'Ghana', 'Tanzania', 
                        'Uganda', 'Mozambique', 'Madagascar', 'Cameroon', 'Mali']
        
        # Risk values based on scenario
        if scenario == 'current':
            risk_values = [7.2, 5.8, 4.3, 6.9, 6.1, 5.2, 8.1, 7.8, 5.9, 3.4]
        elif scenario == '2030':
            risk_values = [7.8, 6.2, 4.9, 7.3, 6.7, 5.8, 8.6, 8.3, 6.4, 3.9]
        else:  # 2050
            risk_values = [8.5, 6.8, 5.6, 7.9, 7.4, 6.5, 9.2, 8.9, 7.1, 4.5]
        
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
         Input('flood-scenario', 'value')]
    )
    def update_flood_risk_stats(risk_levels, scenario):
        """Update flood risk statistics"""
        # Sample statistics data
        risk_categories = ['Low Risk', 'Medium Risk', 'High Risk', 'Very High Risk']
        
        if scenario == 'current':
            country_counts = [12, 18, 15, 8]
        elif scenario == '2030':
            country_counts = [10, 16, 18, 9]
        else:  # 2050
            country_counts = [8, 14, 20, 11]
        
        fig = px.pie(
            values=country_counts,
            names=risk_categories,
            title=f'Flood Risk Distribution - {scenario.title()}',
            color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c', '#8b0000']
        )
        
        fig.update_layout(
            title_font_size=14,
            font={'color': '#2c3e50'}
        )
        
        return fig
    
    @app.callback(
        Output('flood-vulnerability-chart', 'figure'),
        [Input('flood-risk-level', 'value'),
         Input('flood-scenario', 'value')]
    )
    def update_flood_vulnerability_chart(risk_levels, scenario):
        """Update flood vulnerability analysis chart"""
        # Sample vulnerability data
        countries = ['Nigeria', 'Mozambique', 'Madagascar', 'Ghana', 'Tanzania', 
                    'Kenya', 'Uganda', 'Cameroon', 'Ethiopia', 'Mali']
        
        # Vulnerability factors
        exposure = [8.5, 9.2, 8.8, 7.3, 6.9, 6.2, 5.8, 6.4, 5.1, 4.2]
        sensitivity = [7.8, 8.5, 8.1, 6.9, 6.5, 5.9, 5.4, 6.1, 6.8, 5.2]
        adaptive_capacity = [4.2, 3.8, 4.1, 5.8, 5.2, 6.1, 5.9, 5.3, 4.6, 4.9]
        
        # Create vulnerability index (higher exposure + sensitivity - adaptive capacity = higher vulnerability)
        vulnerability_index = [exp + sens - adapt for exp, sens, adapt in 
                             zip(exposure, sensitivity, adaptive_capacity)]
        
        # Create DataFrame
        vuln_data = pd.DataFrame({
            'country': countries,
            'exposure': exposure,
            'sensitivity': sensitivity,
            'adaptive_capacity': adaptive_capacity,
            'vulnerability_index': vulnerability_index
        })
        
        # Sort by vulnerability index
        vuln_data = vuln_data.sort_values('vulnerability_index', ascending=True)
        
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