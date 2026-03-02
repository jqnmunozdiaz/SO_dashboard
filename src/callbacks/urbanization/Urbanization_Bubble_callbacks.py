"""
Callbacks for Urbanization Bubble Chart visualization
Shows bubble chart of all SSA countries:
  X-axis: Current urbanization level (% urban, 2025)
  Y-axis: Urban population growth rate (annual %, 2024-2025)
  Bubble size: Expected relative increase in urban population by 2050 (% of today's urban pop)
Based on UN DESA World Urbanization Prospects 2025 (WUP2025) National Definitions data
"""

from dash import Input, Output, html
import plotly.graph_objects as go
import numpy as np

from ...utils.data_loader import load_wup2025_national_data
from ...utils.country_utils import get_subsaharan_countries, load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES

# Year configuration
CURRENT_YEAR = 2025
PREV_YEAR = 2024
PROJECTION_YEAR = 2050


def register_urbanization_bubble_callbacks(app):
    """Register callbacks for Urbanization Bubble chart"""
    
    # Load static data once at registration time for performance
    wup_data = load_wup2025_national_data()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    ssa_countries = get_subsaharan_countries()
    ssa_codes = set(c['code'] for c in ssa_countries)
    
    @app.callback(
        [Output('urbanization-bubble-chart', 'figure'),
         Output('urbanization-bubble-chart', 'style'),
         Output('urbanization-bubble-title', 'children')],
        [Input('main-country-filter', 'value')],
        prevent_initial_call=False
    )
    def generate_urbanization_bubble_chart(selected_country):
        """Generate bubble chart showing urbanization level vs speed of urbanization for all SSA countries"""
        try:
            if not selected_country:
                raise Exception("No country selected")
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Filter for SSA countries only
            ssa_data = wup_data[wup_data['ISO3_Code'].isin(ssa_codes)].copy()
            
            if ssa_data.empty:
                raise Exception("No data available for Sub-Saharan Africa")
            
            # Get data for previous year, current year, and projection year
            prev_data = ssa_data[ssa_data['Year'] == PREV_YEAR][['ISO3_Code', 'Urban_Pop']].copy()
            current_data = ssa_data[ssa_data['Year'] == CURRENT_YEAR][['ISO3_Code', 'Urbanization_Rate', 'Urban_Pop']].copy()
            future_data = ssa_data[ssa_data['Year'] == PROJECTION_YEAR][['ISO3_Code', 'Urban_Pop']].copy()
            
            prev_data = prev_data.rename(columns={'Urban_Pop': 'prev_urban_pop'})
            current_data = current_data.rename(columns={
                'Urbanization_Rate': 'current_urb_rate',
                'Urban_Pop': 'current_urban_pop'
            })
            future_data = future_data.rename(columns={'Urban_Pop': 'future_urban_pop'})
            
            # Merge all three
            merged = current_data.merge(prev_data, on='ISO3_Code', how='inner')
            merged = merged.merge(future_data, on='ISO3_Code', how='inner')
            
            if merged.empty:
                raise Exception("Insufficient data to create bubble chart")
            
            # Compute metrics
            # X: current urbanization level (%)
            merged['x_current_level'] = merged['current_urb_rate'] * 100
            # Y: urban population growth rate (annual %)
            merged['urb_speed'] = ((merged['current_urban_pop'] - merged['prev_urban_pop']) / merged['prev_urban_pop']) * 100
            # Size: expected relative increase in urban population (%)
            merged['urban_pop_rel_increase'] = ((merged['future_urban_pop'] - merged['current_urban_pop']) / merged['current_urban_pop']) * 100
            # Get country names
            merged['country_name'] = merged['ISO3_Code'].map(countries_dict)
            
            # Remove rows with missing or non-positive values
            merged = merged[merged['current_urban_pop'] > 0].copy()
            
            fig = go.Figure()
            
            # Split into selected vs other countries
            other = merged[merged['ISO3_Code'] != selected_country]
            selected = merged[merged['ISO3_Code'] == selected_country]
            
            # Scale bubble sizes based on relative urban pop increase
            max_rel_increase = merged['urban_pop_rel_increase'].abs().max()
            min_size = 8
            max_size = 60
            
            def scale_size(rel_increase):
                return min_size + (max_size - min_size) * np.sqrt(abs(rel_increase) / max_rel_increase) if max_rel_increase > 0 else min_size
            
            # Other countries (gray/light)
            if not other.empty:
                fig.add_trace(go.Scatter(
                    x=other['x_current_level'],
                    y=other['urb_speed'],
                    mode='markers+text',
                    marker=dict(
                        size=other['urban_pop_rel_increase'].apply(scale_size),
                        color='#bdc3c7',
                        opacity=0.6,
                        line=dict(width=1, color='#95a5a6')
                    ),
                    text=other['ISO3_Code'],
                    textposition='middle center',
                    textfont=dict(size=8, color='#7f8c8d'),
                    name='Other SSA Countries',
                    hovertemplate=(
                        '<b>%{customdata[0]}</b><br>'
                        'Urbanization Level (' + str(CURRENT_YEAR) + '): %{x:.1f}%<br>'
                        'Urban Pop. Growth Rate: %{y:.2f}%/year<br>'
                        'Expected Urban Pop. Increase: %{customdata[1]:.0f}%<br>'
                        '<extra></extra>'
                    ),
                    customdata=list(zip(other['country_name'], other['urban_pop_rel_increase']))
                ))
            
            # Selected country (highlighted)
            if not selected.empty:
                fig.add_trace(go.Scatter(
                    x=selected['x_current_level'],
                    y=selected['urb_speed'],
                    mode='markers+text',
                    marker=dict(
                        size=selected['urban_pop_rel_increase'].apply(scale_size),
                        color='#295e84',
                        opacity=0.9,
                        line=dict(width=2, color='#1a3d5c')
                    ),
                    text=selected['ISO3_Code'],
                    textposition='middle center',
                    textfont=dict(size=10, color='white', family='Arial Black'),
                    name=country_name,
                    hovertemplate=(
                        '<b>%{customdata[0]}</b><br>'
                        'Urbanization Level (' + str(CURRENT_YEAR) + '): %{x:.1f}%<br>'
                        'Urban Pop. Growth Rate: %{y:.2f}%/year<br>'
                        'Expected Urban Pop. Increase: %{customdata[1]:.0f}%<br>'
                        '<extra></extra>'
                    ),
                    customdata=list(zip(selected['country_name'], selected['urban_pop_rel_increase']))
                ))
            
            # Add best fit line (linear regression)
            x_vals = merged['x_current_level'].values
            y_vals = merged['urb_speed'].values
            mask = np.isfinite(x_vals) & np.isfinite(y_vals)
            if mask.sum() >= 2:
                coeffs = np.polyfit(x_vals[mask], y_vals[mask], 1)
                x_line = np.linspace(x_vals[mask].min(), x_vals[mask].max(), 100)
                y_line = np.polyval(coeffs, x_line)
                fig.add_trace(go.Scatter(
                    x=x_line,
                    y=y_line,
                    mode='lines',
                    name='Best Fit',
                    line=dict(color='rgba(255, 100, 100, 0.7)', width=2, dash='dash'),
                    hoverinfo='skip'
                ))
            
            # Create title
            chart_title = html.H6(
                [html.B(country_name), f' | Urbanization Dynamics ({CURRENT_YEAR}–{PROJECTION_YEAR})'],
                className='chart-title'
            )
            
            fig.update_layout(
                xaxis_title=f'Current Urbanization Level ({CURRENT_YEAR}, %)',
                yaxis_title='Urban Population Growth Rate<br>(annual %)',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='#ccc',
                    ticksuffix='%'
                ),
                xaxis=dict(
                    range=[0, 100],
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=False,
                    ticksuffix='%'
                ),
                margin=dict(b=30, t=60)
            )
            
            return fig, {'display': 'block'}, chart_title
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback
    create_simple_download_callback(
        app,
        'urbanization-bubble-download',
        lambda: wup_data[wup_data['ISO3_Code'].isin(ssa_codes)]
    )
