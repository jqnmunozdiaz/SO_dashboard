"""
Sub-Saharan Africa Disaster Risk Management Dashboard
Main application entry point for the Dash application.
"""

import dash
import dash_bootstrap_components as dbc
from flask import redirect, request

from src.layouts.world_bank_layout import create_world_bank_layout
from src.callbacks import disaster_callbacks, urbanization_callbacks, flood_callbacks, flood_projections_callbacks
from src.callbacks.main_callbacks import register_main_callbacks
from src.callbacks.contact_callbacks import register_contact_callbacks

# Initialize the Dash app
app = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css"
    ],
    assets_folder='assets',
    suppress_callback_exceptions=True
)

# Add middleware for HTTPS redirect and www to non-www redirect
@app.server.before_request
def before_request():
    """Force HTTPS and redirect www to non-www in production"""
    import os
    env = os.environ.get('ENVIRONMENT', '').lower()
    
    # Only apply redirects in production
    if env == 'production':
        # Get the forwarded protocol (Cloud Run sets this)
        forwarded_proto = request.headers.get('X-Forwarded-Proto', 'http')
        host = request.headers.get('Host', '')
        
        # Redirect www to non-www
        if host.startswith('www.'):
            new_host = host[4:]  # Remove 'www.'
            return redirect(f'https://{new_host}{request.path}', code=301)
        
        # Redirect HTTP to HTTPS
        if forwarded_proto == 'http':
            return redirect(f'https://{host}{request.path}', code=301)

# Set the title
app.title = "Sub-Saharan Africa DRM Dashboard"

# Create the World Bank-styled layout
app.layout = create_world_bank_layout()

# Register all callbacks
register_main_callbacks(app)
register_contact_callbacks(app)
disaster_callbacks.register_callbacks(app)
urbanization_callbacks.register_callbacks(app)
flood_callbacks.register_callbacks(app)
flood_projections_callbacks.register_callbacks(app)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8050))
    # Show Dev Tools locally, hide on Render
    env = os.environ.get('ENVIRONMENT')
    # Detect Render environment via well-known vars
    is_render = any(k in os.environ for k in (
        'RENDER', 'RENDER_EXTERNAL_URL', 'RENDER_SERVICE_ID', 'RENDER_INSTANCE_ID'
    ))
    if env:
        debug = env.lower() in ('dev', 'development', 'local')
    else:
        # If ENVIRONMENT isn't set, default to debug locally and off on Render
        debug = not is_render
    # Always bind to 0.0.0.0 for compatibility with Render
    host = '0.0.0.0'
    app.run(debug=debug, host=host, port=port)