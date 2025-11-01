"""
Process UN WUP Cities Data for Sub-Saharan Africa
Combines individual cities (F22) with aggregate data (F17a) to ensure totals match
Creates "Other cities" entries for the difference between aggregate and individual cities
"""

import pandas as pd
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.utils.country_utils import load_subsaharan_countries_dict

# Load Sub-Saharan African countries
SUB_SAHARAN_COUNTRIES = load_subsaharan_countries_dict()

# Create mapping between Country Code and ISO3 from WUP locations file
locations_df = pd.read_csv('data/raw/Urban/WUP2018-F00-LOCATIONS_clean.csv')
country_code_to_iso3 = dict(zip(locations_df['Country Code'].astype(int), locations_df['ISO3']))

# Years to extract (based on user requirement)
SELECTED_YEARS = [2020, 2025, 2030, 2035]

def get_city_size_category(population):
    """Determine city size category based on population (in thousands)"""
    if population >= 10000:
        return '10 million or more'
    elif population >= 5000:
        return '5 to 10 million'
    elif population >= 1000:
        return '1 to 5 million'
    elif population >= 500:
        return '500 000 to 1 million'
    elif population >= 300:
        return '300 000 to 500 000'
    else:
        return 'Fewer than 300 000'

def load_aggregate_totals():
    """Load aggregate totals by size class from F17a"""
    df = pd.read_excel(
        'data/raw/Urban/WUP2018-F17a-City_Size_Class.xlsx',
        skiprows=16,
        header=0
    )
    
    # Drop rows with NaN Country Code
    df = df.dropna(subset=['Country Code'])
    
    # Map country codes to ISO3
    df['ISO3'] = df['Country Code'].astype(int).map(country_code_to_iso3)
    
    # Filter for Sub-Saharan African countries only
    df = df[df['ISO3'].isin(SUB_SAHARAN_COUNTRIES.keys())]
    
    # Filter for 'Population' data type
    df = df[df['Type of data'] == 'Population'].copy()
    
    # Create dictionary: {(ISO3, Year, Size Category): Population}
    aggregate_dict = {}
    
    for _, row in df.iterrows():
        iso3 = row['ISO3']
        size_class = row['Size class of urban settlement']
        
        for year in SELECTED_YEARS:
            if year in df.columns:
                population = row[year]
                if pd.notna(population) and population > 0:
                    aggregate_dict[(iso3, year, size_class)] = population
    
    return aggregate_dict

def process_individual_cities():
    """Process WUP2018 Cities Over 300K data and reconcile with aggregate totals"""
    
    # Load aggregate totals from F17a
    print("Loading aggregate totals from F17a...")
    aggregate_totals = load_aggregate_totals()
    
    # Read the individual cities file (F22 - over 300K population)
    print("Loading individual cities from F22...")
    df = pd.read_excel(
        'data/raw/Urban/WUP2018-F22-Cities_Over_300K_Annual.xlsx',
        skiprows=16,
        header=0
    )
    
    # Map country codes to ISO3
    df['ISO3'] = df['Country Code'].astype(int).map(country_code_to_iso3)
    
    # Filter for Sub-Saharan African countries only
    df = df[df['ISO3'].isin(SUB_SAHARAN_COUNTRIES.keys())].copy()
    
    # Create output for all cities
    all_cities = []
    
    # Track totals by country, year, and size category from individual cities
    individual_totals = {}
    
    for _, row in df.iterrows():
        iso3 = row['ISO3']
        country_name = SUB_SAHARAN_COUNTRIES.get(iso3, iso3)
        city_name = row['Urban Agglomeration']
        
        # Extract data for each selected year
        for year in SELECTED_YEARS:
            if year in df.columns:
                population = row[year]  # Population in thousands
                
                if pd.notna(population) and population > 0:
                    # Determine city size category
                    size_category = get_city_size_category(population)
                    
                    all_cities.append({
                        'Country Code': iso3,
                        'Country Name': country_name,
                        'City Name': city_name,
                        'Year': year,
                        'Population': population,  # in thousands
                        'Size Category': size_category
                    })
                    
                    # Track totals for reconciliation
                    key = (iso3, year, size_category)
                    individual_totals[key] = individual_totals.get(key, 0) + population
    
    # Now reconcile: add "Other cities" for differences
    print("Reconciling totals and adding 'Other cities' entries...")
    for (iso3, year, size_category), aggregate_total in aggregate_totals.items():
        individual_total = individual_totals.get((iso3, year, size_category), 0)
        difference = aggregate_total - individual_total
        
        # If there's a positive difference, add "Other cities" entry
        if difference > 1:  # Threshold of 1 thousand to avoid rounding errors
            country_name = SUB_SAHARAN_COUNTRIES.get(iso3, iso3)
            all_cities.append({
                'Country Code': iso3,
                'Country Name': country_name,
                'City Name': f'Other cities ({size_category})',
                'Year': year,
                'Population': difference,
                'Size Category': size_category
            })
    
    # Create DataFrame
    result_df = pd.DataFrame(all_cities)
    
    # Sort by country, city, and year
    result_df = result_df.sort_values(['Country Code', 'City Name', 'Year'])
    
    # Save to processed folder
    output_path = 'data/processed/cities_individual_UNDESA.csv'
    result_df.to_csv(output_path, index=False)
    
    print(f"\n✓ Processed individual cities data with reconciliation")
    print(f"  - Countries: {result_df['Country Code'].nunique()}")
    print(f"  - Cities (including 'Other cities'): {result_df['City Name'].nunique()}")
    print(f"  - Years: {sorted(result_df['Year'].unique())}")
    print(f"  - Output: {output_path}")
    
    # Show sample data including some "Other cities" entries
    print(f"\nSample data (first 10 rows):\n{result_df.head(10)}")
    other_cities = result_df[result_df['City Name'].str.contains('Other cities', na=False)]
    if not other_cities.empty:
        print(f"\nSample 'Other cities' entries:\n{other_cities.head(10)}")
    
    return result_df

if __name__ == "__main__":
    process_individual_cities()
