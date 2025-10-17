"""
Comprehensive test to identify the correct CSS selectors for dbc.Tabs
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Dash Bootstrap Components Tab Selector Test", style={'padding': '20px'}),
    
    html.Div([
        html.H3("Test 1: Standard dbc.Tabs"),
        dbc.Tabs([
            dbc.Tab(label="Urban Population", tab_id="urban-population-projections"),
            dbc.Tab(label="Urbanization Rate", tab_id="urbanization-rate"),
            dbc.Tab(label="Slums", tab_id="urban-population-slums"),
            dbc.Tab(label="Cities", tab_id="cities-distribution")
        ], id="urbanization-subtabs", active_tab="urban-population-projections")
    ], style={'padding': '20px', 'border': '2px solid blue', 'margin': '20px'}),
    
    html.Div([
        html.H3("Inspection Instructions:"),
        html.Ol([
            html.Li("Open browser DevTools (F12)"),
            html.Li("Click on 'Elements' or 'Inspector' tab"),
            html.Li("Click the 'Select Element' tool"),
            html.Li("Click on one of the tabs above"),
            html.Li("Look at the HTML structure in DevTools"),
            html.Li([
                "Check for these possible attributes:",
                html.Ul([
                    html.Li("id attribute"),
                    html.Li("class attribute (nav-link, nav-item, etc)"),
                    html.Li("data-rb-event-key attribute"),
                    html.Li("href attribute"),
                    html.Li("role attribute"),
                    html.Li("aria-* attributes")
                ])
            ])
        ])
    ], style={'padding': '20px', 'background': '#f0f0f0', 'margin': '20px'}),
    
    html.Div([
        html.H3("Possible CSS Selectors to Try:"),
        html.Pre("""
1. Using id of parent container and tab_id:
   #urbanization-subtabs [data-rb-event-key="urban-population-projections"]
   #urbanization-subtabs [data-rb-event-key="urbanization-rate"]

2. Using class and data attribute:
   .nav-link[data-rb-event-key="urban-population-projections"]
   .nav-link[data-rb-event-key="urbanization-rate"]

3. Using id attribute pattern (if tabs have ids):
   #urbanization-subtabs-tab-urban-population-projections
   #urbanization-subtabs-tab-urbanization-rate

4. Using nth-child selector:
   #urbanization-subtabs .nav-item:nth-child(1) .nav-link
   #urbanization-subtabs .nav-item:nth-child(2) .nav-link

5. Direct descendant selector:
   #urbanization-subtabs > .nav-item:nth-child(1) > .nav-link
        """, style={'background': 'black', 'color': 'lime', 'padding': '15px'})
    ], style={'padding': '20px', 'margin': '20px'})
], style={'font-family': 'Arial, sans-serif'})

if __name__ == '__main__':
    print("\n" + "="*80)
    print("Tab Structure Debug App")
    print("Running on: http://localhost:8051")
    print("\nInstructions:")
    print("1. Open http://localhost:8051 in your browser")
    print("2. Open DevTools (F12)")
    print("3. Inspect the tab elements to see their actual HTML structure")
    print("="*80 + "\n")
    app.run(debug=True, port=8051)
