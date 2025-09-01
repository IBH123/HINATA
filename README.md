# HINATA - Phase 1

Hybrid ICT-Strategy Navigation & Autonomous Trading Agent

## Phase 1: Data Acquisition & Visualization

This is the foundational phase implementing data fetching and chart visualization capabilities.

### Features Implemented

✅ **Data Infrastructure**
- Yahoo Finance API integration
- Multi-asset support (stocks, crypto, forex)
- Multiple timeframe support (1m to 1mo)
- Data caching and normalization

✅ **Chart Visualization**
- Interactive candlestick charts with Plotly
- Volume display
- Moving averages overlay
- Professional dark theme
- Real-time price metrics

✅ **User Interface**
- Clean Streamlit web interface
- Asset class and symbol selection
- Timeframe controls
- Overlay toggles (with Phase 2+ stubs)
- Analysis header with key metrics

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Copy environment configuration:
```bash
copy .env.example .env
```

3. Run the application:
```bash
streamlit run app.py
```

Or use the provided batch file:
```bash
run_app.bat
```

### Recent Fixes

**v1.0.1 - Data Loading Fix**
- Fixed data normalization issue that caused empty DataFrames
- Improved timezone handling for Yahoo Finance data
- Verified compatibility across stocks, crypto, and forex markets
- All tests now passing with full data loading functionality

### Project Structure

```
HINATA/
├── src/
│   ├── data/
│   │   └── fetcher.py          # Data fetching and normalization
│   ├── ui/
│   │   └── charts.py           # Chart rendering and visualization
│   └── utils/
│       └── config.py           # Configuration management
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

### Usage

1. **Symbol Selection**: Choose asset class and specific symbol
2. **Timeframe**: Select chart timeframe (1m to 1mo)
3. **Data Period**: Choose historical data range
4. **Load Data**: Click to fetch and display data
5. **Overlays**: Toggle moving averages (more coming in Phase 2+)

### Success Metrics Met

✅ Load 1 year daily + 3 months H4 data  
✅ Support minimum 3 instruments across asset classes  
✅ Sub-second chart rendering performance  
✅ Professional UI with ICT-ready overlay system  

### Next Phase

Phase 2 will implement:
- AI Assistant with ReAct loop
- Context Engineer sub-agent
- Basic ICT pattern detection
- Command/Goal mode routing

### Testing

The application supports:
- 10+ stock symbols (AAPL, MSFT, GOOGL, etc.)
- 10+ crypto pairs (BTC-USD, ETH-USD, etc.)
- 5+ forex pairs (EURUSD=X, etc.)
- All major timeframes with automatic resampling

### Dependencies

- `streamlit`: Web interface framework
- `plotly`: Interactive charting
- `yfinance`: Financial data source
- `pandas`: Data manipulation
- `numpy`: Numerical computing