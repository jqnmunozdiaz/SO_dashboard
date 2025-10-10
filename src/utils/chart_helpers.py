"""
Chart creation utilities for the DRM dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict, Optional


def create_disaster_timeline(data: pd.DataFrame, 
                           countries: Optional[List[str]] = None,
                           disaster_types: Optional[List[str]] = None,
                           year_range: Optional[List[int]] = None) -> go.Figure:
    """
    Create a timeline chart for disaster trends
    
    Args:
        data: DataFrame with disaster data
        countries: List of country codes to include
        disaster_types: List of disaster types to include
        year_range: [start_year, end_year] range
        
    Returns:
        Plotly figure
    """
    # Filter data based on inputs
    filtered_data = data.copy()
    
    if countries:
        filtered_data = filtered_data[filtered_data['country_code'].isin(countries)]
    
    if disaster_types:
        filtered_data = filtered_data[filtered_data['disaster_type'].isin(disaster_types)]
    
    if year_range:
        filtered_data = filtered_data[
            (filtered_data['year'] >= year_range[0]) & 
            (filtered_data['year'] <= year_range[1])
        ]
    
    # Aggregate data by year and country
    agg_data = filtered_data.groupby(['year', 'country']).agg({
        'affected_population': 'sum',
        'economic_damage_usd': 'sum',
        'disaster_type': 'count'  # Count of disasters
    }).reset_index()
    
    agg_data.rename(columns={'disaster_type': 'disaster_count'}, inplace=True)
    
    fig = px.line(
        agg_data,
        x='year',
        y='disaster_count',
        color='country',
        title='Historical Disaster Trends',
        labels={'disaster_count': 'Number of Disasters', 'year': 'Year'},
        hover_data=['affected_population', 'economic_damage_usd']
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': '#2c3e50'},
        title_font_size=16,
        hovermode='x unified'
    )
    
    return fig


def create_disaster_map(data: pd.DataFrame,
                       countries: Optional[List[str]] = None,
                       disaster_types: Optional[List[str]] = None,
                       year_range: Optional[List[int]] = None,
                       metric: str = 'disaster_count') -> go.Figure:
    """
    Create a choropleth map for disaster distribution
    
    Args:
        data: DataFrame with disaster data
        countries: List of country codes to include
        disaster_types: List of disaster types to include
        year_range: [start_year, end_year] range
        metric: Metric to display ('disaster_count', 'affected_population', 'economic_damage_usd')
        
    Returns:
        Plotly figure
    """
    # Filter data
    filtered_data = data.copy()
    
    if countries:
        filtered_data = filtered_data[filtered_data['country_code'].isin(countries)]
    
    if disaster_types:
        filtered_data = filtered_data[filtered_data['disaster_type'].isin(disaster_types)]
    
    if year_range:
        filtered_data = filtered_data[
            (filtered_data['year'] >= year_range[0]) & 
            (filtered_data['year'] <= year_range[1])
        ]
    
    # Aggregate by country
    if metric == 'disaster_count':
        agg_data = filtered_data.groupby('country_code').size().reset_index(name='value')
        colorbar_title = "Number of Disasters"
        hover_text = "disasters"
    elif metric == 'affected_population':
        agg_data = filtered_data.groupby('country_code')['affected_population'].sum().reset_index()
        agg_data.rename(columns={'affected_population': 'value'}, inplace=True)
        colorbar_title = "Affected Population"
        hover_text = "people affected"
    else:  # economic_damage_usd
        agg_data = filtered_data.groupby('country_code')['economic_damage_usd'].sum().reset_index()
        agg_data.rename(columns={'economic_damage_usd': 'value'}, inplace=True)
        colorbar_title = "Economic Damage (USD)"
        hover_text = "USD damage"
    
    fig = go.Figure(data=go.Choropleth(
        locations=agg_data['country_code'],
        z=agg_data['value'],
        locationmode='ISO-3',
        colorscale='Reds',
        text=[f'{val:.0f} {hover_text}' for val in agg_data['value']],
        colorbar_title=colorbar_title
    ))
    
    fig.update_layout(
        title_text='Disaster Impact Distribution',
        geo=dict(
            showframe=False,
            showcoastlines=True,
            scope='africa'
        ),
        title_font_size=16
    )
    
    return fig


def create_urbanization_trend_chart(data: pd.DataFrame,
                                  countries: Optional[List[str]] = None,
                                  indicator: str = 'urban_population_pct') -> go.Figure:
    """
    Create urbanization trend chart
    
    Args:
        data: DataFrame with urbanization data
        countries: List of country codes to include
        indicator: Urbanization indicator to plot
        
    Returns:
        Plotly figure
    """
    # Filter data
    filtered_data = data.copy()
    
    if countries:
        filtered_data = filtered_data[filtered_data['country_code'].isin(countries)]
    
    # Create titles and labels
    title_map = {
        'urban_population_pct': 'Urban Population Percentage Over Time',
        'urban_growth_rate': 'Urban Growth Rate Over Time',
        'population_density': 'Population Density Over Time'
    }
    
    label_map = {
        'urban_population_pct': 'Urban Population %',
        'urban_growth_rate': 'Growth Rate %',
        'population_density': 'People per km²'
    }
    
    fig = px.line(
        filtered_data,
        x='year',
        y=indicator,
        color='country',
        title=title_map.get(indicator, 'Urbanization Trends'),
        labels={indicator: label_map.get(indicator, 'Value'), 'year': 'Year'},
        markers=True
    )
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': '#2c3e50'},
        title_font_size=16,
        hovermode='x unified'
    )
    
    return fig


def create_flood_risk_vulnerability_chart(data: pd.DataFrame,
                                        scenario: str = 'current') -> go.Figure:
    """
    Create flood vulnerability components chart
    
    Args:
        data: DataFrame with flood risk data
        scenario: Risk scenario ('current', '2030', '2050')
        
    Returns:
        Plotly figure
    """
    # Filter data by scenario
    scenario_data = data[data['scenario'] == scenario].copy()
    
    # Sort by flood risk level
    scenario_data = scenario_data.sort_values('flood_risk_level', ascending=True)
    
    fig = go.Figure()
    
    # Add traces for each vulnerability component
    fig.add_trace(go.Bar(
        y=scenario_data['country'],
        x=scenario_data['exposure'],
        name='Exposure',
        orientation='h',
        marker_color='#e74c3c',
        opacity=0.8
    ))
    
    fig.add_trace(go.Bar(
        y=scenario_data['country'],
        x=scenario_data['sensitivity'],
        name='Sensitivity',
        orientation='h',
        marker_color='#f39c12',
        opacity=0.8
    ))
    
    fig.add_trace(go.Bar(
        y=scenario_data['country'],
        x=scenario_data['adaptive_capacity'],
        name='Adaptive Capacity',
        orientation='h',
        marker_color='#2ecc71',
        opacity=0.8
    ))
    
    fig.update_layout(
        title=f'Flood Vulnerability Components - {scenario.title()}',
        xaxis_title='Score (1-10)',
        yaxis_title='Country',
        barmode='group',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': '#2c3e50'},
        title_font_size=16,
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def create_comparison_chart(data: pd.DataFrame,
                           countries: List[str],
                           metrics: List[str],
                           chart_type: str = 'bar') -> go.Figure:
    """
    Create country comparison chart
    
    Args:
        data: DataFrame with comparison data
        countries: List of countries to compare
        metrics: List of metrics to compare
        chart_type: Type of chart ('bar', 'radar', 'scatter')
        
    Returns:
        Plotly figure
    """
    # Filter data for selected countries
    comparison_data = data[data['country'].isin(countries)].copy()
    
    if chart_type == 'bar':
        fig = px.bar(
            comparison_data,
            x='country',
            y=metrics[0] if metrics else 'value',
            title=f'Country Comparison: {metrics[0] if metrics else "Metric"}',
            color='country'
        )
    
    elif chart_type == 'radar':
        # Reshape data for radar chart
        fig = go.Figure()
        
        for country in countries:
            country_data = comparison_data[comparison_data['country'] == country]
            if not country_data.empty:
                fig.add_trace(go.Scatterpolar(
                    r=[country_data[metric].iloc[0] if metric in country_data.columns else 0 
                       for metric in metrics],
                    theta=metrics,
                    fill='toself',
                    name=country
                ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 10]
                )
            ),
            title='Country Comparison - Radar Chart'
        )
    
    else:  # scatter
        if len(metrics) >= 2:
            fig = px.scatter(
                comparison_data,
                x=metrics[0],
                y=metrics[1],
                color='country',
                size=metrics[2] if len(metrics) > 2 else None,
                title=f'Country Comparison: {metrics[0]} vs {metrics[1]}'
            )
        else:
            fig = px.bar(comparison_data, x='country', y=metrics[0] if metrics else 'value')
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': '#2c3e50'},
        title_font_size=16
    )
    
    return fig