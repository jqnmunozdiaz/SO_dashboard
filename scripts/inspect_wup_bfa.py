import pandas as pd
import os

project_root = r"g:\My Drive\World_Bank_DRM\SO_dashboard"
wup_dir = os.path.join(project_root, "data", "processed", "WUP")

# National Definitions
nat_path = os.path.join(wup_dir, "WUP2025_National_Definitions_Population_processed.csv")
nat_df = pd.read_csv(nat_path)
bfa_nat = nat_df[nat_df['ISO3_Code'] == 'BFA']
print("=== NATIONAL DEFINITIONS (BFA) ===")
print("Unique categories:", bfa_nat['Category'].unique())
print("Years available:", sorted(bfa_nat['Year'].unique()))
print("\nSample records (recent years):")
print(bfa_nat[bfa_nat['Year'] >= 2020].sort_values(['Year', 'Category']))

# International (Level 1 / Degree of Urbanisation)
level1_path = os.path.join(wup_dir, "WUP2025_Level1_Population_Surface_processed.csv")
level1_df = pd.read_csv(level1_path)
bfa_level1 = level1_df[level1_df['ISO3_Code'] == 'BFA']
print("\n=== INTERNATIONAL / LEVEL 1 DEFINITIONS (BFA) ===")
print("Unique categories:", bfa_level1['Category'].unique())
print("Years available:", sorted(bfa_level1['Year'].unique()))
print("\nSample records (recent years):")
print(bfa_level1[bfa_level1['Year'] >= 2020].sort_values(['Year', 'Category']))
