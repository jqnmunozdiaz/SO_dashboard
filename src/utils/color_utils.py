"""
Color utilities for disaster types
"""

from typing import Dict


# Hardcoded disaster type colors - edit these directly to change colors
DISASTER_COLORS = {
    'Drought': '#D68910',           # Refined golden orange (dry, sandy)
    'Earthquake': '#8B4513',        # Rich saddle brown (earth, geological)
    'Epidemic': '#27AE60',          # Vibrant emerald green (medical/health)
    'Extreme temperature': '#E74C3C',  # Strong red (heat, danger)
    'Flood': '#3498DB',             # Clear blue (water, floods)
    'Mass movement (dry)': '#A569BD', # Refined purple (landslides)
    'Mass movement (wet)': '#8E44AD', # Deeper purple (wet landslides)
    'Storm': '#5D6D7E',             # Storm gray-blue (stormy skies)
    'Volcanic activity': '#C0392B',  # Deep crimson red (lava, volcanic)
    'Wildfire': "#340000",          # Vibrant orange (flames, fire)
    
    # Default color
    'default': '#000000'
}

# City size category colors for urbanization charts
CITY_SIZE_COLORS = {
    '10 million or more': '#e74c3c',      # Red
    '5 to 10 million': '#e67e22',          # Orange
    '1 to 5 million': '#f39c12',           # Yellow-Orange
    '500 000 to 1 million': '#3498db',     # Blue
    '300 000 to 500 000': '#2ecc71',       # Green
    'Fewer than 300 000': '#95a5a6'        # Gray
}

def get_disaster_color(disaster_type: str, colors_dict: Dict[str, str] = None) -> str:
    """
    Get color for a specific disaster type
    
    Args:
        disaster_type: Name of the disaster type
        colors_dict: Optional pre-loaded colors dictionary
        
    Returns:
        Hex color code for the disaster type
    """
    if colors_dict is None:
        colors_dict = DISASTER_COLORS
    
    return colors_dict.get(disaster_type, colors_dict.get('default', '#000000'))


def get_city_size_color(size_category: str, colors_dict: Dict[str, str] = None) -> str:
    """
    Get color for a specific city size category
    
    Args:
        size_category: Name of the city size category
        colors_dict: Optional pre-loaded colors dictionary
        
    Returns:
        Hex color code for the city size category
    """
    if colors_dict is None:
        colors_dict = CITY_SIZE_COLORS
    
    return colors_dict.get(size_category, '#95a5a6')  # Default gray

