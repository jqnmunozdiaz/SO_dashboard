#%%
"""
Script to create Sub-Saharan Africa visualization with red dots
Loads geospatial data from africa.shp (or similar) and creates a map visualization
"""

import os
import sys
import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Add the project root to the path for imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Define paths
data_raw_path = project_root / "data" / "raw"
output_path = project_root / "assets" / "images"

gpkg_file = data_raw_path / "africa_shp.gpkg"
africa_gdf = gpd.read_file(gpkg_file)

#%%
# Create the plot
fig, ax = plt.subplots(1, 1, figsize=(16, 14), facecolor='none')
ax.patch.set_alpha(0)

# Remove figure borders and spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Plot the base map
# africa_gdf.plot(ax=ax, color='lightgray', edgecolor='black', linewidth=0.5)

# Get the bounds of the geometries
bounds = africa_gdf.bounds
minx, miny = bounds.minx.min(), bounds.miny.min()
maxx, maxy = bounds.maxx.max(), bounds.maxy.max()

# Create a grid of points to fill with red dots
# Adjust density based on the area size
x_range = maxx - minx
y_range = maxy - miny

# Create grid points (adjust density as needed)
n_points_x = int(x_range * 0.5)  # Adjust multiplier for density
n_points_y = int(y_range * 0.5)  # Adjust multiplier for density

x_coords = np.linspace(minx, maxx, n_points_x)
y_coords = np.linspace(miny, maxy, n_points_y)

# Create mesh grid
xx, yy = np.meshgrid(x_coords, y_coords)
points_x = xx.flatten()
points_y = yy.flatten()

# Create GeoDataFrame with points
from shapely.geometry import Point
points_gdf = gpd.GeoDataFrame(
    geometry=[Point(x, y) for x, y in zip(points_x, points_y)],
    crs=africa_gdf.crs
)

# Filter points that are within Africa geometries
points_within = gpd.sjoin(points_gdf, africa_gdf, predicate='within')
    
# Plot the red dots without edge colors
if len(points_within) > 0:
    points_within.plot(ax=ax, color='red', markersize=100, alpha=0.7, edgecolors='none')
    
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
output_path.mkdir(parents=True, exist_ok=True)
output_file = output_path / "SSA-dashboard.svg"
plt.savefig(output_file, format='svg', bbox_inches='tight', 
            facecolor='none', edgecolor='none')
