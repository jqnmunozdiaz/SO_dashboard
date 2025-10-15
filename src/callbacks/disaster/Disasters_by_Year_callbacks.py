"""
Callbacks for disaster timeline visualization - "Disasters by Year" subtab
Shows stacked bar chart of disaster events grouped by 5-year intervals for selected country
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
    from ...utils.component_helpers import create_error_chart
    from config.settings import DATA_CONFIG
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_emdat_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.color_utils import DISASTER_COLORS
    from src.utils.component_helpers import create_error_chart
    from config.settings import DATA_CONFIG


def setup_disasters_by_year_callbacks(app):
    """Setup callbacks for the 'Disasters by Year' timeline chart"""
    
    @app.callback(
        Output('disaster-timeline-chart', 'figure'),
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
                emdat_data = emdat_data[emdat_data['ISO'] == selected_country]
            
            # Create 5-year intervals starting from 1975
            if emdat_data.empty:
                raise Exception("No data available for selected country")
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
                
                # Group by interval and disaster type using the 'Number of Events' column
                timeline_data = emdat_data.groupby(['Year_Interval', 'Disaster Type'])['Number of Events'].sum().reset_index(name='Event Count')
                
                # Convert interval to string for plotting
                timeline_data['Year_Interval'] = timeline_data['Year_Interval'].astype(str)
                
                # Map ISO code to full country/region name
                if selected_country:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    title_suffix = f"{country_name}"
                else:
                    raise Exception("No country selected")
                    
        except Exception as e:
            # Return error chart
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='bar',
                xaxis_title='5-Year Interval',
                yaxis_title='Number of Events',
                title='Disasters by Year'
            )
        
        # Create stacked bar chart with disaster type colors
        fig = px.bar(
            timeline_data,
            x='Year_Interval',
            y='Event Count',
            color='Disaster Type',
            title=f'<b>{title_suffix}</b> | Number of Disasters by 5-Year Intervals ({DATA_CONFIG["analysis_period"]})',
            labels={'Event Count': 'Number of Events', 'Year_Interval': '5-Year Interval'},
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
                tickvals=timeline_data['Year_Interval'].unique(),
                ticktext=[interval.replace('-', ' -<br>') for interval in timeline_data['Year_Interval'].unique()],
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
            margin=dict(b=100, r=150)  # Extra margin for legend
        )
        
        # Update bar styling
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            hovertemplate='<b>%{fullData.name}</b><br>Period: %{x}<br>Events: %{y}<extra></extra>'
        )
        
        return fig