"""
Configuration settings for the DRM dashboard
"""

import os
from typing import Dict, Any

# Dashboard configuration
DASHBOARD_CONFIG = {
    'title': 'Sub-Saharan Africa Disaster Risk Management Dashboard',
    'theme': 'bootstrap',
    'port': 8050,
    'host': '0.0.0.0',
    'debug': True
}

# Data file paths
DATA_PATHS = {
    'disasters': 'data/processed/disasters.csv',
    'urbanization': 'data/processed/urbanization.csv',
    'flood_risk': 'data/processed/flood_risk.csv',
    'countries': 'data/external/ssa_boundaries.geojson'
}

# Chart styling
CHART_STYLES = {
    'colors': {
        'primary': '#2c3e50',
        'secondary': '#34495e',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#3498db'
    },
    'background': {
        'plot': 'white',
        'paper': 'white'
    },
    'font': {
        'family': 'Arial, sans-serif',
        'size': 12,
        'color': '#2c3e50'
    }
}

# Disaster types and their colors
DISASTER_TYPES = {
    'flood': {'label': 'Flood', 'color': '#3498db'},
    'drought': {'label': 'Drought', 'color': '#e67e22'},
    'storm': {'label': 'Storm', 'color': '#9b59b6'},
    'earthquake': {'label': 'Earthquake', 'color': '#95a5a6'},
    'wildfire': {'label': 'Wildfire', 'color': '#e74c3c'},
    'epidemic': {'label': 'Epidemic', 'color': '#f39c12'},
    'volcanic': {'label': 'Volcanic Activity', 'color': '#c0392b'}
}

# Risk levels and colors
RISK_LEVELS = {
    'low': {'label': 'Low Risk', 'color': '#2ecc71', 'range': [0, 3]},
    'medium': {'label': 'Medium Risk', 'color': '#f39c12', 'range': [3, 6]},
    'high': {'label': 'High Risk', 'color': '#e74c3c', 'range': [6, 8]},
    'very_high': {'label': 'Very High Risk', 'color': '#8b0000', 'range': [8, 10]}
}

# Urbanization indicators
URBANIZATION_INDICATORS = {
    'urban_pop_pct': {
        'label': 'Urban Population %',
        'unit': '%',
        'description': 'Percentage of population living in urban areas'
    },
    'urban_growth': {
        'label': 'Urban Growth Rate',
        'unit': '%',
        'description': 'Annual urban population growth rate'
    },
    'pop_density': {
        'label': 'Population Density',
        'unit': 'people/km²',
        'description': 'Number of people per square kilometer'
    }
}

# Map settings
MAP_CONFIG = {
    'scope': 'africa',
    'center': {'lat': 0, 'lon': 20},
    'zoom': 2,
    'style': 'open-street-map'
}

# Data update intervals (in seconds)
UPDATE_INTERVALS = {
    'disaster_data': 3600,  # 1 hour
    'urbanization_data': 86400,  # 24 hours
    'flood_risk_data': 86400,  # 24 hours
}

# API endpoints (if using external data sources)
API_ENDPOINTS = {
    'world_bank': 'https://api.worldbank.org/v2/',
    'emdat': 'https://www.emdat.be/emdat_db/',
    'climate_data': 'https://climateknowledgeportal.worldbank.org/'
}

# File upload settings
UPLOAD_CONFIG = {
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'allowed_extensions': ['.csv', '.xlsx', '.json', '.geojson'],
    'upload_folder': 'data/uploads'
}

def get_config(key: str) -> Any:
    """
    Get configuration value by key
    
    Args:
        key: Configuration key
        
    Returns:
        Configuration value
    """
    config_map = {
        'dashboard': DASHBOARD_CONFIG,
        'data_paths': DATA_PATHS,
        'chart_styles': CHART_STYLES,
        'disaster_types': DISASTER_TYPES,
        'risk_levels': RISK_LEVELS,
        'urbanization_indicators': URBANIZATION_INDICATORS,
        'map_config': MAP_CONFIG,
        'update_intervals': UPDATE_INTERVALS,
        'api_endpoints': API_ENDPOINTS,
        'upload_config': UPLOAD_CONFIG
    }
    
    return config_map.get(key, {})