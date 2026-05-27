"""
Callbacks and layout for Risk Estimates - Probable Maximum Loss Benchmark subtab
"""

from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from typing import Optional

from ...utils.data_loader import load_giri_pmls_data, load_weo_expenditure_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict, load_wb_regional_classifications
from ...utils.component_helpers import create_simple_error_message
from ...utils.ui_helpers import create_methodological_note_button, create_giri_warning_alert
from config.settings import CHART_STYLES


def render_probable_maximum_loss_benchmark_layout(selected_country):
    """Render the Probable Maximum Loss Benchmark layout"""
    return html.Div([
        # Title
        html.Div(id='pml-benchmark-title', className='chart-title'),
        
        # GIRI Data Warning Note
        create_giri_warning_alert(),
        
        # Selectors in filter row
        html.Div([
            # Return Period Selector
            html.Div([
                html.Label("Select Return Period:", className="filter-label"),
                html.Div([
                    dcc.Dropdown(
                        id='pml-benchmark-rp-selector',
                        options=[
                            {'label': '10 Years', 'value': 10.0},
                            {'label': '25 Years', 'value': 25.0},
                            {'label': '50 Years', 'value': 50.0},
                            {'label': '100 Years', 'value': 100.0},
                            {'label': '250 Years', 'value': 250.0},
                            {'label': '500 Years', 'value': 500.0},
                            {'label': '1000 Years', 'value': 1000.0}
                        ],
                        value=100.0,
                        clearable=False,
                        className='custom-dropdown',
                        style={'width': '220px', 'minWidth': '220px'}
                    )
                ], className='filter-dropdown-container', style={'width': '220px', 'minWidth': '220px'})
            ], className='filter-control-group'),
            
            # Hazard Selector as radial buttons
            html.Div([
                html.Label("Select Hazard:", className="filter-label"),
                dcc.RadioItems(
                    id='pml-benchmark-hazard-selector',
                    options=[
                        {'label': ' Earthquake', 'value': 'Earthquake'},
                        {'label': ' Flood', 'value': 'Flood'},
                        {'label': ' Combined', 'value': 'Combined'}
                    ],
                    value='Combined',
                    className='radio-buttons',
                    labelStyle={'display': 'inline-block', 'marginRight': '1.5rem'}
                )
            ], className='filter-control-group', style={'flex': '1', 'minWidth': '380px'}),
            
            # Outlier Toggle
            html.Div([
                html.Label("Filter Extreme Values:", className="filter-label"),
                dcc.Checklist(
                    id='pml-benchmark-outlier-toggle',
                    options=[
                        {'label': ' Hide values exceeding 100% of Government Expenditure', 'value': 'hide_outliers'}
                    ],
                    value=[],
                    className='custom-checklist',
                    labelStyle={'display': 'inline-block', 'cursor': 'pointer'}
                )
            ], className='filter-control-group', style={'flex': '1', 'minWidth': '380px'})
        ], className='filter-container', style={'display': 'flex', 'gap': '2rem', 'flexWrap': 'wrap'}),
        
        # Chart Row
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="pml-benchmark-chart",
                    style={'display': 'block', 'width': '100%'}
                )
            ], xs=12)
        ], className="g-4 align-items-center", style={'marginTop': '1rem', 'marginBottom': '2rem'}),
        
        # Footnotes
        html.Div([
            html.P([
                html.B("Data Source: "), "Global Infrastructure Risk Model & Resilience Index (GIRI). ",
                "General government total expenditure (GGX_NGDP) data for 2018 obtained from the IMF's WEO dataset.", html.Br(),
                html.B("Note: "), "This horizontal bar chart compares the selected hazard PML (as % of Government Expenditure) across all countries in Sub-Saharan Africa for the selected Return Period. ",
                "The selected country or countries belonging to the selected region are highlighted in orange. ",
                "PMLs from the original risk assessment, which are provided with a high level of disaggregation, were aggregated based on key risk modeling assumptions: ",
                "(i) The shape of the exceedance probability curve of the whole asset portfolio matches the shape of the exceedance probability curve of buildings; and ",
                "(ii) the perils assessed (Earthquakes and Floods) are independent. ",
                "Results are a first order approximation and should be treated as such."
            ], className="indicator-note"),
            html.Div([
                create_methodological_note_button()
            ], className="buttons-container")
        ], className="indicator-note-container")
    ], className="chart-container")


