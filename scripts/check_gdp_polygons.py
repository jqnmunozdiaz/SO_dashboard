import geopandas as gpd
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
polygon_path = os.path.join(project_root, 'data', 'raw', 'GDP_Kummu', 'polyg_adm0_gdp_perCapita_1990_2022.gpkg')

print("Loading polygon data...")
gdf = gpd.read_file(polygon_path)

print("\nColumns:", list(gdf.columns))
print("\nFirst few rows:")
print(gdf.head())

print("\nISO-related columns:")
iso_cols = [c for c in gdf.columns if 'iso' in c.lower() or 'adm' in c.lower() or 'code' in c.lower()]
print(iso_cols)

if iso_cols:
    for col in iso_cols[:5]:
        print(f"\n{col} sample values:")
        print(gdf[col].head(10).tolist())
