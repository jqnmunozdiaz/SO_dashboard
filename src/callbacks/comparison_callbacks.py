"""
Callbacks for country comparison functionality
"""

from dash import Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc

try:
    from ..utils.data_loader import (
        create_sample_disaster_data, 
        create_sample_urbanization_data, 
        create_sample_flood_risk_data,
        get_subsaharan_countries
    )
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.data_loader import (
        create_sample_disaster_data, 
        create_sample_urbanization_data, 
        create_sample_flood_risk_data,
        get_subsaharan_countries
    )


def register_callbacks(app):
    """Register all comparison-related callbacks"""
    
    @app.callback(
        Output('comparison-additional-countries', 'options'),
        Input('main-tabs', 'active_tab')
    )
    def update_comparison_additional_countries_options(active_tab):
        """Update country dropdown options for comparison tab"""
        if active_tab == 'comparison':
            countries = get_subsaharan_countries()
            return [{'label': country['name'], 'value': country['code']} 
                   for country in countries[:20]]  # Limit to first 20 for performance
        return []
    
    @app.callback(
        Output('comparison-main-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('comparison-additional-countries', 'value'),
         Input('comparison-metrics', 'value'),
         Input('comparison-chart-type', 'value')]
    )
    def update_comparison_chart(main_country, additional_countries, metrics, chart_type):
        """Update the main comparison chart"""
        # Combine main country with additional countries
        countries = [main_country] if main_country else []
        if additional_countries:
            countries.extend(additional_countries)
        
        if not countries or not metrics:
            # Return empty chart
            fig = go.Figure()
            fig.update_layout(
                title="Select countries and metrics to compare",
                xaxis_title="",
                yaxis_title="",
                showlegend=False
            )
            return fig
        
        # Generate comparison data
        comparison_data = generate_comparison_data(countries, metrics)
        
        if chart_type == 'bar':
            return create_bar_comparison(comparison_data, metrics)
        elif chart_type == 'radar':
            return create_radar_comparison(comparison_data, metrics, countries)
        else:  # scatter
            return create_scatter_comparison(comparison_data, metrics)
    
    @app.callback(
        Output('comparison-summary-table', 'children'),
        [Input('main-country-filter', 'value'),
         Input('comparison-additional-countries', 'value'),
         Input('comparison-metrics', 'value')]
    )
    def update_comparison_table(main_country, additional_countries, metrics):
        """Update the comparison summary table"""
        # Combine main country with additional countries
        countries = [main_country] if main_country else []
        if additional_countries:
            countries.extend(additional_countries)
        
        if not countries or not metrics:
            return html.Div("Select countries and metrics to view comparison table.")
        
        # Generate comparison data
        comparison_data = generate_comparison_data(countries, metrics)
        
        # Create table
        table_data = []
        for country in countries:
            country_data = comparison_data[comparison_data['country_code'] == country]
            if not country_data.empty:
                row = {'Country': country_data['country'].iloc[0]}
                for metric in metrics:
                    if metric in country_data.columns:
                        row[get_metric_label(metric)] = f"{country_data[metric].iloc[0]:.2f}"
                table_data.append(row)
        
        if not table_data:
            return html.Div("No data available for selected countries and metrics.")
        
        # Create Bootstrap table
        table_header = [html.Thead([html.Tr([html.Th(col) for col in table_data[0].keys()])])]
        table_body = [html.Tbody([
            html.Tr([html.Td(row[col]) for col in row.keys()]) 
            for row in table_data
        ])]
        
        return dbc.Table(
            table_header + table_body,
            bordered=True,
            hover=True,
            responsive=True,
            striped=True,
            className="mt-3"
        )


