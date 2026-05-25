"""
Callbacks for Risk Estimates - Average Annual Loss (AAL) chart
"""

from dash import Input, Output, html
import plotly.express as px
import pandas as pd
from typing import Optional

from ...utils.data_loader import load_giri_aals_data, load_weo_expenditure_data
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict, load_wb_regional_classifications
from ...utils.component_helpers import create_simple_error_message
from ...utils.download_helpers import create_simple_download_callback
from config.settings import CHART_STYLES


def create_aal_table(filtered_df, display_mode):
    """Create a styled HTML table with AAL values for each hazard and the overall total"""
    # Calculate overall total
    total_val = filtered_df['Value_Display'].sum()
    
    # Sort the hazards in descending order of value for better readability
    sorted_df = filtered_df.sort_values(by='Value_Display', ascending=False)
    
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
        
    # Premium colors for hazards matching the chart
    HAZARD_COLORS = {
        'Flood': '#1f77b4',             # Mid blue
        'Tropical cyclone': '#ff7f0e',   # Warm orange
        'Landslide': '#8c564b',          # Earthy brown
        'Tsunami': '#17becf',            # Bright teal/cyan
        'Earthquake': '#d62728',         # Soft red
        'Volcano': '#9467bd',            # Purple
        'Storm surge': '#2ca02c'         # Soft green
    }
    
    rows = []
    for _, row in sorted_df.iterrows():
        hazard_name = row['hazard']
        val = row['Value_Display']
        color = HAZARD_COLORS.get(hazard_name, '#6c757d')
        
        rows.append(
            html.Tr([
                html.Td([
                    html.Span(
                        style={
                            'display': 'inline-block',
                            'width': '12px',
                            'height': '12px',
                            'borderRadius': '50%',
                            'backgroundColor': color,
                            'marginRight': '8px',
                            'verticalAlign': 'middle'
                        }
                    ),
                    html.Span(hazard_name, style={'fontWeight': '500', 'verticalAlign': 'middle'})
                ], style={'padding': '12px 16px', 'verticalAlign': 'middle', 'borderBottom': '1px solid #dee2e6'}),
                html.Td(
                    value_format.format(val),
                    style={'padding': '12px 16px', 'textAlign': 'right', 'fontWeight': '600', 'fontFamily': 'monospace', 'borderBottom': '1px solid #dee2e6'}
                )
            ])
        )
        
    # Add overall row
    rows.append(
        html.Tr([
            html.Td(
                html.B("Overall (Total)"),
                style={'padding': '12px 16px', 'borderTop': '2px solid #dee2e6', 'verticalAlign': 'middle', 'borderBottom': 'none'}
            ),
            html.Td(
                html.B(value_format.format(total_val)),
                style={'padding': '12px 16px', 'textAlign': 'right', 'borderTop': '2px solid #dee2e6', 'fontFamily': 'monospace', 'borderBottom': 'none'}
            )
        ], style={'backgroundColor': '#f8f9fa'})
    )
    
    return html.Div([
        html.Div([
            html.H6("AAL Values Summary", style={
                'color': '#002f6c',
                'fontWeight': 'bold',
                'marginBottom': '1rem',
                'borderBottom': '2px solid #002f6c',
                'paddingBottom': '0.5rem'
            }),
            html.Table([
                html.Thead(
                    html.Tr([
                        html.Th("Hazard Type", style={'padding': '10px 16px', 'textAlign': 'left', 'color': '#495057', 'borderBottom': '2px solid #dee2e6', 'fontWeight': 'bold'}),
                        html.Th(f"Value ({unit_label})", style={'padding': '10px 16px', 'textAlign': 'right', 'color': '#495057', 'borderBottom': '2px solid #dee2e6', 'fontWeight': 'bold'})
                    ])
                ),
                html.Tbody(rows)
            ], style={
                'width': '100%',
                'borderCollapse': 'collapse',
                'backgroundColor': 'white',
                'fontSize': '0.9rem'
            })
        ], style={
            'border': '1px solid #dee2e6',
            'borderRadius': '6px',
            'boxShadow': '0 2px 4px rgba(0,0,0,0.05)',
            'padding': '1.5rem',
            'backgroundColor': 'white'
        })
    ])


