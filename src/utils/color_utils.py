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

