"""
Test script to verify disaster data filtering works correctly
"""

import sys
import os
sys.path.append('.')

from src.utils.data_loader import load_real_disaster_data
import pandas as pd

def test_filtering():
    """Test the disaster data filtering functionality"""
    
    print("=== Testing Disaster Data Filtering ===\n")
    
    # Load the data
    print("1. Loading real disaster data...")
    data = load_real_disaster_data()
    print(f"   Total records: {len(data)}")
    print(f"   Columns: {list(data.columns)}")
    print(f"   Year range: {data['year'].min()} - {data['year'].max()}")
    print(f"   Countries: {data['country'].nunique()}")
    print(f"   Disaster types: {data['disaster_type'].nunique()}")
    
    # Test country filtering
    print("\n2. Testing country filtering...")
    test_countries = ['NGA', 'KEN', 'ETH']
    filtered_by_country = data[data['country_code'].isin(test_countries)]
    print(f"   Records for {test_countries}: {len(filtered_by_country)}")
    print(f"   Countries found: {filtered_by_country['country'].unique()}")
    
    # Test disaster type filtering
    print("\n3. Testing disaster type filtering...")
    test_types = ['flood', 'drought', 'epidemic']
    filtered_by_type = data[data['disaster_type'].isin(test_types)]
    print(f"   Records for {test_types}: {len(filtered_by_type)}")
    print(f"   Types found: {filtered_by_type['disaster_type'].unique()}")
    
    # Test year range filtering
    print("\n4. Testing year range filtering...")
    test_years = [2000, 2020]
    filtered_by_year = data[
        (data['year'] >= test_years[0]) & 
        (data['year'] <= test_years[1])
    ]
    print(f"   Records for {test_years[0]}-{test_years[1]}: {len(filtered_by_year)}")
    print(f"   Year range found: {filtered_by_year['year'].min()} - {filtered_by_year['year'].max()}")
    
    # Test combined filtering
    print("\n5. Testing combined filtering...")
    combined_filter = data[
        (data['country_code'].isin(test_countries)) &
        (data['disaster_type'].isin(test_types)) &
        (data['year'] >= test_years[0]) &
        (data['year'] <= test_years[1])
    ]
    print(f"   Records with all filters: {len(combined_filter)}")
    
    if len(combined_filter) > 0:
        print("   Sample of filtered data:")
        print(combined_filter[['year', 'country', 'disaster_type', 'deaths']].head())
        
        # Test aggregation
        print("\n6. Testing aggregation...")
        agg_data = combined_filter.groupby(['year', 'country']).size().reset_index(name='disaster_count')
        print(f"   Aggregated records: {len(agg_data)}")
        print("   Sample aggregation:")
        print(agg_data.head())
    else:
        print("   No data found with combined filters - this might be the issue!")
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    test_filtering()