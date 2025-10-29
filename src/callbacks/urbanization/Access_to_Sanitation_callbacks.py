"""
Callbacks for Access to Sanitation visualization
Shows stacked area chart of urban sanitation access categories over time for selected country
Data from JMP WASH database: At least basic, Limited, Unimproved, Open defecation
"""

from dash import Input, Output
import plotly.graph_objects as go
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ...utils.data_loader import load_jmp_sanitation_data
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.component_helpers import create_simple_error_message
    from ...utils.download_helpers import prepare_csv_download, create_simple_download_callback
    from config.settings import CHART_STYLES
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_jmp_sanitation_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.component_helpers import create_simple_error_message
    from src.utils.download_helpers import prepare_csv_download
    from config.settings import CHART_STYLES


def register_access_to_sanitation_callbacks(app):
    """Register callbacks for Access to Sanitation chart"""
    
    # Load static data once at registration time for performance
    sanitation_data = load_jmp_sanitation_data()
    countries_dict = load_subsaharan_countries_and_regions_dict()

    @app.callback(
        [Output('access-to-sanitation-chart', 'figure'),
         Output('access-to-sanitation-chart', 'style')],
        [Input('main-country-filter', 'value')],
        prevent_initial_call=False
    )
    def generate_access_to_sanitation_chart(selected_country):
        """Generate stacked area chart showing sanitation access categories over time"""
        try:
            # Load JMP sanitation data (pre-loaded)

            # Load country mapping for ISO code to full name conversion (pre-loaded)

            if sanitation_data.empty:
                raise Exception("No data available")

            # Filter for selected country
            if selected_country and selected_country in sanitation_data['Country Code'].values:
                country_data = sanitation_data[sanitation_data['Country Code'] == selected_country].copy()

                if country_data.empty:
                    raise Exception(f"No data available for selected country")

                country_name = countries_dict.get(selected_country, selected_country)
            else:
                raise Exception("No country selected")

            # Create the figure with stacked area chart
            fig = go.Figure()

            # Define sanitation access categories with colors (green gradient for better to worse)
            categories = [
                ('At least basic', '#10b981', 'At least basic sanitation service'),
                ('Limited (shared)', '#fbbf24', 'Limited (shared) sanitation service'),
                ('Unimproved', '#fb923c', 'Unimproved sanitation facility'),
                ('Open defecation', '#ef4444', 'Open defecation')
            ]

            # Add traces in order (bottom to top) - filter long format data for each indicator
            for indicator_name, color, hover_name in categories:
                indicator_data = country_data[country_data['Indicator'] == indicator_name].copy()
                indicator_data = indicator_data.sort_values('Year')

                if not indicator_data.empty:
                    fig.add_trace(go.Scatter(
                        x=indicator_data['Year'],
                        y=indicator_data['Value'],
                        mode='lines',
                        name=indicator_name,
                        line=dict(width=0.5, color=color),
                        fillcolor=color,
                        fill='tonexty' if fig.data else 'tozeroy',
                        stackgroup='one',
                        hovertemplate=f'<b>{hover_name}</b><br>Percentage: %{{y:.0%}}<extra></extra>'
                    ))

            # Update layout
            fig.update_layout(
                title=f'<b>{country_name}</b> | Access to Sanitation, Urban (% of Urban Population)<br>',
                xaxis_title='Year',
                yaxis_title='Access to Sanitation<br>(% of Urban Population)',
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
                    range=[0, 1],
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=True,
                    zerolinewidth=1,
                    zerolinecolor='#e5e7eb',
                    tickformat=".0%",
                    ticksuffix=''
                ),
                xaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#e5e7eb',
                    zeroline=False
                ),
                margin=dict(b=80, t=100),
                hovermode='x unified'
            )

            return fig, {'display': 'block'}

        except Exception as e:
            return create_simple_error_message(str(e))

    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'access-to-sanitation-download',
        lambda: sanitation_data,
        'access_to_sanitation_urban'
    )