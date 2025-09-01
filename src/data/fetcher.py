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
        cache_key = f"{symbol}_{period}_{interval}"
        
        # Check cache first
        if cache_key in self.cache:
            cache_time, data = self.cache[cache_key]
            if datetime.now() - cache_time < timedelta(minutes=5):  # 5-minute cache
                self.logger.info(f"Returning cached data for {symbol}")
                return data
        
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
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
        
        # Create normalized DataFrame directly from the copy
        normalized = pd.DataFrame({
            'timestamp': data_copy['Date'],
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
        """Return dictionary of supported timeframes"""
        return {
            '1m': '1 Minute',
            '5m': '5 Minutes', 
            '15m': '15 Minutes',
            '30m': '30 Minutes',
            '1h': '1 Hour',
            '4h': '4 Hours',  # Will use 1h data and resample
            '1d': '1 Day',
            '1wk': '1 Week',
            '1mo': '1 Month'
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