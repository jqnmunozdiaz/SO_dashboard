import pandas as pd
import os
import matplotlib.pyplot as plt

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_dir = os.path.join(project_root, 'data', 'raw', 'data_worldpopg2_fathom3_nov2025')

# Examine dynamic file
print("=" * 80)
print("DYNAMIC FILE")
print("=" * 80)
df_dynamic = pd.read_csv(os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_dynamic.csv'))
print(f"\nShape: {df_dynamic.shape}")
print(f"\nColumns: {df_dynamic.columns.tolist()}")
print(f"\nUnique worldpop_year values: {sorted(df_dynamic['worldpop_year'].unique())}")
print(f"\nFirst 5 rows:")
print(df_dynamic.head())
print(f"\nSample unique_ids: {df_dynamic['unique_id'].head(10).tolist()}")

# Examine static file
print("\n" + "=" * 80)
print("STATIC 2020 FILE")
print("=" * 80)
df_static = pd.read_csv(os.path.join(data_dir, 'df_agglo_worldpop_stats_geom_static_2020.csv'))
print(f"\nShape: {df_static.shape}")
print(f"\nColumns: {df_static.columns.tolist()}")
if 'worldpop_year' in df_static.columns:
    print(f"\nUnique worldpop_year values: {sorted(df_static['worldpop_year'].unique())}")
else:
    print("\nNo worldpop_year column in static file")
print(f"\nFirst 5 rows:")
print(df_static.head())

# Check unique_ids overlap
print("\n" + "=" * 80)
print("COMPARISON")
print("=" * 80)
dynamic_ids = set(df_dynamic['unique_id'].unique())
static_ids = set(df_static['unique_id'].unique())
print(f"\nUnique IDs in dynamic: {len(dynamic_ids)}")
print(f"Unique IDs in static: {len(static_ids)}")
print(f"IDs in both: {len(dynamic_ids.intersection(static_ids))}")
print(f"IDs only in dynamic: {len(dynamic_ids - static_ids)}")
print(f"IDs only in static: {len(static_ids - dynamic_ids)}")

# Get rows only in dynamic file
ids_only_in_dynamic = dynamic_ids - static_ids
df_only_dynamic = df_dynamic[df_dynamic['unique_id'].isin(ids_only_in_dynamic)].copy()

print("\n" + "=" * 80)
print("ROWS ONLY IN DYNAMIC FILE")
print("=" * 80)
print(f"\nTotal rows: {len(df_only_dynamic)}")
print(f"\nRows with non-null population: {df_only_dynamic['worldpop_population_total'].notna().sum()}")

# Filter for non-null population values
df_only_dynamic_with_pop = df_only_dynamic[df_only_dynamic['worldpop_population_total'].notna()]

if len(df_only_dynamic_with_pop) > 0:
    print(f"\nPopulation statistics:")
    print(df_only_dynamic_with_pop['worldpop_population_total'].describe())
    
    # Create histogram
    plt.figure(figsize=(12, 6))
    plt.hist(df_only_dynamic_with_pop['worldpop_population_total'], bins=50, edgecolor='black', alpha=0.7)
    plt.xlabel('Population', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title('Population Distribution for Cities Only in Dynamic File', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    
    print(f"\nSample of cities only in dynamic file:")
    print(df_only_dynamic_with_pop[['ISO3', 'unique_id', 'Agglomeration_Name', 'worldpop_year', 'worldpop_population_total']].head(10))
else:
    print("\nNo rows with population data found in dynamic-only cities")
