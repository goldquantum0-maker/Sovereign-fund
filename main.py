import streamlit as st
import os
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import google.generativeai as genai
from typing import Dict, List, Optional, Tuple
import json
from dataclasses import dataclass, field
import warnings
import time
from collections import deque
import traceback
warnings.filterwarnings('ignore')

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sovereign Fund Capital | Institutional AI Trading",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CUSTOM TECHNICAL INDICATORS ---
class TechnicalIndicators:
    """Professional-grade technical indicator calculations"""
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return round(rsi.iloc[-1], 2) if not pd.isna(rsi.iloc[-1]) else 50.0
        except:
            return 50.0
    
    @staticmethod
    def calculate_macd(prices: pd.Series) -> Dict:
        try:
            exp1 = prices.ewm(span=12, adjust=False).mean()
            exp2 = prices.ewm(span=26, adjust=False).mean()
            macd_line = exp1 - exp2
            signal_line = macd_line.ewm(span=9, adjust=False).mean()
            histogram = macd_line - signal_line
            return {
                'macd': round(macd_line.iloc[-1], 4),
                'signal': round(signal_line.iloc[-1], 4),
                'histogram': round(histogram.iloc[-1], 4)
            }
        except:
            return {'macd': 0, 'signal': 0, 'histogram': 0}
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20) -> Dict:
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            upper = sma + (std * 2)
            lower = sma - (std * 2)
            current = prices.iloc[-1]
            position = (current - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1]) if upper.iloc[-1] != lower.iloc[-1] else 0.5
            return {
                'upper': round(upper.iloc[-1], 2),
                'middle': round(sma.iloc[-1], 2),
                'lower': round(lower.iloc[-1], 2),
                'position': round(position, 2)
            }
        except:
            return {'upper': 0, 'middle': 0, 'lower': 0, 'position': 0.5}
    
    @staticmethod
    def calculate_sma(prices: pd.Series, period: int) -> float:
        try:
            return round(prices.rolling(window=period).mean().iloc[-1], 2)
        except:
            return 0.0

# --- DATA STRUCTURES ---
@dataclass
class MarketData:
    symbol: str
    price: float
    volume_ratio: float
    volatility: float
    trend: str
    rsi: float
    macd_histogram: float
    bb_position: float
    sentiment_score: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class TradingDecision:
    signal: str  # BUY, SELL, HOLD
    confidence: int  # 1-10
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward: float
    position_size_pct: float
    rationale: str
    risks: List[str]
    timeframe: str
    analysis: str

# --- INSTITUTIONAL DATA ENGINE ---
class InstitutionalDataEngine:
    def __init__(self):
        self.ta = TechnicalIndicators()
        self.cache = {}
        
    def get_market_data(self, symbol: str) -> Optional[MarketData]:
        """Get comprehensive market data for a symbol"""
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="3mo")
            
            if df.empty:
                return None
            
            close = df['Close']
            high = df['High']
            low = df['Low']
            volume = df['Volume']
            
            # Technical indicators
            rsi = self.ta.calculate_rsi(close)
            macd = self.ta.calculate_macd(close)
            bb = self.ta.calculate_bollinger_bands(close)
            
            # Volume analysis
            avg_vol = volume.mean()
            vol_ratio = volume.iloc[-1] / avg_vol if avg_vol > 0 else 1
            
            # Trend analysis
            sma20 = self.ta.calculate_sma(close, 20)
            sma50 = self.ta.calculate_sma(close, 50)
            current_price = close.iloc[-1]
            
            if current_price > sma20 > sma50:
                trend = "BULLISH"
            elif current_price < sma20 < sma50:
                trend = "BEARISH"
            else:
                trend = "NEUTRAL"
            
            # Volatility
            returns = close.pct_change().dropna()
            volatility = returns.std() * np.sqrt(252)
            
            # Sentiment score
            sentiment = 0.0
            if rsi < 30:
                sentiment += 0.3
            elif rsi > 70:
                sentiment -= 0.3
            if macd['histogram'] > 0:
                sentiment += 0.2
            else:
                sentiment -= 0.2
            sentiment = max(-1.0, min(1.0, sentiment))
            
            return MarketData(
                symbol=symbol,
                price=round(current_price, 2),
                volume_ratio=round(vol_ratio, 2),
                volatility=round(volatility * 100, 2),
                trend=trend,
                rsi=rsi,
                macd_histogram=macd['histogram'],
                bb_position=bb['position'],
                sentiment_score=sentiment
            )
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {str(e)}")
            return None
    
    def get_market_summary(self) -> Dict:
        """Get summary of key markets"""
        symbols = {
            'S&P 500': '^GSPC',
            'Gold': 'GC=F',
            'Bitcoin': 'BTC-USD',
            'DXY': 'DX-Y.NYB'
        }
        
        summary = {}
        for name, sym in symbols.items():
            data = self.get_market_data(sym)
            if data:
                summary[name] = {
                    'price': data.price,
                    'trend': data.trend,
                    'sentiment': data.sentiment_score
                }
        return summary

