"""
Orchestrator for flood projections callbacks
Handles the "Projections of Flood Risk" main tab
"""

from dash import Input, Output, html, dcc

from .flood_projections.Precipitation_callbacks import register_precipitation_callbacks
from .flood_projections.Urbanization_vs_Climate_Change_callbacks import register_urbanization_vs_climate_change_callbacks
from ..utils.ui_helpers import create_download_trigger_button, create_methodological_note_button
from ..utils.country_utils import get_subsaharan_countries
from ..utils.data_loader import load_precipitation_data


def register_callbacks(app):
    """Register all flood projections callbacks"""
    
    # Register individual chart callbacks
    register_precipitation_callbacks(app)
    register_urbanization_vs_climate_change_callbacks(app)
    
    # Callback to filter country dropdown options based on active flood projections subtab
    @app.callback(
        Output('main-country-filter', 'options', allow_duplicate=True),
        Input('flood-projections-subtabs', 'active_tab'),
        prevent_initial_call=True
    )
    def update_country_filter_options_flood_projections(projections_subtab):
        """Update country filter options for flood projections tabs - hide regional aggregates for all flood projection subtabs"""
        try:
            # Get individual countries (without regional aggregates)
            countries = get_subsaharan_countries()
            
            # Sort countries alphabetically by name
            countries = sorted(countries, key=lambda x: x['name'])
            
            # For all flood projections tabs, only show individual countries (no regional aggregates)
            return [{'label': country['name'], 'value': country['code']} for country in countries]
                
        except Exception as e:
            print(f"Error updating country filter options for flood projections: {str(e)}")
            # Fallback to individual countries only
            countries = get_subsaharan_countries()
            countries = sorted(countries, key=lambda x: x['name'])
            return [{'label': country['name'], 'value': country['code']} for country in countries]
    
    def create_precipitation_tab_content():
        """Helper function to create precipitation patterns tab content"""
        
        # Return period checkboxes selector
        rp_selector = html.Div([
            html.Label('Return Periods:', className='filter-label'),
            dcc.Checklist(
                id='precipitation-rp-selector',
                options=[
                    {'label': ' 5-year (20% annual probability)', 'value': 5},
                    {'label': ' 10-year (10% annual probability)', 'value': 10},
                    {'label': ' 100-year (1% annual probability)', 'value': 100}
                ],
                value=[5, 10, 100],  # All selected by default
                className='benchmark-checkboxes',
                inline=True,
                labelStyle={'display': 'inline-block', 'margin-right': '1.5rem'}
            )
        ], className='filter-container')
        
        # Data source note
        data_source = "World Bank Climate Change Knowledge Portal (CCKP) - Future precipitation return periods based on climate projections."
        note_prefix = "This chart shows how precipitation patterns are projected to change by 2050 under different climate scenarios (SSPs). "
        
        note_text = [
            html.B("Data Source: "), 
            data_source,
            html.Br(),
            html.B("Note: "), 
            note_prefix,
            "The 'Today' marker represents current conditions, while the colored dots show future projections. ",
            "Values moving to the right indicate increased frequency of precipitation events. ",
            "SSP1-1.9 represents the most optimistic scenario with strong climate mitigation, ",
            "while SSP5-8.5 represents a high-emissions scenario."
        ]
        
        return html.Div([
            # Title
            html.Div(id='precipitation-title', className='chart-title'),
            # Explanatory text - dynamic content based on selected country
            html.Div(id='precipitation-explanation', className='chart-explanation'),
            # Return period selector
            rp_selector,
            
            # Chart
            dcc.Graph(id='precipitation-chart'),
            
            # Data source note
            html.Div([
                html.P(note_text, className="indicator-note"),
                html.Div([
                    create_download_trigger_button('precipitation-download'),
                    create_methodological_note_button()
                ], className="buttons-container")
            ], className="indicator-note-container")
        ], className="chart-container")
    
    # Add callback to update precipitation explanation text dynamically
    @app.callback(
        Output('precipitation-explanation', 'children'),
        Input('main-country-filter', 'value'),
        prevent_initial_call=False
    )
    def update_precipitation_explanation(selected_country):
        """Update explanation text with country-specific precipitation data"""
        try:
            if not selected_country:
                return html.P([
                    html.B("Extreme precipitation events in the region will become more frequent and thus affect the already exposed population more often. "),
                    "Flood hazard could evolve due to changing climate patterns, as climate models indicate an increase in the frequency of extreme precipitation events in the coming decades. ",
                    "This corresponds to a national spatial average, and local changes are heterogeneous."
                ])
            
            # Load precipitation data
            data = load_precipitation_data('1day')
            
            # Filter for selected country, 2050, 10-year return period
            country_data = data[
                (data['ISO3'] == selected_country) & 
                (data['year'] == 2050) & 
                (data['RP'] == 10)
            ]
            
            if country_data.empty:
                # Fallback to generic text
                return html.P([
                    html.B("Extreme precipitation events in the region will become more frequent and thus affect the already exposed population more often. "),
                    "Flood hazard could evolve due to changing precipitation patterns, as climate models indicate an increase in the frequency of extreme precipitation events in the coming decades. ",
                    "This corresponds to a national spatial average, and local changes are heterogeneous."
                ])
            
            # Calculate min and max future exceedance probability across all SSPs
            min_ep = country_data['Future_EP'].min() * 100  # Convert to percentage
            max_ep = country_data['Future_EP'].max() * 100
            
            # Calculate corresponding return periods (inverse of exceedance probability)
            max_rp = 1 / (country_data['Future_EP'].min())  # Lower EP = higher RP
            min_rp = 1 / (country_data['Future_EP'].max())  # Higher EP = lower RP
            
            return html.P([
                html.B("Extreme precipitation events in the region will become more frequent and thus affect the already exposed population more often. "),
                f"Flood hazard could evolve due to changing precipitation patterns, as climate models indicate an increase in the frequency of extreme precipitation events in the coming decades. For instance, a heavy daily rainfall event which today has a 10% annual exceedance probability (or that will be exceeded once every 10 years on average) will change its exceedance probability to between {min_ep:.1f}% and {max_ep:.1f}% by 2050 due to climate change (which means that instead of occurring once every 10 years on average, it will occur between once every {min_rp:.1f} and {max_rp:.1f} years). ",
                "This corresponds to a national spatial average, and local changes are heterogeneous."
            ])
            
        except Exception as e:
            # Fallback to generic text on error
            return html.P([
                html.B("Extreme precipitation events in the region will become more frequent and thus affect the already exposed population more often. "),
                "Flood hazard could evolve due to changing precipitation patterns, as climate models indicate an increase in the frequency of extreme precipitation events in the coming decades. ",
                "This corresponds to a national spatial average, and local changes are heterogeneous."
            ])
        
    
    def create_overview_tab_content():
        """Helper function to create overview tab content with explanatory text"""
        
        return html.Div([
            # Header with large image square on right and text wrapper on left
            html.Div([
                # Left side: text wrapper
                html.Div([
                    html.H3("Future Precipitation Extremes and Flood Exposure", style={'color': '#295e84', 'marginTop': '0', 'marginBottom': '1rem'}),
                    html.P([
                         html.B("Future flood risk will be determined by evolving risk drivers."), " Understanding how these drivers may evolve is critical for disaster risk management planning and infrastructure investment decisions. In Sub-Saharan Africa, two simultaneous dynamics are unfolding."
                    ], style={'marginBottom': '0'}),
                    
                    # Climate Change section within left column
                    html.Div([
                        html.H5("1. Climate Change", style={'color': '#295e84', 'marginTop': '1.5rem', 'marginBottom': '0.5rem'}),
                        html.P([
                            "Climate models project an increase in the frequency and intensity of extreme precipitation events across the region. ",
                            "The ", html.B("Changes in Extreme Precipitation"), " subtab shows how precipitation return periods are expected to shift by 2050 under different climate scenarios. For instance, a heavy rainfall event that currently occurs once every 10 years may become significantly more frequent due to climate change. This implies that flood events could become more recurrent, impacting the already exposed population."
                        ], style={'marginBottom': '0'})
                    ])
                ], style={'flex': '1', 'paddingRight': '2rem'}),
                
                # Right side: image square
                html.Div([
                    html.Img(
                        src="/assets/images/flood_risk.svg",
                        style={'width': '100%', 'height': '100%', 'objectFit': 'contain'}
                    )
                ], style={'width': '450px', 'minWidth': '450px', 'height': '450px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'padding': '1rem'})
            ], style={'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'flex-start', 'marginBottom': '2rem', 'gap': '2rem'}),
            
            # Urbanization section - full width
            html.Div([
                html.H5("2. Urbanization and Population Growth", style={'color': '#295e84', 'marginTop': '0', 'marginBottom': '0.5rem'}),
                html.P([
                    "Rapid urbanization and population growth in Sub-Saharan Africa mean that more people and assets will be exposed to flood hazards, even if the hazard itself remains constant. ",
                    "The ", html.B("Urbanization and Climate Change"), " subtab compares the relative contributions of demographic changes and climate change to future flood exposure. ",
                    "This analysis helps identify which driver dominates flood risk changes in different countries, informing adaptation priorities."
                ], style={'marginBottom': '0'})
            ], style={'marginBottom': '2rem'}),
            
            # Note section
            html.Div([
                html.P([
                    html.B("Note: "),
                    "These projections are based on current understanding of climate science and demographic trends. The projections should be interpreted as illustrative scenarios rather than precise predictions. Actual outcomes will depend on the intersection of risk drivers such as climate change, demographic dynamics, urbanization, environmental and land degradation, and socioeconomic vulnerability. Further understanding and addressing these interactions is crucial to develop effective adaptation strategies, strengthen resilience, and reduce the impacts of flooding."
                ], style={'fontStyle': 'italic', 'backgroundColor': '#f8f9fa', 'padding': '1rem', 'borderLeft': '4px solid #295e84', 'marginBottom': '0'})
            ])
        ], style={'maxWidth': '1100px', 'margin': '0 auto', 'padding': '2rem'})
    
    def create_urbanization_vs_climate_change_tab_content():
        """Helper function to create urbanization vs climate change comparison tab content"""
        
        # Data source note
        data_source = "Fathom3 flood maps (2020), GHSL Built-up Surface (2023), and UN World Population Prospects (2022)."
        note_prefix = "This chart compares built-up area exposed to flooding (fluvial and pluvial) under different future scenarios. "
        
        note_text = [
            html.B("Data Source: "), 
            data_source,
            html.Br(),
            html.B("Note: "), 
            note_prefix,
            "Demographic scenarios (left group) show flood exposure changes based on population growth and urbanization, ",
            "assuming constant built-up area per capita from 2020. ",
            "Climate change scenarios (right group) show exposure changes from climate-driven flood pattern changes. ",
            "The horizontal dashed line represents 2020 baseline conditions. ",
            "Bars above this line indicate increased flood exposure."
        ]
        
        return html.Div([
            # Title
            html.Div(id='urbanization-vs-climate-change-title', className='chart-title'),
            
            # Explanatory text
            html.Div([
                html.P([
                    "To provide insights on potential national-level flood exposure by 2050, two complementary \"back-of-the-envelope\" analyses were conducted:"
                ], style={'marginBottom': '0.5rem'}),
                html.Ul([
                    html.Li([
                        html.B("Demographic and Urbanization Scenario: "),
                        "Assesses how population growth and urban expansion could increase the extent of built-up areas exposed to floods by 2050. This scenario assumes current climate conditions and constant vulnerability (i.e., fixed built-up area per capita)."
                    ], style={'marginBottom': '0.5rem'}),
                    html.Li([
                        html.B("Climate Change Scenario: "),
                        "Estimates flood exposure based on projected changes in precipitation and flood hazard patterns, while keeping today's population and built-up areas constant."
                    ], style={'marginBottom': '0.5rem'})
                ], style={'marginLeft': '1.5rem', 'marginBottom': '0.75rem'}),
                html.P([
                    "Overall, results indicate that in most countries of the region, urban growth and demographic trends are likely to drive a greater increase in flood exposure than climate change itself. This is expected given the region's strong forecasted urbanization dynamics and highlights the importance of integrating flood risk considerations into urban planning. Climate change, however, may exacerbate impacts by increasing the frequency and intensity of flood events."
                ], style={'marginBottom': '0.75rem'}),
                html.P([
                    "These analyses are illustrative rather than predictive and aim to provide an order-of-magnitude understanding of future exposure under different drivers. Flood exposure estimates from the two scenarios should not be combined, given their distinct assumptions."
                ], style={'fontStyle': 'italic', 'marginBottom': '0'})
            ], className='chart-explanation', style={'marginBottom': '1.5rem'}),
            
            # Chart (no additional filters needed - uses main country filter)
            dcc.Graph(id='urbanization-vs-climate-change-chart'),
            
            # Data source note
            html.Div([
                html.P(note_text, className="indicator-note"),
                html.Div([
                    create_download_trigger_button('urbanization-vs-climate-change-download'),
                    create_methodological_note_button()
                ], className="buttons-container")
            ], className="indicator-note-container")
        ], className="chart-container")
    
    @app.callback(
        Output('flood-projections-content', 'children'),
        Input('flood-projections-subtabs', 'active_tab'),
        prevent_initial_call=False
    )
    def render_flood_projections_chart(active_subtab):
        """Render the appropriate flood projections visualization"""
        
        # Create all tab contents
        overview_content = create_overview_tab_content()
        precipitation_content = create_precipitation_tab_content()
        urbanization_vs_climate_content = create_urbanization_vs_climate_change_tab_content()
        
        # Return all, but only display the active one
        return html.Div([
            html.Div(
                overview_content,
                style={'display': 'block' if active_subtab == 'overview' else 'none'}
            ),
            html.Div(
                precipitation_content,
                style={'display': 'block' if active_subtab == 'precipitation' else 'none'}
            ),
            html.Div(
                urbanization_vs_climate_content,
                style={'display': 'block' if active_subtab == 'urbanization-vs-climate' else 'none'}
            )
        ])

