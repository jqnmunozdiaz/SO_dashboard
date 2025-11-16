#%%
"""
Merge Africapolis_GIS_2024 with agglomeration_population_stats.csv
Filter Africapolis for 2020 geometry year, create ID column, and merge with population data
Includes function to visualize CAGR distributions by country with variability analysis
"""

import pandas as pd
import geopandas as gpd
import os
import numpy as np
import matplotlib.pyplot as plt

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define file paths
africapolis_gpkg = os.path.join(project_root, 'data', 'raw', 'Africapolis_GIS_2024.gpkg')

# Years for comparison
year1 = 2015
year2 = 2020

df = gpd.read_file(africapolis_gpkg)

# Step 1: Filter Africapolis for Select_Geometry_Year
df = df[df['Select_Geometry_Year'] == year2]
# df = df[df['ISO3'] == 'NGA']

# Ensure numeric types
df[f'Population_{year1}'] = pd.to_numeric(df[f'Population_{year1}'], errors='coerce')
df[f'Population_{year2}'] = pd.to_numeric(df[f'Population_{year2}'], errors='coerce')

# Compute 5-year CAGR (2015 -> 2020) safely (as fractional growth, e.g. 0.02 == 2%)
periods = year2 - year1
# valid = (df[f'Population_{year1}'] > 0) & (df[f'Population_{year2}'] > 0)
# df.loc[valid, f'pop_cagr_{year1}_{year2}'] = (
#     (df.loc[valid, f'Population_{year2}'] / df.loc[valid, f'Population_{year1}']) ** (1 / periods) - 1
# )
# df.loc[~valid, f'pop_cagr_{year1}_{year2}'] = np.nan

df[f'pop_cagr_{year1}_{year2}'] = ((df[f'Population_{year2}'] / df[f'Population_{year1}']) ** (1 / periods) - 1)

# Remove infinite values and outliers from CAGR
df[f'pop_cagr_{year1}_{year2}'] = df[f'pop_cagr_{year1}_{year2}'].replace([np.inf, -np.inf], np.nan)

# Remove rows with NaN in CAGR column
df = df.dropna(subset=[f'pop_cagr_{year1}_{year2}'])

# Create histogram of the CAGR variable
plt.figure(figsize=(10, 6))
plt.hist(df[f'pop_cagr_{year1}_{year2}'], bins=50, edgecolor='black')
plt.title(f'Histogram of Population CAGR ({year1} to {year2})')
plt.xlabel('CAGR')
plt.ylabel('Frequency')
plt.show()
