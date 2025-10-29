"""
Callbacks for disaster affected population visualization - "Total Affected Population" subtab
Shows stacked bar chart of total affected population by disaster type in 5-year intervals for selected country
"""

from dash import Input, Output, html
import plotly.express as px
import pandas as pd

from ...utils.data_loader import load_emdat_data, load_population_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.color_utils import DISASTER_COLORS
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import DATA_CONFIG


def setup_total_affected_population_callbacks(app):
    """Setup callbacks for the 'Total Affected Population' disaster chart"""
    
    @app.callback(
        [Output('disaster-affected-chart', 'figure'),
         Output('disaster-affected-chart', 'style'),
         Output('disaster-affected-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('disaster-affected-mode-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_total_affected_population_chart(selected_country, display_mode):
        """Generate stacked bar chart showing total affected population by year (absolute or relative)"""
        try:
            # Load real EM-DAT data
            emdat_data = load_emdat_data()
            
            # Load country and region mapping for ISO code to full name conversion
            countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
            
            # Filter data based on country input only
            if selected_country and 'ISO' in emdat_data.columns:
                emdat_data = emdat_data[emdat_data['ISO'] == selected_country].copy()
            
            # Check if data is available
            if emdat_data.empty:
                raise Exception("No data available for selected country")
            else:
                # Group by year and disaster type, sum affected population
                affected_data = emdat_data.groupby(['Year', 'Disaster Type'])['Total Affected'].sum().reset_index()
                
                # Create complete year range from start year to end year
                start_year = DATA_CONFIG['emdat_start_year']
                end_year = DATA_CONFIG['emdat_end_year']
                all_years = pd.DataFrame({'Year': range(start_year, end_year + 1)})
                
                # Get all disaster types
                all_disaster_types = affected_data['Disaster Type'].unique()
                
                # Create all combinations of years and disaster types
                year_disaster_combinations = pd.MultiIndex.from_product(
                    [all_years['Year'], all_disaster_types],
                    names=['Year', 'Disaster Type']
                ).to_frame(index=False)
                
                # Merge with actual data to include years with no disasters
                affected_data = year_disaster_combinations.merge(
                    affected_data, 
                    on=['Year', 'Disaster Type'], 
                    how='left'
                ).fillna(0)
                
                # If relative mode, normalize by population
                if display_mode == 'relative':
                    try:
                        if not selected_country:
                            raise Exception("No country selected")

                        # Load population data for selected country
                        pop_data = load_population_data(selected_country)
                        
                        # Merge with affected data
                        affected_data = affected_data.merge(pop_data, left_on='Year', right_on='Year', how='left')
                        
                        # Check if population data is available for all years
                        if affected_data['population'].isna().any():
                            raise Exception("Population data not available for all years. Relative chart not available.")
                        
                        # Calculate percentage of population affected
                        affected_data['Total Affected'] = (affected_data['Total Affected'] / affected_data['population']) * 100
                        
                    except Exception as e:
                        return create_simple_error_message(str(e))
                
                # Sort by year in ascending order
                affected_data = affected_data.sort_values('Year')
                
                # Convert year to string for plotting
                affected_data['Year'] = affected_data['Year'].astype(str)
                
                # Map ISO code to full country/region name
                if selected_country:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    title_suffix = f"{country_name}"
                else:
                    raise Exception("No country selected")
                    
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
        
        # Set labels based on display mode
        if display_mode == 'relative':
            y_label = 'Total Affected (% of population)'
            chart_title = html.H6([
                html.B(title_suffix),
                f' | Total Affected Population by Year - Relative ({DATA_CONFIG["analysis_period"]})'
            ], className='chart-title')
            hover_format = '%{y:.2f}%'
        else:
            y_label = 'Total Affected Population'
            chart_title = html.H6([
                html.B(title_suffix),
                f' | Total Affected Population by Year ({DATA_CONFIG["analysis_period"]})'
            ], className='chart-title')
            hover_format = '%{y:,.0f}'
        
        # Create stacked bar chart with disaster type colors
        fig = px.bar(
            affected_data,
            x='Year',
            y='Total Affected',
            color='Disaster Type',
            labels={'Total Affected': y_label, 'Year': 'Year'},
            color_discrete_map=DISASTER_COLORS,
            category_orders={'Year': sorted(affected_data['Year'].unique())}
        )
        
        # Update layout styling
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            showlegend=True,
            legend=dict(
                orientation="v",
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.02
            ),
            xaxis=dict(
                showgrid=False,
                gridwidth=0,
                gridcolor='#e5e7eb',
                tickangle=-45,
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                dtick=1 if affected_data['Total Affected'].max() <= 10 else None,
                rangemode='tozero',
                showgrid=True,
                gridwidth=1,
                gridcolor='#e5e7eb',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='#e5e7eb',
                title=y_label,
                ticksuffix='%' if display_mode == 'relative' else '',
                range=[0, max(affected_data['Total Affected'].max() * 1.1, 0.01)] if display_mode == 'relative' else None
            ),
            margin=dict(b=100, r=150)  # Extra margin for legend
        )
        
        # Update bar styling with appropriate hover template
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            hovertemplate=f'<b>%{{fullData.name}}</b><br>Year: %{{x}}<br>Affected: {hover_format}<extra></extra>'
        )
        
        return fig, {'display': 'block'}, chart_title
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'disaster-affected-download',
        lambda: load_emdat_data(),
        'african_disasters_emdat'
    )
    
    
