"""
HINATA Chart Rendering Module
Handles candlestick charts and technical overlays using Plotly
"""
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import logging
from src.utils.config import Config

class ChartRenderer:
    """Main chart rendering class for HINATA"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.colors = Config.COLORS
        self.ict_colors = Config.ICT_COLORS
        
    def create_candlestick_chart(self, data: pd.DataFrame, symbol: str, 
                               timeframe: str, height: int = 600) -> go.Figure:
        """
        Create main candlestick chart with volume
        
        Args:
            data: OHLCV DataFrame
            symbol: Trading symbol
            timeframe: Chart timeframe
            height: Chart height in pixels
            
        Returns:
            Plotly Figure object
        """
        if data.empty:
            return self._create_empty_chart("No data available")
        
        # Create subplots: main chart + volume
        fig = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.8, 0.2],
            subplot_titles=('', 'Volume')
        )
        
        # Add candlestick chart
        candlestick = go.Candlestick(
            x=data['timestamp'],
            open=data['open'],
            high=data['high'], 
            low=data['low'],
            close=data['close'],
            name='OHLC',
            increasing=dict(line=dict(color=self.colors['bullish'])),
            decreasing=dict(line=dict(color=self.colors['bearish']))
        )
        fig.add_trace(candlestick, row=1, col=1)
        
        # Add volume bars
        volume_colors = [
            self.colors['bullish'] if close >= open else self.colors['bearish']
            for close, open in zip(data['close'], data['open'])
        ]
        
        volume_bars = go.Bar(
            x=data['timestamp'],
            y=data['volume'],
            name='Volume',
            marker_color=volume_colors,
            opacity=0.6
        )
        fig.add_trace(volume_bars, row=2, col=1)
        
        # Update layout
        fig.update_layout(
            title=f"{symbol} - {timeframe.upper()} Chart",
            height=height,
            template='plotly_dark',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['paper'],
            font=dict(color=self.colors['text']),
            xaxis_rangeslider_visible=False,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        # Update axes
        fig.update_xaxes(
            gridcolor=self.colors['grid'],
            linecolor=self.colors['grid']
        )
        fig.update_yaxes(
            gridcolor=self.colors['grid'],
            linecolor=self.colors['grid']
        )
        
        # Hide volume y-axis title
        fig.update_yaxes(title_text="", row=2, col=1)
        
        return fig
    
    def add_moving_averages(self, fig: go.Figure, data: pd.DataFrame, 
                          periods: List[int] = [20, 50]) -> go.Figure:
        """Add moving averages to chart"""
        for i, period in enumerate(periods):
            if len(data) >= period:
                ma = data['close'].rolling(window=period).mean()
                color = self.colors['ma_fast'] if i == 0 else self.colors['ma_slow']
                
                fig.add_trace(
                    go.Scatter(
                        x=data['timestamp'],
                        y=ma,
                        mode='lines',
                        name=f'MA{period}',
                        line=dict(color=color, width=1.5),
                        opacity=0.8
                    ),
                    row=1, col=1
                )
        
        return fig
    
    def add_order_blocks(self, fig: go.Figure, order_blocks: List[Dict]) -> go.Figure:
        """Add ICT Order Blocks to chart"""
        for ob in order_blocks:
            color = (self.ict_colors['order_block_bullish'] 
                    if ob['type'] == 'bullish' 
                    else self.ict_colors['order_block_bearish'])
            
            fig.add_shape(
                type="rect",
                x0=ob['start_time'],
                x1=ob['end_time'],
                y0=ob['low'],
                y1=ob['high'],
                fillcolor=color,
                line=dict(width=1, color=color.replace('40', '')),
                name=f"OB ({ob['type']})"
            )
        
        return fig
    
    def add_fair_value_gaps(self, fig: go.Figure, fvgs: List[Dict]) -> go.Figure:
        """Add ICT Fair Value Gaps to chart"""
        for fvg in fvgs:
            color = (self.ict_colors['fvg_bullish'] 
                    if fvg['type'] == 'bullish'
                    else self.ict_colors['fvg_bearish'])
            
            fig.add_shape(
                type="rect", 
                x0=fvg['start_time'],
                x1=fvg['end_time'],
                y0=fvg['low'],
                y1=fvg['high'],
                fillcolor=color,
                line=dict(width=1, color=color.replace('40', ''), dash="dash"),
                name=f"FVG ({fvg['type']})"
            )
        
        return fig
    
    def add_liquidity_levels(self, fig: go.Figure, levels: List[Dict]) -> go.Figure:
        """Add liquidity levels (BSL/SSL) to chart"""
        for level in levels:
            fig.add_hline(
                y=level['price'],
                line=dict(
                    color=self.ict_colors['liquidity'],
                    width=2,
                    dash="dot"
                ),
                annotation=dict(
                    text=f"{level['type']} - {level['price']:.2f}",
                    bgcolor=self.ict_colors['liquidity'],
                    bordercolor=self.colors['text']
                )
            )
        
        return fig
    
    def add_structure_lines(self, fig: go.Figure, structure: List[Dict]) -> go.Figure:
        """Add market structure lines (BOS/ChoCH)"""
        for line in structure:
            fig.add_trace(
                go.Scatter(
                    x=[line['start_time'], line['end_time']],
                    y=[line['start_price'], line['end_price']],
                    mode='lines+markers',
                    name=f"{line['type']} - {line['direction']}",
                    line=dict(
                        color=self.ict_colors['structure'],
                        width=2,
                        dash="solid" if line['type'] == 'BOS' else "dashdot"
                    ),
                    marker=dict(size=8)
                ),
                row=1, col=1
            )
        
        return fig
    
    def create_analysis_header(self, data: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Create analysis header with key metrics"""
        if data.empty:
            return {}
        
        latest = data.iloc[-1]
        prev = data.iloc[-2] if len(data) > 1 else latest
        
        change = latest['close'] - prev['close']
        change_pct = (change / prev['close']) * 100 if prev['close'] != 0 else 0
        
        return {
            'symbol': symbol,
            'current_price': latest['close'],
            'change': change,
            'change_pct': change_pct,
            'high_24h': data['high'].tail(24).max() if len(data) >= 24 else latest['high'],
            'low_24h': data['low'].tail(24).min() if len(data) >= 24 else latest['low'],
            'volume': latest['volume'],
            'timestamp': latest['timestamp']
        }
    
    def _create_empty_chart(self, message: str = "No data") -> go.Figure:
        """Create empty chart with message"""
        fig = go.Figure()
        fig.add_annotation(
            text=message,
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=20, color=self.colors['text'])
        )
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=self.colors['background'],
            plot_bgcolor=self.colors['paper'],
            height=400
        )
        return fig
    
    def calculate_support_resistance(self, data: pd.DataFrame, 
                                   window: int = 20) -> Dict[str, List[float]]:
        """Calculate dynamic support and resistance levels"""
        if len(data) < window:
            return {'support': [], 'resistance': []}
        
        highs = data['high'].rolling(window=window, center=True).max()
        lows = data['low'].rolling(window=window, center=True).min()
        
        # Find local peaks and troughs
        resistance_levels = []
        support_levels = []
        
        for i in range(window, len(data) - window):
            if data['high'].iloc[i] == highs.iloc[i]:
                resistance_levels.append(data['high'].iloc[i])
            if data['low'].iloc[i] == lows.iloc[i]:
                support_levels.append(data['low'].iloc[i])
        
        # Remove duplicates and sort
        resistance_levels = sorted(list(set(resistance_levels)))[-5:]  # Top 5
        support_levels = sorted(list(set(support_levels)), reverse=True)[-5:]  # Bottom 5
        
        return {
            'support': support_levels,
            'resistance': resistance_levels
        }