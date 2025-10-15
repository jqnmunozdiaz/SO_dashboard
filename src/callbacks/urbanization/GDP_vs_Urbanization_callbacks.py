"""
Callbacks for GDP vs Urbanization scatterplot visualization
Shows scatterplot of GDP per capita (y) vs Urbanization Rate (x) for selected country and country benchmarks
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ...utils.data_loader import load_wdi_data
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_error_chart
    from ...utils.GLOBAL_BENCHMARK_CONFIG import get_global_benchmark_colors, get_global_benchmark_names
    from config.settings import CHART_STYLES
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_wdi_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from src.utils.GLOBAL_BENCHMARK_CONFIG import get_global_benchmark_colors, get_global_benchmark_names
    from config.settings import CHART_STYLES

GDP_INDICATOR = "NY.GDP.PCAP.PP.KD"
URBAN_INDICATOR = "SP.URB.TOTL.IN.ZS"

def register_gdp_vs_urbanization_callbacks(app):
    """Register callbacks for GDP vs Urbanization chart"""
    @app.callback(
        Output('gdp-vs-urbanization-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('gdp-vs-urbanization-country-benchmark-selector', 'value'),
         Input('gdp-vs-urbanization-global-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_gdp_vs_urbanization_chart(selected_country, benchmark_countries, global_benchmarks):
        try:            
            # Load data for both indicators
            gdp_df = load_wdi_data(GDP_INDICATOR)
            urb_df = load_wdi_data(URBAN_INDICATOR)
            
            # Handle no country selected case
            countries_dict = load_subsaharan_countries_and_regions_dict()
            
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
                        mode='markers+lines',
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
                global_colors = get_global_benchmark_colors()
                global_names = get_global_benchmark_names()
                # Define sample regional development paths (urbanization %, GDP per capita PPP)
                regional_paths = {
                    'SSA': ([25, 35, 45, 55], [1500, 2200, 3200, 4500]),  # Sub-Saharan Africa
                    'AFE': ([20, 30, 42, 52], [1400, 2000, 3000, 4200]),  # Eastern/Southern Africa
                    'AFW': ([30, 40, 48, 58], [1600, 2400, 3400, 4800]),  # Western/Central Africa
                    'EAP': ([35, 50, 65, 75], [3000, 6000, 12000, 18000]),  # East Asia & Pacific
                    'ECA': ([55, 65, 70, 75], [8000, 12000, 16000, 20000]),  # Europe & Central Asia
                    'LCR': ([65, 75, 80, 82], [6000, 9000, 13000, 15000]),  # Latin America & Caribbean
                    'MNA': ([60, 70, 75, 78], [5000, 8000, 11000, 13000]),  # Middle East & North Africa
                    'SAR': ([30, 35, 40, 45], [1800, 2500, 3500, 5000])   # South Asia
                }
                for region_code in global_benchmarks:
                    if region_code in global_colors and region_code in regional_paths:
                        urb_values, gdp_values = regional_paths[region_code]
                        region_name = global_names[region_code]
                        fig.add_trace(go.Scatter(
                            x=urb_values,
                            y=gdp_values,
                            mode='markers+lines',
                            name=f"{region_code}",
                            line=dict(color=global_colors[region_code], width=2, dash='dash'),
                            marker=dict(size=4, color=global_colors[region_code]),
                            hovertemplate=f'<b>{region_name} (Global Benchmark)</b><br>Urbanization Rate: %{{x:.1f}}%<br>GDP per Capita: %{{y:,.0f}} PPP$<extra></extra>'
                        ))
            fig.update_layout(
                title=f'<b>{title_suffix}</b> | GDP per Capita vs Urbanization Rate',
                xaxis_title='Urbanization Rate (% of Population)',
                yaxis_title='GDP per Capita (PPP, constant 2017 international $)',
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
                    range=[0, None],
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='#e5e7eb'
                ),
                xaxis=dict(
                    range=[0, None],
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
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='scatter',
                xaxis_title='Urbanization Rate (% of Population)',
                yaxis_title='GDP per Capita (PPP, constant 2017 international $)',
                yaxis_range=[0, None],
                title='GDP per Capita vs Urbanization Rate'
            )
