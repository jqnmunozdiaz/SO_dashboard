#%%
"""
Script to create region visualization with red dots
Loads geospatial data from a shapefile and creates a map visualization
"""

import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from shapely.geometry import Point

# Add the project root to the path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


def create_region_image(
    shapefile_path,
    output_filename="region-dashboard.svg",
    output_dir=None,
    figsize=(16, 14),
    dot_color='red',
    dot_size=100,
    dot_alpha=0.7,
    density_multiplier=0.5
):
    """
    Create a visualization of a region with red dots filling the area.
    
    Parameters
    ----------
    shapefile_path : str or Path
        Path to the shapefile/geopackage to visualize
    output_filename : str, optional
        Name of the output file (default: "region-dashboard.svg")
    output_dir : str or Path, optional
        Directory to save the output (default: project_root/assets/images)
    figsize : tuple, optional
        Figure size as (width, height) (default: (16, 14))
    dot_color : str, optional
        Color of the dots (default: 'red')
    dot_size : int, optional
        Size of the dots (default: 100)
    dot_alpha : float, optional
        Transparency of the dots, 0-1 (default: 0.7)
    density_multiplier : float, optional
        Multiplier for point density (default: 0.5)
    
    Returns
    -------
    Path
        Path to the saved output file
    """
    # Read the shapefile
    region_gdf = gpd.read_file(shapefile_path)
    
    # Set output directory
    if output_dir is None:
        output_dir = project_root / "assets" / "images"
    else:
        output_dir = Path(output_dir)
    
    # Create the plot
    fig, ax = plt.subplots(1, 1, figsize=figsize, facecolor='none')
    ax.patch.set_alpha(0)
    
    # Remove figure borders and spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    
    # Get the bounds of the geometries
    bounds = region_gdf.bounds
    minx, miny = bounds.minx.min(), bounds.miny.min()
    maxx, maxy = bounds.maxx.max(), bounds.maxy.max()
    
    # Create a grid of points to fill with dots
    x_range = maxx - minx
    y_range = maxy - miny
    
    # Create grid points (adjust density as needed)
    n_points_x = int(x_range * density_multiplier)
    n_points_y = int(y_range * density_multiplier)
    
    x_coords = np.linspace(minx, maxx, n_points_x)
    y_coords = np.linspace(miny, maxy, n_points_y)
    
    # Create mesh grid
    xx, yy = np.meshgrid(x_coords, y_coords)
    points_x = xx.flatten()
    points_y = yy.flatten()
    
    # Create GeoDataFrame with points
    points_gdf = gpd.GeoDataFrame(
        geometry=[Point(x, y) for x, y in zip(points_x, points_y)],
        crs=region_gdf.crs
    )
    
    # Filter points that are within region geometries
    points_within = gpd.sjoin(points_gdf, region_gdf, predicate='within')
        
    # Plot the dots without edge colors
    if len(points_within) > 0:
        points_within.plot(ax=ax, color=dot_color, markersize=dot_size, 
                          alpha=dot_alpha, edgecolors='none')
        
    # Remove axis ticks for cleaner look
    ax.tick_params(labelsize=8)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlabel('')
    ax.set_ylabel('')
    
    # Set aspect ratio to equal for proper geographic representation
    ax.set_aspect('equal')
    
    # Tight layout
    plt.tight_layout()
    
    # Save the image as SVG with transparent background
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / output_filename
    plt.savefig(output_file, format='svg', bbox_inches='tight', 
                facecolor='none', edgecolor='none')
    
    plt.close(fig)
    
    print(f"Image saved to: {output_file}")
    return output_file


# Default execution: create SSA image
# data_raw_path = project_root / "data" / "raw"
# gpkg_file = data_raw_path / "africa_shp.gpkg"
# create_region_image(
#     shapefile_path=gpkg_file,
#     output_filename="SSA-dashboard.svg"
# )

# BFA image
data_raw_path = project_root / "data" / "raw" / "BFA_SHP"
gpkg_file = data_raw_path / "gadm41_BFA_0.shp"
create_region_image(
    shapefile_path=gpkg_file,
    output_filename="BFA-dashboard.svg",
    figsize=(16, 14),
    dot_color='red',
    dot_size=100,
    dot_alpha=0.7,
    density_multiplier=6
)

