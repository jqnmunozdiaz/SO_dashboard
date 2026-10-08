import os
import pandas as pd

project_root = r"g:\My Drive\World_Bank_DRM\SO_dashboard"
level1_path = os.path.join(project_root, "data", "processed", "WUP", "WUP2025_Level1_Population_Surface_processed.csv")
level1_df = pd.read_csv(level1_path)

# Filter for Burkina Faso (BFA)
bfa_level1 = level1_df[level1_df['ISO3_Code'] == 'BFA'].copy()

# Pivot level 1 to get Categories (Cities, Towns, Rural) as columns
bfa_pivot = bfa_level1.pivot_table(
    index='Year',
    columns='Category',
    values='Pop',
    aggfunc='first'
).reset_index()

bfa_pivot['Int_Urban_Pop'] = bfa_pivot['Cities'] + bfa_pivot['Towns']
bfa_pivot['Total_Pop'] = bfa_pivot['Cities'] + bfa_pivot['Towns'] + bfa_pivot['Rural']

# Calculate shares
bfa_pivot['Cities_Share'] = bfa_pivot['Cities'] / bfa_pivot['Total_Pop']
bfa_pivot['Towns_Share'] = bfa_pivot['Towns'] / bfa_pivot['Total_Pop']
bfa_pivot['Rural_Share'] = bfa_pivot['Rural'] / bfa_pivot['Total_Pop']

print("Burkina Faso Disaggregated International Population (Selected Years):")
print("=" * 120)
print(f"{'Year':<6} | {'Cities Pop':<15} | {'Cities Share':<12} | {'Towns Pop':<15} | {'Towns Share':<12} | {'Rural Pop':<15} | {'Rural Share':<12}")
print("-" * 120)

selected_years = [1975, 1985, 1995, 2000, 2005, 2010, 2015, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
for year in selected_years:
    row = bfa_pivot[bfa_pivot['Year'] == year]
    if not row.empty:
        r = row.iloc[0]
        print(f"{int(year):<6} | {r['Cities']:15,.0f} | {r['Cities_Share']:12.2%} | {r['Towns']:15,.0f} | {r['Towns_Share']:12.2%} | {r['Rural']:15,.0f} | {r['Rural_Share']:12.2%}")
print("=" * 120)
