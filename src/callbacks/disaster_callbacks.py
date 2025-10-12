"""
Callbacks for historical disasters functionality
"""

from dash import Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

try:
    from ..utils.data_loader import load_disaster_data, create_sample_disaster_data, load_real_disaster_data
    from ..utils.chart_helpers import create_disaster_timeline, create_disaster_map
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from src.utils.data_loader import load_disaster_data, create_sample_disaster_data, load_real_disaster_data
    from src.utils.chart_helpers import create_disaster_timeline, create_disaster_map


def register_callbacks(app):
    """Register all disaster-related callbacks"""
    

    
    @app.callback(
        Output('disaster-type-dropdown', 'options'),
        Input('main-tabs', 'active_tab')
    )
    def update_disaster_type_options(active_tab):
        """Update disaster type dropdown options"""
        if active_tab == 'disasters':
            try:
                # Load real disaster data to get available disaster types
                disaster_data = load_real_disaster_data()
                if 'disaster_type' in disaster_data.columns:
                    # Get unique disaster types from real data
                    unique_types = disaster_data['disaster_type'].dropna().unique()
                    
                    # Create human-readable labels
                    type_labels = {
                        'flood': 'Flood',
                        'drought': 'Drought',
                        'storm': 'Storm',
                        'earthquake': 'Earthquake',
                        'wildfire': 'Wildfire',
                        'epidemic': 'Epidemic',
                        'volcanic': 'Volcanic Activity',
                        'extreme_temperature': 'Extreme Temperature',
                        'landslide': 'Landslide',
                        'other': 'Other'
                    }
                    
                    disaster_types = [
                        {'label': type_labels.get(dtype, dtype.title()), 'value': dtype}
                        for dtype in unique_types
                        if dtype and dtype != 'nan'
                    ]
                    
                    # Sort by label
                    disaster_types = sorted(disaster_types, key=lambda x: x['label'])
                    return disaster_types
                else:
                    raise ValueError("disaster_type column not found")
            except Exception as e:
                # Fallback disaster types
                disaster_types = [
                    {'label': 'Flood', 'value': 'flood'},
                    {'label': 'Drought', 'value': 'drought'},
                    {'label': 'Epidemic', 'value': 'epidemic'},
                    {'label': 'Storm', 'value': 'storm'},
                    {'label': 'Earthquake', 'value': 'earthquake'},
                    {'label': 'Wildfire', 'value': 'wildfire'},
                    {'label': 'Other', 'value': 'other'},
                ]
                return disaster_types
        return []
    
    @app.callback(
        Output('disaster-timeline-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('disaster-type-dropdown', 'value'),
         Input('disaster-year-slider', 'value')],
        prevent_initial_call=False
    )
    def update_disaster_timeline(selected_country, disaster_types, year_range):
        """Update disaster timeline chart"""
        # Load real EM-DAT data
        try:
            sample_data = load_real_disaster_data()
            
            # Ensure we have data
            if sample_data.empty:
                raise ValueError("No sample data available")
            
            # Make a copy to avoid modifying the original
            filtered_data = sample_data.copy()
            
            # Filter data based on inputs (with None checks)
            if selected_country and 'country_code' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['country_code'] == selected_country]
            
            if disaster_types and len(disaster_types) > 0 and 'disaster_type' in filtered_data.columns:
                filtered_data = filtered_data[filtered_data['disaster_type'].isin(disaster_types)]
            
            if year_range and len(year_range) == 2 and 'year' in filtered_data.columns:
                filtered_data = filtered_data[
                    (filtered_data['year'] >= year_range[0]) & 
                    (filtered_data['year'] <= year_range[1])
                ]
            
            # Check if we still have data after filtering
            if filtered_data.empty:
                agg_data = pd.DataFrame(columns=['year', 'country', 'disaster_count'])
            else:
                # Check which columns are available for aggregation
                if 'year' in filtered_data.columns and 'country' in filtered_data.columns:
                    # Count disasters per year/country combination
                    agg_data = filtered_data.groupby(['year', 'country']).size().reset_index(name='disaster_count')
                    
                    # Add additional metrics if available
                    if 'affected_population' in filtered_data.columns:
                        pop_agg = filtered_data.groupby(['year', 'country'])['affected_population'].sum().reset_index()
                        agg_data = agg_data.merge(pop_agg, on=['year', 'country'], how='left')
                    
                    if 'economic_damage_usd' in filtered_data.columns:
                        damage_agg = filtered_data.groupby(['year', 'country'])['economic_damage_usd'].sum().reset_index()
                        agg_data = agg_data.merge(damage_agg, on=['year', 'country'], how='left')
                        
                elif 'year' in filtered_data.columns:
                    # Aggregate by year only if country column is missing
                    disaster_counts = filtered_data.groupby('year').size().reset_index(name='disaster_count')
                    disaster_counts['country'] = 'All Selected Countries'
                    agg_data = disaster_counts
                else:
                    raise ValueError("Cannot create timeline without year data")
            
        except Exception as e:
            # Return empty data and show error message
            agg_data = pd.DataFrame(columns=['year', 'country', 'disaster_count'])
        
        # Handle empty data case
        if agg_data.empty:
            fig = go.Figure()
            fig.update_layout(
                title="No data available for selected filters<br><sub>Try different filter combinations</sub>",
                xaxis_title="Year",
                yaxis_title="Number of Disasters",
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': '#2c3e50'},
                title_font_size=16,
                yaxis=dict(
                    dtick=1,
                    rangemode='tozero'
                )
            )
            return fig
        
        # Create the line chart
        if 'country' in agg_data.columns and len(agg_data['country'].unique()) > 1:
            # Multiple countries - use color by country
            fig = px.line(
                agg_data, 
                x='year', 
                y='disaster_count', 
                color='country',
                title='Historical Disaster Trends in Africa<br><sub>Data Source: EM-DAT (Emergency Events Database)</sub>',
                labels={'disaster_count': 'Number of Disasters', 'year': 'Year'}
            )
        else:
            # Single country or no country column - simple line
            fig = px.line(
                agg_data, 
                x='year', 
                y='disaster_count',
                title='Historical Disaster Trends in Africa<br><sub>Data Source: EM-DAT (Emergency Events Database)</sub>',
                labels={'disaster_count': 'Number of Disasters', 'year': 'Year'}
            )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=16,
            hovermode='x unified',
            yaxis=dict(
                dtick=1,  # Integer tick intervals
                rangemode='tozero'  # Start from 0
            )
        )
        
        return fig
    
    @app.callback(
        Output('disaster-map', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('disaster-type-dropdown', 'value'),
         Input('disaster-year-slider', 'value')],
        prevent_initial_call=False
    )
    def update_disaster_map(selected_country, disaster_types, year_range):
        """Update disaster map visualization"""
        try:
            # Load real disaster data
            sample_data = load_real_disaster_data()
            
            if selected_country:
                sample_data = sample_data[sample_data['country_code'] == selected_country]
            if disaster_types and len(disaster_types) > 0:
                sample_data = sample_data[sample_data['disaster_type'].isin(disaster_types)]
            if year_range and len(year_range) == 2:
                sample_data = sample_data[
                    (sample_data['year'] >= year_range[0]) & 
                    (sample_data['year'] <= year_range[1])
                ]
            
            # Aggregate by country
            if sample_data.empty:
                sample_countries = []
                sample_values = []
            else:
                country_data = sample_data.groupby('country_code').size().reset_index(name='disaster_count')
                sample_countries = country_data['country_code'].tolist()
                sample_values = country_data['disaster_count'].tolist()
            
        except Exception as e:
            # Return empty data and show error
            sample_countries = []
            sample_values = []
        
        # Handle empty data case
        if not sample_countries or not sample_values:
            fig = go.Figure()
            fig.update_layout(
                title="No disaster data available for selected filters",
                geo=dict(showframe=False, showcoastlines=True, scope='africa')
            )
            return fig
        
        fig = go.Figure(data=go.Choropleth(
            locations=sample_countries,
            z=sample_values,
            locationmode='ISO-3',
            colorscale='Reds',
            text=[f'{val} disasters' for val in sample_values],
            colorbar_title="Disaster Count"
        ))
        
        fig.update_layout(
            title_text='Disaster Distribution Across Africa<br><sub>Data Source: EM-DAT (Emergency Events Database)</sub>',
            geo=dict(
                showframe=False,
                showcoastlines=True,
                scope='africa'
            ),
            title_font_size=16
        )
        
        return fig
    
    @app.callback(
        Output('disaster-impact-chart', 'figure'),
        [Input('main-country-filter', 'value'),
         Input('disaster-type-dropdown', 'value'),
         Input('disaster-year-slider', 'value')],
        prevent_initial_call=False
    )
    def update_disaster_impact_chart(selected_country, disaster_types, year_range):
        """Update disaster impact statistics chart"""
        try:
            # Load real EM-DAT data
            sample_data = load_real_disaster_data()
            
            # Filter data based on inputs
            if selected_country:
                sample_data = sample_data[sample_data['country_code'] == selected_country]
            if disaster_types and len(disaster_types) > 0:
                sample_data = sample_data[sample_data['disaster_type'].isin(disaster_types)]
            if year_range and len(year_range) == 2:
                sample_data = sample_data[
                    (sample_data['year'] >= year_range[0]) & 
                    (sample_data['year'] <= year_range[1])
                ]
            
            # Aggregate by disaster type
            if sample_data.empty:
                impact_data = pd.DataFrame({
                    'disaster_type': ['No Data'],
                    'affected_population': [0],
                    'economic_damage_usd': [0]
                })
            else:
                impact_data = sample_data.groupby('disaster_type').agg({
                    'affected_population': 'sum',
                    'economic_damage_usd': 'sum'
                }).reset_index()
                
        except Exception as e:
            # Return empty data to show error message
            impact_data = pd.DataFrame(columns=['disaster_type', 'affected_population', 'economic_damage_usd'])
        
        fig = px.bar(
            impact_data,
            x='disaster_type',
            y='affected_population',
            title='Disaster Impact by Type<br><sub>Data Source: EM-DAT</sub>',
            labels={'affected_population': 'Affected Population', 'disaster_type': 'Disaster Type'}
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2c3e50'},
            title_font_size=14,
            xaxis_tickangle=-45
        )
        
        return fig