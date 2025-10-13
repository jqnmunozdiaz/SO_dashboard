"""
Sub-Saharan Africa Disaster Risk Management Dashboard
Main application entry point for the Dash application.
"""

import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

from src.layouts.world_bank_layout import create_world_bank_layout
from src.callbacks import disaster_callbacks, urbanization_callbacks
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

# Create the World Bank-styled layout
app.layout = create_world_bank_layout()

# Register all callbacks
register_main_callbacks(app)
disaster_callbacks.register_callbacks(app)
urbanization_callbacks.register_callbacks(app)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('ENVIRONMENT', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)