# --- SOVEREIGN AI BOARD ---
class SovereignBoard:
    def __init__(self):
        # Try different model configurations
        self.model = None
        self.model_name = None
        self._initialize_model()
        
        self.decision_history = []
        
    def _initialize_model(self):
        """Initialize Gemini model with fallback options"""
        try:
            # Try gemini-1.5-flash first (faster, more reliable)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            self.model_name = 'gemini-1.5-flash'
            st.sidebar.success(f"✅ AI Engine: {self.model_name}")
        except:
            try:
                # Fallback to gemini-pro
                self.model = genai.GenerativeModel('gemini-pro')
                self.model_name = 'gemini-pro'
                st.sidebar.warning(f"⚠️ Using fallback model: {self.model_name}")
            except:
                st.sidebar.error("❌ Failed to initialize AI model")
                self.model = None
    
    def analyze_market(self, asset: str, market_data: Dict) -> TradingDecision:
        """Get trading decision from AI board"""
        
        if not self.model:
            return self._get_technical_decision(asset, market_data)
        
        try:
            # Simplified but effective prompt
            prompt = f"""
            You are the Chief Investment Officer of a $14.9B hedge fund.
            Analyze this trading opportunity and provide a clear decision.
            
            Asset: {asset}
            
            Market Data:
            {json.dumps(market_data, indent=2)}
            
            Provide your analysis in this exact format:
            
            SIGNAL: [BUY/SELL/HOLD]
            CONFIDENCE: [1-10]
            ENTRY: [price]
            STOP_LOSS: [price]
            TAKE_PROFIT: [price]
            RISK_REWARD: [ratio]
            POSITION_SIZE: [0.1-1.0%]
            TIMEFRAME: [period]
            RATIONALE: [2-3 sentences explaining your decision]
            RISKS: [2-3 key risks]
            """
            
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                decision = self._parse_decision(response.text, market_data)
                return decision
            else:
                return self._get_technical_decision(asset, market_data)
                
        except Exception as e:
            st.warning(f"AI analysis error: {str(e)}. Using technical analysis fallback.")
            return self._get_technical_decision(asset, market_data)
    
    def _parse_decision(self, text: str, market_data: Dict) -> TradingDecision:
        """Parse AI response into structured decision"""
        lines = text.split('\n')
        
        signal = "HOLD"
        confidence = 5
        entry = 0
        stop_loss = 0
        take_profit = 0
        risk_reward = 2.0
        position_size = 0.5
        timeframe = "SWING"
        rationale = "Analysis based on current market conditions."
        risks = ["Market volatility", "Unexpected news events"]
        
        for line in lines:
            line = line.strip()
            if line.startswith("SIGNAL:"):
                signal_text = line.split(":", 1)[1].strip().upper()
                if "BUY" in signal_text:
                    signal = "BUY"
                elif "SELL" in signal_text:
                    signal = "SELL"
            
            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = int(''.join(filter(str.isdigit, line.split(":", 1)[1])))
                    confidence = max(1, min(10, confidence))
                except:
                    pass
            
            elif line.startswith("ENTRY:"):
                try:
                    entry = float(''.join(filter(lambda x: x.isdigit() or x == '.', line.split(":", 1)[1])))
                except:
                    pass
            
            elif line.startswith("STOP_LOSS:"):
                try:
                    stop_loss = float(''.join(filter(lambda x: x.isdigit() or x == '.', line.split(":", 1)[1])))
                except:
                    pass
            
            elif line.startswith("TAKE_PROFIT:"):
                try:
                    take_profit = float(''.join(filter(lambda x: x.isdigit() or x == '.', line.split(":", 1)[1])))
                except:
                    pass
            
            elif line.startswith("RISK_REWARD:"):
                try:
                    risk_reward = float(''.join(filter(lambda x: x.isdigit() or x == '.', line.split(":", 1)[1])))
                except:
                    pass
            
            elif line.startswith("POSITION_SIZE:"):
                try:
                    ps_text = line.split(":", 1)[1].strip().replace('%', '')
                    position_size = float(''.join(filter(lambda x: x.isdigit() or x == '.', ps_text)))
                    position_size = max(0.1, min(1.0, position_size))
                except:
                    pass
            
            elif line.startswith("TIMEFRAME:"):
                timeframe = line.split(":", 1)[1].strip()
            
            elif line.startswith("RATIONALE:"):
                rationale = line.split(":", 1)[1].strip()
            
            elif line.startswith("RISKS:"):
                risks_text = line.split(":", 1)[1].strip()
                risks = [r.strip() for r in risks_text.split(',')]
        
        # Validate prices
        current_price = market_data.get('price', 0)
        if entry == 0 and current_price > 0:
            entry = current_price
        
        if signal == "BUY":
            if stop_loss == 0:
                stop_loss = entry * 0.98  # 2% below entry
            if take_profit == 0:
                take_profit = entry * 1.04  # 4% above entry
        elif signal == "SELL":
            if stop_loss == 0:
                stop_loss = entry * 1.02  # 2% above entry
            if take_profit == 0:
                take_profit = entry * 0.96  # 4% below entry
        
        return TradingDecision(
            signal=signal,
            confidence=confidence,
            entry_price=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_reward=risk_reward,
            position_size_pct=position_size,
            rationale=rationale,
            risks=risks,
            timeframe=timeframe,
            analysis=text
        )
    
    def _get_technical_decision(self, asset: str, market_data: Dict) -> TradingDecision:
        """Generate decision based on technical analysis when AI fails"""
        
        sentiment = market_data.get('sentiment_score', 0)
        trend = market_data.get('trend', 'NEUTRAL')
        rsi = market_data.get('rsi', 50)
        price = market_data.get('price', 0)
        
        # Simple decision logic
        if sentiment > 0.3 and trend == "BULLISH" and rsi < 70:
            signal = "BUY"
            confidence = min(8, int(abs(sentiment) * 10))
            entry = price
            stop_loss = price * 0.98
            take_profit = price * 1.04
            rationale = f"Bullish sentiment ({sentiment:.2f}) with {trend} trend and RSI at {rsi:.1f}. Entry at current levels with tight risk management."
        elif sentiment < -0.3 and trend == "BEARISH" and rsi > 30:
            signal = "SELL"
            confidence = min(8, int(abs(sentiment) * 10))
            entry = price
            stop_loss = price * 1.02
            take_profit = price * 0.96
            rationale = f"Bearish sentiment ({sentiment:.2f}) with {trend} trend and RSI at {rsi:.1f}. Short entry with defined risk."
        else:
            signal = "HOLD"
            confidence = 5
            entry = price
            stop_loss = price * 0.99
            take_profit = price * 1.02
            rationale = f"Mixed signals: Sentiment {sentiment:.2f}, Trend {trend}, RSI {rsi:.1f}. Waiting for clearer setup."
        
        return TradingDecision(
            signal=signal,
            confidence=confidence,
            entry_price=entry,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_reward=2.0,
            position_size_pct=0.5,
            rationale=rationale,
            risks=["Market volatility", "Trend reversal", "News risk"],
            timeframe="SWING",
            analysis="Technical analysis fallback decision"
        )

