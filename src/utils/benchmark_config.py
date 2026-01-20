"""
Centralized configuration for regional benchmarks used across urbanization charts
"""

# Regional benchmark configuration
BENCHMARK_CONFIG = {
    'SSA': {
        'name': 'Sub-Saharan Africa',
        'color': '#e74c3c'  # Red
    },
    'AFE': {
        'name': 'Eastern and Southern Africa', 
        'color': '#f39c12'  # Orange
    },
    'AFW': {
        'name': 'Western and Central Africa',
        'color': '#27ae60'  # Green
    }
}

# Full regional benchmark configuration including all World Bank regions
# Extends BENCHMARK_CONFIG with additional global regions
# Region codes match those in WB_Classification.csv
_ADDITIONAL_REGIONS = {
    'EAP': {
        'name': 'East Asia & Pacific',
        'color': '#2980b9'  # Blue
    },
    'ECA': {
        'name': 'Europe & Central Asia',
        'color': '#8e44ad'  # Purple
    },
    'LCN': {
        'name': 'Latin America & Caribbean',
        'color': '#d35400'  # Deep Orange
    },
    'MENA': {
        'name': 'Middle East & North Africa',
        'color': '#16a085'  # Teal
    },
    'NAC': {
        'name': 'North America',
        'color': '#34495e'  # Dark Gray
    },
    'SAS': {
        'name': 'South Asia',
        'color': '#c0392b'  # Dark Red
    }
}

# Merge BENCHMARK_CONFIG with additional regions
FULL_REGIONAL_BENCHMARK_CONFIG = {**BENCHMARK_CONFIG, **_ADDITIONAL_REGIONS}

def get_full_regional_benchmark_names():
    """Get dictionary of all regional benchmark codes to names"""
    return {code: config['name'] for code, config in FULL_REGIONAL_BENCHMARK_CONFIG.items()}

def get_full_regional_benchmark_colors():
    """Get dictionary of all regional benchmark codes to colors"""
    return {code: config['color'] for code, config in FULL_REGIONAL_BENCHMARK_CONFIG.items()}

def get_full_regional_benchmark_options():
    """Get list of options for Dash dropdown components (all regions)"""
    return [
        {'label': config['name'], 'value': code}
        for code, config in FULL_REGIONAL_BENCHMARK_CONFIG.items()
    ]

# Convenience functions for backward compatibility
def get_benchmark_colors():
    """Get dictionary of benchmark region codes to colors"""
    return {code: config['color'] for code, config in BENCHMARK_CONFIG.items()}

def get_benchmark_names():
    """Get dictionary of benchmark region codes to names"""
    return {code: config['name'] for code, config in BENCHMARK_CONFIG.items()}

def get_benchmark_options():
    """Get list of options for Dash checklist components"""
    return [
        {'label': config['name'], 'value': code}
        for code, config in BENCHMARK_CONFIG.items()
    ]