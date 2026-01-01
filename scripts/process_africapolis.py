import geopandas as gpd
import os

# Define paths
input_path = r"G:\My Drive\World_Bank_DRM\Datasets\Africapolis\Africapolis_2024\Africapolis_GIS_2024.gpkg"
output_dir = os.path.dirname(input_path)
output_path = os.path.join(output_dir, "Africapolis_GIS_2024_GeometryYear2020_CRS4326.gpkg")

gdf = gpd.read_file(input_path, engine='pyogrio')

print(f"Original CRS: {gdf.crs}")
print(f"Filtering rows where Select_Geometry_Year == 2020...")

# Filter
gdf_2020 = gdf[gdf['Select_Geometry_Year'] == 2020].copy()

print(f"Number of rows after filtering: {len(gdf_2020)}")

print("Reprojecting to EPSG:4326...")
gdf_2020 = gdf_2020.to_crs(epsg=4326)

print(f"Saving to {output_path}...")
gdf_2020.to_file(output_path, driver="GPKG", engine='pyogrio')

print("Processing complete.")
