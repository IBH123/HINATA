"""
HINATA Configuration Module
Handles application configuration and environment variables
"""
import os
from dotenv import load_dotenv
from typing import Dict, Any
import logging

# Load environment variables
load_dotenv()

class Config:
    """Application configuration class"""
    
    # Data Configuration
    YAHOO_FINANCE_ENABLED = os.getenv('YAHOO_FINANCE_ENABLED', 'true').lower() == 'true'
    
    # UI Configuration
    DEFAULT_SYMBOL = os.getenv('DEFAULT_SYMBOL', 'AAPL')
    DEFAULT_TIMEFRAME = os.getenv('DEFAULT_TIMEFRAME', '1d')
    CHART_HEIGHT = int(os.getenv('CHART_HEIGHT', '600'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'hinata.log')
    
    # Application Settings
    APP_TITLE = "HINATA - Hybrid ICT-Strategy Navigation & Autonomous Trading Agent"
    APP_VERSION = "1.0.0"
    
    # Chart Colors (Enhanced Dark Theme with Better Contrast)
    COLORS = {
        'background': '#1a1a1a',     # Darker background for better contrast
        'paper': '#2d2d30',          # Slightly lighter plot area
        'text': '#ffffff',           # Pure white text for maximum readability
        'grid': '#404040',           # More visible grid lines
        'bullish': '#00ff88',        # Bright green for bullish candles
        'bearish': '#ff4757',        # Bright red for bearish candles
        'volume_bullish': '#00ff8850',  # Semi-transparent green for volume
        'volume_bearish': '#ff475750',  # Semi-transparent red for volume
        'volume': '#5dade2',         # Brighter blue for neutral volume
        'ma_fast': '#ffa502',        # Bright orange for fast MA
        'ma_slow': '#9c88ff',        # Bright purple for slow MA
        'border': '#555555',         # Visible borders
        'hover': '#ffffff',          # White hover text
        'title': '#ffffff'           # White titles
    }
    
    # ICT Colors (Enhanced for overlays with better visibility)
    ICT_COLORS = {
        'order_block_bullish': '#00ff8850',    # Semi-transparent bright green
        'order_block_bearish': '#ff475750',    # Semi-transparent bright red
        'fvg_bullish': '#2ed57350',            # Semi-transparent emerald
        'fvg_bearish': '#ff6b3550',            # Semi-transparent orange-red
        'liquidity': '#f39c1270',              # Semi-transparent bright yellow
        'structure': '#e056fd',                # Bright purple for structure lines
        'support': '#00ff88',                  # Bright green for support
        'resistance': '#ff4757'                # Bright red for resistance
    }
    
    @classmethod
    def get_page_config(cls) -> Dict[str, Any]:
        """Get Streamlit page configuration"""
        return {
            'page_title': cls.APP_TITLE,
            'page_icon': '🎯',
            'layout': 'wide',
            'initial_sidebar_state': 'expanded'
        }
    
    @classmethod
    def setup_logging(cls) -> None:
        """Setup application logging"""
        logging.basicConfig(
            level=getattr(logging, cls.LOG_LEVEL),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(cls.LOG_FILE),
                logging.StreamHandler()
            ]
        )

# Initialize configuration
Config.setup_logging()