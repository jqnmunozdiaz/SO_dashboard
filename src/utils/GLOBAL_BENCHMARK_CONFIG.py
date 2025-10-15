
"""
Global benchmark configuration for all regions, expanding benchmark_config.py with additional regions
"""

from .benchmark_config import BENCHMARK_CONFIG

# Additional global regions
_ADDITIONAL_REGIONS = {
    'EAP': {
        'name': 'East Asia & Pacific',
        'color': '#2980b9'
    },
    'ECA': {
        'name': 'Europe & Central Asia',
        'color': '#8e44ad'
    },
    'LCR': {
        'name': 'Latin America & Caribbean',
        'color': '#d35400'
    },
    'MNA': {
        'name': 'Middle East & North Africa',
        'color': '#16a085'
    },
    'SAR': {
        'name': 'South Asia',
        'color': '#c0392b'
    }
}

# Merge BENCHMARK_CONFIG and additional regions
GLOBAL_BENCHMARK_CONFIG = dict(BENCHMARK_CONFIG)
GLOBAL_BENCHMARK_CONFIG.update(_ADDITIONAL_REGIONS)

def get_global_benchmark_colors():
    """Get dictionary of global benchmark region codes to colors"""
    return {code: config['color'] for code, config in GLOBAL_BENCHMARK_CONFIG.items()}

def get_global_benchmark_names():
    """Get dictionary of global benchmark region codes to names"""
    return {code: config['name'] for code, config in GLOBAL_BENCHMARK_CONFIG.items()}

def get_global_benchmark_options():
    """Get list of options for Dash checklist components (global)"""
    return [
        {'label': config['name'], 'value': code}
        for code, config in GLOBAL_BENCHMARK_CONFIG.items()
    ]