def generate_comparison_data(countries, metrics):
    """Generate comparison data for selected countries and metrics"""
    # Get sample data
    disaster_data = create_sample_disaster_data()
    urban_data = create_sample_urbanization_data()
    flood_data = create_sample_flood_risk_data()
    
    comparison_data = []
    
    for country_code in countries:
        # Find country name
        country_info = next((c for c in get_subsaharan_countries() if c['code'] == country_code), None)
        country_name = country_info['name'] if country_info else country_code
        
        row = {
            'country': country_name,
            'country_code': country_code
        }
        
        # Calculate metrics
        if 'disaster_freq' in metrics:
            country_disasters = disaster_data[disaster_data['country_code'] == country_code]
            row['disaster_freq'] = len(country_disasters) / 10  # Normalize to per year
        
        if 'pop_risk' in metrics:
            country_disasters = disaster_data[disaster_data['country_code'] == country_code]
            row['pop_risk'] = country_disasters['affected_population'].sum() / 1000000 if len(country_disasters) > 0 else 0
        
        if 'economic_impact' in metrics:
            country_disasters = disaster_data[disaster_data['country_code'] == country_code]
            row['economic_impact'] = country_disasters['economic_damage_usd'].sum() / 1000000 if len(country_disasters) > 0 else 0
        
        if 'urban_growth' in metrics:
            country_urban = urban_data[urban_data['country_code'] == country_code]
            row['urban_growth'] = country_urban['urban_growth_rate'].mean() if len(country_urban) > 0 else 0
        
        if 'flood_risk' in metrics:
            country_flood = flood_data[
                (flood_data['country_code'] == country_code) & 
                (flood_data['scenario'] == 'current')
            ]
            row['flood_risk'] = country_flood['flood_risk_level'].iloc[0] if len(country_flood) > 0 else 0
        
        comparison_data.append(row)
    
    return pd.DataFrame(comparison_data)


def create_bar_comparison(data, metrics):
    """Create bar chart comparison"""
    if len(metrics) == 1:
        fig = px.bar(
            data,
            x='country',
            y=metrics[0],
            title=f'Country Comparison: {get_metric_label(metrics[0])}',
            labels={'country': 'Country', metrics[0]: get_metric_label(metrics[0])}
        )
    else:
        # Create grouped bar chart
        melted_data = pd.melt(
            data,
            id_vars=['country', 'country_code'],
            value_vars=metrics,
            var_name='metric',
            value_name='value'
        )
        melted_data['metric_label'] = melted_data['metric'].apply(get_metric_label)
        
        fig = px.bar(
            melted_data,
            x='country',
            y='value',
            color='metric_label',
            title='Country Comparison: Multiple Metrics',
            labels={'value': 'Value', 'country': 'Country'},
            barmode='group'
        )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': '#2c3e50'},
        title_font_size=16
    )
    
    return fig


def create_radar_comparison(data, metrics, countries):
    """Create radar chart comparison"""
    fig = go.Figure()
    
    # Normalize data for radar chart (0-10 scale)
    normalized_data = data.copy()
    for metric in metrics:
        if metric in data.columns:
            max_val = data[metric].max()
            min_val = data[metric].min()
            if max_val > min_val:
                normalized_data[metric] = 10 * (data[metric] - min_val) / (max_val - min_val)
            else:
                normalized_data[metric] = 5  # Default middle value
    
    colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
    
    for i, (_, row) in enumerate(normalized_data.iterrows()):
        fig.add_trace(go.Scatterpolar(
            r=[row[metric] for metric in metrics],
            theta=[get_metric_label(metric) for metric in metrics],
            fill='toself',
            name=row['country'],
            line_color=colors[i % len(colors)]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        title='Country Comparison - Radar Chart',
        title_font_size=16,
        font={'color': '#2c3e50'}
    )
    
    return fig


def create_scatter_comparison(data, metrics):
    """Create scatter plot comparison"""
    if len(metrics) < 2:
        # If less than 2 metrics, create a simple scatter with index
        fig = px.scatter(
            data,
            x=list(range(len(data))),
            y=metrics[0] if metrics else 'disaster_freq',
            text='country',
            title=f'Country Values: {get_metric_label(metrics[0]) if metrics else "Disaster Frequency"}'
        )
        fig.update_traces(textposition="top center")
        fig.update_layout(xaxis_title="Country Index")
    else:
        # Use first two metrics for x and y
        size_metric = metrics[2] if len(metrics) > 2 else None
        
        fig = px.scatter(
            data,
            x=metrics[0],
            y=metrics[1],
            text='country',
            size=size_metric,
            title=f'Country Comparison: {get_metric_label(metrics[0])} vs {get_metric_label(metrics[1])}',
            labels={
                metrics[0]: get_metric_label(metrics[0]),
                metrics[1]: get_metric_label(metrics[1])
            }
        )
        fig.update_traces(textposition="top center")
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': '#2c3e50'},
        title_font_size=16
    )
    
    return fig


def get_metric_label(metric):
    """Get human-readable label for metric"""
    labels = {
        'disaster_freq': 'Disaster Frequency (per year)',
        'pop_risk': 'Population at Risk (millions)',
        'economic_impact': 'Economic Impact (millions USD)',
        'urban_growth': 'Urban Growth Rate (%)',
        'flood_risk': 'Flood Risk Level (1-10)'
    }
    return labels.get(metric, metric.replace('_', ' ').title())