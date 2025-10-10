"""
Unit tests for the DRM dashboard utilities
"""

import unittest
import pandas as pd
import sys
import os

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils.data_loader import (
    create_sample_disaster_data,
    create_sample_urbanization_data,
    create_sample_flood_risk_data,
    get_subsaharan_countries
)


class TestDataLoader(unittest.TestCase):
    """Test data loading utilities"""
    
    def test_create_sample_disaster_data(self):
        """Test sample disaster data creation"""
        df = create_sample_disaster_data()
        
        # Check if DataFrame is not empty
        self.assertGreater(len(df), 0)
        
        # Check required columns exist
        required_columns = [
            'year', 'country', 'country_code', 'disaster_type',
            'affected_population', 'economic_damage_usd'
        ]
        for col in required_columns:
            self.assertIn(col, df.columns)
        
        # Check data types
        self.assertTrue(df['year'].dtype in ['int64', 'int32'])
        self.assertTrue(df['affected_population'].dtype in ['int64', 'int32'])
        
        # Check year range
        self.assertTrue(df['year'].min() >= 2000)
        self.assertTrue(df['year'].max() <= 2023)
    
    def test_create_sample_urbanization_data(self):
        """Test sample urbanization data creation"""
        df = create_sample_urbanization_data()
        
        # Check if DataFrame is not empty
        self.assertGreater(len(df), 0)
        
        # Check required columns
        required_columns = [
            'year', 'country', 'country_code', 'urban_population_pct',
            'urban_growth_rate', 'population_density'
        ]
        for col in required_columns:
            self.assertIn(col, df.columns)
        
        # Check value ranges
        self.assertTrue(df['urban_population_pct'].min() >= 0)
        self.assertTrue(df['urban_population_pct'].max() <= 100)
    
    def test_create_sample_flood_risk_data(self):
        """Test sample flood risk data creation"""
        df = create_sample_flood_risk_data()
        
        # Check if DataFrame is not empty
        self.assertGreater(len(df), 0)
        
        # Check required columns
        required_columns = [
            'country', 'country_code', 'scenario', 'flood_risk_level',
            'exposure', 'sensitivity', 'adaptive_capacity'
        ]
        for col in required_columns:
            self.assertIn(col, df.columns)
        
        # Check scenarios
        scenarios = df['scenario'].unique()
        expected_scenarios = ['current', '2030', '2050']
        for scenario in expected_scenarios:
            self.assertIn(scenario, scenarios)
        
        # Check risk level range
        self.assertTrue(df['flood_risk_level'].min() >= 0)
        self.assertTrue(df['flood_risk_level'].max() <= 10)
    
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


class TestChartHelpers(unittest.TestCase):
    """Test chart creation utilities"""
    
    def setUp(self):
        """Set up test data"""
        self.sample_disaster_data = create_sample_disaster_data()
        self.sample_urbanization_data = create_sample_urbanization_data()
    
    def test_disaster_data_structure(self):
        """Test disaster data has correct structure for charts"""
        df = self.sample_disaster_data
        
        # Check groupable columns
        grouped = df.groupby(['year', 'country']).size()
        self.assertGreater(len(grouped), 0)
    
    def test_urbanization_data_structure(self):
        """Test urbanization data structure"""
        df = self.sample_urbanization_data
        
        # Check for time series data
        country_data = df[df['country'] == df['country'].iloc[0]]
        self.assertGreater(len(country_data), 1)  # Multiple years per country


if __name__ == '__main__':
    unittest.main()