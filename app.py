"""
HINATA Phase 1 - Main Streamlit Application
Data Acquisition & Visualization
"""
import streamlit as st
import pandas as pd
import logging
from datetime import datetime
import sys
import os

# Add src to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.data.fetcher import DataFetcher
from src.ui.charts import ChartRenderer
from src.utils.config import Config

# Configure Streamlit page
st.set_page_config(**Config.get_page_config())

class HinataApp:
    """Main HINATA Application Class"""
    
    def __init__(self):
        self.data_fetcher = DataFetcher()
        self.chart_renderer = ChartRenderer()
        self.logger = logging.getLogger(__name__)
        
        # Initialize session state
        if 'current_data' not in st.session_state:
            st.session_state.current_data = pd.DataFrame()
        if 'current_symbol' not in st.session_state:
            st.session_state.current_symbol = Config.DEFAULT_SYMBOL
        if 'current_timeframe' not in st.session_state:
            st.session_state.current_timeframe = Config.DEFAULT_TIMEFRAME
    
    def render_header(self):
        """Render application header"""
        st.title("🎯 HINATA")
        st.markdown("**Hybrid ICT-Strategy Navigation & Autonomous Trading Agent**")
        st.markdown("*Phase 1: Data Acquisition & Visualization*")
        st.markdown("---")
    
    def render_sidebar(self):
        """Render sidebar with controls"""
        st.sidebar.title("📊 Trading Controls")
        
        # Symbol Selection
        st.sidebar.subheader("Asset Selection")
        supported_symbols = self.data_fetcher.get_supported_symbols()
        
        # Asset class selection
        asset_classes = list(supported_symbols.keys())
        selected_class = st.sidebar.selectbox("Asset Class", asset_classes, index=0)
        
        # Symbol selection within class
        symbols_in_class = supported_symbols[selected_class]
        current_symbol_idx = 0
        if st.session_state.current_symbol in symbols_in_class:
            current_symbol_idx = symbols_in_class.index(st.session_state.current_symbol)
        
        selected_symbol = st.sidebar.selectbox(
            "Symbol", 
            symbols_in_class, 
            index=current_symbol_idx
        )
        
        # Timeframe Selection  
        st.sidebar.subheader("Timeframe")
        timeframes = self.data_fetcher.get_supported_timeframes()
        timeframe_keys = list(timeframes.keys())
        timeframe_labels = [f"{k} - {v}" for k, v in timeframes.items()]
        
        current_tf_idx = 0
        if st.session_state.current_timeframe in timeframe_keys:
            current_tf_idx = timeframe_keys.index(st.session_state.current_timeframe)
        
        selected_timeframe_idx = st.sidebar.selectbox(
            "Chart Timeframe",
            range(len(timeframe_labels)),
            format_func=lambda x: timeframe_labels[x],
            index=current_tf_idx
        )
        selected_timeframe = timeframe_keys[selected_timeframe_idx]
        
        # Check and warn about period/timeframe compatibility
        compatibility = self.data_fetcher.get_period_interval_compatibility()
        recommended_periods = compatibility.get(selected_timeframe, [])
        
        # Data Period
        st.sidebar.subheader("Data Period")
        periods = {
            '1d': '1 Day',
            '5d': '5 Days', 
            '1mo': '1 Month',
            '3mo': '3 Months',
            '6mo': '6 Months',
            '1y': '1 Year',
            '2y': '2 Years',
            'max': 'Maximum'
        }
        
        selected_period = st.sidebar.selectbox(
            "Historical Data",
            list(periods.keys()),
            format_func=lambda x: periods[x],
            index=6  # Default to 1 year
        )
        
        # Show compatibility warning if needed
        if recommended_periods and selected_period not in recommended_periods:
            st.sidebar.warning(f"⚠️ {selected_period} period may not work optimally with {selected_timeframe} timeframe. Recommended periods: {', '.join(recommended_periods[:3])}")
        
        # Show timeframe-specific info
        intraday_intervals = ['1m', '2m', '5m', '15m', '30m', '1h']
        if selected_timeframe in intraday_intervals:
            st.sidebar.info(f"📊 Intraday data: {selected_timeframe} intervals have limited historical range")
        
        # Overlay Controls (Phase 1: stubs)
        st.sidebar.subheader("📈 ICT Overlays")
        st.sidebar.markdown("*Phase 2+ Features*")
        
        overlays = {
            'moving_averages': st.sidebar.checkbox("Moving Averages", value=True),
            'order_blocks': st.sidebar.checkbox("Order Blocks", disabled=True),
            'fair_value_gaps': st.sidebar.checkbox("Fair Value Gaps", disabled=True), 
            'liquidity_levels': st.sidebar.checkbox("Liquidity Levels", disabled=True),
            'structure_lines': st.sidebar.checkbox("Market Structure", disabled=True)
        }
        
        # Analysis Header Placeholder
        st.sidebar.subheader("📋 Analysis Header")
        analysis_placeholder = st.sidebar.empty()
        
        return {
            'symbol': selected_symbol,
            'timeframe': selected_timeframe,
            'period': selected_period,
            'overlays': overlays,
            'analysis_placeholder': analysis_placeholder
        }
    
    def load_data(self, symbol: str, period: str, timeframe: str):
        """Load data and update session state"""
        try:
            with st.spinner(f"Loading {symbol} data ({period}/{timeframe})..."):
                data = self.data_fetcher.fetch_ohlcv(symbol, period, timeframe)
                
                # Handle 4h timeframe resampling
                if timeframe == '4h':
                    hourly_data = self.data_fetcher.fetch_ohlcv(symbol, period, '1h')
                    data = self.data_fetcher.resample_data(hourly_data, '4h')
                
                if data.empty:
                    st.error(f"No data available for {symbol} with {period} period and {timeframe} timeframe")
                    return False
                
                st.session_state.current_data = data
                st.session_state.current_symbol = symbol
                st.session_state.current_timeframe = timeframe
                
                # Show enhanced data summary
                data_range = f"{data['timestamp'].min().strftime('%Y-%m-%d %H:%M')} to {data['timestamp'].max().strftime('%Y-%m-%d %H:%M')}"
                st.success(f"✅ Loaded **{len(data)}** candles for **{symbol}** | 🗺 Range: {data_range}")
                self.logger.info(f"Loaded {len(data)} candles for {symbol}")
                return True
                
        except Exception as e:
            error_msg = str(e)
            if "period" in error_msg.lower() and "interval" in error_msg.lower():
                st.error(f"❌ **Timeframe Compatibility Issue**\n\n{error_msg}\n\n💡 **Tip:** Try a different period/timeframe combination for optimal results.")
            else:
                st.error(f"❌ **Error Loading Data**\n\n{error_msg}\n\n🔧 Please check your symbol or try again.")
            self.logger.error(f"Data loading error: {error_msg}")
            return False
    
    def render_chart(self, data: pd.DataFrame, symbol: str, timeframe: str, overlays: dict):
        """Render enhanced main chart with additional features"""
        if data.empty:
            st.warning("📊 No data to display. Please select a symbol and click 'Load Data'.")
            return
        
        # Create analysis header info
        header_info = self.chart_renderer.create_analysis_header(data, symbol)
        
        # Display key metrics above chart
        if header_info:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                price_color = "normal" if header_info['change'] == 0 else ("normal" if header_info['change'] > 0 else "inverse")
                st.metric(
                    label=f"💰 {symbol} Price",
                    value=f"${header_info['current_price']:.2f}",
                    delta=f"{header_info['change']:.2f} ({header_info['change_pct']:.1f}%)"
                )
            
            with col2:
                st.metric(
                    label="📈 24H High",
                    value=f"${header_info['high_24h']:.2f}"
                )
            
            with col3:
                st.metric(
                    label="📉 24H Low", 
                    value=f"${header_info['low_24h']:.2f}"
                )
            
            with col4:
                st.metric(
                    label="📊 Volume",
                    value=f"{header_info['volume']:,.0f}"
                )
        
        # Create enhanced base chart
        fig = self.chart_renderer.create_candlestick_chart(
            data, symbol, timeframe, height=Config.CHART_HEIGHT
        )
        
        # Add price action annotations
        fig = self.chart_renderer.add_price_action_annotations(fig, data)
        
        # Add overlays
        if overlays.get('moving_averages', False):
            fig = self.chart_renderer.add_moving_averages(fig, data)
        
        # Display enhanced chart
        st.plotly_chart(fig, use_container_width=True, config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d'],
            'modeBarButtonsToAdd': ['drawline', 'drawopenpath', 'eraseshape']
        })
        
        # Chart analysis summary
        with st.expander("📊 Chart Analysis", expanded=False):
            if not data.empty:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 Technical Overview")
                    
                    # Price action summary
                    latest = data.iloc[-1]
                    prev_week = data.iloc[-7] if len(data) > 7 else data.iloc[0]
                    week_change = latest['close'] - prev_week['close']
                    week_change_pct = (week_change / prev_week['close']) * 100 if prev_week['close'] != 0 else 0
                    
                    st.write(f"**Weekly Change:** ${week_change:.2f} ({week_change_pct:.1f}%)")
                    st.write(f"**Average Volume:** {data['volume'].mean():,.0f}")
                    st.write(f"**Price Volatility:** {((data['high'] - data['low']) / data['close']).mean() * 100:.1f}%")
                
                with col2:
                    st.subheader("🎢 Support & Resistance")
                    
                    # Calculate and display S/R levels
                    sr_levels = self.chart_renderer.calculate_support_resistance(data)
                    
                    if sr_levels['resistance']:
                        st.write(f"**Resistance:** ${sr_levels['resistance'][-1]:.2f}")
                    if sr_levels['support']:
                        st.write(f"**Support:** ${sr_levels['support'][-1]:.2f}")
                    
                    st.write(f"**Data Points:** {len(data)} candles")
                    st.write(f"**Timeframe:** {timeframe.upper()}")
        
        # Original metrics code moved up above chart (removed from here)
        col1, col2, col3, col4 = st.columns(4)
        
        if False:  # Disable original metrics display
            with col1:
                st.metric(
                    "Current Price", 
                    f"${latest['close']:.2f}",
                    f"{change:+.2f} ({change_pct:+.1f}%)"
                )
            
            with col2:
                st.metric("Volume", f"{latest['volume']:,.0f}")
            
            with col3:
                high_24h = data['high'].tail(24).max() if len(data) >= 24 else latest['high']
                st.metric("24h High", f"${high_24h:.2f}")
            
            with col4:
                low_24h = data['low'].tail(24).min() if len(data) >= 24 else latest['low']
                st.metric("24h Low", f"${low_24h:.2f}")
    
    def render_analysis_header(self, data: pd.DataFrame, symbol: str, placeholder):
        """Render analysis header in sidebar"""
        if not data.empty:
            analysis = self.chart_renderer.create_analysis_header(data, symbol)
            
            with placeholder.container():
                st.markdown(f"**Symbol:** {analysis['symbol']}")
                st.markdown(f"**Price:** ${analysis['current_price']:.2f}")
                st.markdown(f"**Change:** {analysis['change']:+.2f} ({analysis['change_pct']:+.1f}%)")
                st.markdown(f"**Volume:** {analysis['volume']:,.0f}")
                st.markdown(f"**Updated:** {analysis['timestamp'].strftime('%H:%M:%S')}")
        else:
            placeholder.markdown("*No data loaded*")
    
    def render_data_table(self, data: pd.DataFrame):
        """Render data table"""
        if not data.empty:
            st.subheader("📊 Raw Data")
            
            # Display options
            col1, col2 = st.columns([1, 3])
            
            with col1:
                show_rows = st.selectbox(
                    "Show rows:",
                    [10, 25, 50, 100, "All"],
                    index=0
                )
            
            # Prepare display data
            display_data = data.copy()
            display_data['timestamp'] = display_data['timestamp'].dt.strftime('%Y-%m-%d %H:%M')
            
            # Apply row limit
            if show_rows != "All":
                display_data = display_data.tail(show_rows)
            
            # Display table
            st.dataframe(
                display_data[['timestamp', 'open', 'high', 'low', 'close', 'volume']],
                use_container_width=True
            )
    
    def run(self):
        """Main application loop"""
        self.render_header()
        
        # Render sidebar and get controls
        controls = self.render_sidebar()
        
        # Main content area
        col1, col2 = st.columns([3, 1])
        
        with col2:
            st.subheader("🎛️ Data Controls")
            
            # Load data button
            if st.button("📥 Load Data", type="primary"):
                success = self.load_data(
                    controls['symbol'], 
                    controls['period'], 
                    controls['timeframe']
                )
                if success:
                    st.success(f"Loaded data for {controls['symbol']}")
            
            # Refresh button
            if st.button("🔄 Refresh"):
                st.session_state.current_data = pd.DataFrame()
                st.rerun()
            
            # Export data button (placeholder)
            st.button("📊 Export Data", disabled=True)
            st.markdown("*Export functionality coming in Phase 7*")
        
        with col1:
            st.subheader("📈 Chart Display")
            
            # Auto-load default data on first run
            if st.session_state.current_data.empty and controls['symbol'] == Config.DEFAULT_SYMBOL:
                with st.spinner("Loading default data..."):
                    self.load_data(
                        Config.DEFAULT_SYMBOL, 
                        "1y", 
                        Config.DEFAULT_TIMEFRAME
                    )
            
            # Render chart
            self.render_chart(
                st.session_state.current_data,
                st.session_state.current_symbol,
                st.session_state.current_timeframe, 
                controls['overlays']
            )
        
        # Update analysis header
        self.render_analysis_header(
            st.session_state.current_data,
            st.session_state.current_symbol,
            controls['analysis_placeholder']
        )
        
        # Data table (collapsible)
        with st.expander("📋 View Raw Data", expanded=False):
            self.render_data_table(st.session_state.current_data)
        
        # Footer
        st.markdown("---")
        st.markdown("**HINATA Phase 1** - Data Acquisition & Visualization | Version 1.0.0")

def main():
    """Main entry point"""
    try:
        app = HinataApp()
        app.run()
    except Exception as e:
        st.error(f"Application error: {str(e)}")
        logging.error(f"Application error: {str(e)}")

if __name__ == "__main__":
    main()