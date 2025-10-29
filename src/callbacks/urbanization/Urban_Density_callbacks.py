"""
Callbacks for Built-up per capita visualization
Shows line chart of built-up area per person (m² per capita) in cities
"""

from dash import Input, Output
import plotly.graph_objects as go
import pandas as pd

try:
    from ...utils.data_loader import load_urban_density_data
    from ...utils.country_utils import (
        load_subsaharan_countries_and_regions_dict,
        load_wb_regional_classifications,
        load_subsaharan_countries_dict,
    )
    from ...utils.benchmark_config import get_benchmark_colors, get_benchmark_names
    from ...utils.component_helpers import create_simple_error_message
    from ...utils.download_helpers import prepare_csv_download, create_simple_download_callback
    from config.settings import CHART_STYLES
except ImportError:
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_urban_density_data
    from src.utils.country_utils import (
        load_subsaharan_countries_and_regions_dict,
        load_wb_regional_classifications,
        load_subsaharan_countries_dict,
    )
    from src.utils.benchmark_config import get_benchmark_colors, get_benchmark_names
    from src.utils.component_helpers import create_simple_error_message
    from src.utils.download_helpers import prepare_csv_download, create_simple_download_callback
    from config.settings import CHART_STYLES


def register_urban_density_callbacks(app):
    """Register callbacks for Built-up per capita chart"""

    density_data_cache = load_urban_density_data()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    individual_countries = load_subsaharan_countries_dict()
    benchmark_colors = get_benchmark_colors()
    benchmark_names = get_benchmark_names()

    afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()
    region_country_map = {
        'AFE': afe_countries,
        'AFW': afw_countries,
        'SSA': ssa_countries,
    }

    def compute_series_for_code(code: str) -> pd.DataFrame:
        """Return a dataframe with year and built_up_per_capita_m2 for a country or region code"""
        if code in region_country_map:
            region_countries = region_country_map[code]
            region_subset = density_data_cache[density_data_cache['ISO3'].isin(region_countries)].copy()
            if region_subset.empty:
                return region_subset[['year', 'built_up_per_capita_m2']]
            aggregated = (
                region_subset.groupby('year', as_index=False)
                .agg({'population': 'sum', 'built_up_km2': 'sum'})
            )
            aggregated = aggregated[aggregated['built_up_km2'] > 0]
            aggregated['built_up_per_capita_m2'] = (aggregated['built_up_km2'] / aggregated['population']) * 1000000
            return aggregated[['year', 'built_up_per_capita_m2']]

        subset = density_data_cache[density_data_cache['ISO3'] == code].copy()
        return subset[['year', 'built_up_per_capita_m2']]

    @app.callback(
        [Output('urban-density-chart', 'figure'),
         Output('urban-density-chart', 'style')],
        [
            Input('main-country-filter', 'value'),
            Input('urban-density-combined-benchmark-selector', 'value'),
        ],
        prevent_initial_call=False,
    )
    def generate_urban_density_chart(selected_country, selected_benchmarks):
        try:
            if not selected_country:
                raise Exception("No country selected")

            country_name = countries_dict.get(selected_country, selected_country)

            main_series = compute_series_for_code(selected_country)
            if main_series.empty:
                raise Exception(
                    f"No built-up per capita data available for {country_name}"
                )

            main_series = main_series.sort_values('year')
            fig = go.Figure()

            # Main line
            fig.add_trace(
                go.Scatter(
                    x=main_series['year'],
                    y=main_series['built_up_per_capita_m2'],
                    mode='lines+markers',
                    name=country_name,
                    line=dict(color=CHART_STYLES['colors']['info'], width=3),
                    marker=dict(size=6),
                    hovertemplate=f'<b>{country_name}</b><br>Built-up per capita: %{{y:.2f}} m²/person<extra></extra>'
                )
            )

            # Benchmarks
            selected_benchmarks = selected_benchmarks or []
            benchmark_line_styles = ['dash', 'dot', 'dashdot', 'solid']
            default_benchmark_color = CHART_STYLES['colors']['secondary']

            for idx, benchmark_code in enumerate(selected_benchmarks):
                benchmark_series = compute_series_for_code(benchmark_code)
                if benchmark_series.empty:
                    continue

                benchmark_series = benchmark_series.sort_values('year')
                line_color = benchmark_colors.get(benchmark_code, default_benchmark_color)
                display_name = countries_dict.get(benchmark_code) or benchmark_names.get(benchmark_code) or individual_countries.get(benchmark_code, benchmark_code)

                fig.add_trace(
                    go.Scatter(
                        x=benchmark_series['year'],
                        y=benchmark_series['built_up_per_capita_m2'],
                        mode='lines+markers',
                        name=display_name,
                        line=dict(
                            color=line_color,
                            width=2,
                            dash=benchmark_line_styles[idx % len(benchmark_line_styles)],
                        ),
                        marker=dict(size=5),
                        hovertemplate=f'<b>{display_name}</b><br>Built-up per capita: %{{y:.2f}} m²/person<extra></extra>'
                    )
                )

            country_name = countries_dict.get(selected_country, selected_country)
            
            fig.update_layout(
                title=f'<b>{country_name}</b> | Built-up per capita in Cities',
                xaxis=dict(
                    title='Year',
                    showgrid=True,
                    gridcolor='#e2e8f0',
                    zeroline=False,
                ),
                yaxis=dict(
                    title='Built-up per capita (m²/person)',
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
                hovermode='x unified',
                height=600,
            )

            return fig, {'display': 'block'}

        except Exception as e:
            return create_simple_error_message(str(e))

    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'urban-density-download',
        lambda: density_data_cache,
        'built_up_per_capita_cities'
    )
