"""
Callbacks and layout for Risk Estimates - Probable Maximum Losses (PML) placeholder subtab
"""

from dash import html
from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
from ...utils.ui_helpers import create_methodological_note_button
from config.settings import CHART_STYLES


def render_probable_maximum_losses_layout(selected_country):
    """Render the Probable Maximum Losses (PML) placeholder layout dynamically based on selected country"""
    countries_dict = load_subsaharan_countries_and_regions_dict()
    label_name = countries_dict.get(selected_country, selected_country)
    
    return html.Div([
        # Dynamic Title
        html.Div([
            html.H6([
                html.B(label_name),
                " | Probable Maximum Losses by Hazard"
            ], className='chart-title')
        ]),
        
        # Placeholder Box
        html.Div([
            html.H5("Probable Maximum Losses (PML)", className="chart-title", style={'textAlign': 'center', 'marginBottom': '1.5rem', 'fontWeight': 'bold'}),
            html.P([
                html.B("Placeholder: "),
                "This subtab will present Probable Maximum Loss (PML) risk estimates for natural hazards at various return periods (e.g., 50, 100, 250, and 500 years)."
            ], style={'textAlign': 'center', 'color': CHART_STYLES['colors']['primary']})
        ], style={'padding': '3rem', 'backgroundColor': '#f8f9fa', 'borderRadius': '8px', 'border': '1px dashed #cbd5e1', 'marginBottom': '2rem'}),
        
        # Detailed Footnote Note
        html.Div([
            html.P([
                html.B("Data Source: "), "Global Infrastructure Risk Model & Resilience Index (GIRI).", html.Br(),
                html.B("Note: "), "Due to data limitations, only Earthquake and Floods are included in this analysis. ",
                "PMLs from the original risk assessment, which are provided with a high level of disaggregation, were aggregated based on two key assumptions: ",
                "(i) The shape of the exceedance probability curve of the whole asset portfolio matches the shape of the exceedance probability curve of buildings; and ",
                "(ii) the perils assessed are independent. ",
                "These two assumptions are important and results should be treated as a first order approximation rather than a full risk assessment."
            ], className="indicator-note"),
            html.Div([
                create_methodological_note_button()
            ], className="buttons-container")
        ], className="indicator-note-container")
    ], className="chart-container")


def setup_probable_maximum_losses_callbacks(app):
    """Setup callbacks for GIRI PML (currently static placeholder layout, no active callbacks)"""
    pass
