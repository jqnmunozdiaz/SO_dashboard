"""
Main GIRI Risk Estimates callbacks orchestrator
Coordinates all GIRI-related visualization callbacks organized in risk_estimates subfolder
"""

from dash import Input, Output, dcc, html
import dash_bootstrap_components as dbc

# Import individual sub-callback setup modules from the risk_estimates subfolder
from .risk_estimates.Average_Annual_Loss_callbacks import setup_average_annual_loss_callbacks
from .risk_estimates.PML_by_Sector_callbacks import setup_pml_by_sector_callbacks
from .risk_estimates.Probable_Maximum_Losses_callbacks import setup_probable_maximum_losses_callbacks, render_probable_maximum_losses_layout

from ..utils.country_utils import load_subsaharan_countries_and_regions_dict
from ..utils.ui_helpers import create_download_trigger_button, create_methodological_note_button
from config.settings import CHART_STYLES


def register_callbacks(app):
    """Register all GIRI risk estimates callbacks with organized structure"""
    
    # Register individual sub-callback setup functions
    setup_average_annual_loss_callbacks(app)
    setup_pml_by_sector_callbacks(app)
    setup_probable_maximum_losses_callbacks(app)
    
    # 1. Main chart container callback (orchestrates layout and controls based on subtab selection)
    @app.callback(
        Output('risk-estimates-chart-container', 'children'),
        [Input('risk-estimates-subtabs', 'active_tab'),
         Input('main-country-filter', 'value')],
        prevent_initial_call=False
    )
    def render_risk_estimates_chart_by_subtab(active_subtab, selected_country):
        """Render GIRI risk estimates tab components based on selected subtab"""
        if active_subtab == 'average-annual-loss':
            return html.Div([
                # Title
                html.Div(id='risk-estimates-title', className='chart-title'),
                
                # Display mode selector in filter row
                html.Div([
                    html.Div([
                        html.Label("Display Mode:", className="filter-label"),
                        dcc.RadioItems(
                            id='risk-estimates-mode-selector',
                            options=[
                                {'label': ' Absolute (USD)', 'value': 'absolute'},
                                {'label': ' Relative (% of GDP)', 'value': 'relative'},
                                {'label': ' Relative (as % of Government Expenditure)', 'value': 'relative_gov_exp'}
                            ],
                            value='absolute',
                            className='radio-buttons',
                            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
                        )
                    ], className='filter-control-group', style={'flex': '1', 'min-width': '250px'})
                ], className='filter-container', style={'display': 'flex', 'gap': '2rem', 'flex-wrap': 'wrap'}),
                
                # Chart and Table row
                dbc.Row([
                    dbc.Col([
                        dcc.Graph(
                            id="risk-estimates-chart",
                            style={'display': 'block', 'width': '100%'}
                        )
                    ], xs=12, lg=7),
                    dbc.Col([
                        html.Div(id="risk-estimates-table-container")
                    ], xs=12, lg=5)
                ], className="g-4 align-items-center", style={'marginTop': '1rem', 'marginBottom': '2rem'}),
                
                # Indicator note and download button
                html.Div([
                    html.P([
                        html.B("Data Source: "), "Global Infrastructure Risk Model & Resilience Index (GIRI). ",
                        "General government total expenditure (GGX_NGDP) data for 2025 obtained from the IMF's WEO dataset, v. April 2025.", html.Br(),
                        html.B("Note: "), "This stacked bar chart shows the Average Annual Loss (AAL) by hazard under existing climate conditions. ",
                        "Losses are stacked by hazard type. ",
                        "Due to data limitations, only Earthquakes and Floods are included in this analysis. ",
                        "The chart displays the hazard breakdown specifically for the selected country or region."
                    ], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('risk-estimates-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'probable-maximum-losses':
            return render_probable_maximum_losses_layout(selected_country)
        elif active_subtab == 'pml-by-sector':
            countries_dict = load_subsaharan_countries_and_regions_dict()
            label_name = countries_dict.get(selected_country, selected_country)
            return html.Div([
                # Title
                html.Div(id='pml-sector-title', className='chart-title'),
                
                # Hazard Selector Row
                html.Div([
                    html.Div([
                        html.Label("Select Hazard:", className="filter-label"),
                        dcc.RadioItems(
                            id='pml-sector-hazard-selector',
                            options=[
                                {'label': ' Earthquake', 'value': 'Earthquake'},
                                {'label': ' Flood', 'value': 'Flood'}
                            ],
                            value='Earthquake',
                            className='radio-buttons',
                            labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
                        )
                    ], className='filter-control-group', style={'flex': '1', 'min-width': '250px'})
                ], className='filter-container', style={'display': 'flex', 'gap': '2rem', 'flex-wrap': 'wrap', 'marginBottom': '1.5rem'}),
                
                # Chart
                dcc.Graph(
                    id="pml-sector-chart",
                    style={'display': 'block', 'width': '100%', 'maxWidth': '1100px', 'margin': '0 auto'}
                ),
                
                # Footnotes
                html.Div([
                    html.P([
                        html.B("Data Source: "), "Global Infrastructure Risk Model & Resilience Index (GIRI).", html.Br(),
                        html.B("Note: "), "This line chart shows the Probable Maximum Loss (PML) risk estimates for natural hazards across different Return Periods (RP) for every subsector under the selected country and hazard. ",
                        "Due to data limitations, only Earthquakes and Floods are included in this analysis."
                    ], className="indicator-note"),
                    html.Div([
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")
