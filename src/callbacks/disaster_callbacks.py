"""
Main disaster callbacks orchestrator
Coordinates all disaster-related visualization callbacks organized in disaster subfolder
"""

from dash import Input, Output, dcc, html

# Import individual callback modules from disaster subfolder with clear naming
from .disaster.Frequency_by_Type_callbacks import setup_frequency_by_type_callbacks
from .disaster.Disasters_by_Year_callbacks import setup_disasters_by_year_callbacks
from .disaster.Total_Affected_Population_callbacks import setup_total_affected_population_callbacks
from .disaster.Total_Deaths_callbacks import setup_total_deaths_callbacks

from ..utils.ui_helpers import create_download_trigger_button, create_methodological_note_button, create_absolute_relative_selector


def register_callbacks(app):
    """Register all disaster-related callbacks with organized structure"""
    
    # Register individual callback modules using clear function names
    setup_frequency_by_type_callbacks(app)
    setup_disasters_by_year_callbacks(app)
    setup_total_affected_population_callbacks(app)
    setup_total_deaths_callbacks(app)
    
    # Main chart container callback (orchestrates which chart to show based on subtab selection)
    @app.callback(
        Output('disaster-chart-container', 'children'),
        [Input('disaster-subtabs', 'active_tab'),
         Input('main-country-filter', 'value')]
    )
    def render_disaster_chart_by_subtab(active_subtab, selected_country):
        """Render different disaster charts based on selected subtab with clear chart mapping"""
        if active_subtab == 'disaster-frequency':
            return html.Div([
                # Title
                html.Div(id='disaster-frequency-title', className='chart-title'),
                # Display mode selector
                html.Div([
                    html.Label("Display Mode:", className="filter-label"),
                    dcc.RadioItems(
                        id='disaster-frequency-mode-selector',
                        options=[
                            {'label': ' Absolute', 'value': 'absolute'},
                            {'label': ' Relative', 'value': 'relative'}
                        ],
                        value='absolute',
                        className='radio-buttons',
                        labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
                    )
                ], className='filter-container'),
                # Chart
                dcc.Graph(id="disaster-frequency-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "EM-DAT (Emergency Events Database).", html.Br(), html.B("Note:"), " Figures may be lower than actual values due to gaps in data reporting."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('disaster-frequency-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'disaster-timeline':
            return html.Div([
                # Title
                html.Div(id='disaster-timeline-title', className='chart-title'),
                # Chart
                dcc.Graph(id="disaster-timeline-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "EM-DAT (Emergency Events Database).", html.Br(), html.B("Note:"), " Figures may be lower than actual values due to gaps in data reporting."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('disaster-timeline-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'disaster-affected':
            return html.Div([
                # Title
                html.Div(id='disaster-affected-title', className='chart-title'),
                # Display mode selector
                create_absolute_relative_selector('disaster-affected-mode-selector'),
                # Chart
                dcc.Graph(id="disaster-affected-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "EM-DAT (Emergency Events Database).", html.Br(), html.B("Note:"), " Figures may be lower than actual values due to gaps in data reporting."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('disaster-affected-download'),
                        create_methodological_note_button()
                    ], className="buttons-container"),
                ], className="indicator-note-container")
            ], className="chart-container")
        elif active_subtab == 'disaster-deaths':
            return html.Div([
                # Title
                html.Div(id='disaster-deaths-title', className='chart-title'),
                # Display mode selector
                create_absolute_relative_selector('disaster-deaths-mode-selector'),
                # Chart
                dcc.Graph(id="disaster-deaths-chart"),
                # Indicator note
                html.Div([
                    html.P([html.B("Data Source: "), "EM-DAT (Emergency Events Database).", html.Br(), html.B("Note:"), " Figures may be lower than actual values due to gaps in data reporting."], className="indicator-note"),
                    html.Div([
                        create_download_trigger_button('disaster-deaths-download'),
                        create_methodological_note_button()
                    ], className="buttons-container")
                ], className="indicator-note-container")
            ], className="chart-container")
        else:
            return html.Div("Select a chart type above")