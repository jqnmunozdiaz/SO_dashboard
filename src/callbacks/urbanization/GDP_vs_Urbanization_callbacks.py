"""
Callbacks for GDP vs Urbanization scatterplot visualization
Shows scatterplot of GDP per capita (y) vs Urbanization Rate (x) for selected country and country benchmarks
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd

from ...utils.data_loader import load_wdi_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.GLOBAL_BENCHMARK_CONFIG import get_global_benchmark_colors, get_global_benchmark_names
from ...utils.download_helpers import create_multi_csv_download_callback
from config.settings import CHART_STYLES

GDP_INDICATOR = "NY.GDP.PCAP.PP.KD"
URBAN_INDICATOR = "SP.URB.TOTL.IN.ZS"

def register_gdp_vs_urbanization_callbacks(app):
    """Register callbacks for GDP vs Urbanization chart"""
    
    # Load static data once at registration time for performance
    gdp_df = load_wdi_data(GDP_INDICATOR)
    urb_df = load_wdi_data(URBAN_INDICATOR)
    countries_dict = load_subsaharan_countries_and_regions_dict()
    global_colors = get_global_benchmark_colors()
    global_names = get_global_benchmark_names()
    
    @app.callback(
        [Output('gdp-vs-urbanization-chart', 'figure'),
         Output('gdp-vs-urbanization-chart', 'style')],
        [Input('main-country-filter', 'value'),
         Input('gdp-vs-urbanization-country-benchmark-selector', 'value'),
         Input('gdp-vs-urbanization-global-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_gdp_vs_urbanization_chart(selected_country, benchmark_countries, global_benchmarks):
        try:            
            # Handle no country selected case (pre-loaded)     
            if selected_country:
                title_suffix = countries_dict.get(selected_country)
            else:
                raise Exception("No country selected")

            fig = go.Figure()
            # Helper to merge and plot for a country
            def plot_country(iso, name, color, dash=None):
                gdp = gdp_df[gdp_df['Country Code'] == iso]
                urb = urb_df[urb_df['Country Code'] == iso]
                merged = pd.merge(urb, gdp, on=['Country Code', 'Year'], suffixes=('_urb', '_gdp'))
                merged = merged.sort_values('Year')
                if not merged.empty:
                    fig.add_trace(go.Scatter(
                        x=merged['Value_urb'],
                        y=merged['Value_gdp'],
                        mode='lines',
                        name=name,
                        line=dict(color=color, width=3, dash=dash) if dash else dict(color=color, width=3),
                        marker=dict(size=6, color=color),
                        hovertemplate=f'<b>{name}</b><br>Year: %{{text}}<br>Urbanization Rate: %{{x:.1f}}%<br>GDP per Capita: %{{y:,.0f}} PPP$<extra></extra>',
                        text=merged['Year']
                    ) )
            # Main country
            if selected_country and selected_country in countries_dict:
                plot_country(selected_country, countries_dict[selected_country], '#295e84')
            else:
                raise Exception("No country selected")
            # Country benchmarks
            if benchmark_countries:
                palette = ['#e74c3c', '#f39c12', '#27ae60', '#3498db', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
                for i, iso in enumerate(benchmark_countries):
                    if iso in countries_dict:
                        plot_country(iso, countries_dict[iso], palette[i % len(palette)], dash='dot')
            # Global benchmarks
            if global_benchmarks:
                # Use actual data from processed WDI files for global regions
                for region_code in global_benchmarks:
                    if region_code in global_colors:
                        # Get urbanization and GDP data for the region
                        urb_region = urb_df[urb_df['Country Code'] == region_code].sort_values('Year')
                        gdp_region = gdp_df[gdp_df['Country Code'] == region_code].sort_values('Year')
                        merged_region = pd.merge(urb_region, gdp_region, on=['Country Code', 'Year'], suffixes=('_urb', '_gdp'))
                        if not merged_region.empty:
                            fig.add_trace(go.Scatter(
                                x=merged_region['Value_urb'],
                                y=merged_region['Value_gdp'],
                                mode='lines',
                                name=f"{global_names[region_code]}",
                                line=dict(color=global_colors[region_code], width=2, dash='dash'),
                                marker=dict(size=4, color=global_colors[region_code]),
                                hovertemplate=f'<b>{global_names[region_code]}</b><br>Year: %{{text}}<br>Urbanization Rate: %{{x:.1f}}%<br>GDP per Capita: %{{y:,.0f}} PPP$<extra></extra>',
                                text=merged_region['Year']
                            ))
            fig.update_layout(
                title=f'<b>{title_suffix}</b> | GDP per Capita vs Urbanization Rate',
                xaxis_title='Urbanization Rate (% of Population)',
                yaxis_title='GDP per Capita<br>(PPP, constant 2017 international $)',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                title_font_size=16,
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=0.98,
                    xanchor="right",
                    x=1
                ),
                yaxis=dict(
                    range=[0, None],
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='#e5e7eb'
                ),
                xaxis=dict(
                    range=[0, 100],
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=False,
                    ticksuffix='%'
                ),
                margin=dict(b=80, t=100)
            )
            return fig, {'display': 'block'}
        except Exception as e:
            # Return error chart
            return create_simple_error_message(str(e))
    
    # Register download callback using the reusable helper
    create_multi_csv_download_callback(
        app,
        'gdp-vs-urbanization-download',
        lambda: {
            f'gdp_per_capita_{GDP_INDICATOR}': gdp_df,
            f'urbanization_rate_{URBAN_INDICATOR}': urb_df
        },
        'gdp_urbanization'
    )
