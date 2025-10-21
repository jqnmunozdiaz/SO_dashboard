"""
Callbacks for Cities Distribution d3.js treemap visualization
Shows distribution of urban population across city size categories using d3.js
"""

from dash import Input, Output
import pandas as pd

try:
    from ...utils.data_loader import load_city_size_distribution
    from ...utils.country_utils import load_subsaharan_countries_and_regions_dict
    from ...utils.download_helpers import prepare_csv_download
    from ...utils.color_utils import CITY_SIZE_COLORS
except ImportError:
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    from src.utils.data_loader import load_city_size_distribution
    from src.utils.country_utils import load_subsaharan_countries_and_regions_dict
    from src.utils.download_helpers import prepare_csv_download
    from src.utils.color_utils import CITY_SIZE_COLORS

def register_cities_distribution_callbacks(app):
    """Register callbacks for Cities Distribution d3.js treemap chart"""
    
    # Load static data once at registration time for performance
    data = load_city_size_distribution()
    countries_dict = load_subsaharan_countries_and_regions_dict()
    
    @app.callback(
        Output('cities-distribution-store', 'data'),
        [
            Input('main-country-filter', 'value'),
            Input('cities-distribution-year-filter', 'value')
        ],
        prevent_initial_call=False
    )
    def update_cities_distribution_store(selected_country, selected_year):
        """Populate data store for d3.js rendering"""
        try:
            # Handle no country selected
            if not selected_country:
                return {
                    'data': [],
                    'error': 'No country selected',
                    'country_name': '',
                    'year': selected_year,
                    'colors': CITY_SIZE_COLORS
                }
            
            # Filter for selected country and year
            filtered_data = data[
                (data['Country Code'] == selected_country) & 
                (data['Year'] == selected_year)
            ].copy()
            
            country_name = countries_dict.get(selected_country, selected_country)
            
            if filtered_data.empty:
                return {
                    'data': [],
                    'error': f'No data available for {country_name} in {selected_year}',
                    'country_name': country_name,
                    'year': selected_year,
                    'colors': CITY_SIZE_COLORS
                }
            
            # Define size categories in order
            size_categories_ordered = [
                '10 million or more',
                '5 to 10 million',
                '1 to 5 million',
                '500 000 to 1 million',
                '300 000 to 500 000',
                'Fewer than 300 000'
            ]
            
            # Create sorting keys
            category_order = {cat: i for i, cat in enumerate(size_categories_ordered)}
            filtered_data['category_sort_order'] = filtered_data['Size Category'].map(category_order)
            filtered_data['is_other_cities'] = filtered_data['City Name'].str.startswith('Other cities').astype(int)
            
            # Sort by: 1) size category, 2) named cities before "Other cities", 3) population descending
            sorted_data = filtered_data.sort_values(
                ['category_sort_order', 'is_other_cities', 'Population'], 
                ascending=[True, True, False]
            ).reset_index(drop=True)
            
            # Prepare data for d3.js
            city_data = []
            for _, row in sorted_data.iterrows():
                city_data.append({
                    'name': row['City Name'],
                    'population': float(row['Population'] * 1000),  # Convert from thousands
                    'size_category': row['Size Category'],
                    'color': CITY_SIZE_COLORS.get(row['Size Category'], '#95a5a6')
                })
            
            return {
                'data': city_data,
                'country_name': country_name,
                'year': int(selected_year),
                'colors': CITY_SIZE_COLORS,
                'size_categories': size_categories_ordered,
                'error': None
            }
            
        except Exception as e:
            return {
                'data': [],
                'error': f'Error loading data: {str(e)}',
                'country_name': '',
                'year': selected_year,
                'colors': CITY_SIZE_COLORS
            }
    
    @app.callback(
        Output('cities-distribution-download', 'data'),
        Input('cities-distribution-download-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def download_cities_distribution_data(n_clicks):
        """Download city size distribution data as CSV"""
        if n_clicks is None or n_clicks == 0:
            return None
        
        try:
            return prepare_csv_download(data, "cities_individual")
        
        except Exception as e:
            print(f"Error preparing download: {str(e)}")
            return None
