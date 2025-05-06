"""
Bubble analysis module for the AI Bubble Dashboard.
Provides comprehensive analysis of AI sector bubble indicators.
"""

import numpy as np
import pandas as pd
from datetime import datetime
import yfinance as yf
import pandas_datareader.data as web
import warnings
from typing import Dict
import logging

warnings.filterwarnings('ignore')
logger = logging.getLogger(__name__)

class BubbleAnalyzer:
    def __init__(self, start_date: str = '2020-01-01'):
        """Initialize the bubble analyzer with data collection parameters."""
        self.start_date = start_date
        self.end_date = datetime.now().strftime('%Y-%m-%d')
        self.data = None
        
    def collect_data(self) -> pd.DataFrame:
        """Collect and process all required data for bubble analysis."""
        logger.info("Starting data collection for bubble analysis...")
        
        # Collect ETF data
        try:
            botz = yf.download('BOTZ', start=self.start_date, end=self.end_date, interval='1mo')
            logger.info("Successfully downloaded BOTZ ETF data")
            ai_etf = botz[['Close']].copy()
            ai_etf.columns = ['price']
        except Exception as e:
            logger.error(f"Error downloading ETF data: {e}")
            ai_etf = self._generate_simulated_data()

        # Calculate P/S ratio (simplified for demonstration)
        ai_etf['ps_ratio'] = ai_etf['price'] * 10  # Simplified P/S calculation
        
        # Collect market data
        market_data = self._collect_market_data()
        
        # Combine data
        self.data = pd.concat([ai_etf, market_data], axis=1)
        return self.data

    def _collect_market_data(self) -> pd.DataFrame:
        """Collect market indicators data."""
        market_data = pd.DataFrame()
        
        try:
            # VIX data
            vix = web.DataReader('^VIX', 'yahoo', start=self.start_date, end=self.end_date)
            market_data['vix'] = vix['Close'].resample('M').mean()
            
            # Fed Funds Rate
            fed_rate = web.DataReader('FEDFUNDS', 'fred', start=self.start_date, end=self.end_date)
            market_data['fed_rate'] = fed_rate['FEDFUNDS'].resample('M').mean()
            
            # M2 Money Supply (simplified)
            market_data['m2_yoy'] = np.random.normal(5, 2, len(market_data))  # Simulated M2 growth
            
        except Exception as e:
            logger.error(f"Error collecting market data: {e}")
            market_data = self._generate_simulated_market_data()
            
        return market_data

    def _generate_simulated_data(self) -> pd.DataFrame:
        """Generate simulated ETF data."""
        months = pd.date_range(start=self.start_date, end=self.end_date, freq='MS')
        data = pd.DataFrame(index=months)
        base_value = 25
        trend = np.linspace(0, 15, len(months))
        data['price'] = base_value + trend + np.random.normal(0, 2, len(months))
        return data

    def _generate_simulated_market_data(self) -> pd.DataFrame:
        """Generate simulated market data."""
        months = pd.date_range(start=self.start_date, end=self.end_date, freq='MS')
        data = pd.DataFrame(index=months)
        data['vix'] = np.random.normal(20, 5, len(months))
        data['fed_rate'] = np.random.normal(2, 0.5, len(months))
        data['m2_yoy'] = np.random.normal(5, 2, len(months))
        return data

    def analyze_bubble_risk(self) -> Dict[str, float]:
        """Analyze bubble risk indicators and return risk metrics."""
        if self.data is None:
            self.collect_data()

        # Calculate moving average
        self.data['ps_ratio_ma12'] = self.data['ps_ratio'].rolling(window=12).mean()
        
        # Calculate deviation from moving average
        current_deviation = ((self.data['ps_ratio'].iloc[-1] / self.data['ps_ratio_ma12'].iloc[-1]) - 1) * 100
        
        # Calculate volatility
        volatility = self.data['ps_ratio'].pct_change().std() * 100
        
        # Determine risk level
        if current_deviation > 40 or (current_deviation > 20 and volatility > 30):
            risk_level = "HIGH"
        elif current_deviation > 20 or (current_deviation > 10 and volatility > 20):
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"

        return {
            'current_deviation': current_deviation,
            'volatility': volatility,
            'bubble_risk_level': risk_level
        } 