"""
City-related helper functions for the DRM dashboard
"""

import pandas as pd


def categorize_city_size(pop):
    """
    Categorize city by population size
    
    Args:
        pop: Population value (absolute count, not in thousands)
        
    Returns:
        str: Size category name
    """
    if pd.isna(pop) or pop == 0:
        return 'Fewer than 300 000'
    elif pop >= 10_000_000:
        return '10 million or more'
    elif pop >= 5_000_000:
        return '5 to 10 million'
    elif pop >= 1_000_000:
        return '1 to 5 million'
    elif pop >= 500_000:
        return '500 000 to 1 million'
    elif pop >= 300_000:
        return '300 000 to 500 000'
    else:
        return 'Fewer than 300 000'


def get_city_size_category(population_thousands):
    """
    Determine city size category based on population in thousands
    (For compatibility with WUP data)
    
    Args:
        population_thousands: Population value in thousands
        
    Returns:
        str: Size category name
    """
    if population_thousands >= 10000:
        return '10 million or more'
    elif population_thousands >= 5000:
        return '5 to 10 million'
    elif population_thousands >= 1000:
        return '1 to 5 million'
    elif population_thousands >= 500:
        return '500 000 to 1 million'
    elif population_thousands >= 300:
        return '300 000 to 500 000'
    else:
        return 'Fewer than 300 000'
