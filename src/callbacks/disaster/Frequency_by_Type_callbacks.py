"""
Callbacks for disaster frequency visualization - "Frequency by Type" subtab
Shows bar chart of disaster event counts grouped by disaster type for selected country
"""

from dash import Input, Output
import plotly.express as px
import pandas as pd
import warnings
import textwrap

# Suppress pandas future warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

try:
    from ...utils.data_loader import load_emdat_data
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.color_utils import get_disaster_color, DISASTER_COLORS
    from ...utils.component_helpers import create_error_chart
    from ...utils.download_helpers import prepare_csv_download
    from config.settings import DATA_CONFIG
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_emdat_data
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.color_utils import get_disaster_color, DISASTER_COLORS
    from src.utils.component_helpers import create_error_chart
    from src.utils.download_helpers import prepare_csv_download
    from config.settings import DATA_CONFIG


def wrap_text(text, width=15):
    """Wrap text to specified width with line breaks"""
    if pd.isna(text) or text == '':
        return text
    return '<br>'.join(textwrap.wrap(str(text), width=width))


def setup_frequency_by_type_callbacks(app):
    """Setup callbacks for the 'Frequency by Type' disaster chart"""
    
    @app.callback(
        Output('disaster-frequency-chart', 'figure'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def generate_disaster_frequency_by_type_chart(selected_country):
        """Generate bar chart showing frequency of historical disasters by disaster type since configured start year"""
        try:
            # Load real EM-DAT data
            emdat_data = load_emdat_data()
            
            # Load country and region mapping for ISO code to full name conversion
            countries_and_regions_dict = load_subsaharan_countries_and_regions_dict()
            
            # Filter data based on country input only
            if selected_country and 'ISO' in emdat_data.columns:
                emdat_data = emdat_data[emdat_data['ISO'] == selected_country].copy()
            
            # Count frequency by disaster type using the 'Number of Events' column
            if emdat_data.empty:
                raise Exception("No data available for selected country")
            else:
                frequency_data = emdat_data.groupby('Disaster Type')['Number of Events'].sum().reset_index(name='Event Count')
                frequency_data = frequency_data.sort_values('Event Count', ascending=False)
                
                # Add wrapped labels for display
                frequency_data['Disaster Type Wrapped'] = frequency_data['Disaster Type'].apply(wrap_text)
                
                # Add colors for each disaster type
                frequency_data['Color'] = frequency_data['Disaster Type'].apply(
                    lambda x: get_disaster_color(x, DISASTER_COLORS)
                )
                
                # Create title with country/region info - map ISO code to full name
                if selected_country:
                    country_name = countries_and_regions_dict.get(selected_country, selected_country)
                    title_suffix = f"{country_name}"
                else:
                    raise Exception("No country selected")
                
        except Exception as e:
            # Return error chart using shared utility
            return create_error_chart(
                error_message=f"Error loading data: {str(e)}",
                chart_type='bar',
                xaxis_title='Disaster Type',
                yaxis_title='Number of Events',
                title='Frequency of Disasters by Type'
            )
        
        # Create bar chart with custom colors
        fig = px.bar(
            frequency_data,
            x='Disaster Type Wrapped',
            y='Event Count',
            title=f'<b>{title_suffix}</b> | Frequency of Disasters by Type ({DATA_CONFIG["analysis_period"]})',
            labels={'Event Count': 'Number of Events', 'Disaster Type Wrapped': 'Disaster Type'},
            color='Disaster Type',
            color_discrete_map={
            row['Disaster Type']: row['Color'] 
            for _, row in frequency_data.iterrows()
            }
        )
        
        # Update layout styling
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
            xaxis_tickangle=0,
            showlegend=False,
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(len(frequency_data))),
                ticktext=frequency_data['Disaster Type Wrapped'].tolist()
            ),
            yaxis=dict(
                dtick=1 if frequency_data['Event Count'].max() <= 10 else None,
                rangemode='tozero',
                showgrid=True,
                gridwidth=1,
                gridcolor='#e5e7eb',
                zeroline=True,
                zerolinewidth=1,
                zerolinecolor='#e5e7eb'
            ),
            margin=dict(b=100)
        )
        
        # Update bar styling
        fig.update_traces(
            marker_line_color='white',
            marker_line_width=0.5,
            hovertemplate='<b>%{customdata}</b><br>Events: %{y}<extra></extra>',
            customdata=frequency_data['Disaster Type']
        )
        
        return fig
    
    @app.callback(
        Output('disaster-frequency-download', 'data'),
        Input('disaster-frequency-download-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_disaster_frequency_data(n_clicks):
        """Download EM-DAT disaster data as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            # Load full dataset (raw data, no filtering)
            emdat_data = load_emdat_data()
            
            filename = "african_disasters_emdat"
            
            return prepare_csv_download(emdat_data, filename)
        
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None