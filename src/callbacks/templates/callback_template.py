"""
Standard callback template to use when adding new visualizations.
Place new callbacks in the appropriate subfolder (e.g., `disaster/` or `urbanization/`) and
follow this pattern:
- thin registration function: `register_<feature>_callbacks(app)`
- use centralized data loaders in `src.utils.data_loader`
- use `create_error_chart` from `src.utils.component_helpers` for errors
- use `handle_callback_errors` from `src.utils.callback_helpers` as decorator
- validate inputs and return empty charts consistently
"""

from dash import Input, Output
import plotly.express as px
import pandas as pd

try:
    from ...utils.data_loader import load_emdat_data  # or load_wdi_data
    from ...utils.component_helpers import create_error_chart
    from ...utils.callback_helpers import handle_callback_errors
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from config.settings import DATA_CONFIG
except ImportError:
    # Fallback for direct script execution
    import os, sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_emdat_data
    from src.utils.component_helpers import create_error_chart
    from src.utils.callback_helpers import handle_callback_errors
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from config.settings import DATA_CONFIG


def register_sample_chart_callbacks(app):
    """Register callbacks for a sample chart following the project's conventions."""

    @app.callback(
        Output('sample-chart', 'figure'),
        Input('main-country-filter', 'value')
    )
    @handle_callback_errors(default_title="Sample Chart Error")
    def render_sample_chart(selected_country):
        """Example small callback using the shared helpers."""
        # Load data via centralized loader
        data = load_emdat_data()
        countries = load_subsaharan_countries_and_regions_dict()

        if selected_country and 'ISO' in data.columns:
            data = data[data['ISO'] == selected_country]

        if data.empty:
            # Use shared error chart
            return create_error_chart("No data for selected country", chart_type='bar', title='Sample Chart')

        # Minimal plot (replace with actual logic)
        agg = data.groupby('Disaster Type').size().reset_index(name='count')
        fig = px.bar(agg, x='Disaster Type', y='count', title=f"Sample Chart for {selected_country}")
        return fig

*** End of file
