"""
Callbacks for disaster affected population visualization - "Total Affected Population" subtab
Shows stacked bar chart of total affected population by disaster type in 5-year intervals for selected country
"""

from dash import Input, Output
import plotly.express as px
import pandas as pd
import warnings

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ...utils.data_loader import load_emdat_data
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.color_utils import DISASTER_COLORS
    from config.settings import DATA_CONFIG
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_emdat_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.color_utils import DISASTER_COLORS
    from config.settings import DATA_CONFIG


def setup_total_affected_population_callbacks(app):
    """Setup callbacks for the 'Total Affected Population' disaster chart"""
    
    @app.callback(
        Output('disaster-affected-chart', 'figure'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def generate_total_affected_population_chart(selected_country):
        """Generate stacked bar chart showing total affected population by 5-year intervals since configured start year"""
        try:
            # Load real EM-DAT data
            emdat_data = load_emdat_data()
            
            # Load country and region mapping for ISO code to full name conversion
            countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
            
            # Filter data based on country input only
            if selected_country and 'ISO' in emdat_data.columns:
                emdat_data = emdat_data[emdat_data['ISO'] == selected_country]
            
            # Create 5-year intervals starting from configured year
            if emdat_data.empty:
                # Create empty data structure
                affected_data = pd.DataFrame({
                    'Year_Interval': ['1975-1979'],
                    'Disaster Type': ['No Data'],
                    'Total Affected': [0]
                })
                title_suffix = "No data available for selected country"
            else:
                # Create 5-year interval bins starting from configured year
                start_year = DATA_CONFIG['emdat_start_year']
                emdat_data['Year_Interval'] = pd.cut(
                    emdat_data['Year'],
                    bins=range(start_year, 2030, 5),
                    labels=[f"{year}-{year+4}" for year in range(start_year, 2025, 5)],
                    include_lowest=True,
                    right=False
                )
                
                # Group by interval and disaster type, sum affected population
                affected_data = emdat_data.groupby(['Year_Interval', 'Disaster Type'])['Total Affected'].sum().reset_index()
                
                # Convert interval to string for plotting
                affected_data['Year_Interval'] = affected_data['Year_Interval'].astype(str)
                
                # Map ISO code to full country/region name
                if selected_country:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    title_suffix = f"{country_name}"
                else:
                    raise ValueError("No country selected")
                    
        except Exception as e:
            # Return empty data on error
            affected_data = pd.DataFrame({
                'Year_Interval': ['1975-1979'],
                'Disaster Type': ['Error'],
                'Total Affected': [0]
            })
            title_suffix = f"Error loading data"
        
        # Create stacked bar chart with disaster type colors
        fig = px.bar(
            affected_data,
            x='Year_Interval',
            y='Total Affected',
            color='Disaster Type',
            title=f'<b>{title_suffix}</b> | Total Affected Population by 5-Year Intervals ({DATA_CONFIG["analysis_period"]})<br><sub>Data Source: EM-DAT</sub>',
            labels={'Total Affected': 'Total Affected Population', 'Year_Interval': '5-Year Interval'},
            color_discrete_map=DISASTER_COLORS
        )
        
        # Update layout styling
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
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
                tickmode='array',
                tickvals=affected_data['Year_Interval'].unique(),
                ticktext=[interval.replace('-', ' -<br>') for interval in affected_data['Year_Interval'].unique()],
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
                zerolinecolor='#e5e7eb'
            ),
            margin=dict(b=100, r=150)  # Extra margin for legend
        )
        
        # Update bar styling
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            hovertemplate='<b>%{fullData.name}</b><br>Period: %{x}<br>Affected: %{y:,.0f}<extra></extra>'
        )
        
        return fig
    
    
    