def setup_probable_maximum_loss_benchmark_callbacks(app):
    """Setup callbacks for GIRI PML Benchmark visualization"""
    
    @app.callback(
        [Output('pml-benchmark-chart', 'figure'),
         Output('pml-benchmark-title', 'children')],
        [Input('main-country-filter', 'value'),
         Input('pml-benchmark-rp-selector', 'value'),
         Input('pml-benchmark-hazard-selector', 'value'),
         Input('pml-benchmark-outlier-toggle', 'value')],
        prevent_initial_call=False
    )
    def generate_pml_benchmark_chart(selected_country, selected_rp, selected_hazard, outlier_options):
        """Generate horizontal bar chart of GIRI PML benchmark across all countries"""
        try:
            # Load the PML data
            df = load_giri_pmls_data()
            countries_dict = load_subsaharan_countries_and_regions_dict()
            
            # Load WEO Gov Expenditure data and merge
            weo_df = load_weo_expenditure_data()
            weo_df = weo_df.rename(columns={'ISO3': 'iso3cd', 'Value': 'Gov_Exp_Pct_GDP'})
            df = df.merge(weo_df[['iso3cd', 'Gov_Exp_Pct_GDP']], on='iso3cd', how='left')
            
            # Compute Gov Expenditure in USD at the country level
            df['Gov_Exp_USD'] = (df['Gov_Exp_Pct_GDP'] / 100.0) * df['GDP']
            
            # Filter for selected hazard and selected Return Period
            filtered_df = df[(df['hazard'] == selected_hazard) & (df['RP'] == selected_rp)].copy()
            
            # Exclude countries with no Gov Exp data
            filtered_df = filtered_df[filtered_df['Gov_Exp_USD'].notna() & (filtered_df['Gov_Exp_USD'] > 0)].copy()
            
            if filtered_df.empty:
                raise Exception(f"No {selected_hazard} PML data available for the selected return period")
                
            # Compute Value Display (% of Gov Exp) with exactly 2 decimals
            filtered_df['Value_Display'] = (filtered_df['Loss'] / filtered_df['Gov_Exp_USD']) * 100.0
            
            # Hide outliers if selected
            if outlier_options and 'hide_outliers' in outlier_options:
                filtered_df = filtered_df[filtered_df['Value_Display'] <= 100.0].copy()
            
            # Map country codes to country names
            filtered_df['Country_Name'] = filtered_df['iso3cd'].map(lambda code: countries_dict.get(code, code))
            
            # Sort the dataframe in ascending order of Value_Display so that the highest values plot at the top
            filtered_df = filtered_df.sort_values(by='Value_Display', ascending=True)
            
            # Determine highlighting color for each bar
            afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()
            is_region = selected_country in ['SSA', 'AFE', 'AFW']
            
            if is_region:
                if selected_country == 'SSA':
                    highlight_list = ssa_countries
                elif selected_country == 'AFE':
                    highlight_list = afe_countries
                elif selected_country == 'AFW':
                    highlight_list = afw_countries
            else:
                highlight_list = [selected_country]
                
            # Create a color list: Orange for highlighted countries/regions, Slate grey for others
            highlight_color = '#ff7f0e'  # Dynamic WB/GFDRR Orange
            base_color = '#cbd5e1'       # Premium light slate grey
            
            filtered_df['Color'] = filtered_df['iso3cd'].apply(
                lambda code: highlight_color if code in highlight_list else base_color
            )
            
            # Create horizontal bar chart
            fig = px.bar(
                filtered_df,
                x='Value_Display',
                y='Country_Name',
                orientation='h',
                category_orders={'Country_Name': filtered_df['Country_Name'].tolist()},
                labels={'Value_Display': f'{selected_hazard} PML (% of Government Expenditure)', 'Country_Name': 'Country'}
            )
            
            # Configure bar colors and hover templates
            fig.update_traces(
                marker_color=filtered_df['Color'].tolist(),
                hovertemplate=(
                    "<b>%{y}</b><br>" +
                    f"{selected_hazard} PML: %{{x:.2f}}% of Government Expenditure<br>" +
                    "<extra></extra>"
                )
            )
            
            # Resolve selected country/region name
            if selected_country == 'SSA':
                country_name = "Sub-Saharan Africa"
            elif selected_country == 'AFE':
                country_name = "Eastern & Southern Africa"
            elif selected_country == 'AFW':
                country_name = "Western & Central Africa"
            else:
                country_name = countries_dict.get(selected_country, selected_country)

            # Chart title
            chart_title = html.H6([
                html.B(country_name),
                f" | {int(selected_rp)}-Year Return Period | {selected_hazard} PML Benchmark (% of Government Expenditure)"
            ], className='chart-title')
            
            # Calculate height dynamically based on the number of countries
            num_countries = len(filtered_df)
            chart_height = max(350, num_countries * 16)
            
            fig.update_layout(
                xaxis_title=f'{selected_hazard} PML (% of Government Expenditure)',
                yaxis_title='',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=False,
                height=chart_height,
                margin=dict(r=40, l=180, t=20, b=40),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    tickformat=',.2f'
                ),
                yaxis=dict(
                    showgrid=False,
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    dtick=1  # Forces Plotly to display every country label
                )
            )
            
            return fig, chart_title
            
        except Exception as e:
            fig, _ = create_simple_error_message(str(e))
            return fig, ""
