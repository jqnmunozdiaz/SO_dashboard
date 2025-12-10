#%%
# 
"""
Check whether Africapolis 2020 geometries fully contain 2015 geometries
"""
import random
import geopandas as gpd
import pandas as pd

# Hardcoded parameters
GPKG_FILE = 'data/raw/Africapolis_GIS_2024.gpkg'
SAMPLE_SIZE = 1000
SEED = 42
OUTPUT_FILE = 'scripts/africapolis_containment_results.csv'
NAME_COL = 'Agglomeration_ID'
# Area ratio threshold: 2020 area >= (threshold * 2015 area) -> considered 'covers' by area
# Default 1.05 means 2020 must be at least 5% larger than 2015 to be considered covering
AREA_RATIO_THRESHOLD = 0.9999

#%%
# Load GPKG
gdf = gpd.read_file(GPKG_FILE)

# Filter by year
g2015 = gdf[gdf['Select_Geometry_Year'] == 2015].copy()
g2020 = gdf[gdf['Select_Geometry_Year'] == 2020].copy()

# Get unique cities for each year
cities_2015 = g2015[NAME_COL].unique().tolist()
cities_2020 = g2020[NAME_COL].unique().tolist()

# Find common cities
common = list(set(cities_2015) & set(cities_2020))
print(f"Common cities: {len(common)}")

#%%

# Sample cities
random.seed(SEED)
k = min(SAMPLE_SIZE, len(common))
sampled_cities = random.sample(common, k)
print(f"Sampled {k} cities")

# Check containment
results = []
for city in sampled_cities:
    geom_2015 = g2015[g2015[NAME_COL] == city]['geometry'].iloc[0]
    geom_2020 = g2020[g2020[NAME_COL] == city]['geometry'].iloc[0]

    # Area-based comparison: consider 2020 'covers' 2015 if area is larger by threshold
    area_2015 = geom_2015.area
    area_2020 = geom_2020.area
    # Protect against zero/invalid areas
    try:
        covers_by_area = (area_2020 >= (AREA_RATIO_THRESHOLD * area_2015)) if area_2015 > 0 else False
    except Exception:
        covers_by_area = False

    results.append({
        'city_name': city,
        'covers_by_area_threshold': covers_by_area,
        'area_ratio_2020_over_2015': (area_2020 / area_2015) if area_2015 > 0 else None,
        'area_2015': area_2015,
        'area_2020': area_2020,
    })

# Create results dataframe
out_df = pd.DataFrame(results)

# Print summary
total = len(out_df)
covers_by_area_count = out_df['covers_by_area_threshold'].sum()
print(f"\nResults:")
print(f"Sampled: {total} cities")
print(f"Area-based covers (ratio >= {AREA_RATIO_THRESHOLD}): {covers_by_area_count}/{total}")

# Print cities where covers is False
not_covered = out_df[out_df['covers_by_area_threshold'] == False]
if not not_covered.empty:
    print(f"\n{len(not_covered)} cities where 2020 does NOT cover 2015 (area-based):")
    for idx, row in not_covered.iterrows():
        ratio = row['area_ratio_2020_over_2015']
        print(f"  - {row['city_name']}: area_ratio={ratio:.4f} (2020 is {(ratio*100-100):.1f}% {'larger' if ratio > 1 else 'smaller'})")
else:
    print("\nAll sampled cities have 2020 area >= 2015 area * threshold")

# Save results
out_df.to_csv(OUTPUT_FILE, index=False)
print(f"\nSaved results to {OUTPUT_FILE}")
# %%
