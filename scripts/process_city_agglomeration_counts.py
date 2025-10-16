"""
Process UN WUP F17a data to extract number of urban agglomerations by size class
Creates a CSV with agglomeration counts for Sub-Saharan African countries
"""

import pandas as pd
import sys
import os

# Get the absolute path to the project root directory
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.join(current_dir, '..')
sys.path.append(project_root)

from src.utils.country_utils import load_subsaharan_countries_dict

# Load Sub-Saharan African countries
SUB_SAHARAN_COUNTRIES = load_subsaharan_countries_dict()

# Create mapping between Country Code and ISO3 from WUP locations file
locations_path = os.path.join(project_root, 'data', 'raw', 'Urban', 'WUP2018-F00-LOCATIONS_clean.csv')
locations_df = pd.read_csv(locations_path)
country_code_to_iso3 = dict(zip(locations_df['Country Code'].astype(int), locations_df['ISO3']))

# Years to extract
SELECTED_YEARS = [2020, 2025, 2030, 2035]

def process_agglomeration_counts():
    """Extract number of agglomerations by size class from F17a"""
    
    print("Loading agglomeration counts from F17a...")
    f17a_path = os.path.join(project_root, 'data', 'raw', 'Urban', 'WUP2018-F17a-City_Size_Class.xlsx')
    df = pd.read_excel(f17a_path, skiprows=16, header=0)
    
    # Drop rows with NaN Country Code
    df = df.dropna(subset=['Country Code'])
    
    # Map country codes to ISO3
    df['ISO3'] = df['Country Code'].astype(int).map(country_code_to_iso3)
    
    # Filter for Sub-Saharan African countries only
    df = df[df['ISO3'].isin(SUB_SAHARAN_COUNTRIES.keys())]
    
    # Filter for 'Number of Agglomerations' data type (note the capital A)
    df_counts = df[df['Type of data'] == 'Number of Agglomerations'].copy()
    
    # Create output data
    agglomeration_data = []
    
    for _, row in df_counts.iterrows():
        iso3 = row['ISO3']
        country_name = SUB_SAHARAN_COUNTRIES.get(iso3, iso3)
        size_class = row['Size class of urban settlement']
        
        for year in SELECTED_YEARS:
            if year in df_counts.columns:
                count = row[year]
                if pd.notna(count):
                    agglomeration_data.append({
                        'Country Code': iso3,
                        'Country Name': country_name,
                        'Size Category': size_class,
                        'Year': year,
                        'Number of Agglomerations': int(count)
                    })
    
    # Create DataFrame
    result_df = pd.DataFrame(agglomeration_data)
    
    # Check if we have data
    if result_df.empty:
        print("WARNING: No agglomeration data found!")
        return result_df
    
    # Sort by country, year, and size category
    result_df = result_df.sort_values(['Country Code', 'Year', 'Size Category'])
    
    # Save to processed folder
    output_path = os.path.join(project_root, 'data', 'processed', 'city_agglomeration_counts.csv')
    result_df.to_csv(output_path, index=False)
    
    print(f"\n✓ Processed agglomeration counts")
    print(f"  - Countries: {result_df['Country Code'].nunique()}")
    print(f"  - Years: {sorted(result_df['Year'].unique())}")
    print(f"  - Size categories: {result_df['Size Category'].nunique()}")
    print(f"  - Output: {output_path}")
    
    # Show sample data
    print(f"\nSample data (first 15 rows):\n{result_df.head(15)}")
    
    return result_df

if __name__ == "__main__":
    process_agglomeration_counts()
