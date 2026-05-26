"""
Callbacks and layout for Risk Estimates - Probable Maximum Losses (PML) subtab
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


def create_pml_table(filtered_df, display_mode, aal_dict=None):
    """Create a styled HTML table showing PML values by return period and hazard, plus AAL at the bottom"""
    # Pivot the data so that rows are RP and columns are hazards
    pivot_df = filtered_df.pivot(index='RP', columns='hazard', values='Value_Display')
    
    # Sort index (RP) in ascending order
    pivot_df = pivot_df.sort_index()
    
    # Define unit labels and formats
    if display_mode == 'relative_gov_exp':
        unit_label = "% of Gov. Exp."
        value_format = "{:.2f}%"
    elif display_mode == 'relative':
        unit_label = "% of GDP"
        value_format = "{:.2f}%"
    else:
        unit_label = "Million USD"
        value_format = "${:,.1f} M"
        
    # Hazards list order (Combined is placed on the right as the portfolio aggregate)
    hazards = ['Flood', 'Earthquake', 'Combined']
    available_hazards = [h for h in hazards if h in pivot_df.columns]
    
    # Generate table headers
    header_cols = [
        html.Th("Return Period", style={'padding': '10px 12px', 'textAlign': 'left', 'color': '#495057', 'borderBottom': '2px solid #dee2e6', 'fontWeight': 'bold'})
    ]
    for h in available_hazards:
        header_cols.append(
            html.Th(h, style={'padding': '10px 12px', 'textAlign': 'right', 'color': '#495057', 'borderBottom': '2px solid #dee2e6', 'fontWeight': 'bold'})
        )
        
    # Generate table rows
    rows = []
    for rp, row in pivot_df.iterrows():
        row_cols = [
            html.Td(f"{int(rp)} Years", style={'padding': '10px 12px', 'fontWeight': 'bold', 'verticalAlign': 'middle', 'borderBottom': '1px solid #dee2e6'})
        ]
        for h in available_hazards:
            val = row.get(h)
            formatted_val = value_format.format(val) if pd.notna(val) else "-"
            
            style = {
                'padding': '10px 12px',
                'textAlign': 'right',
                'fontFamily': 'monospace',
                'borderBottom': '1px solid #dee2e6',
                'verticalAlign': 'middle'
            }
            if h == 'Combined':
                style['fontWeight'] = 'bold'
                style['color'] = '#4b5563'  # Charcoal
                
            row_cols.append(html.Td(formatted_val, style=style))
            
        rows.append(html.Tr(row_cols))
        
    # Append Average Annual Loss (AAL) at the bottom
    if aal_dict:
        aal_row_cols = [
            html.Td(
                html.B("Average Annual Loss (AAL)"),
                style={'padding': '12px 12px', 'borderTop': '2px solid #dee2e6', 'verticalAlign': 'middle', 'borderBottom': 'none'}
            )
        ]
        for h in available_hazards:
            val = aal_dict.get(h)
            formatted_val = value_format.format(val) if pd.notna(val) else "-"
            
            style = {
                'padding': '12px 12px',
                'textAlign': 'right',
                'fontFamily': 'monospace',
                'borderTop': '2px solid #dee2e6',
                'borderBottom': 'none',
                'verticalAlign': 'middle',
                'fontWeight': 'bold'
            }
            if h == 'Combined':
                style['color'] = '#002f6c'  # Dark blue emphasis
                
            aal_row_cols.append(html.Td(formatted_val, style=style))
            
        rows.append(html.Tr(aal_row_cols, style={'backgroundColor': '#f8f9fa'}))
        
    return html.Div([
        html.Div([
            html.H6("PML Values Summary", style={
                'color': '#002f6c',
                'fontWeight': 'bold',
                'marginBottom': '1rem',
                'borderBottom': '2px solid #002f6c',
                'paddingBottom': '0.5rem'
            }),
            html.Table([
                html.Thead(html.Tr(header_cols)),
                html.Tbody(rows)
            ], style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'backgroundColor': 'white',
                'fontSize': '0.85rem'
            })
        ], style={
            'border': '1px solid #dee2e6',
            'borderRadius': '6px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
            'padding': '1.25rem',
            'backgroundColor': 'white'
        })
    ])


def render_probable_maximum_losses_layout(selected_country):
    """Render GIRI risk estimates tab components based on selected country"""
    countries_dict = load_subsaharan_countries_and_regions_dict()
    label_name = countries_dict.get(selected_country, selected_country)
    
    is_region = selected_country in ['SSA', 'AFE', 'AFW']
    
    if is_region:
        return html.Div([
            # Title
            html.Div([
                html.H6([
                    html.B(label_name),
                    " | Probable Maximum Loss by Return Period"
                ], className='chart-title'),
            ]),
            # GIRI Data Warning Note
            create_giri_warning_alert(),
            
            # Warning Card
            html.Div([
                html.Div([
                    html.H5("Probable Maximum Losses (PML)", style={'fontWeight': 'bold', 'color': '#002f6c', 'marginBottom': '1rem'}),
                    html.P([
                        "Probable Maximum Loss (PML) estimates are only available at the country level. ",
                        "PML curve aggregation for regional portfolios requires specific asset correlation and joint exceedance probability assumptions that are not representative at a regional scale. ",
                        html.Br(), html.Br(),
                        html.B("Please select an individual country from the dropdown at the top to view the PML curves and summary values table.")
                    ], style={'fontSize': '1rem', 'lineHeight': '1.6'})
                ], style={
                    'border': '1px solid #dee2e6',
                    'borderRadius': '8px',
                    'padding': '3rem',
                    'backgroundColor': '#f8f9fa',
                    'textAlign': 'center',
                    'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
                    'maxWidth': '700px',
                    'margin': '2rem auto'
                })
            ]),
            html.Div([
                create_methodological_note_button()
            ], className="buttons-container", style={'justifyContent': 'center', 'marginTop': '2rem'})
        ], className="chart-container")
        
    return html.Div([
        # Title
        html.Div(id='pml-title', className='chart-title'),
        
        # GIRI Data Warning Note
        create_giri_warning_alert(),
        
        # Display mode and x-axis scale selectors in filter row
        html.Div([
            html.Div([
                html.Label("Display Mode:", className="filter-label"),
                dcc.RadioItems(
                    id='pml-mode-selector',
                    options=[
                        {'label': ' Absolute (USD)', 'value': 'absolute'},
                        {'label': ' Relative (% of GDP)', 'value': 'relative'},
                        {'label': ' Relative (as % of Government Expenditure)', 'value': 'relative_gov_exp'}
                    ],
                    value='absolute',
                    className='radio-buttons',
                    labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
                )
            ], className='filter-control-group', style={'flex': '1', 'min-width': '250px'}),
            
            html.Div([
                html.Label("X-Axis Scale:", className="filter-label"),
                dcc.RadioItems(
                    id='pml-scale-selector',
                    options=[
                        {'label': ' Linear Scale', 'value': 'linear'},
                        {'label': ' Logarithmic Scale', 'value': 'log'}
                    ],
                    value='linear',
                    className='radio-buttons',
                    labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
                )
            ], className='filter-control-group', style={'flex': '1', 'min-width': '250px'})
        ], className='filter-container', style={'display': 'flex', 'gap': '2rem', 'flex-wrap': 'wrap'}),
        
        # Chart and Table row
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="pml-chart",
                    style={'display': 'block', 'width': '100%'}
                )
            ], xs=12, lg=7),
            dbc.Col([
                html.Div(id="pml-table-container")
            ], xs=12, lg=5)
        ], className="g-4 align-items-center", style={'marginTop': '1rem', 'marginBottom': '2rem'}),
        
        # Indicator note and download button
        html.Div([
            html.P([
                html.B("Data Source: "), "Global Infrastructure Risk Model & Resilience Index (GIRI). ",
                "General government total expenditure (GGX_NGDP) data for 2018 obtained from the IMF's WEO dataset.", html.Br(),
                html.B("Note: "), "This scatterplot shows the Probable Maximum Losses (PML) for Earthquakes, Floods, and Combined hazards across different Return Periods. ",
                "PMLs from the original risk assessment, which are provided with a high level of disaggregation, were aggregated based on key risk modeling assumptions: ",
                "(i) The shape of the exceedance probability curve of the whole asset portfolio matches the shape of the exceedance probability curve of buildings; and ",
                "(ii) the perils assessed (Earthquakes and Floods) are independent. ",
                "These assumptions are important and results should be treated as a first order approximation rather than a full risk assessment."
            ], className="indicator-note"),
            html.Div([
                create_methodological_note_button()
            ], className="buttons-container")
        ], className="indicator-note-container")
    ], className="chart-container")


def setup_probable_maximum_losses_callbacks(app):
    """Setup callbacks for GIRI PML visualization"""
    
    @app.callback(
        [Output('pml-chart', 'figure'),
         Output('pml-chart', 'style'),
         Output('pml-title', 'children'),
         Output('pml-table-container', 'children')],
        [Input('main-country-filter', 'value'),
         Input('pml-mode-selector', 'value'),
         Input('pml-scale-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_pml_chart(selected_country, display_mode, scale_mode):
        """Generate scatterplot of GIRI PML with actual values summary table and AAL"""
        try:
            if not selected_country:
                raise Exception("No country selected")
            
            # Check if selection is a region or an individual country
            is_region = selected_country in ['SSA', 'AFE', 'AFW']
            if is_region:
                # Return empty layout elements safely if called while in region mode
                return {}, {'display': 'none'}, "", ""
            
            # Load the PML data
            df = load_giri_pmls_data()
            countries_dict = load_subsaharan_countries_and_regions_dict()
            
            # Load WEO Gov Expenditure data and merge
            weo_df = load_weo_expenditure_data()
            weo_df = weo_df.rename(columns={'ISO3': 'iso3cd', 'Value': 'Gov_Exp_Pct_GDP'})
            df = df.merge(weo_df[['iso3cd', 'Gov_Exp_Pct_GDP']], on='iso3cd', how='left')
            
            # Compute Gov Expenditure in USD at the country level
            df['Gov_Exp_USD'] = (df['Gov_Exp_Pct_GDP'] / 100.0) * df['GDP']
            
            # Identify regional groupings
            afe_countries, afw_countries, ssa_countries = load_wb_regional_classifications()
            
            # Filter based on display mode requirements
            if display_mode == 'relative_gov_exp':
                df = df[df['Gov_Exp_USD'].notna() & (df['Gov_Exp_USD'] > 0)].copy()
            elif display_mode == 'relative':
                df = df[df['GDP'].notna() & (df['GDP'] > 0)].copy()
            
            label_name = countries_dict.get(selected_country, selected_country)
            title_suffix = label_name
            
            # Filter for the selected country
            country_df = df[df['iso3cd'] == selected_country].copy()
            
            if country_df.empty:
                raise Exception(f"No risk data available for {title_suffix}")
            
            # Check the number of unique individual hazards (excluding Combined)
            unique_individual_hazards = country_df[country_df['hazard'] != 'Combined']['hazard'].unique()
            if len(unique_individual_hazards) < 2:
                # Exclude the redundant 'Combined' hazard when only one peril exists
                country_df = country_df[country_df['hazard'] != 'Combined'].copy()
                
            country_df['Country_Label'] = label_name
            filtered_df = country_df
            
            # Compute Value Display and AAL Display based on selected display mode
            if display_mode == 'relative_gov_exp':
                filtered_df['Value_Display'] = (filtered_df['Loss'] / filtered_df['Gov_Exp_USD']) * 100.0
                filtered_df['AAL_Display'] = (filtered_df['Total_AAL'] / filtered_df['Gov_Exp_USD']) * 100.0
                yaxis_title = "Probable Maximum Loss (% of Government Expenditure)"
                hover_format = ".2f"
                hover_suffix = "% of Government Expenditure"
            elif display_mode == 'relative':
                filtered_df['Value_Display'] = (filtered_df['Loss'] / filtered_df['GDP']) * 100.0
                filtered_df['AAL_Display'] = (filtered_df['Total_AAL'] / filtered_df['GDP']) * 100.0
                yaxis_title = "Probable Maximum Loss (% of GDP)"
                hover_format = ".2f"
                hover_suffix = "% of GDP"
            else:
                filtered_df['Value_Display'] = filtered_df['Loss'] / 1e6
                filtered_df['AAL_Display'] = filtered_df['Total_AAL'] / 1e6
                yaxis_title = "Probable Maximum Loss (Million USD)"
                hover_format = ",.1f"
                hover_suffix = "M USD"
            
            # Premium color palette for hazards matching the chart
            HAZARD_COLORS = {
                'Flood': '#1f77b4',             # Mid blue
                'Earthquake': '#d62728',         # Soft red
                'Combined': '#4b5563'            # Premium charcoal
            }
            
            # Create scatter/line chart using plotly express
            fig = px.line(
                filtered_df,
                x='RP',
                y='Value_Display',
                color='hazard',
                markers=True,
                color_discrete_map=HAZARD_COLORS,
                category_orders={
                    'hazard': ['Combined', 'Flood', 'Earthquake']
                },
                labels={'RP': 'Return Period (Years)', 'Value_Display': yaxis_title, 'hazard': 'Hazard'}
            )
            
            # Standardize hover template
            hover_template = (
                "<b>Return Period: %{x} Years</b><br>" +
                "Hazard: %{fullData.name}<br>" +
                f"PML: %{{y:{hover_format}}}{hover_suffix}<br>" +
                "<extra></extra>"
            )
            fig.update_traces(hovertemplate=hover_template)
            
            # Chart title
            chart_title = html.H6([
                html.B(title_suffix),
                f" | Probable Maximum Loss by Return Period"
            ], className='chart-title')
            
            # Layout updates matching World Bank styling
            fig.update_layout(
                xaxis_title='Return Period (Years)' + (' [Log Scale]' if scale_mode == 'log' else ''),
                yaxis_title=yaxis_title,
                plot_bgcolor='white',
                paper_bgcolor='white',
                font={'color': CHART_STYLES['colors']['primary']},
                showlegend=True,
                legend=dict(
                    title="Hazards",
                    orientation="v",
                    yanchor="top",
                    y=1,
                    xanchor="left",
                    x=1.02,
                    bgcolor="rgba(255, 255, 255, 0.8)",
                    bordercolor="#e2e8f0",
                    borderwidth=0
                ),
                height=500,
                margin=dict(r=150, l=80, t=40, b=40),
                xaxis=dict(
                    type=scale_mode,
                    tickvals=[10, 25, 50, 100, 250, 500, 1000],
                    ticktext=['10', '25', '50', '100', '250', '500', '1000'],
                    showgrid=True,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    tickformat=',.2f' if display_mode in ['relative', 'relative_gov_exp'] else ',.1f'
                )
            )
            
            # Build AAL dictionary to append at the bottom of the table
            aal_series = filtered_df.groupby('hazard')['AAL_Display'].first()
            aal_dict = aal_series.to_dict()
            
            # Build summary table html content
            table_content = create_pml_table(filtered_df, display_mode, aal_dict)
            
            return fig, {'display': 'block', 'width': '100%'}, chart_title, table_content
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, "", ""
