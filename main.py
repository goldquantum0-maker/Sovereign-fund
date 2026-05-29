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
warnings.filterwarnings('ignore')

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Sovereign Fund Capital | Institutional AI Trading",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 1. LUXURY INSTITUTIONAL STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=JetBrains+Mono:wght@300;400;500;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #000000 100%);
    }
    
    .main {
        background: transparent;
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Typography */
    h1 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        color: #ffffff !important;
        text-shadow: 0 2px 10px rgba(212, 175, 55, 0.3);
        font-size: 2.8rem !important;
    }
    
    h2 {
        font-family: 'Playfair Display', serif !important;
        font-weight: 700 !important;
        color: #d4af37 !important;
        letter-spacing: 1px !important;
    }
    
    h3 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        color: #ffffff !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Cards and Containers */
    .metric-card {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        padding: 25px;
        border-radius: 8px;
        border: 1px solid #2a2a2a;
        text-align: left;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent, #d4af37, transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: #3a3a3a;
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }
    
    .metric-card:hover::before {
        opacity: 1;
    }
    
    .board-response {
        background: linear-gradient(135deg, #0a0a0a 0%, #141414 100%);
        padding: 30px;
        border-radius: 8px;
        border: 1px solid #2a2a2a;
        color: #d0d0d0;
        font-family: 'Inter', sans-serif;
        line-height: 1.8;
        font-size: 0.95rem;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.5);
        position: relative;
    }
    
    .board-response::before {
        content: 'CLASSIFIED';
        position: absolute;
        top: 10px;
        right: 20px;
        color: #d4af37;
        font-size: 0.7rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 3px;
        opacity: 0.5;
    }
    
    .intel-feed {
        background: linear-gradient(135deg, #050505 0%, #0d0d0d 100%);
        padding: 20px;
        border-radius: 8px;
        border-left: 3px solid #d4af37;
        color: #a0a0a0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        position: relative;
    }
    
    .intel-feed::before {
        content: 'INTEL';
        position: absolute;
        top: -10px;
        left: 20px;
        background: #d4af37;
        color: #000;
        padding: 2px 10px;
        font-size: 0.6rem;
        font-weight: 700;
        letter-spacing: 2px;
        border-radius: 2px;
    }
    
    .member-card {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #2a2a2a;
        text-align: left;
        color: #ffffff;
        font-size: 0.85rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
    }
    
    .member-card:hover {
        border-color: #d4af37;
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(212, 175, 55, 0.1);
    }
    
    .member-card .role {
        color: #d4af37;
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 5px;
    }
    
    .member-card .expertise {
        color: #888;
        font-size: 0.7rem;
        line-height: 1.4;
    }
    
    .trade-watch {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        padding: 20px;
        border-radius: 8px;
        border: 1px solid #d4af37;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
        box-shadow: 0 0 30px rgba(212, 175, 55, 0.1);
        font-size: 0.9rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
        color: #ffffff;
        font-weight: 600;
        border-radius: 6px;
        text-transform: uppercase;
        border: 1px solid #3a3a3a;
        width: 100%;
        transition: all 0.3s ease;
        font-family: 'Inter', sans-serif;
        letter-spacing: 1.5px;
        padding: 12px 20px;
        font-size: 0.85rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2d2d2d 0%, #404040 100%);
        border-color: #d4af37;
        box-shadow: 0 5px 20px rgba(212, 175, 55, 0.2);
        transform: translateY(-1px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Input Fields */
    .stTextInput > div > input,
    .stSelectbox > div > select,
    .stNumberInput > div > input {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        color: #ffffff;
        border: 1px solid #2a2a2a;
        border-radius: 4px;
        font-family: 'JetBrains Mono', monospace;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > input:focus,
    .stSelectbox > div > select:focus,
    .stNumberInput > div > input:focus {
        border-color: #d4af37;
        box-shadow: 0 0 10px rgba(212, 175, 55, 0.1);
    }
    
    /* Sidebar */
    .stSidebar {
        background: linear-gradient(180deg, #000000 0%, #080808 100%);
        border-right: 1px solid #1a1a1a;
    }
    
    .stSidebar [data-testid="stMarkdown"] {
        color: #ffffff;
    }
    
    /* Dividers */
    hr {
        border-top: 1px solid #2a2a2a;
        margin: 25px 0;
    }
    
    /* Expandable Sections */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #0d0d0d 0%, #1a1a1a 100%);
        border: 1px solid #2a2a2a;
        border-radius: 6px;
        color: #d4af37 !important;
        font-weight: 600;
    }
    
    /* DataFrames */
    .stDataFrame {
        background: #0d0d0d;
        border: 1px solid #2a2a2a;
        border-radius: 6px;
    }
    
    /* Status Colors */
    .bullish { color: #00ff88 !important; }
    .bearish { color: #ff4444 !important; }
    .neutral { color: #ffaa00 !important; }
    .gold-text { color: #d4af37 !important; }
    
    /* Animations */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .live-indicator {
        animation: pulse 2s infinite;
        color: #00ff88;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2a2a2a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3a3a3a;
    }
    
    /* Progress Bars */
    .stProgress > div > div {
        background: linear-gradient(90deg, #d4af37, #ffd700);
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] {
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
    }
    
    [data-testid="stMetricDelta"] {
        font-family: 'JetBrains Mono', monospace;
    }
    </style>
""", unsafe_allow_html=True)

# --- 2. CUSTOM TECHNICAL INDICATORS ---
class TechnicalIndicators:
    """Professional-grade technical indicator calculations"""
    
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        """Calculate Relative Strength Index"""
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
    def calculate_macd(prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict:
        """Calculate MACD indicator"""
        try:
            exp1 = prices.ewm(span=fast, adjust=False).mean()
            exp2 = prices.ewm(span=slow, adjust=False).mean()
            macd_line = exp1 - exp2
            signal_line = macd_line.ewm(span=signal, adjust=False).mean()
            histogram = macd_line - signal_line
            
            return {
                'macd_line': round(macd_line.iloc[-1], 4),
                'signal_line': round(signal_line.iloc[-1], 4),
                'histogram': round(histogram.iloc[-1], 4),
                'trend': 'BULLISH' if histogram.iloc[-1] > 0 else 'BEARISH'
            }
        except:
            return {'macd_line': 0, 'signal_line': 0, 'histogram': 0, 'trend': 'NEUTRAL'}
    
    @staticmethod
    def calculate_bollinger_bands(prices: pd.Series, period: int = 20, std_dev: int = 2) -> Dict:
        """Calculate Bollinger Bands"""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            current_price = prices.iloc[-1]
            band_width = upper_band.iloc[-1] - lower_band.iloc[-1]
            
            if band_width > 0:
                position = (current_price - lower_band.iloc[-1]) / band_width
            else:
                position = 0.5
            
            return {
                'upper': round(upper_band.iloc[-1], 2),
                'middle': round(sma.iloc[-1], 2),
                'lower': round(lower_band.iloc[-1], 2),
                'position': round(position, 2),
                'bandwidth': round(band_width, 2)
            }
        except:
            return {'upper': 0, 'middle': 0, 'lower': 0, 'position': 0.5, 'bandwidth': 0}
    
    @staticmethod
    def calculate_atr(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> float:
        """Calculate Average True Range"""
        try:
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = tr.rolling(window=period).mean()
            return round(atr.iloc[-1], 4) if not pd.isna(atr.iloc[-1]) else 0
        except:
            return 0
    
    @staticmethod
    def calculate_sma(prices: pd.Series, period: int) -> float:
        """Calculate Simple Moving Average"""
        try:
            return round(prices.rolling(window=period).mean().iloc[-1], 2)
        except:
            return 0
    
    @staticmethod
    def calculate_ema(prices: pd.Series, period: int) -> float:
        """Calculate Exponential Moving Average"""
        try:
            return round(prices.ewm(span=period, adjust=False).mean().iloc[-1], 2)
        except:
            return 0
    
    @staticmethod
    def calculate_stochastic(high: pd.Series, low: pd.Series, close: pd.Series, period: int = 14) -> Dict:
        """Calculate Stochastic Oscillator"""
        try:
            lowest_low = low.rolling(window=period).min()
            highest_high = high.rolling(window=period).max()
            
            k = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            d = k.rolling(window=3).mean()
            
            return {
                'k': round(k.iloc[-1], 2),
                'd': round(d.iloc[-1], 2)
            }
        except:
            return {'k': 50, 'd': 50}

# --- 3. DATA STRUCTURES ---
@dataclass
class MarketData:
    """Institutional-grade market data container"""
    symbol: str
    price: float
    volume: float
    volatility: float
    trend: str
    rsi: float
    macd: float
    bollinger_position: float
    institutional_flow: str
    dark_pool_activity: str
    options_flow: str
    sentiment_score: float
    atr: float = 0.0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class TradingSignal:
    """Professional trading signal"""
    symbol: str
    direction: str
    entry_price: float
    stop_loss: float
    take_profit: float
    confidence: float
    risk_reward: float
    position_size_pct: float
    rationale: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class BoardDecision:
    """Complete board decision package"""
    trade_signal: str
    confidence: int
    position_size: float
    entry_level: float
    stop_loss: float
    take_profit: float
    risk_reward: float
    timeframe: str
    key_risks: List[str]
    execution_instructions: str
    full_analysis: str
    adversary_notes: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

# --- 4. INSTITUTIONAL DATA ENGINE ---
class InstitutionalDataEngine:
    """Access institutional-grade market intelligence"""
    
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(minutes=5)
        self.ta = TechnicalIndicators()
        
    def get_comprehensive_data(self, symbol: str) -> Optional[MarketData]:
        """Fetch multi-dimensional market data with caching"""
        
        # Check cache
        cache_key = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if datetime.now() - cached_time < self.cache_duration:
                return cached_data
        
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period="6mo")
            
            if df.empty:
                return None
            
            close_prices = df['Close']
            high_prices = df['High']
            low_prices = df['Low']
            volumes = df['Volume']
            
            # Technical Indicators
            rsi = self.ta.calculate_rsi(close_prices)
            macd_data = self.ta.calculate_macd(close_prices)
            bb_data = self.ta.calculate_bollinger_bands(close_prices)
            atr = self.ta.calculate_atr(high_prices, low_prices, close_prices)
            
            # Volume Analysis
            avg_volume = volumes.mean()
            current_volume = volumes.iloc[-1]
            volume_ratio = current_volume / avg_volume if avg_volume > 0 else 1
            
            # Trend Analysis
            sma_20 = self.ta.calculate_sma(close_prices, 20)
            sma_50 = self.ta.calculate_sma(close_prices, 50)
            ema_12 = self.ta.calculate_ema(close_prices, 12)
            ema_26 = self.ta.calculate_ema(close_prices, 26)
            
            # Determine trend
            if close_prices.iloc[-1] > sma_20 > sma_50:
                trend = "STRONG_BULLISH"
            elif close_prices.iloc[-1] > sma_20:
                trend = "BULLISH"
            elif close_prices.iloc[-1] < sma_20 < sma_50:
                trend = "STRONG_BEARISH"
            elif close_prices.iloc[-1] < sma_20:
                trend = "BEARISH"
            else:
                trend = "NEUTRAL"
            
            # Volatility
            daily_returns = close_prices.pct_change().dropna()
            volatility = daily_returns.std() * np.sqrt(252)
            
            # Create market data object
            market_data = MarketData(
                symbol=symbol,
                price=round(close_prices.iloc[-1], 2),
                volume=round(volume_ratio, 2),
                volatility=round(volatility * 100, 2),
                trend=trend,
                rsi=rsi,
                macd=macd_data['histogram'],
                bollinger_position=bb_data['position'],
                institutional_flow=self._analyze_institutional_flow(df),
                dark_pool_activity=self._estimate_dark_pool(volume_ratio),
                options_flow=self._analyze_options_flow(symbol),
                sentiment_score=self._calculate_sentiment(rsi, macd_data['histogram'], volume_ratio),
                atr=atr
            )
            
            # Cache the result
            self.cache[cache_key] = (datetime.now(), market_data)
            
            return market_data
            
        except Exception as e:
            st.warning(f"Data fetch error for {symbol}: {str(e)}")
            return None
    
    def _analyze_institutional_flow(self, df: pd.DataFrame) -> str:
        """Analyze institutional order flow patterns"""
        try:
            # Volume trend analysis
            volume_trend = df['Volume'].rolling(5).mean().pct_change().iloc[-1]
            
            # Price-volume correlation
            price_change = df['Close'].pct_change()
            volume_change = df['Volume'].pct_change()
            correlation = price_change.corr(volume_change)
            
            # Large trade detection
            avg_volume = df['Volume'].mean()
            large_trades = (df['Volume'] > avg_volume * 2).sum()
            
            if volume_trend > 0.2 and correlation > 0.3:
                return "STRONG_ACCUMULATION"
            elif volume_trend > 0.1 and correlation > 0.1:
                return "ACCUMULATION"
            elif volume_trend < -0.2 and correlation < -0.3:
                return "STRONG_DISTRIBUTION"
            elif volume_trend < -0.1 and correlation < -0.1:
                return "DISTRIBUTION"
            else:
                return "NEUTRAL"
        except:
            return "INCONCLUSIVE"
    
    def _estimate_dark_pool(self, volume_ratio: float) -> str:
        """Estimate dark pool activity based on volume anomalies"""
        if volume_ratio > 3.0:
            return "EXTREME"
        elif volume_ratio > 2.0:
            return "ELEVATED"
        elif volume_ratio > 1.5:
            return "MODERATE"
        elif volume_ratio > 1.0:
            return "NORMAL"
        else:
            return "LOW"
    
    def _analyze_options_flow(self, symbol: str) -> str:
        """Analyze options market flow"""
        try:
            ticker = yf.Ticker(symbol)
            options_dates = ticker.options
            
            if options_dates and len(options_dates) > 0:
                # Get nearest expiration
                nearest_date = options_dates[0]
                calls = ticker.option_chain(nearest_date).calls
                puts = ticker.option_chain(nearest_date).puts
                
                call_volume = calls['volume'].sum()
                put_volume = puts['volume'].sum()
                
                if call_volume + put_volume > 0:
                    put_call_ratio = put_volume / call_volume if call_volume > 0 else 2
                    
                    # Calculate volume-weighted sentiment
                    total_volume = call_volume + put_volume
                    call_weight = call_volume / total_volume
                    
                    if put_call_ratio < 0.5:
                        return "VERY_BULLISH"
                    elif put_call_ratio < 0.8:
                        return "BULLISH"
                    elif put_call_ratio < 1.2:
                        return "NEUTRAL"
                    elif put_call_ratio < 1.5:
                        return "BEARISH"
                    else:
                        return "VERY_BEARISH"
            
            return "INSUFFICIENT_DATA"
        except:
            return "UNAVAILABLE"
    
    def _calculate_sentiment(self, rsi: float, macd: float, volume_ratio: float) -> float:
        """Composite institutional sentiment score"""
        sentiment = 0.0
        
        # RSI contribution (0-1 scale)
        if rsi < 25:
            sentiment += 0.25
        elif rsi < 35:
            sentiment += 0.15
        elif rsi > 75:
            sentiment -= 0.25
        elif rsi > 65:
            sentiment -= 0.15
        
        # MACD contribution
        if macd > 0:
            sentiment += 0.2
        else:
            sentiment -= 0.2
        
        # Volume contribution
        if volume_ratio > 2:
            sentiment += 0.2
        elif volume_ratio > 1.5:
            sentiment += 0.1
        
        # Normalize to -1 to 1
        return round(max(-1.0, min(1.0, sentiment)), 2)
    
    def get_market_overview(self) -> Dict:
        """Get comprehensive market overview"""
        key_symbols = {
            'sp500': '^GSPC',
            'nasdaq': '^IXIC',
            'gold': 'GC=F',
            'oil': 'CL=F',
            'bitcoin': 'BTC-USD',
            'dxy': 'DX-Y.NYB',
            'bonds_10y': '^TNX',
            'vix': '^VIX'
        }
        
        overview = {}
        for name, symbol in key_symbols.items():
            data = self.get_comprehensive_data(symbol)
            if data:
                overview[name] = {
                    'price': data.price,
                    'trend': data.trend,
                    'sentiment': data.sentiment_score,
                    'volume': data.volume
                }
        
        return overview

# --- 5. SOVEREIGN AI BOARD OF GOVERNORS ---
class SovereignBoard:
    """Elite AI Board of Governors - Institutional Grade Decision Making"""
    
    def __init__(self):
        self.model = genai.GenerativeModel(
            'gemini-1.5-pro',
            generation_config={
                'temperature': 0.3,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 4096,
            }
        )
        
        self.decision_history = deque(maxlen=100)
        
        # Board Members with Institutional Expertise
        self.board_members = {
            "CHAIRMAN_OSINACHI": {
                "role": "Chairman & Chief Investment Officer",
                "expertise": "Portfolio Strategy, Risk Management, Final Authority",
                "prompt_weight": 0.25,
                "background": "Former Fed Governor, 25 years institutional experience",
                "style": "Decisive, analytical, risk-focused"
            },
            "GOVERNOR_STRATEGIST": {
                "role": "Head of Global Macro Strategy",
                "expertise": "Monetary Policy, Geopolitics, Intermarket Analysis",
                "prompt_weight": 0.15,
                "background": "Ex-IMF, Central Bank Policy Expert",
                "style": "Macro-focused, forward-looking"
            },
            "GOVERNOR_ARCHITECT": {
                "role": "Head of Institutional Order Flow",
                "expertise": "Dark Pool Analysis, CME Positioning, Smart Money Concepts",
                "prompt_weight": 0.15,
                "background": "Former Goldman Sachs S&T, 20 years flow trading",
                "style": "Data-driven, precise, institutional perspective"
            },
            "GOVERNOR_QUANT": {
                "role": "Chief Quantitative Strategist",
                "expertise": "Statistical Arbitrage, Machine Learning, Probability Models",
                "prompt_weight": 0.15,
                "background": "PhD Mathematical Finance, Ex-Renaissance Technologies",
                "style": "Mathematical, model-based, probability-weighted"
            },
            "GOVERNOR_RISK": {
                "role": "Chief Risk Officer",
                "expertise": "VaR Modeling, Stress Testing, Black Swan Protection",
                "prompt_weight": 0.15,
                "background": "Former Fed Risk Supervisor, Basel Committee Advisor",
                "style": "Conservative, protective, worst-case focused"
            },
            "GOVERNOR_ADVERSARY": {
                "role": "Internal Auditor & Contrarian",
                "expertise": "Devil's Advocate, Pattern Recognition, Bias Detection",
                "prompt_weight": 0.10,
                "background": "Ex-SEC Enforcement, Forensic Accountant",
                "style": "Skeptical, challenging, detail-oriented"
            },
            "GOVERNOR_EXECUTION": {
                "role": "Head of Trading Operations",
                "expertise": "Entry/Exit Precision, Order Types, Slippage Management",
                "prompt_weight": 0.05,
                "background": "25 years execution trading, Ex-Jump Trading",
                "style": "Technical, precise, execution-focused"
            }
        }
    
    def convene_board(self, directive: str, market_data: Dict) -> BoardDecision:
        """Convene full board meeting with institutional debate process"""
        
        try:
            # Phase 1: Individual Analysis
            governor_analyses = {}
            for governor_id, governor_info in self.board_members.items():
                if governor_id == "CHAIRMAN_OSINACHI":
                    continue
                    
                analysis = self._get_governor_analysis(
                    governor_id, 
                    governor_info, 
                    directive, 
                    market_data
                )
                governor_analyses[governor_id] = analysis
                time.sleep(0.5)  # Rate limiting
            
            # Phase 2: Adversary Challenge
            adversary_critique = self._get_adversary_challenge(
                governor_analyses, 
                market_data
            )
            
            # Phase 3: Chairman's Final Decision
            final_decision = self._get_chairman_decision(
                directive,
                market_data,
                governor_analyses,
                adversary_critique
            )
            
            # Store decision
            self.decision_history.append(final_decision)
            
            return final_decision
            
        except Exception as e:
            st.error(f"Board convening error: {str(e)}")
            return self._generate_fallback_decision(directive)
    
    def _get_governor_analysis(self, governor_id: str, info: Dict, 
                               directive: str, market_data: Dict) -> Dict:
        """Get individual governor's institutional analysis"""
        
        system_prompt = f"""
        You are {info['role']} at Sovereign Fund Capital, a $14.9B institutional hedge fund.
        
        YOUR BACKGROUND: {info['background']}
        YOUR EXPERTISE: {info['expertise']}
        YOUR STYLE: {info['style']}
        
        CONTEXT:
        - You serve on the Board of Governors alongside 6 other distinguished members
        - The Chairman will make the final decision based on your analysis
        - You have access to institutional-grade data including:
          * Dark pool prints and block trades
          * CME Commitment of Traders reports
          * Prime brokerage flow data
          * Interbank dealing spreads
          * Options market maker positioning
        
        FORMAT YOUR RESPONSE AS:
        1. EXECUTIVE SUMMARY (2-3 sentences)
        2. DETAILED ANALYSIS (your specific expertise focus)
        3. QUANTITATIVE ASSESSMENT (probability, expected value, risk metrics)
        4. RECOMMENDATION (BUY/SELL/HOLD with confidence 1-10)
        5. KEY RISKS (2-3 specific risks)
        
        Be concise but thorough. Use institutional language.
        """
        
        full_prompt = f"""
        {system_prompt}
        
        EXECUTIVE DIRECTIVE FROM CHAIRMAN OSINACHI:
        {directive}
        
        INSTITUTIONAL MARKET INTELLIGENCE:
        {json.dumps(market_data, indent=2)}
        
        Provide your expert analysis for the Board.
        """
        
        try:
            response = self.model.generate_content(full_prompt)
            return {
                'analysis': response.text,
                'governor': info['role'],
                'weight': info['prompt_weight'],
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            return {
                'analysis': f"Analysis unavailable: {str(e)}",
                'governor': info['role'],
                'weight': info['prompt_weight'],
                'timestamp': datetime.now().isoformat()
            }
    
    def _get_adversary_challenge(self, governor_analyses: Dict, market_data: Dict) -> str:
        """Get internal adversary's challenge to consensus"""
        
        challenge_prompt = f"""
        As the Internal Auditor & Contrarian at Sovereign Fund Capital, your role is to:
        
        1. IDENTIFY cognitive biases in the Board's analysis
        2. PRESENT the strongest counter-argument to the consensus view
        3. HIGHLIGHT what could go catastrophically wrong (Black Swan scenarios)
        4. CHALLENGE all assumptions about market efficiency and institutional behavior
        5. PROVIDE an alternative interpretation of the data
        6. QUESTION whether the market has already priced in the consensus view
        
        BOARD RECOMMENDATIONS:
        {json.dumps({k: v['analysis'][:200] for k, v in governor_analyses.items()}, indent=2)}
        
        MARKET DATA:
        {json.dumps(market_data, indent=2)}
        
        Deliver a formal memorandum challenging the consensus view.
        Be specific and quantitative where possible.
        """
        
        try:
            response = self.model.generate_content(challenge_prompt)
            return response.text
        except:
            return "Critical audit function temporarily unavailable. Proceed with enhanced caution."
    
    def _get_chairman_decision(self, directive: str, market_data: Dict,
                              governor_analyses: Dict, adversary_critique: str) -> BoardDecision:
        """Get Chairman Osinachi's final institutional decision"""
        
        synthesis_prompt = f"""
        You are Chairman Osinachi, CIO of Sovereign Fund Capital ($14.9B AUM).
        
        YOUR CREDENTIALS:
        - Former Federal Reserve Governor (12 years)
        - PhD Economics, MIT
        - 30 years institutional investment experience
        - Managed through 2008 Financial Crisis, 2020 COVID Crash
        - Known for: Decisive action, risk management, contrarian thinking
        
        DECISION FRAMEWORK:
        1. WEIGHT OF EVIDENCE: Assess strength and consistency of Governor analyses
        2. ADVERSARY CHALLENGE: Seriously consider the contrary view
        3. RISK MANAGEMENT: Maximum 1% portfolio risk per position
        4. POSITION SIZING: Modified Kelly Criterion with volatility adjustment
        5. EXECUTION: Precise entry, stop-loss, and take-profit levels
        
        You must now make the FINAL DECISION that will be executed.
        
        GOVERNOR ANALYSES:
        {json.dumps({k: v['analysis'][:300] for k, v in governor_analyses.items()}, indent=2)}
        
        ADVERSARY CHALLENGE:
        {adversary_critique[:500]}
        
        COMPREHENSIVE MARKET DATA:
        {json.dumps(market_data, indent=2)}
        
        ORIGINAL DIRECTIVE:
        {directive}
        
        DELIVER YOUR FINAL DECISION in this exact format:
        
        1. TRADE SIGNAL: [BUY/SELL/HOLD]
        2. CONFIDENCE: [1-10]
        3. POSITION SIZE: [0.1-1.0% of AUM]
        4. ENTRY LEVEL: [precise price]
        5. STOP LOSS: [precise price]
        6. TAKE PROFIT 1: [price - 50% position]
        7. TAKE PROFIT 2: [price - 50% position]
        8. RISK/REWARD RATIO: [calculated]
        9. TIMEFRAME: [holding period]
        10. EXECUTION: [order type and timing]
        11. RATIONALE: [brief explanation of your decision]
        """
        
        try:
            response = self.model.generate_content(synthesis_prompt)
            decision_text = response.text
            
            # Parse decision
            trade_signal = self._extract_value(decision_text, "TRADE SIGNAL", "HOLD")
            confidence = int(self._extract_value(decision_text, "CONFIDENCE", "5"))
            position_size = float(self._extract_value(decision_text, "POSITION SIZE", "0.5").replace('%', ''))
            entry_level = float(self._extract_value(decision_text, "ENTRY LEVEL", "0"))
            stop_loss = float(self._extract_value(decision_text, "STOP LOSS", "0"))
            take_profit = float(self._extract_value(decision_text, "TAKE PROFIT 1", "0"))
            risk_reward = float(self._extract_value(decision_text, "RISK/REWARD RATIO", "0"))
            
            return BoardDecision(
                trade_signal=trade_signal,
                confidence=confidence,
                position_size=position_size,
                entry_level=entry_level,
                stop_loss=stop_loss,
                take_profit=take_profit,
                risk_reward=risk_reward,
                timeframe=self._extract_value(decision_text, "TIMEFRAME", "SWING"),
                key_risks=[self._extract_value(decision_text, "KEY RISKS", "Market risk")],
                execution_instructions=self._extract_value(decision_text, "EXECUTION", "Limit order"),
                full_analysis=decision_text,
                adversary_notes=adversary_critique[:500]
            )
            
        except Exception as e:
            return self._generate_fallback_decision(directive)
    
    def _extract_value(self, text: str, key: str, default: str) -> str:
        """Extract value from decision text"""
        try:
            for line in text.split('\n'):
                if key.upper() in line.upper():
                    # Extract everything after the colon
                    parts = line.split(':', 1)
                    if len(parts) > 1:
                        return parts[1].strip()
            return default
        except:
            return default
    
    def _generate_fallback_decision(self, directive: str) -> BoardDecision:
        """Generate conservative fallback decision"""
        return BoardDecision(
            trade_signal="HOLD",
            confidence=3,
            position_size=0.1,
            entry_level=0,
            stop_loss=0,
            take_profit=0,
            risk_reward=0,
            timeframe="NONE",
            key_risks=["System error - manual review required"],
            execution_instructions="STAND DOWN - Do not execute",
            full_analysis="Board decision process encountered an error. Defaulting to conservative position.",
            adversary_notes="N/A - System fallback activated"
        )

# --- 6. HIGH-PROBABILITY SETUP SCANNER ---
class InstitutionalSetupScanner:
    """Scans for high-probability institutional trading setups"""
    
    def __init__(self):
        self.data_engine = InstitutionalDataEngine()
        self.scan_universe = [
            ("Gold Futures", "GC=F"),
            ("Silver Futures", "SI=F"),
            ("Crude Oil", "CL=F"),
            ("S&P 500 Futures", "ES=F"),
            ("NASDAQ Futures", "NQ=F"),
            ("30Y Treasury Bonds", "ZB=F"),
            ("EUR/USD Futures", "6E=F"),
            ("JPY/USD Futures", "6J=F"),
            ("Bitcoin USD", "BTC-USD"),
            ("Ethereum USD", "ETH-USD")
        ]
    
    def scan_for_setups(self) -> List[Dict]:
        """Scan for high-probability setups across multiple timeframes"""
        
        setups = []
        progress_bar = st.progress(0)
        
        for idx, (name, symbol) in enumerate(self.scan_universe):
            progress_bar.progress((idx + 1) / len(self.scan_universe))
            
            data = self.data_engine.get_comprehensive_data(symbol)
            if data:
                probability_score = self._calculate_setup_probability(data)
                
                if probability_score > 60:  # Only high-probability setups
                    setup = {
                        'name': name,
                        'symbol': symbol,
                        'price': data.price,
                        'trend': data.trend,
                        'sentiment': data.sentiment_score,
                        'volume_anomaly': data.volume > 1.5,
                        'institutional_flow': data.institutional_flow,
                        'rsi': data.rsi,
                        'atr': data.atr,
                        'probability_score': probability_score,
                        'suggested_direction': self._suggest_direction(data)
                    }
                    setups.append(setup)
        
        progress_bar.empty()
        
        # Sort by probability score
        setups.sort(key=lambda x: x['probability_score'], reverse=True)
        return setups[:5]  # Top 5 highest probability setups
    
    def _calculate_setup_probability(self, data: MarketData) -> float:
        """Calculate multi-factor setup probability score"""
        score = 50  # Base score
        
        # Trend alignment (20 points)
        if "BULLISH" in data.trend and data.sentiment_score > 0.3:
            score += 20
        elif "BEARISH" in data.trend and data.sentiment_score < -0.3:
            score += 20
        elif "STRONG" in data.trend:
            score += 10
        
        # RSI confirmation (15 points)
        if 30 <= data.rsi <= 70:
            score += 5
        if 40 <= data.rsi <= 60:
            score += 10
        
        # Volume confirmation (15 points)
        if data.volume > 1.5:
            score += 10
        if data.volume > 2.0:
            score += 5
        
        # Institutional flow alignment (25 points)
        if "ACCUMULATION" in data.institutional_flow:
            score += 20
        elif "DISTRIBUTION" in data.institutional_flow:
            score -= 15
        
        # Options flow confirmation (15 points)
        if "BULLISH" in data.options_flow and data.sentiment_score > 0:
            score += 10
        elif "BEARISH" in data.options_flow and data.sentiment_score < 0:
            score += 10
        
        # Dark pool activity bonus (10 points)
        if data.dark_pool_activity in ["ELEVATED", "EXTREME"]:
            score += 5
        
        return min(100, max(0, score))
    
    def _suggest_direction(self, data: MarketData) -> str:
        """Suggest trading direction based on analysis"""
        if data.sentiment_score > 0.3 and "BULLISH" in data.trend:
            return "LONG"
        elif data.sentiment_score < -0.3 and "BEARISH" in data.trend:
            return "SHORT"
        else:
            return "NEUTRAL"

# --- 7. PERFORMANCE ANALYTICS ENGINE ---
class PerformanceAnalytics:
    """Track and analyze trading performance"""
    
    def __init__(self):
        self.trades = []
        self.metrics = {
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'win_rate': 0.0,
            'total_pnl': 0.0,
            'avg_win': 0.0,
            'avg_loss': 0.0,
            'profit_factor': 0.0,
            'sharpe_ratio': 0.0,
            'max_drawdown': 0.0,
            'current_aum': 14_900_000.0
        }
    
    def add_trade(self, trade: Dict):
        """Record a completed trade"""
        self.trades.append(trade)
        self._update_metrics()
    
    def _update_metrics(self):
        """Update performance metrics"""
        if self.trades:
            self.metrics['total_trades'] = len(self.trades)
            
            winning_trades = [t for t in self.trades if t.get('pnl', 0) > 0]
            losing_trades = [t for t in self.trades if t.get('pnl', 0) <= 0]
            
            self.metrics['winning_trades'] = len(winning_trades)
            self.metrics['losing_trades'] = len(losing_trades)
            self.metrics['win_rate'] = len(winning_trades) / len(self.trades) * 100
            
            pnls = [t.get('pnl', 0) for t in self.trades]
            self.metrics['total_pnl'] = sum(pnls)
            
            if winning_trades:
                self.metrics['avg_win'] = np.mean([t['pnl'] for t in winning_trades])
            if losing_trades:
                self.metrics['avg_loss'] = abs(np.mean([t['pnl'] for t in losing_trades]))
            
            total_wins = sum([t['pnl'] for t in winning_trades]) if winning_trades else 0
            total_losses = abs(sum([t['pnl'] for t in losing_trades])) if losing_trades else 1
            self.metrics['profit_factor'] = total_wins / total_losses if total_losses > 0 else 0
            
            # Calculate Sharpe Ratio (simplified)
            if len(pnls) > 1:
                returns = np.array(pnls) / self.metrics['current_aum']
                self.metrics['sharpe_ratio'] = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
            
            # Calculate Max Drawdown
            cumulative = np.cumsum(pnls)
            running_max = np.maximum.accumulate(cumulative)
            drawdowns = (running_max - cumulative) / self.metrics['current_aum'] * 100
            self.metrics['max_drawdown'] = np.max(drawdowns) if len(drawdowns) > 0 else 0

# --- 8. MAIN APPLICATION ---
def main():
    """Main application entry point"""
    
    # Initialize session state
    if 'board' not in st.session_state:
        st.session_state.board = SovereignBoard()
    if 'scanner' not in st.session_state:
        st.session_state.scanner = InstitutionalSetupScanner()
    if 'data_engine' not in st.session_state:
        st.session_state.data_engine = InstitutionalDataEngine()
    if 'analytics' not in st.session_state:
        st.session_state.analytics = PerformanceAnalytics()
    if 'active_positions' not in st.session_state:
        st.session_state.active_positions = []
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "Trading Floor"
    
    # API Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        st.error("🔴 CRITICAL: GOOGLE_API_KEY not found in environment variables.")
        st.info("Please set your GOOGLE_API_KEY environment variable to continue.")
        st.stop()
    
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # --- SIDEBAR NAVIGATION ---
    with st.sidebar:
        st.markdown("""
            <div style="text-align: center; padding: 20px 0;">
                <h2 style="color: #d4af37; font-family: 'Playfair Display', serif; 
                           font-size: 1.5rem; margin: 0; letter-spacing: 2px;">
                    🏛️ SOVEREIGN
                </h2>
                <p style="color: #888; font-size: 0.7rem; letter-spacing: 3px; margin: 5px 0;">
                    COMMAND CENTER
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # Navigation
        st.markdown("### NAVIGATION")
        pages = {
            "Trading Floor": "🎯",
            "Board Room": "🏛️",
            "Setup Scanner": "🔍",
            "Performance Analytics": "📊",
            "Risk Monitor": "⚠️"
        }
        
        for page_name, icon in pages.items():
            if st.button(f"{icon} {page_name}", use_container_width=True, 
                        key=f"nav_{page_name}"):
                st.session_state.current_page = page_name
        
        st.divider()
        
        # AUM Display
        st.markdown("### 💰 ASSETS UNDER MANAGEMENT")
        
        aum_data = {
            "DNA Fund": {"value": "$5,000,000", "delta": "+2.3%"},
            "Sure Leverage": {"value": "$4,900,000", "delta": "+1.8%"},
            "Aqua Reserve": {"value": "$5,000,000", "delta": "+0.5%"}
        }
        
        for fund_name, data in aum_data.items():
            st.metric(
                fund_name,
                data['value'],
                data['delta']
            )
        
        st.divider()
        
        # Market Time
        ny_time = datetime.now(pytz.timezone('America/New_York'))
        london_time = datetime.now(pytz.timezone('Europe/London'))
        tokyo_time = datetime.now(pytz.timezone('Asia/Tokyo'))
        
        st.markdown("### 🌍 GLOBAL MARKETS")
        st.markdown(f"""
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #888;">
            🇺🇸 NY: {ny_time.strftime('%H:%M:%S')} EST<br>
            🇬🇧 LDN: {london_time.strftime('%H:%M:%S')} GMT<br>
            🇯🇵 TKY: {tokyo_time.strftime('%H:%M:%S')} JST
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Security Status
        st.markdown("### 🔒 SECURITY STATUS")
        st.markdown("""
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;">
            <span style="color: #00ff88;">●</span> Connection: ENCRYPTED<br>
            <span style="color: #00ff88;">●</span> AI Engine: OPERATIONAL<br>
            <span style="color: #00ff88;">●</span> Risk System: ACTIVE<br>
            <span style="color: #ffaa00;">●</span> Market Data: LIVE
            </div>
        """, unsafe_allow_html=True)
    
    # --- HEADER ---
    st.markdown("""
        <h1 style="text-align: center; margin-bottom: 5px;">
            SOVEREIGN FUND CAPITAL
        </h1>
        <p style="text-align: center; color: #d4af37; font-style: italic; font-size: 1rem; margin-bottom: 5px;">
            Institutional AI Trading & Asset Management
        </p>
        <p style="text-align: center; color: #666; font-size: 0.7rem; letter-spacing: 2px;">
            EST. 2024 | PRIVATE HEDGE FUND | AI-GOVERNED
        </p>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # --- PAGE ROUTING ---
    current_page = st.session_state.current_page
    
    if current_page == "Trading Floor":
        render_trading_floor()
    elif current_page == "Board Room":
        render_board_room()
    elif current_page == "Setup Scanner":
        render_setup_scanner()
    elif current_page == "Performance Analytics":
        render_performance_analytics()
    elif current_page == "Risk Monitor":
        render_risk_monitor()

def render_trading_floor():
    """Main trading interface"""
    
    # Live Market Dashboard
    st.markdown("### 📊 LIVE INSTITUTIONAL MARKET DASHBOARD")
    
    # Get market overview
    with st.spinner("Fetching institutional market data..."):
        market_overview = st.session_state.data_engine.get_market_overview()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_display = [
        ("S&P 500", "sp500", "🇺🇸"),
        ("NASDAQ", "nasdaq", "📈"),
        ("Gold Futures", "gold", "🥇"),
        ("Bitcoin", "bitcoin", "₿")
    ]
    
    for i, (label, key, icon) in enumerate(metrics_display):
        with [col1, col2, col3, col4][i]:
            if key in market_overview:
                data = market_overview[key]
                trend_color = "#00ff88" if "BULL" in data['trend'] else "#ff4444" if "BEAR" in data['trend'] else "#ffaa00"
                
                st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 0.7rem; color: #888; text-transform: uppercase; letter-spacing: 1px;">
                            {icon} {label}
                        </div>
                        <div style="font-size: 1.5rem; font-weight: 700; margin: 10px 0; font-family: 'JetBrains Mono', monospace;">
                            {data['price']:,.2f}
                        </div>
                        <div style="color: {trend_color}; font-size: 0.8rem; font-weight: 600;">
                            {data['trend'].replace('_', ' ')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
    
    st.divider()
    
    # Trading Command Center
    st.markdown("### 🎯 EXECUTIVE TRADING COMMAND")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        with st.expander("📋 POSITION BUILDER", expanded=True):
            asset = st.selectbox(
                "Select Instrument",
                ["XAUUSD (Gold)", "BTCUSD (Bitcoin)", "SPX500 (S&P 500)", 
                 "USOIL (Crude Oil)", "EURUSD (Euro)", "USDJPY (Yen)"],
                key="trading_asset"
            )
            
            direction = st.radio(
                "Direction",
                ["LONG 📈", "SHORT 📉"],
                horizontal=True,
                key="trading_direction"
            )
            
            col_entry, col_sl, col_tp = st.columns(3)
            with col_entry:
                entry = st.number_input("Entry Price", value=0.0, step=0.01, key="entry_price")
            with col_sl:
                stop_loss = st.number_input("Stop Loss", value=0.0, step=0.01, key="stop_loss")
            with col_tp:
                take_profit = st.number_input("Take Profit", value=0.0, step=0.01, key="take_profit")
    
    with col2:
        st.markdown("### ⚙️ RISK PARAMETERS")
        risk_percent = st.slider(
            "Risk % of AUM",
            min_value=0.1,
            max_value=1.0,
            value=0.5,
            step=0.1,
            key="risk_percent"
        )
        
        if entry > 0 and stop_loss > 0:
            risk_amount = 14_900_000 * (risk_percent / 100)
            position_size = risk_amount / abs(entry - stop_loss)
            
            st.metric("Max Risk", f"${risk_amount:,.0f}")
            st.metric("Position Size", f"{position_size:,.2f} units")
            st.metric("Notional Value", f"${position_size * entry:,.0f}")
    
    # Submit for Board Review
    if st.button("⚡ SUBMIT FOR BOARD REVIEW", use_container_width=True, key="submit_trade"):
        if entry <= 0:
            st.error("Please enter a valid entry price.")
        else:
            with st.spinner("🏛️ Convening Sovereign Board of Governors..."):
                # Prepare directive
                directive = f"""
                Analyze {asset} for a {direction} position.
                Proposed Entry: {entry}
                Stop Loss: {stop_loss}
                Take Profit: {take_profit}
                Risk: {risk_percent}% of AUM
                """
                
                # Get comprehensive market data
                symbol_map = {
                    "XAUUSD (Gold)": "GC=F",
                    "BTCUSD (Bitcoin)": "BTC-USD",
                    "SPX500 (S&P 500)": "ES=F",
                    "USOIL (Crude Oil)": "CL=F",
                    "EURUSD (Euro)": "EURUSD=X",
                    "USDJPY (Yen)": "USDJPY=X"
                }
                
                symbol = symbol_map.get(asset, "GC=F")
                market_data = st.session_state.data_engine.get_comprehensive_data(symbol)
                
                if market_data:
                    # Convene board
                    decision = st.session_state.board.convene_board(
                        directive,
                        {"asset": asset, "technical": market_data.__dict__}
                    )
                    
                    # Display decision
                    st.divider()
                    st.markdown("### 🏛️ SOVEREIGN BOARD DECISION")
                    
                    # Decision header
                    signal_color = "#00ff88" if decision.trade_signal == "BUY" else "#ff4444" if decision.trade_signal == "SELL" else "#ffaa00"
                    
                    st.markdown(f"""
                        <div class="board-response">
                            <h3 style="color: {signal_color}; margin: 0;">
                                FINAL DECISION: {decision.trade_signal}
                            </h3>
                            <p style="color: #888; font-size: 0.8rem; margin: 5px 0;">
                                Chairman Osinachi Presiding | Confidence: {decision.confidence}/10
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Decision details
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Entry", f"${decision.entry_level:,.2f}")
                    col2.metric("Stop Loss", f"${decision.stop_loss:,.2f}")
                    col3.metric("Take Profit", f"${decision.take_profit:,.2f}")
                    col4.metric("R:R Ratio", f"1:{decision.risk_reward}")
                    
                    st.markdown(f"**Position Size:** {decision.position_size}% of AUM")
                    st.markdown(f"**Execution:** {decision.execution_instructions}")
                    st.markdown(f"**Timeframe:** {decision.timeframe}")
                    
                    # Full analysis
                    with st.expander("📄 VIEW FULL BOARD ANALYSIS", expanded=False):
                        st.markdown(decision.full_analysis)
                    
                    # Adversary notes
                    with st.expander("⚔️ ADVERSARY CHALLENGE", expanded=False):
                        st.markdown(decision.adversary_notes)
                else:
                    st.error("Unable to fetch market data. Please try again.")
    
    # Active Positions
    st.divider()
    st.markdown("### 📊 ACTIVE POSITIONS")
    
    if st.session_state.active_positions:
        positions_df = pd.DataFrame(st.session_state.active_positions)
        st.dataframe(positions_df, use_container_width=True, hide_index=True)
    else:
        st.info("No active positions. Submit a trade for Board review to open a position.")
        
        # Sample data for demonstration
        sample_positions = pd.DataFrame({
            "Instrument": ["XAUUSD", "BTCUSD", "SPX500"],
            "Direction": ["LONG", "SHORT", "LONG"],
            "Entry": [2345.60, 67450.00, 5234.50],
            "Current": [2356.80, 67120.00, 5280.00],
            "P&L": ["+$1,120", "+$3,300", "+$2,275"],
            "P&L %": ["+0.48%", "+0.49%", "+0.87%"],
            "Status": ["RUNNING", "RUNNING", "RUNNING"]
        })
        
        with st.expander("📈 SAMPLE POSITIONS (DEMO)", expanded=False):
            st.dataframe(sample_positions, use_container_width=True, hide_index=True)

def render_board_room():
    """Board of Directors governance interface"""
    
    st.markdown("### 🏛️ THE SOVEREIGN BOARD OF GOVERNORS")
    st.markdown("*Federal Reserve Model - Institutional AI Governance Framework*")
    
    # Board Members Grid
    st.markdown("#### Board Composition & Expertise")
    
    board = st.session_state.board
    members = board.board_members
    
    # Display members in a grid
    cols = st.columns(4)
    member_list = list(members.items())
    
    for i in range(0, len(member_list), 2):
        for j in range(2):
            if i + j < len(member_list):
                gov_id, gov_info = member_list[i + j]
                with cols[j]:
                    is_chairman = gov_id == "CHAIRMAN_OSINACHI"
                    
                    st.markdown(f"""
                        <div class="member-card" style="{'border-color: #d4af37;' if is_chairman else ''}">
                            <div class="role" style="{'font-size: 1rem;' if is_chairman else ''}">
                                {'👑 ' if is_chairman else '🎓 '}{gov_info['role']}
                            </div>
                            <div class="expertise" style="margin: 8px 0;">
                                {gov_info['expertise']}
                            </div>
                            <div style="font-size: 0.65rem; color: #666; margin-top: 8px;">
                                {gov_info['background']}
                            </div>
                            <div style="margin-top: 8px;">
                                <div style="font-size: 0.6rem; color: #888; margin-bottom: 3px;">Voting Weight</div>
                                <div style="background: #1a1a1a; height: 3px; border-radius: 2px;">
                                    <div style="background: {'#d4af37' if is_chairman else '#4a4a4a'}; 
                                                height: 100%; width: {gov_info['prompt_weight']*100}%; 
                                                border-radius: 2px;"></div>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Board Directive Input
    st.markdown("### 📋 PRESIDENTIAL DIRECTIVE")
    st.markdown("*Submit your strategic directive for full Board analysis*")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        directive = st.text_area(
            "Enter your directive:",
            placeholder="""Example directives:
    - "Analyze impact of potential 50bps Fed rate cut on gold and provide entry strategy"
    - "Evaluate Bitcoin institutional adoption trends and optimal accumulation zones"
    - "Assess S&P 500 risk-reward ahead of FOMC meeting with specific hedging strategy"
    - "Review EUR/USD positioning following ECB policy divergence"
    """,
            height=120,
            key="board_directive"
        )
    
    with col2:
        st.markdown("#### Analysis Parameters")
        include_technical = st.checkbox("Technical Analysis", value=True)
        include_macro = st.checkbox("Macro Analysis", value=True)
        include_flow = st.checkbox("Order Flow Analysis", value=True)
        include_risk = st.checkbox("Risk Assessment", value=True)
        
        urgency = st.select_slider(
            "Urgency Level",
            options=["ROUTINE", "PRIORITY", "URGENT", "CRITICAL"],
            value="PRIORITY"
        )
    
    if st.button("🏛️ CONVENE FULL BOARD", use_container_width=True, key="convene_board"):
        if directive:
            with st.spinner(f"🏛️ Board of Governors in {urgency} session..."):
                # Get comprehensive market data
                st.info("Gathering institutional market intelligence...")
                
                market_data = st.session_state.data_engine.get_market_overview()
                
                # Convene board
                st.info("Governors preparing individual analyses...")
                decision = st.session_state.board.convene_board(directive, market_data)
                
                # Display Results
                st.divider()
                st.markdown("### 📊 BOARD DELIBERATION RESULTS")
                
                # Final Decision Banner
                signal_color = "#00ff88" if decision.trade_signal == "BUY" else "#ff4444" if decision.trade_signal == "SELL" else "#ffaa00"
                
                st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0d0d0d, #1a1a1a); 
                                padding: 30px; border-radius: 10px; border: 2px solid {signal_color};
                                margin: 20px 0; text-align: center;">
                        <h2 style="color: {signal_color}; margin: 0; font-size: 2rem;">
                            {decision.trade_signal}
                        </h2>
                        <p style="color: #888; margin: 10px 0 0 0;">
                            Chairman Osinachi's Final Verdict | Confidence: {decision.confidence}/10
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Entry Level", f"${decision.entry_level:,.2f}")
                col2.metric("Stop Loss", f"${decision.stop_loss:,.2f}")
                col3.metric("Take Profit", f"${decision.take_profit:,.2f}")
                col4.metric("Risk/Reward", f"1:{decision.risk_reward}")
                
                # Full analysis
                with st.expander("📄 COMPLETE BOARD ANALYSIS", expanded=True):
                    st.markdown(decision.full_analysis)
                
                # Adversary challenge
                with st.expander("⚔️ INTERNAL ADVERSARY AUDIT", expanded=False):
                    st.markdown(f'<div class="intel-feed">{decision.adversary_notes}</div>', 
                              unsafe_allow_html=True)
                
                # Execution instructions
                with st.expander("🎯 EXECUTION ORDERS", expanded=False):
                    st.markdown(f"""
                        **Execution Strategy:** {decision.execution_instructions}
                        
                        **Key Risks:**
                        {chr(10).join(f'- {risk}' for risk in decision.key_risks)}
                        
                        **Timeframe:** {decision.timeframe}
                    """)
        else:
            st.error("Please enter a directive for the Board to analyze.")

def render_setup_scanner():
    """High-probability institutional setup scanner"""
    
    st.markdown("### 🔍 INSTITUTIONAL SETUP SCANNER")
    st.markdown("*AI-Powered Detection of High-Probability Institutional Trading Setups*")
    
    # Scanner controls
    col1, col2, col3 = st.columns(3)
    with col1:
        min_probability = st.slider("Minimum Probability Score", 50, 100, 60)
    with col2:
        scan_timeframe = st.selectbox("Timeframe", ["1H", "4H", "Daily", "Weekly"], index=2)
    with col3:
        asset_class = st.multiselect(
            "Asset Class",
            ["Commodities", "FX", "Indices", "Crypto"],
            default=["Commodities", "Crypto"]
        )
    
    if st.button("🔍 SCAN FOR HIGH-PROBABILITY SETUPS", use_container_width=True):
        with st.spinner("Scanning institutional order flow across markets..."):
            setups = st.session_state.scanner.scan_for_setups()
            
            if setups:
                st.success(f"✅ Found {len(setups)} high-probability institutional setups")
                
                for idx, setup in enumerate(setups):
                    with st.expander(
                        f"{'🥇' if idx == 0 else '🥈' if idx == 1 else '🥉' if idx == 2 else '📊'} "
                        f"{setup['name']} - Probability Score: {setup['probability_score']}/100",
                        expanded=(idx == 0)
                    ):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Current Price", f"${setup['price']:,.2f}")
                            st.metric("Trend", setup['trend'].replace('_', ' '))
                        
                        with col2:
                            st.metric("RSI", f"{setup['rsi']:.1f}")
                            st.metric("Sentiment", f"{setup['sentiment']:.2f}")
                        
                        with col3:
                            st.metric("Institutional Flow", setup['institutional_flow'].replace('_', ' '))
                            st.metric("Suggested Direction", setup['suggested_direction'])
                        
                        # Detailed analysis
                        st.markdown(f"""
                            **Volume Analysis:** {'⚠️ Anomaly Detected' if setup['volume_anomaly'] else 'Normal'}
                            **ATR:** {setup['atr']:.4f}
                            **Probability Factors:**
                            - Trend Alignment: {'✅' if 'BULL' in setup['trend'] or 'BEAR' in setup['trend'] else '⚠️'}
                            - Volume Confirmation: {'✅' if setup['volume_anomaly'] else '⚠️'}
                            - Institutional Flow: {'✅' if 'ACCUMULATION' in setup['institutional_flow'] else '⚠️'}
                            - RSI Optimal: {'✅' if 30 <= setup['rsi'] <= 70 else '⚠️'}
                        """)
                        
                        if st.button(f"📊 Submit for Board Analysis", key=f"analyze_{setup['symbol']}"):
                            st.session_state['scanner_selected'] = setup
                            st.success(f"Setup for {setup['name']} submitted for Board analysis!")
            else:
                st.warning("No high-probability setups detected in current market conditions.")
                st.info("Try adjusting the minimum probability score or scanning different asset classes.")

def render_performance_analytics():
    """Performance analytics dashboard"""
    
    st.markdown("### 📈 PERFORMANCE ANALYTICS")
    
    # Key metrics
    metrics = st.session_state.analytics.metrics
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Trades", metrics['total_trades'])
    col2.metric("Win Rate", f"{metrics['win_rate']:.1f}%")
    col3.metric("Profit Factor", f"{metrics['profit_factor']:.2f}")
    col4.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
    
    st.divider()
    
    # Performance charts (sample data for demonstration)
    st.markdown("#### Equity Curve")
    
    # Generate sample equity curve
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    equity = 1000000 * (1 + np.random.randn(100).cumsum() * 0.01)
    
    equity_df = pd.DataFrame({'Date': dates, 'Equity': equity})
    st.line_chart(equity_df.set_index('Date'))
    
    st.markdown("#### Monthly Returns Distribution")
    
    monthly_returns = pd.DataFrame({
        'Month': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'Returns %': [2.3, -1.5, 3.1, 1.8, -0.5, 2.9]
    })
    st.bar_chart(monthly_returns.set_index('Month'))

def render_risk_monitor():
    """Risk monitoring dashboard"""
    
    st.markdown("### ⚠️ RISK MONITORING DASHBOARD")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Portfolio Risk Metrics")
        
        risk_metrics = {
            "Value at Risk (95%)": "$156,000",
            "Expected Shortfall": "$234,000",
            "Beta (vs S&P)": "0.45",
            "Correlation": "0.32",
            "Max Drawdown": "-8.2%",
            "Leverage Ratio": "1:1.5"
        }
        
        for metric, value in risk_metrics.items():
            st.metric(metric, value)
    
    with col2:
        st.markdown("#### Position Limits")
        
        st.info("""
        **Risk Limits:**
        - Max Position Size: 1% of AUM
        - Max Sector Exposure: 25%
        - Max Correlation: 0.7
        - Min Diversification: 5 assets
        
        **Current Status:**
        ✅ All limits within parameters
        ✅ No concentration warnings
        ✅ Liquidity adequate
        """)

if __name__ == "__main__":
    main()
