"""
Script to clean and process WPP 2024 Total Population data
Extracts total population data for countries with ISO3 codes
"""

import pandas as pd
import os

# Get the project root directory
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

input_file = os.path.join(project_root, 'data', 'raw', 'Urban', 'WPP2024_Demographic_Indicators_Medium.csv')
output_file = os.path.join(project_root, 'data', 'processed', 'WPP2024_Total_Population.csv')
wb_classification_file = os.path.join(project_root, 'data', 'Definitions', 'WB_Classification.csv')

df = pd.read_csv(input_file, low_memory=False) # Read the CSV file with low_memory=False to avoid dtype warnings

df = df[df['ISO3_code'].notna()].copy() # Filter to keep only rows with ISO3_code

# Select and rename columns
df = df[['Time', 'ISO3_code', 'TPopulation1Jan']].copy()
df.rename(columns={'Time': 'Year', 'ISO3_code': 'ISO3', 'TPopulation1Jan': 'population'}, inplace=True)
df['population'] = df['population'] * 1_000

# Load World Bank Classification to get regional groupings
wb_class = pd.read_csv(wb_classification_file)

# Get country lists for each region
afe_countries = wb_class[wb_class['Subregion Code'] == 'AFE']['ISO3'].tolist()
afw_countries = wb_class[wb_class['Subregion Code'] == 'AFW']['ISO3'].tolist()
ssa_countries = wb_class[wb_class['Region Code'] == 'SSA']['ISO3'].tolist()

print(f"AFE countries: {len(afe_countries)}")
print(f"AFW countries: {len(afw_countries)}")
print(f"SSA countries: {len(ssa_countries)}")

# AFE aggregation
afe_data = df[df['ISO3'].isin(afe_countries)].groupby('Year')['population'].sum().reset_index()
afe_data['ISO3'] = 'AFE'

# AFW aggregation
afw_data = df[df['ISO3'].isin(afw_countries)].groupby('Year')['population'].sum().reset_index()
afw_data['ISO3'] = 'AFW'

# SSA aggregation
ssa_data = df[df['ISO3'].isin(ssa_countries)].groupby('Year')['population'].sum().reset_index()
ssa_data['ISO3'] = 'SSA'

# Combine original data with regional aggregations
df_final = pd.concat([df, afe_data, afw_data, ssa_data], ignore_index=True)

# Sort by ISO3 and Year
df_final = df_final.sort_values(['ISO3', 'Year']).reset_index(drop=True)

# Save to CSV
df_final.to_csv(output_file, index=False)

print(f"\nProcessed data saved to: {output_file}")
print(f"Final data: {len(df_final)} rows")
print(f"Years range: {df_final['Year'].min()} - {df_final['Year'].max()}")
print(f"Number of countries (including regions): {df_final['ISO3'].nunique()}")
print(f"\nRegional aggregation sample:")
print(df_final[df_final['ISO3'].isin(['SSA', 'AFE', 'AFW'])].head(15))
print(f"\nCountry sample:")
print(df_final[df_final['ISO3'] == 'AGO'].head(10))