def setup_average_annual_loss_callbacks(app):
    """Setup callbacks for GIRI AAL visualization"""
    
    @app.callback(
        [Output('risk-estimates-chart', 'figure'),
         Output('risk-estimates-chart', 'style'),
         Output('risk-estimates-title', 'children'),
         Output('risk-estimates-table-container', 'children')],
        [Input('main-country-filter', 'value'),
         Input('risk-estimates-mode-selector', 'value')],
        prevent_initial_call=False
    )
    def generate_risk_estimates_chart(selected_country, display_mode):
        """Generate stacked bar chart of GIRI AAL by hazard"""
        try:
            # Handle no country selected
            if not selected_country:
                raise Exception("No country selected")
            
            # Load the AAL data
            df = load_giri_aals_data()
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
            
            # Check if selection is a region or an individual country
            is_region = selected_country in ['SSA', 'AFE', 'AFW']
            
            if is_region:
                if selected_country == 'SSA':
                    target_countries = ssa_countries
                    title_suffix = "Sub-Saharan Africa"
                elif selected_country == 'AFE':
                    target_countries = afe_countries
                    title_suffix = "Eastern & Southern Africa"
                elif selected_country == 'AFW':
                    target_countries = afw_countries
                    title_suffix = "Western & Central Africa"
                
                # Filter for target countries and exclude 'Combined' hazard (to avoid double-counting)
                region_df = df[(df['iso3cd'].isin(target_countries)) & (df['hazard'] != 'Combined')].copy()
                
                if region_df.empty:
                    raise Exception("No risk data available for the selected region")
                
                # Aggregate GIRI AAL losses per hazard for the region
                # Sum the first GDP / Gov Exp row for each unique country in the region to avoid compounding
                country_gdps = region_df.groupby('iso3cd')['GDP'].first()
                regional_gdp = country_gdps.sum()
                
                country_gov_exps = region_df.groupby('iso3cd')['Gov_Exp_USD'].first()
                regional_gov_exp = country_gov_exps.sum()
                
                # Group by hazard and sum the Loss across countries in the region
                aggregated_df = region_df.groupby('hazard')['Loss'].sum().reset_index()
                aggregated_df['GDP'] = regional_gdp
                aggregated_df['Gov_Exp_USD'] = regional_gov_exp
                aggregated_df['iso3cd'] = selected_country
                aggregated_df['Country_Label'] = title_suffix
                
                filtered_df = aggregated_df
                label_name = title_suffix
            else:
                label_name = countries_dict.get(selected_country, selected_country)
                title_suffix = label_name
                
                # Filter for the selected country and exclude 'Combined' hazard
                country_df = df[(df['iso3cd'] == selected_country) & (df['hazard'] != 'Combined')].copy()
                
                if country_df.empty:
                    raise Exception(f"No risk data available for {title_suffix}")
                
                country_df['Country_Label'] = label_name
                filtered_df = country_df
            
            # Compute Value Display based on selected display mode
            if display_mode == 'relative_gov_exp':
                # Relative view: percentage of Government Expenditure
                filtered_df['Value_Display'] = (filtered_df['Loss'] / filtered_df['Gov_Exp_USD']) * 100.0
                yaxis_title = "Average Annual Loss (% of Government Expenditure)"
                hover_format = ".2f"
                hover_suffix = "% of Government Expenditure"
            elif display_mode == 'relative':
                # Relative view: percentage of GDP
                filtered_df['Value_Display'] = (filtered_df['Loss'] / filtered_df['GDP']) * 100.0
                yaxis_title = "Average Annual Loss (% of GDP)"
                hover_format = ".2f"
                hover_suffix = "% of GDP"
            else:
                # Absolute view: Million USD
                filtered_df['Value_Display'] = filtered_df['Loss'] / 1e6
                yaxis_title = "Average Annual Loss (Million USD)"
                hover_format = ",.1f"
                hover_suffix = "M USD"
            
            # Premium color palette for hazards (harmonious and modern DRM tones)
            HAZARD_COLORS = {
                'Flood': '#1f77b4',             # Mid blue
                'Tropical cyclone': '#ff7f0e',   # Warm orange
                'Landslide': '#8c564b',          # Earthy brown
                'Tsunami': '#17becf',            # Bright teal/cyan
                'Earthquake': '#d62728',         # Soft red
                'Volcano': '#9467bd',            # Purple
                'Storm surge': '#2ca02c'         # Soft green
            }
            
            # Create stacked bar chart using plotly express
            fig = px.bar(
                filtered_df,
                x='Country_Label',
                y='Value_Display',
                color='hazard',
                color_discrete_map=HAZARD_COLORS,
                category_orders={
                    'Country_Label': [label_name],
                    'hazard': sorted(list(HAZARD_COLORS.keys()))
                },
                labels={'Country_Label': '', 'Value_Display': yaxis_title, 'hazard': 'Hazard'}
            )
            
            # Standardize hover template
            hover_template = (
                "<b>%{x}</b><br>" +
                "Hazard: %{fullData.name}<br>" +
                f"AAL: %{{y:{hover_format}}}{hover_suffix}<br>" +
                "<extra></extra>"
            )
            fig.update_traces(hovertemplate=hover_template)
            
            # Chart title
            chart_title = html.H6([
                html.B(title_suffix),
                f" | Average Annual Loss by Hazard"
            ], className='chart-title')
            
            # Calculate y-axis range to give headroom at the top (30% padding)
            total_height = filtered_df['Value_Display'].sum()
            y_max = total_height * 1.30 if total_height > 0 else 1.0
            
            # Layout updates matching World Bank styling
            fig.update_layout(
                xaxis_title='',
                yaxis_title=yaxis_title,
                barmode='stack',
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
                height=550,
                margin=dict(r=200, l=80, t=40, b=40),  # reduced bottom margin since tick is not rotated
                xaxis=dict(
                    showgrid=False,
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    tickangle=0
                ),
                yaxis=dict(
                    showgrid=True,
                    gridwidth=1,
                    gridcolor='#f0f0f0',
                    showline=True,
                    linewidth=1,
                    linecolor='#e2e8f0',
                    tickformat=',.2f' if display_mode in ['relative', 'relative_gov_exp'] else ',.1f',
                    range=[0, y_max]
                )
            )
            
            # Build summary table html content
            table_content = create_aal_table(filtered_df, display_mode)
            
            return fig, {'display': 'block', 'width': '100%'}, chart_title, table_content
            
        except Exception as e:
            fig, style = create_simple_error_message(str(e))
            return fig, style, "", ""

    # Register download callback using standard helper
    create_simple_download_callback(
        app,
        'risk-estimates-download',
        load_giri_aals_data
    )
