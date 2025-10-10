#!/usr/bin/env python3
"""
Check updated Sub-Saharan African disaster data
"""

import pandas as pd

# Load the data
df = pd.read_csv('data/processed/african_disasters_emdat.csv')

print(f"Total disasters: {len(df)}")
print(f"Countries: {df['country'].nunique()}")
print("\nTop 10 countries by disaster count:")
print(df['country'].value_counts().head(10))

# Check for North African countries
north_african = ['Algeria', 'Egypt', 'Libya', 'Morocco', 'Tunisia']
north_african_data = df[df['country'].isin(north_african)]

print(f"\nNorth African countries in data: {len(north_african_data)}")
if len(north_african_data) > 0:
    print("Found North African countries:")
    print(north_african_data['country'].value_counts())
else:
    print("No North African countries found - filtering successful!")

print(f"\nDate range: {df['year'].min()} - {df['year'].max()}")
print(f"Disaster types: {df['disaster_type'].nunique()}")
print(f"Most common disaster types:")
print(df['disaster_type'].value_counts().head(5))