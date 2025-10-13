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
        'name': 'Africa Eastern and Southern', 
        'color': '#f39c12'  # Orange
    },
    'AFW': {
        'name': 'Africa Western and Central',
        'color': '#27ae60'  # Green
    }
}

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