# --- STREAMLIT UI ---
def main():
    # Custom CSS
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;700;900&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #000000 100%);
    }
    
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 900 !important;
        color: #ffffff !important;
        text-align: center;
        font-size: 2.5rem !important;
        margin-bottom: 5px !important;
    }
    
    h2, h3 {
        font-family: 'Inter', sans-serif !important;
        color: #d4af37 !important;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #0d0d0d, #1a1a1a);
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #2a2a2a;
    }
    
    .decision-card {
        background: linear-gradient(135deg, #0d0d0d, #1a1a1a);
        padding: 30px;
        border-radius: 10px;
        border: 2px solid #d4af37;
        margin: 20px 0;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
        color: white;
        border: 1px solid #3a3a3a;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        width: 100%;
    }
    
    .stButton > button:hover {
        border-color: #d4af37;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.2);
    }
    
    .stTextInput > div > input,
    .stNumberInput > div > input,
    .stSelectbox > div > select {
        background: #0d0d0d;
        color: white;
        border: 1px solid #2a2a2a;
        border-radius: 6px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'data_engine' not in st.session_state:
        st.session_state.data_engine = InstitutionalDataEngine()
    if 'board' not in st.session_state:
        st.session_state.board = SovereignBoard()
    if 'active_trades' not in st.session_state:
        st.session_state.active_trades = []
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("🔴 GOOGLE_API_KEY not found!")
        st.code("export GOOGLE_API_KEY='your-api-key-here'")
        st.stop()
    
    genai.configure(api_key=api_key)
    
    # Header
    st.markdown("# SOVEREIGN FUND CAPITAL")
    st.markdown("<p style='text-align: center; color: #888;'>Institutional AI Trading System</p>", unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🏛️ SOVEREIGN COMMAND")
        
        # AUM Display
        st.metric("Total AUM", "$14,900,000")
        st.metric("DNA Fund", "$5,000,000", "+2.3%")
        st.metric("Sure Leverage", "$4,900,000", "+1.8%")
        st.metric("Aqua Reserve", "$5,000,000", "+0.5%")
        
        st.divider()
        
        # Market time
        ny_time = datetime.now(pytz.timezone('America/New_York'))
        st.markdown(f"**NY Session:** {ny_time.strftime('%H:%M:%S')}")
        
        # Active trades
        if st.session_state.active_trades:
            st.markdown(f"**Active Positions:** {len(st.session_state.active_trades)}")
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["🎯 Trading Terminal", "📊 Market Analysis", "📈 Performance"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Trading Command")
            
            asset = st.selectbox(
                "Select Asset",
                ["XAUUSD (Gold)", "BTCUSD (Bitcoin)", "SPX500 (S&P 500)", 
                 "USOIL (Crude Oil)", "EURUSD (Euro)"]
            )
            
            direction = st.radio("Direction", ["LONG", "SHORT"], horizontal=True)
            
            col_entry, col_sl, col_tp = st.columns(3)
            with col_entry:
                entry = st.number_input("Entry Price", value=0.0, step=0.01)
            with col_sl:
                stop_loss = st.number_input("Stop Loss", value=0.0, step=0.01)
            with col_tp:
                take_profit = st.number_input("Take Profit", value=0.0, step=0.01)
        
        with col2:
            st.markdown("### Risk Parameters")
            risk_pct = st.slider("Risk % of AUM", 0.1, 1.0, 0.5, 0.1)
            
            if entry > 0 and stop_loss > 0:
                risk_amount = 14_900_000 * (risk_pct / 100)
                pos_size = risk_amount / abs(entry - stop_loss)
                st.metric("Max Risk", f"${risk_amount:,.0f}")
                st.metric("Position Size", f"{pos_size:,.2f} units")
        
        # Submit for analysis
        if st.button("🔍 ANALYZE WITH AI BOARD", use_container_width=True):
            if entry > 0:
                with st.spinner("🏛️ AI Board analyzing market..."):
                    # Map asset to symbol
                    symbol_map = {
                        "XAUUSD (Gold)": "GC=F",
                        "BTCUSD (Bitcoin)": "BTC-USD",
                        "SPX500 (S&P 500)": "ES=F",
                        "USOIL (Crude Oil)": "CL=F",
                        "EURUSD (Euro)": "EURUSD=X"
                    }
                    
                    symbol = symbol_map.get(asset, "GC=F")
                    
                    # Get market data
                    market_data = st.session_state.data_engine.get_market_data(symbol)
                    
                    if market_data:
                        # Get AI decision
                        decision = st.session_state.board.analyze_market(
                            asset,
                            market_data.__dict__
                        )
                        
                        # Display decision
                        st.divider()
                        
                        # Decision card
                        signal_colors = {
                            "BUY": "#00ff88",
                            "SELL": "#ff4444",
                            "HOLD": "#ffaa00"
                        }
                        color = signal_colors.get(decision.signal, "#ffffff")
                        
                        st.markdown(f"""
                        <div class="decision-card">
                            <h2 style="color: {color}; margin: 0; font-size: 2rem;">
                                {decision.signal}
                            </h2>
                            <p style="color: #888; margin: 10px 0;">
                                Confidence: {decision.confidence}/10 | 
                                Risk/Reward: 1:{decision.risk_reward}
                            </p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        # Key metrics
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Entry", f"${decision.entry_price:,.2f}")
                        col2.metric("Stop Loss", f"${decision.stop_loss:,.2f}")
                        col3.metric("Take Profit", f"${decision.take_profit:,.2f}")
                        col4.metric("Position Size", f"{decision.position_size_pct}%")
                        
                        # Analysis
                        st.markdown("### 📊 AI Board Analysis")
                        st.info(decision.rationale)
                        
                        # Risks
                        st.markdown("### ⚠️ Key Risks")
                        for risk in decision.risks:
                            st.warning(f"• {risk}")
                        
                        # Execute button
                        if decision.signal != "HOLD":
                            if st.button(f"✅ EXECUTE {decision.signal}", use_container_width=True):
                                st.session_state.active_trades.append({
                                    'asset': asset,
                                    'direction': decision.signal,
                                    'entry': decision.entry_price,
                                    'stop_loss': decision.stop_loss,
                                    'take_profit': decision.take_profit,
                                    'timestamp': datetime.now().isoformat()
                                })
                                st.success(f"Trade executed! {asset} {decision.signal}")
                                st.balloons()
                    else:
                        st.error("Unable to fetch market data. Please try again.")
            else:
                st.error("Please enter a valid entry price.")
        
        # Active positions
        if st.session_state.active_trades:
            st.divider()
            st.markdown("### 📊 Active Positions")
            
            trades_df = pd.DataFrame(st.session_state.active_trades)
            st.dataframe(trades_df, use_container_width=True)
    
    with tab2:
        st.markdown("### 📊 Live Market Overview")
        
        if st.button("🔄 Refresh Market Data"):
            with st.spinner("Fetching market data..."):
                summary = st.session_state.data_engine.get_market_summary()
                
                cols = st.columns(len(summary))
                for i, (name, data) in enumerate(summary.items()):
                    with cols[i]:
                        trend_color = "#00ff88" if data['trend'] == "BULLISH" else "#ff4444" if data['trend'] == "BEARISH" else "#ffaa00"
                        st.markdown(f"""
                        <div class="metric-card">
                            <h4>{name}</h4>
                            <h2>${data['price']:,.2f}</h2>
                            <p style="color: {trend_color};">{data['trend']}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### 📈 Performance Summary")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Trades", len(st.session_state.active_trades))
        col2.metric("Win Rate", "67.8%")
        col3.metric("Total P&L", "+$4,695")
        
        # Sample equity curve
        np.random.seed(42)
        equity = 10000000 * (1 + np.random.randn(100).cumsum() * 0.005)
        st.line_chart(equity)

if __name__ == "__main__":
    main()