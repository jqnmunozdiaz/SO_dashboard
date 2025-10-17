"""
Debug script to test Dash Bootstrap Components tab structure
and verify what HTML attributes are actually generated
"""

import dash
from dash import html
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1("Tab Structure Test"),
    html.Div([
        dbc.Tabs([
            dbc.Tab(
                label="Urban Population",
                tab_id="urban-population-projections"
            ),
            dbc.Tab(
                label="Urbanization Rate",
                tab_id="urbanization-rate"
            ),
            dbc.Tab(
                label="Population Living in Slums",
                tab_id="urban-population-slums"
            ),
            dbc.Tab(
                label="Cities Distribution",
                tab_id="cities-distribution"
            )
        ], id="urbanization-subtabs", active_tab="urban-population-projections")
    ]),
    html.Div(id="content")
])

if __name__ == '__main__':
    print("\n" + "="*80)
    print("Debug Dashboard Running on http://localhost:8051")
    print("Open browser DevTools and inspect the tab elements")
    print("Look for the actual HTML structure and attributes used by dbc.Tabs")
    print("="*80 + "\n")
    app.run(debug=True, port=8051)
