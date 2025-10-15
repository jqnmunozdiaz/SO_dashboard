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
    from config.settings import CHART_STYLES
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_wdi_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_error_chart
    from config.settings import CHART_STYLES

GDP_INDICATOR = "NY.GDP.PCAP.PP.KD"
URBAN_INDICATOR = "SP.URB.TOTL.IN.ZS"

def register_gdp_vs_urbanization_callbacks(app):
    """Register callbacks for GDP vs Urbanization chart"""
    @app.callback(
        Output('gdp-vs-urbanization-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('gdp-vs-urbanization-country-benchmark-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_gdp_vs_urbanization_chart(selected_country, benchmark_countries):
        try:            
            # Load data for both indicators
            gdp_df = load_wdi_data(GDP_INDICATOR)
            urb_df = load_wdi_data(URBAN_INDICATOR)
            
            # Handle no country selected case
            countries_dict = load_subsaharan_countries_and_regions_dict()
            title_suffix = countries_dict.get(selected_country, "No country selected") if selected_country else "No country selected"

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
            # Country benchmarks
            if benchmark_countries:
                palette = ['#e74c3c', '#f39c12', '#27ae60', '#3498db', '#9b59b6', '#1abc9c', '#34495e', '#e67e22']
                for i, iso in enumerate(benchmark_countries):
                    if iso in countries_dict:
                        plot_country(iso, countries_dict[iso], palette[i % len(palette)], dash='dot')
            fig.update_layout(
                title=f'<b>{title_suffix}</b> | GDP per Capita vs Urbanization Rate<br><sub>Data Source: World Bank WDI</sub>',
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
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='#e5e7eb'
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
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='scatter',
                xaxis_title='Urbanization Rate (% of Population)',
                yaxis_title='GDP per Capita (PPP, constant 2017 international $)',
                title='GDP per Capita vs Urbanization Rate'
            )
