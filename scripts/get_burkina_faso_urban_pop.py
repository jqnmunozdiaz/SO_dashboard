import os
import pandas as pd

project_root = r"g:\My Drive\World_Bank_DRM\SO_dashboard"
wup_dir = os.path.join(project_root, "data", "processed", "WUP")

# Load national definitions pivoted data
nat_pivot_path = os.path.join(wup_dir, "WUP2025_National_Definitions_Population_processed_pivoted.csv")
nat_df = pd.read_csv(nat_pivot_path)
bfa_nat = nat_df[nat_df['ISO3_Code'] == 'BFA'].copy()

# Load international definitions (Level 1 / DEGURBA)
level1_path = os.path.join(wup_dir, "WUP2025_Level1_Population_Surface_processed.csv")
level1_df = pd.read_csv(level1_path)
bfa_level1 = level1_df[level1_df['ISO3_Code'] == 'BFA'].copy()

# Pivot level 1 to get Cities, Towns, Rural in columns
bfa_level1_pivot = bfa_level1.pivot_table(
    index='Year',
    columns='Category',
    values='Pop',
    aggfunc='first'
).reset_index()

# Under the Degree of Urbanisation (DEGURBA Level 1), the international urban population
# is the sum of population in Cities (dense) and Towns (semi-dense / intermediate).
bfa_level1_pivot['Int_Urban_Pop'] = bfa_level1_pivot['Cities'] + bfa_level1_pivot['Towns']
bfa_level1_pivot['Int_Total_Pop'] = bfa_level1_pivot['Cities'] + bfa_level1_pivot['Towns'] + bfa_level1_pivot['Rural']
bfa_level1_pivot['Int_Urbanization_Rate'] = bfa_level1_pivot['Int_Urban_Pop'] / bfa_level1_pivot['Int_Total_Pop']

# Merge national and international data for comparison
bfa_nat = bfa_nat[['Year', 'Urban_Pop', 'Total_Pop', 'Urbanization_Rate']].rename(columns={
    'Urban_Pop': 'Nat_Urban_Pop',
    'Total_Pop': 'Nat_Total_Pop',
    'Urbanization_Rate': 'Nat_Urbanization_Rate'
})

comparison_df = pd.merge(bfa_nat, bfa_level1_pivot[['Year', 'Cities', 'Towns', 'Int_Urban_Pop', 'Int_Total_Pop', 'Int_Urbanization_Rate']], on='Year', how='outer')

# Format values for readability
comparison_df = comparison_df.sort_values('Year')

# Save to output folder
output_dir = os.path.join(project_root, "outputs", "Custom_Figure_Burkina_Faso")
os.makedirs(output_dir, exist_ok=True)
csv_output = os.path.join(output_dir, "burkina_faso_urban_population_comparison.csv")
comparison_df.to_csv(csv_output, index=False)

print(f"Data saved to: {csv_output}\n")
print("Burkina Faso Urban Population Comparison (Selected Years):")
print("=" * 110)
print(f"{'Year':<6} | {'National Def Urban Pop':<23} | {'National Urb Rate':<17} | {'Int Def Urban Pop':<20} | {'Int Urb Rate':<14} | {'Diff (Int - Nat)':<18}")
print("-" * 110)

selected_years = [1975, 1985, 1995, 2000, 2005, 2010, 2015, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
for year in selected_years:
    row = comparison_df[comparison_df['Year'] == year]
    if not row.empty:
        r = row.iloc[0]
        nat_pop = r['Nat_Urban_Pop']
        nat_rate = r['Nat_Urbanization_Rate']
        int_pop = r['Int_Urban_Pop']
        int_rate = r['Int_Urbanization_Rate']
        diff = int_pop - nat_pop
        
        print(f"{int(year):<6} | {nat_pop:23,.0f} | {nat_rate:17.2%} | {int_pop:20,.0f} | {int_rate:14.2%} | {diff:+18,.0f}")
print("=" * 110)
