import pandas as pd
import os

project_root = r"g:\My Drive\World_Bank_DRM\SO_dashboard"
wup_dir = os.path.join(project_root, "data", "processed", "WUP")

print("Files in processed/WUP:")
for f in os.listdir(wup_dir):
    print(f"- {f}")

for filename in ["WUP2025_National_Definitions_Population_processed.csv", "WUP2025_Level1_Population_Surface_processed.csv"]:
    path = os.path.join(wup_dir, filename)
    if os.path.exists(path):
        print(f"\n--- {filename} ---")
        df = pd.read_csv(path, nrows=5)
        print("Columns:", df.columns.tolist())
        
        # Try to find Burkina Faso (BFA)
        df_full = pd.read_csv(path)
        bfa = df_full[df_full.astype(str).apply(lambda x: x.str.contains('BFA|Burkina', case=False)).any(axis=1)]
        if not bfa.empty:
            print("Burkina Faso samples:")
            print(bfa.head(2))
            print(f"Total rows for BFA: {len(bfa)}")
        else:
            print("Burkina Faso not found with simple filter.")
