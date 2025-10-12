"""
Unit tests for the DRM dashboard utilities
"""

import unittest
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.utils.data_loader import load_emdat_data
from src.utils.country_utils import get_subsaharan_countries, load_subsaharan_countries_dict
from src.utils.callback_helpers import safe_filter_data, safe_aggregate_data


class TestDataLoader(unittest.TestCase):
    """Test data loading utilities"""
    
    def test_load_emdat_data(self):
        """Test EM-DAT data loading"""
        try:
            df = load_emdat_data()
            
            # Check if DataFrame is not empty
            self.assertGreater(len(df), 0)
            
            # Check required columns exist (actual EM-DAT structure)
            required_columns = [
                'Disaster Type', 'ISO', 'Year', 'Total Deaths', 'Total Affected'
            ]
            for col in required_columns:
                self.assertIn(col, df.columns)
            
            # Check data types
            self.assertTrue(df['Year'].dtype in ['int64', 'int32'])
            self.assertTrue(df['Total Deaths'].dtype in ['int64', 'int32', 'float64'])
            self.assertTrue(df['Total Affected'].dtype in ['int64', 'int32', 'float64'])
            
            # Check year range (EM-DAT covers 1975-2025)
            self.assertTrue(df['Year'].min() >= 1975)
            self.assertTrue(df['Year'].max() <= 2025)
            
            # Check ISO codes are 3 characters
            iso_codes = df['ISO'].dropna().unique()
            for iso in iso_codes[:5]:  # Check first 5
                self.assertEqual(len(iso), 3)
                
        except FileNotFoundError:
            # Skip test if EM-DAT file not available
            self.skipTest("EM-DAT data file not found")
    
    def test_get_subsaharan_countries(self):
        """Test Sub-Saharan countries list"""
        countries = get_subsaharan_countries()
        
        # Check if list is not empty
        self.assertGreater(len(countries), 0)
        
        # Check structure
        self.assertIsInstance(countries, list)
        
        # Check first country structure
        if countries:
            country = countries[0]
            self.assertIn('name', country)
            self.assertIn('code', country)
            self.assertEqual(len(country['code']), 3)  # ISO codes are 3 letters
    
    def test_load_subsaharan_countries_dict(self):
        """Test Sub-Saharan countries dictionary loading"""
        countries_dict = load_subsaharan_countries_dict()
        
        # Check if dict is not empty
        self.assertGreater(len(countries_dict), 0)
        
        # Check structure
        self.assertIsInstance(countries_dict, dict)
        
        # Check some known countries
        self.assertIn('NGA', countries_dict)  # Nigeria
        self.assertIn('KEN', countries_dict)  # Kenya


class TestCallbackHelpers(unittest.TestCase):
    """Test callback helper utilities"""
    
    def setUp(self):
        """Set up test data"""
        # Create sample EM-DAT structure data for testing
        self.sample_data = pd.DataFrame({
            'Disaster Type': ['Flood', 'Storm', 'Flood', 'Drought'],
            'ISO': ['NGA', 'KEN', 'ETH', 'NGA'],
            'Year': [2020, 2021, 2020, 2022],
            'Total Deaths': [10, 5, 0, 15],
            'Total Affected': [1000, 500, 2000, 800]
        })
    
    def test_safe_filter_data_by_country(self):
        """Test filtering data by country"""
        filtered = safe_filter_data(
            self.sample_data, 
            countries=['NGA']
        )
        
        self.assertEqual(len(filtered), 2)  # 2 NGA records
        self.assertTrue(all(filtered['ISO'] == 'NGA'))
    
    def test_safe_filter_data_by_disaster_type(self):
        """Test filtering data by disaster type"""
        filtered = safe_filter_data(
            self.sample_data, 
            disaster_types=['Flood']
        )
        
        self.assertEqual(len(filtered), 2)  # 2 Flood records
        self.assertTrue(all(filtered['Disaster Type'] == 'Flood'))
    
    def test_safe_filter_data_combined(self):
        """Test combined filtering"""
        filtered = safe_filter_data(
            self.sample_data,
            countries=['NGA'],
            disaster_types=['Flood']
        )
        
        self.assertEqual(len(filtered), 1)  # 1 NGA Flood record
        self.assertEqual(filtered.iloc[0]['ISO'], 'NGA')
        self.assertEqual(filtered.iloc[0]['Disaster Type'], 'Flood')
    
    def test_safe_filter_data_empty(self):
        """Test filtering with empty data"""
        empty_df = pd.DataFrame()
        filtered = safe_filter_data(empty_df, countries=['NGA'])
        
        self.assertTrue(filtered.empty)
    
    def test_safe_aggregate_data(self):
        """Test safe data aggregation"""
        agg_data = safe_aggregate_data(
            self.sample_data,
            group_by=['Disaster Type'],
            agg_dict={'Total Deaths': 'sum', 'Total Affected': 'sum'}
        )
        
        # Should have 3 disaster types: Flood, Storm, Drought
        self.assertEqual(len(agg_data), 3)
        self.assertIn('Disaster Type', agg_data.columns)
        self.assertIn('Total Deaths', agg_data.columns)
        self.assertIn('Total Affected', agg_data.columns)
        
        # Check Flood aggregation (2 records: 10+0=10 deaths, 1000+2000=3000 affected)
        flood_data = agg_data[agg_data['Disaster Type'] == 'Flood']
        self.assertEqual(len(flood_data), 1)
        self.assertEqual(flood_data.iloc[0]['Total Deaths'], 10)
        self.assertEqual(flood_data.iloc[0]['Total Affected'], 3000)


if __name__ == '__main__':
    unittest.main()