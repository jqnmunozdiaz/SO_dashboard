"""
Sub-Saharan Africa Disaster Risk Management Dashboard
Main application entry point for the Dash application.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.layouts.main_layout import create_main_layout
from src.callbacks import disaster_callbacks, urbanization_callbacks, flood_risk_callbacks
from src.callbacks.main_callbacks import register_main_callbacks

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    assets_folder='assets',
    suppress_callback_exceptions=True
)

# Set the title
app.title = "Sub-Saharan Africa DRM Dashboard"

# Create the main layout
app.layout = create_main_layout()

# Register all callbacks
register_main_callbacks(app)
disaster_callbacks.register_callbacks(app)
urbanization_callbacks.register_callbacks(app)
flood_risk_callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)