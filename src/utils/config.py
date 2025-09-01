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
    
    # Chart Colors (Dark Theme)
    COLORS = {
        'background': '#0E1117',
        'paper': '#262730', 
        'text': '#FAFAFA',
        'grid': '#2F3349',
        'bullish': '#26A69A',  # Teal for bullish candles
        'bearish': '#EF5350',  # Red for bearish candles
        'volume': '#42A5F5',   # Blue for volume
        'ma_fast': '#FFA726',  # Orange for fast MA
        'ma_slow': '#AB47BC'   # Purple for slow MA
    }
    
    # ICT Colors (for overlays)
    ICT_COLORS = {
        'order_block_bullish': '#26A69A40',  # Semi-transparent teal
        'order_block_bearish': '#EF535040',  # Semi-transparent red
        'fvg_bullish': '#4CAF5040',          # Semi-transparent green
        'fvg_bearish': '#FF571640',          # Semi-transparent orange
        'liquidity': '#FFEB3B60',            # Semi-transparent yellow
        'structure': '#9C27B0'               # Purple for structure lines
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