"""
Callbacks for disaster timeline visualization - "Disasters by Year" subtab
Shows stacked bar chart of disaster events grouped by 5-year intervals for selected country
"""

from dash import Input, Output, html
import plotly.express as px
import pandas as pd

from ...utils.data_loader import load_emdat_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.color_utils import DISASTER_COLORS
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import DATA_CONFIG


def setup_disasters_by_year_callbacks(app):
    """Setup callbacks for the 'Disasters by Year' timeline chart"""
    
    @app.callback(
        [Output('disaster-timeline-chart', 'figure'),
         Output('disaster-timeline-chart', 'style'),
         Output('disaster-timeline-title', 'children')],
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def generate_disasters_by_year_timeline_chart(selected_country):
        """Generate stacked bar chart showing disasters by 5-year intervals since configured start year"""
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
                # Group by year and disaster type using the 'Number of Events' column
                timeline_data = emdat_data.groupby(['Year', 'Disaster Type'])['Number of Events'].sum().reset_index(name='Event Count')
                
                # Create complete year range from start year to 2024
                start_year = DATA_CONFIG['emdat_start_year']
                end_year = DATA_CONFIG['emdat_end_year']
                all_years = pd.DataFrame({'Year': range(start_year, end_year + 1)})
                
                # Get all disaster types
                all_disaster_types = timeline_data['Disaster Type'].unique()
                
                # Create all combinations of years and disaster types
                year_disaster_combinations = pd.MultiIndex.from_product(
                    [all_years['Year'], all_disaster_types],
                    names=['Year', 'Disaster Type']
                ).to_frame(index=False)
                
                # Merge with actual data to include years with no disasters
                timeline_data = year_disaster_combinations.merge(
                    timeline_data, 
                    on=['Year', 'Disaster Type'], 
                    how='left'
                ).fillna(0)
                
                # Sort by year in ascending order
                timeline_data = timeline_data.sort_values('Year')
                
                # Convert year to string for plotting
                timeline_data['Year'] = timeline_data['Year'].astype(str)
                
                # Map ISO code to full country/region name
                if selected_country:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    title_suffix = f"{country_name}"
                else:
                    raise Exception("No country selected")
                    
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, ""
        
        # Create stacked bar chart with disaster type colors
        fig = px.bar(
            timeline_data,
            x='Year',
            y='Event Count',
            color='Disaster Type',
            labels={'Event Count': 'Number of Events', 'Year': 'Year'},
            color_discrete_map=DISASTER_COLORS,
            category_orders={'Year': sorted(timeline_data['Year'].unique())}
        )
        
        # Create title separately
        chart_title = html.H6([
            html.B(title_suffix),
            f' | Number of Disasters by Year ({DATA_CONFIG["analysis_period"]})'
        ], className='chart-title')
        
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
                dtick=1 if timeline_data['Event Count'].max() <= 10 else None,
                rangemode='tozero',
                showgrid=True,
                gridwidth=1,
                gridcolor='#e5e7eb',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='#e5e7eb'
            ),
            margin=dict(b=0, r=150)  # Extra margin for legend
        )
        
        # Update bar styling
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            hovertemplate='<b>%{fullData.name}</b><br>Period: %{x}<br>Events: %{y}<extra></extra>'
        )
        
        return fig, {'display': 'block'}, chart_title
    
    # Register download callback using the reusable helper
    create_simple_download_callback(
        app,
        'disaster-timeline-download',
        lambda: load_emdat_data(),
        'african_disasters_emdat'
    )