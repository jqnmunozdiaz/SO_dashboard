"""
Configuration settings for the DRM dashboard
"""

# Dashboard configuration
DASHBOARD_CONFIG = {
    'title': 'Sub-Saharan Africa Disaster Risk Management Dashboard',
    'theme': 'bootstrap',
    'port': 8050,
    'host': '0.0.0.0',
    'debug': True
}

# Data analysis configuration
DATA_CONFIG = {
    'emdat_start_year': 1976,  # Starting year for EM-DAT analysis
    'emdat_end_year': 2025,    # Ending year for EM-DAT analysis
    'analysis_period': '1976 - Present'
}

# Chart styling
CHART_STYLES = {
    'colors': {
        'primary': '#2c3e50',
        'secondary': '#34495e',
        'success': '#2ecc71',
        'warning': '#f39c12',
        'danger': '#e74c3c',
        'info': '#3498db',
        'urban': '#1f77b4',
        'rural': '#2ca02c'
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

# File upload settings
UPLOAD_CONFIG = {
    'max_file_size': 50 * 1024 * 1024,  # 50MB
    'allowed_extensions': ['.csv', '.xlsx', '.json', '.geojson'],
    'upload_folder': 'data/uploads'
}