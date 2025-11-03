"""
Callbacks for Population & Economic Activity visualization
Shows side-by-side raster images of population and GDP distribution
"""

from dash import Input, Output, html
import os
import base64

try:
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
except ImportError:
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict


def load_image_as_base64(image_path):
    """Load an image file and return it as a base64 encoded data URI"""
    try:
        with open(image_path, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode('ascii')
        return f'data:image/png;base64,{encoded}'
    except Exception as e:
        print(f"Error loading image {image_path}: {str(e)}")
        return None

def register_population_economic_activity_callbacks(app):
    """Register callbacks for Population & Economic Activity visualization"""
    
    @app.callback(
        Output('population-economic-activity-container', 'children'),
        [Input('main-country-filter', 'value')],
        prevent_initial_call=False
    )
    def generate_population_economic_activity_display(selected_country):
        """Generate side-by-side population and GDP raster images"""
        try:
            countries_dict = load_subsaharan_countries_and_regions_dict()
            
            # Handle no country selected
            if not selected_country:
                return html.Div([
                    html.Div([
                        html.P("Please select a country to view population and economic activity maps.",
                               style={'textAlign': 'center', 'color': '#6B7280', 'padding': '2rem'})
                    ])
                ], style={'width': '100%'})
            
            # Get country name for title
            country_name = countries_dict.get(selected_country, selected_country)
            
            # Construct image paths
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            pop_image_path = os.path.join(project_root, 'data', 'processed', 'gdp_pop_raster_images', f'{selected_country}_POP_2020.png')
            gdp_image_path = os.path.join(project_root, 'data', 'processed', 'gdp_pop_raster_images', f'{selected_country}_GDP_2020.png')
            
            # Check if images exist
            pop_exists = os.path.exists(pop_image_path)
            gdp_exists = os.path.exists(gdp_image_path)
            
            # Create image components or error messages
            if pop_exists:
                pop_base64 = load_image_as_base64(pop_image_path)
                if pop_base64:
                    pop_component = html.Img(
                        src=pop_base64,
                        style={'width': '100%', 'height': 'auto', 'maxHeight': '600px', 'objectFit': 'contain'}
                    )
                else:
                    pop_component = html.Div([
                        html.P("Error loading population distribution figure.",
                               style={'textAlign': 'center', 'color': '#EF4444', 'padding': '2rem'})
                    ], style={'border': '2px dashed #EF4444', 'borderRadius': '8px', 'minHeight': '300px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            else:
                pop_component = html.Div([
                    html.P("No figure available for population distribution.",
                           style={'textAlign': 'center', 'color': '#EF4444', 'padding': '2rem'})
                ], style={'border': '2px dashed #EF4444', 'borderRadius': '8px', 'minHeight': '300px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            
            if gdp_exists:
                gdp_base64 = load_image_as_base64(gdp_image_path)
                if gdp_base64:
                    gdp_component = html.Img(
                        src=gdp_base64,
                        style={'width': '100%', 'height': 'auto', 'maxHeight': '600px', 'objectFit': 'contain'}
                    )
                else:
                    gdp_component = html.Div([
                        html.P("Error loading GDP distribution figure.",
                               style={'textAlign': 'center', 'color': '#EF4444', 'padding': '2rem'})
                    ], style={'border': '2px dashed #EF4444', 'borderRadius': '8px', 'minHeight': '300px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            else:
                gdp_component = html.Div([
                    html.P("No figure available for GDP distribution.",
                           style={'textAlign': 'center', 'color': '#EF4444', 'padding': '2rem'})
                ], style={'border': '2px dashed #EF4444', 'borderRadius': '8px', 'minHeight': '300px', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'})
            
            # Return side-by-side layout
            return html.Div([
                html.Div([
                    html.Div([
                        html.H6([html.B(country_name), ' | Population Distribution (2020)'], 
                                className='chart-title'),
                        pop_component
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '1rem'}),
                    html.Div([
                        html.H6([html.B(country_name), ' | GDP Distribution (2020)'], 
                                className='chart-title'),
                        gdp_component
                    ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '1rem'})
                ], style={'display': 'flex', 'justifyContent': 'space-between', 'gap': '2%'})
            ])
            
        except Exception as e:
            print(f"Error loading population and economic activity images: {str(e)}")
            return html.Div([
                html.P(f"Error loading data: {str(e)}",
                       style={'textAlign': 'center', 'color': '#EF4444', 'padding': '2rem'})
            ])
