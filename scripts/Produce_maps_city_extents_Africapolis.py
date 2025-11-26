#%%
"""
Script to explore and produce maps from Africapolis GIS 2024 data
"""

import os
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

ISO3 = 'BFA'  # Burkina Faso
output_dir = r'C:\Users\jqnmu\OneDrive\World_Bank_DRM\Burkina Faso\Data'
image_output_dir = os.path.join(output_dir, 'City_extent_images')

# Create output directory if it doesn't exist
os.makedirs(image_output_dir, exist_ok=True)

# Load Africapolis GIS 2024 geopackage
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
gpkg_path = os.path.join(project_root, 'data', 'raw', 'Africapolis_GIS_2024.gpkg')
gdf = gpd.read_file(gpkg_path)

# Filter for the specified country ISO3 code and year 2020
gdf = gdf[(gdf['ISO3'] == ISO3) & (gdf['Select_Geometry_Year'] == 2020)]

gdf = gdf[['Agglomeration_Name','Population_2020', 'geometry']]

# Export the filtered data to the specified directory
output_path = os.path.join(output_dir, f'{ISO3}_africapolis_2020.gpkg')
gdf.to_file(output_path, driver='GPKG')


#%%
# Get the 20 largest cities by population
top_20_cities = gdf.nlargest(20, 'Population_2020').copy()

# Reproject to Web Mercator for basemap compatibility
top_20_cities = top_20_cities.to_crs(epsg=3857)

# Create maps for each of the top 20 cities
for idx, row in top_20_cities.iterrows():
    city_name = row['Agglomeration_Name']
    population = row['Population_2020']
    
    print(f"Creating map for {city_name} (Pop: {population:,.0f})...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 10))
    
    # Plot the city extent
    top_20_cities[top_20_cities['Agglomeration_Name'] == city_name].plot(
        ax=ax,
        facecolor='#d62728',
        edgecolor='#8b0000',
        alpha=0.6,
        linewidth=2
    )
    
    # Add buffer for context (500m buffer)
    bounds = top_20_cities[top_20_cities['Agglomeration_Name'] == city_name].total_bounds
    buffer = 2000  # 2km buffer in meters
    ax.set_xlim(bounds[0] - buffer, bounds[2] + buffer)
    ax.set_ylim(bounds[1] - buffer, bounds[3] + buffer)
    
    # Add basemap (OpenStreetMap)
    try:
        cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik, zoom='auto')
    except:
        try:
            cx.add_basemap(ax, source=cx.providers.CartoDB.Positron, zoom='auto')
        except:
            print(f"  Warning: Could not load basemap for {city_name}")
    
    # Add title
    ax.set_title(f'{city_name}\nPopulation 2020: {population:,.0f}', 
                 fontsize=16, fontweight='bold', pad=20)
    
    # Remove axes
    ax.set_axis_off()
    
    # Tight layout
    plt.tight_layout()
    
    # Save the figure
    safe_city_name = city_name.replace('/', '_').replace('\\', '_').replace(' ', '_')
    output_file = os.path.join(image_output_dir, f'{safe_city_name}_{ISO3}_2020.png')
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()

print(f"\nAll maps saved to: {image_output_dir}")

# %%
