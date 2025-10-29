"""
Callbacks for Access to Drinking Water visualization
Shows stacked area chart of urban drinking water access categories over time for selected country
Data from JMP WASH database: At least basic, Limited (>30 mins), Unimproved, Surface water
"""

from dash import Input, Output, html
import plotly.graph_objects as go


from ...utils.data_loader import load_jmp_water_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def register_access_to_drinking_water_callbacks(app):
    """Register callbacks for Access to Drinking Water chart"""
    
    # Load static data once at registration time for performance
    water_data = load_jmp_water_data()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        [Output('access-to-drinking-water-chart', 'figure'),
         Output('access-to-drinking-water-chart', 'style'),
         Output('access-to-drinking-water-title', 'children')],
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def generate_access_to_drinking_water_chart(selected_country):
        """Generate stacked area chart showing drinking water access categories over time"""
        try:
            if not selected_country:
                raise Exception("No country selected")
            
            if water_data.empty:
                raise Exception("No data available")
            
            # Filter for selected country
            if selected_country and selected_country in water_data['Country Code'].values:
                country_data = water_data[water_data['Country Code'] == selected_country].copy()
                
                if country_data.empty:
                    raise Exception(f"No data available for selected country")
                
                country_name = countries_dict.get(selected_country, selected_country)
            else:
                raise Exception(f"No data available for selected country")
            
            # Create the figure with stacked area chart
            fig = go.Figure()
            
            # Define water access categories with colors (green gradient for better to worse)
            categories = [
                ('At least basic', '#10b981', 'At least basic water service'),
                ('Limited (more than 30 mins)', '#fbbf24', 'Limited service (>30 mins)'),
                ('Unimproved', '#fb923c', 'Unimproved water source'),
                ('Surface water', '#ef4444', 'Surface water')
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
            
            # Create separate title
            title_text = html.H6([html.B(country_name), ' | Access to Drinking Water, Urban (% of Urban Population)'], 
                                className='chart-title')
            
            # Update layout
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Access to Drinking Water<br>(% of Urban Population)',
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

            return fig, {'display': 'block'}, title_text
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'access-to-drinking-water-download',
        lambda: water_data,
        'access_to_drinking_water_urban'
    )
