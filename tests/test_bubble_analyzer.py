"""
Test suite for the bubble analyzer module.
"""

import unittest
from datetime import datetime
import pandas as pd
import numpy as np
from src.analysis.bubble_analysis import BubbleAnalyzer

class TestBubbleAnalyzer(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = BubbleAnalyzer(start_date='2020-01-01')
        
    def test_data_collection(self):
        """Test data collection functionality."""
        data = self.analyzer.collect_data()
        self.assertIsInstance(data, pd.DataFrame)
        self.assertFalse(data.empty)
        
    def test_bubble_risk_analysis(self):
        """Test bubble risk analysis functionality."""
        risk_metrics = self.analyzer.analyze_bubble_risk()
        self.assertIsInstance(risk_metrics, dict)
        self.assertIn('bubble_risk_level', risk_metrics)
        self.assertIn(risk_metrics['bubble_risk_level'], ['LOW', 'MODERATE', 'HIGH'])
        
    def test_regression_analysis(self):
        """Test regression analysis functionality."""
        regression_results = self.analyzer.get_regression_analysis()
        self.assertIsInstance(regression_results, dict)
        self.assertIn('r_squared', regression_results)
        self.assertIn('coefficients', regression_results)
        
    def test_plot_generation(self):
        """Test plot generation functionality."""
        plots = self.analyzer.generate_plots()
        self.assertIsInstance(plots, dict)
        self.assertIn('trend', plots)
        self.assertIn('correlation', plots)
        
    def test_risk_level_calculation(self):
        """Test risk level calculation logic."""
        # Test high risk scenario
        high_risk = self.analyzer._calculate_risk_level(deviation=45, volatility=25, trend_strength=0.5)
        self.assertEqual(high_risk, 'HIGH')
        
        # Test moderate risk scenario
        moderate_risk = self.analyzer._calculate_risk_level(deviation=25, volatility=15, trend_strength=0.3)
        self.assertEqual(moderate_risk, 'MODERATE')
        
        # Test low risk scenario
        low_risk = self.analyzer._calculate_risk_level(deviation=5, volatility=10, trend_strength=0.1)
        self.assertEqual(low_risk, 'LOW')

if __name__ == '__main__':
    unittest.main() 