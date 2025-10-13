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

# Data analysis configuration
DATA_CONFIG = {
    'emdat_start_year': 1976,  # Starting year for EM-DAT analysis
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
        'data_config': DATA_CONFIG,
        'chart_styles': CHART_STYLES,
        'upload_config': UPLOAD_CONFIG
    }
    
    return config_map.get(key, {})