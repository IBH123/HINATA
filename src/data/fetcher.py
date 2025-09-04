"""
HINATA Data Fetcher Module
Handles fetching and normalizing OHLCV data from various sources
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
import logging
from dataclasses import dataclass

@dataclass
class CandleData:
    """Unified candle data structure"""
    timestamp: pd.Timestamp
    open: float
    high: float
    low: float
    close: float
    volume: int
    
class DataFetcher:
    """Main data fetching class for HINATA"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.cache = {}  # Simple in-memory cache
        
    def fetch_ohlcv(self, symbol: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Fetch OHLCV data for a given symbol
        
        Args:
            symbol: Trading symbol (e.g., 'AAPL', 'BTC-USD')
            period: Data period ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')
            interval: Data interval ('1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo')
            
        Returns:
            DataFrame with normalized OHLCV data
        """
        # Validate and adjust period/interval compatibility
        adjusted_period, adjusted_interval = self._validate_and_adjust_timeframe(period, interval)
        
        cache_key = f"{symbol}_{adjusted_period}_{adjusted_interval}"
        
        # Check cache first
        if cache_key in self.cache:
            cache_time, data = self.cache[cache_key]
            if datetime.now() - cache_time < timedelta(minutes=5):  # 5-minute cache
                self.logger.info(f"Returning cached data for {symbol}")
                return data
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=adjusted_period, interval=adjusted_interval)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol} with period={adjusted_period}, interval={adjusted_interval}")
            
            # Normalize column names and data structure
            normalized_data = self._normalize_data(data, symbol)
            
            # Cache the result
            self.cache[cache_key] = (datetime.now(), normalized_data)
            
            self.logger.info(f"Fetched {len(normalized_data)} candles for {symbol}")
            return normalized_data
            
        except Exception as e:
            self.logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise
    
    def _normalize_data(self, raw_data: pd.DataFrame, symbol: str) -> pd.DataFrame:
        """Normalize raw data to HINATA standard format"""
        if raw_data.empty:
            return pd.DataFrame()
            
        # Reset index to make timestamp a column
        data_copy = raw_data.reset_index()
        
        # Handle both 'Date' and 'Datetime' index names from yfinance
        timestamp_col = None
        if 'Date' in data_copy.columns:
            timestamp_col = 'Date'
        elif 'Datetime' in data_copy.columns:
            timestamp_col = 'Datetime'
        else:
            # Fallback: use the index if it's datetime-like
            if hasattr(raw_data.index, 'tz'):
                data_copy['timestamp'] = raw_data.index
                timestamp_col = 'timestamp'
            else:
                raise ValueError(f"Could not find timestamp column in data. Columns: {list(data_copy.columns)}")
        
        # Create normalized DataFrame directly from the copy
        normalized = pd.DataFrame({
            'timestamp': data_copy[timestamp_col],
            'open': data_copy['Open'].astype(float),
            'high': data_copy['High'].astype(float),
            'low': data_copy['Low'].astype(float),
            'close': data_copy['Close'].astype(float),
            'volume': data_copy['Volume'].astype(float),  # Use float to handle any issues
            'symbol': symbol
        })
        
        # Remove any rows with NaN values
        normalized = normalized.dropna()
        
        # Convert volume back to int after NaN removal
        if not normalized.empty:
            normalized['volume'] = normalized['volume'].astype(int)
        
        # Sort by timestamp and reset index
        normalized = normalized.sort_values('timestamp').reset_index(drop=True)
        
        return normalized
    
    def get_supported_symbols(self) -> Dict[str, List[str]]:
        """Return dictionary of supported symbols by asset class"""
        return {
            'stocks': [
                'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 
                'NVDA', 'META', 'NFLX', 'AMD', 'CRM'
            ],
            'crypto': [
                'BTC-USD', 'ETH-USD', 'ADA-USD', 'DOT-USD', 'LINK-USD',
                'MATIC-USD', 'SOL-USD', 'AVAX-USD', 'ATOM-USD', 'ALGO-USD'
            ],
            'forex': [
                'EURUSD=X', 'GBPUSD=X', 'USDJPY=X', 'AUDUSD=X', 'USDCAD=X'
            ]
        }
    
    def get_supported_timeframes(self) -> Dict[str, str]:
        """Return dictionary of supported timeframes with better descriptions"""
        return {
            '1m': '1 Minute (intraday)',
            '5m': '5 Minutes (intraday)', 
            '15m': '15 Minutes (intraday)',
            '30m': '30 Minutes (intraday)',
            '1h': '1 Hour (intraday)',
            '4h': '4 Hours (resampled)',  # Will use 1h data and resample
            '1d': '1 Day (daily)',
            '1wk': '1 Week (weekly)',
            '1mo': '1 Month (monthly)'
        }
    
    def resample_data(self, data: pd.DataFrame, target_interval: str) -> pd.DataFrame:
        """Resample data to different timeframe"""
        if target_interval == '4h':
            # Resample 1h data to 4h
            data_copy = data.copy()
            data_copy.set_index('timestamp', inplace=True)
            
            resampled = data_copy.resample('4H').agg({
                'open': 'first',
                'high': 'max', 
                'low': 'min',
                'close': 'last',
                'volume': 'sum',
                'symbol': 'first'
            }).dropna()
            
            resampled.reset_index(inplace=True)
            return resampled
            
        return data
    
    def validate_symbol(self, symbol: str) -> bool:
        """Validate if symbol exists and has data"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return 'symbol' in info or 'shortName' in info
        except:
            return False
    
    def get_latest_price(self, symbol: str) -> Optional[float]:
        """Get latest price for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period="1d", interval="1m")
            if not data.empty:
                return float(data['Close'].iloc[-1])
            return None
        except:
            return None
    
    def _validate_and_adjust_timeframe(self, period: str, interval: str) -> Tuple[str, str]:
        """
        Validate and adjust period/interval combinations for yfinance compatibility
        
        Args:
            period: Original period
            interval: Original interval
            
        Returns:
            Tuple of (adjusted_period, adjusted_interval)
        """
        # Define interval categories
        intraday_intervals = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h']
        daily_plus_intervals = ['1d', '5d', '1wk', '1mo', '3mo']
        
        # Define period constraints for intraday data
        intraday_max_periods = {
            '1m': ['1d', '5d', '7d'],  # 1m data limited to ~7 days
            '2m': ['1d', '5d', '7d', '60d'], 
            '5m': ['1d', '5d', '7d', '60d'],
            '15m': ['1d', '5d', '7d', '60d'],
            '30m': ['1d', '5d', '7d', '60d'],
            '60m': ['1d', '5d', '7d', '60d', '730d'],
            '90m': ['1d', '5d', '7d', '60d', '730d'],
            '1h': ['1d', '5d', '7d', '60d', '730d']
        }
        
        adjusted_period = period
        adjusted_interval = interval
        
        # Handle intraday intervals with inappropriate periods
        if interval in intraday_intervals:
            # Convert period names to days for easier comparison
            period_to_days = {
                '1d': 1, '5d': 5, '7d': 7, '1mo': 30, '3mo': 90, '6mo': 180,
                '1y': 365, '2y': 730, '5y': 1825, '10y': 3650, 'ytd': 365, 'max': 3650
            }
            
            current_days = period_to_days.get(period, 365)
            
            # Adjust period based on interval limitations
            if interval in ['1m', '2m', '5m'] and current_days > 7:
                self.logger.warning(f"Period {period} too long for {interval} interval, adjusting to 5d")
                adjusted_period = '5d'
            elif interval in ['15m', '30m'] and current_days > 60:
                self.logger.warning(f"Period {period} too long for {interval} interval, adjusting to 60d")
                adjusted_period = '60d'
            elif interval in ['60m', '90m', '1h'] and current_days > 730:
                self.logger.warning(f"Period {period} too long for {interval} interval, adjusting to 730d")
                adjusted_period = '730d'
        
        # Handle daily+ intervals with very short periods
        elif interval in daily_plus_intervals:
            if period in ['1d'] and interval != '1d':
                # For 1d period with weekly/monthly intervals, extend period
                if interval in ['1wk']:
                    adjusted_period = '3mo'
                    self.logger.warning(f"Period {period} too short for {interval} interval, adjusting to 3mo")
                elif interval in ['1mo']:
                    adjusted_period = '2y'
                    self.logger.warning(f"Period {period} too short for {interval} interval, adjusting to 2y")
        
        return adjusted_period, adjusted_interval
    
    def get_period_interval_compatibility(self) -> Dict[str, List[str]]:
        """
        Return recommended period/interval combinations
        
        Returns:
            Dictionary mapping intervals to recommended periods
        """
        return {
            '1m': ['1d', '5d'],
            '2m': ['1d', '5d'], 
            '5m': ['1d', '5d'],
            '15m': ['1d', '5d', '1mo'],
            '30m': ['1d', '5d', '1mo'],
            '1h': ['5d', '1mo', '3mo', '6mo'],
            '90m': ['5d', '1mo', '3mo', '6mo'],
            '1d': ['1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'max'],
            '1wk': ['6mo', '1y', '2y', '5y', '10y', 'max'],
            '1mo': ['1y', '2y', '5y', '10y', 'max']
        }