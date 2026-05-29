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
from enum import Enum
import warnings
import time
from collections import deque
import threading
warnings.filterwarnings('ignore')

# ============================================
# SOVEREIGN FUND CAPITAL - INSTITUTIONAL AI BOARD
# ============================================
# AUM: DNA Fund $4,995 | Sure Leverage $4,968
# Objective: Multi-Billion Dollar Growth
# Architecture: Federal Reserve Board Model
# ============================================

st.set_page_config(
    page_title="Sovereign Fund Capital | Institutional AI Board",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# INSTITUTIONAL STYLING
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

.stApp {
    background: linear-gradient(135deg, #0a0a0a 0%, #000000 100%);
    color: #e0e0e0;
}

.institutional-header {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #C8A84E;
    text-align: center;
    border-bottom: 1px solid #C8A84E;
    padding-bottom: 20px;
    margin-bottom: 20px;
}

.classified-stamp {
    position: absolute;
    top: 10px;
    right: 20px;
    color: #FF1744;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 4px;
    opacity: 0.7;
    transform: rotate(-15deg);
    border: 1px solid #FF1744;
    padding: 2px 8px;
}

.governor-card {
    background: linear-gradient(145deg, #0D0D0D, #1A1A1A);
    border: 1px solid #222;
    border-radius: 4px;
    padding: 20px;
    position: relative;
    transition: all 0.3s ease;
}

.governor-card:hover {
    border-color: #C8A84E;
    box-shadow: 0 4px 20px rgba(200, 168, 78, 0.1);
}

.governor-role {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    color: #C8A84E;
    font-weight: 600;
    letter-spacing: 1px;
}

.governor-name {
    font-family: 'Inter', sans-serif;
    font-size: 0.8rem;
    color: #666;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.board-directive {
    background: #000;
    border: 1px solid #C8A84E;
    padding: 30px;
    border-radius: 4px;
    position: relative;
    margin: 20px 0;
}

.decision-banner {
    padding: 30px;
    text-align: center;
    border: 2px solid;
    border-radius: 4px;
    margin: 20px 0;
    font-family: 'Cormorant Garamond', serif;
}

.decision-banner.buy { 
    border-color: #00C853; 
    background: rgba(0,200,83,0.05); 
}
.decision-banner.sell { 
    border-color: #FF1744; 
    background: rgba(255,23,68,0.05); 
}
.decision-banner.hold { 
    border-color: #FFD600; 
    background: rgba(255,214,0,0.05); 
}

.param-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin: 20px 0;
}

.param-item {
    background: #0D0D0D;
    border: 1px solid #1A1A1A;
    padding: 15px;
    text-align: center;
}

.param-label {
    font-size: 0.6rem;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #666;
}

.param-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.2rem;
    color: #FFF;
    font-weight: 600;
}

.stButton > button {
    font-family: 'Inter', sans-serif;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 500;
    border-radius: 2px;
    padding: 15px 30px;
    transition: all 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    border-color: #C8A84E;
}

.data-feed {
    background: #050505;
    border-left: 3px solid #C8A84E;
    padding: 15px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #666;
}

/* ─── LIVE TICKER STRIP ─── */
.ticker-strip {
    background: #050505;
    border-top: 1px solid #1A1A1A;
    border-bottom: 1px solid #1A1A1A;
    padding: 10px 0;
    margin-bottom: 20px;
    overflow: hidden;
}

.ticker-item {
    display: inline-block;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    padding: 4px 24px;
    border-right: 1px solid #1A1A1A;
}

.ticker-sym {
    color: #C8A84E;
    font-weight: 600;
    margin-right: 6px;
}

.ticker-price {
    color: #FFF;
    margin-right: 4px;
}

.ticker-up   { color: #00C853; }
.ticker-down { color: #FF1744; }
.ticker-flat { color: #888; }

/* ─── PRICE GRID ON SIDEBAR ─── */
.price-card {
    background: #0D0D0D;
    border: 1px solid #1A1A1A;
    border-radius: 3px;
    padding: 10px 12px;
    margin-bottom: 6px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.price-card-sym  { color: #C8A84E; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; font-weight: 600; }
.price-card-val  { color: #FFF;    font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; }
.price-card-chg  { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #222; }
::-webkit-scrollbar-thumb:hover { background: #C8A84E; }

@keyframes scan {
    0% { opacity: 0.3; }
    50% { opacity: 1; }
    100% { opacity: 0.3; }
}

.scanning { animation: scan 2s infinite; }
</style>

<div style="position:fixed; top:50%; left:50%; transform:translate(-50%,-50%) rotate(-45deg); 
     font-size:8rem; color:rgba(200,168,78,0.02); pointer-events:none; z-index:-1; 
     font-family:'Cormorant Garamond',serif; white-space:nowrap;">SOVEREIGN</div>
""", unsafe_allow_html=True)

# ============================================
# ENUMS AND DATA CLASSES
# ============================================

class SignalType(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class ConvictionLevel(Enum):
    VERY_LOW = 1
    LOW = 3
    MODERATE = 5
    HIGH = 7
    VERY_HIGH = 9
    MAXIMUM = 10

class TimeFrame(Enum):
    SCALP = "SCALP"
    INTRADAY = "INTRADAY"
    SWING = "SWING"
    POSITION = "POSITION"
    INVESTMENT = "INVESTMENT"

@dataclass
class BoardVote:
    governor_id: str
    governor_role: str
    signal: SignalType
    conviction: ConvictionLevel
    rationale: str
    risk_assessment: str
    conditions: List[str]
    timestamp: str

@dataclass
class BoardDirective:
    directive_id: str
    asset: str
    signal: SignalType
    conviction: ConvictionLevel
    entry_zone: Tuple[float, float]
    stop_loss: float
    targets: List[float]
    position_size_pct: float
    risk_per_trade_pct: float
    timeframe: TimeFrame
    votes: List[BoardVote]
    macro_context: str
    fundamental_view: str
    technical_setup: str
    risk_assessment: str
    execution_protocol: str
    chairman_statement: str
    timestamp: str
    expiry: str

# ============================================
# TECHNICAL INDICATORS
# ============================================

class TechnicalIndicators:
    @staticmethod
    def calculate_rsi(prices: pd.Series, period: int = 14) -> float:
        try:
            delta = prices.diff()
            gain = delta.where(delta > 0, 0.0).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0.0)).rolling(window=period).mean()
            rs = gain / loss
            return round(100 - (100 / (1 + rs.iloc[-1])), 1)
        except:
            return 50.0
    
    @staticmethod
    def calculate_macd(prices: pd.Series) -> float:
        try:
            ema12 = prices.ewm(span=12).mean()
            ema26 = prices.ewm(span=26).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9).mean()
            return round((macd - signal).iloc[-1], 4)
        except:
            return 0.0
    
    @staticmethod
    def calculate_bb_position(prices: pd.Series) -> float:
        try:
            sma = prices.rolling(20).mean()
            std = prices.rolling(20).std()
            upper = sma + 2 * std
            lower = sma - 2 * std
            pos = (prices.iloc[-1] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1])
            return round(pos, 2)
        except:
            return 0.5
    
    @staticmethod
    def calculate_atr(high, low, close, period=14) -> float:
        try:
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            return round(tr.rolling(period).mean().iloc[-1], 4)
        except:
            return 0.0
    
    @staticmethod
    def calculate_sma(prices: pd.Series, period: int) -> float:
        try:
            return round(prices.rolling(window=period).mean().iloc[-1], 2)
        except:
            return 0.0

# ============================================
# INSTITUTIONAL DATA ENGINE
# ============================================

class InstitutionalDataEngine:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = timedelta(minutes=2)
        self.ta = TechnicalIndicators()
        self.lock = threading.Lock()
        
    def fetch_institutional_data(self, symbol: str) -> Dict:
        cache_key = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H%M')}"
        
        with self.lock:
            for key, (cached_time, data) in list(self.cache.items()):
                if symbol in key and datetime.now() - cached_time < self.cache_ttl:
                    return data
        
        try:
            ticker = yf.Ticker(symbol)
            df_6mo = ticker.history(period="6mo", interval="1d")
            
            if df_6mo.empty:
                return self._generate_synthetic_data(symbol)
            
            close = df_6mo['Close']
            high = df_6mo['High']
            low = df_6mo['Low']
            volume = df_6mo['Volume']
            current_price = close.iloc[-1]
            
            data = {
                'price': round(current_price, 2),
                'change_1d': round(((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100, 2) if len(close) > 1 else 0,
                'volatility_30d': round(close.pct_change().std() * np.sqrt(252) * 100, 2),
                'volume_ratio': round(volume.iloc[-1] / volume.mean(), 2) if volume.mean() > 0 else 1.0,
                'rsi_14': self.ta.calculate_rsi(close),
                'macd_histogram': self.ta.calculate_macd(close),
                'bb_position': self.ta.calculate_bb_position(close),
                'atr_14': self.ta.calculate_atr(high, low, close),
                'sma_20': self.ta.calculate_sma(close, 20),
                'sma_50': self.ta.calculate_sma(close, 50),
                'sma_200': self.ta.calculate_sma(close, 200) if len(close) >= 200 else round(close.mean(), 2),
                'volume_trend': self._analyze_volume_trend(volume),
                'price_structure': self._analyze_market_structure(close, high, low),
                'support_resistance': self._find_key_levels(high, low, close),
                'liquidity_zones': self._identify_liquidity(high, low, volume),
            }
            
            with self.lock:
                self.cache[cache_key] = (datetime.now(), data)
            
            return data
            
        except Exception as e:
            return self._generate_synthetic_data(symbol)
    
    def fetch_live_price(self, symbol: str) -> Dict:
        """Lightweight live price fetch — returns price + 1d change only."""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d", interval="1d")
            if hist.empty:
                return {'price': 0.0, 'change_1d': 0.0}
            price = hist['Close'].iloc[-1]
            change = 0.0
            if len(hist) > 1:
                change = round(((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100, 2)
            return {'price': round(price, 4), 'change_1d': change}
        except:
            return {'price': 0.0, 'change_1d': 0.0}

    def _analyze_volume_trend(self, volume: pd.Series) -> str:
        try:
            vol_ma = volume.rolling(20).mean()
            current = volume.iloc[-1]
            if current > vol_ma.iloc[-1] * 1.5:
                return "CLIMACTIC"
            elif current > vol_ma.iloc[-1] * 1.2:
                return "ELEVATED"
            elif current < vol_ma.iloc[-1] * 0.5:
                return "SUBDUED"
            return "NORMAL"
        except:
            return "NORMAL"
    
    def _analyze_market_structure(self, close, high, low) -> str:
        try:
            highs = high.iloc[-20:]
            lows = low.iloc[-20:]
            higher_highs = (highs.diff().dropna() > 0).sum()
            higher_lows = (lows.diff().dropna() > 0).sum()
            total = 19
            
            if higher_highs > total * 0.6 and higher_lows > total * 0.6:
                return "BULLISH_STRUCTURE"
            elif higher_highs < total * 0.4 and higher_lows < total * 0.4:
                return "BEARISH_STRUCTURE"
            return "CONSOLIDATION"
        except:
            return "CONSOLIDATION"
    
    def _find_key_levels(self, high, low, close) -> Dict:
        try:
            recent_high = high.iloc[-20:].max()
            recent_low = low.iloc[-20:].min()
            current = close.iloc[-1]
            
            return {
                'resistance_1': round(recent_high, 2),
                'resistance_2': round(recent_high * 1.02, 2),
                'pivot': round((recent_high + recent_low + current) / 3, 2),
                'support_1': round(recent_low, 2),
                'support_2': round(recent_low * 0.98, 2),
                'current': round(current, 2)
            }
        except:
            return {
                'resistance_1': 0, 'resistance_2': 0,
                'pivot': 0, 'support_1': 0, 'support_2': 0, 'current': 0
            }
    
    def _identify_liquidity(self, high, low, volume) -> List[Dict]:
        try:
            vol_profile = pd.DataFrame({
                'high': high.iloc[-20:],
                'low': low.iloc[-20:],
                'volume': volume.iloc[-20:]
            })
            
            high_vol = vol_profile[vol_profile['volume'] > vol_profile['volume'].mean() * 1.5]
            zones = []
            for _, row in high_vol.iterrows():
                zones.append({
                    'level': round((row['high'] + row['low']) / 2, 2),
                    'volume_ratio': round(row['volume'] / vol_profile['volume'].mean(), 2)
                })
            return zones[:3]
        except:
            return []
    
    def _generate_synthetic_data(self, symbol: str) -> Dict:
        price_map = {
            'GC=F': 2350, 'BTC-USD': 68000, 'ES=F': 5250,
            'CL=F': 78, 'EURUSD=X': 1.08, 'USDJPY=X': 156
        }
        base_price = price_map.get(symbol, 100)
        
        return {
            'price': base_price,
            'change_1d': 0.0,
            'volatility_30d': 15.0,
            'volume_ratio': 1.0,
            'rsi_14': 50.0,
            'macd_histogram': 0.0,
            'bb_position': 0.5,
            'atr_14': base_price * 0.01,
            'sma_20': base_price,
            'sma_50': base_price,
            'sma_200': base_price,
            'volume_trend': 'NORMAL',
            'price_structure': 'CONSOLIDATION',
            'support_resistance': {
                'resistance_1': base_price * 1.02,
                'resistance_2': base_price * 1.04,
                'pivot': base_price,
                'support_1': base_price * 0.98,
                'support_2': base_price * 0.96,
                'current': base_price
            },
            'liquidity_zones': [
                {'level': base_price, 'volume_ratio': 1.5}
            ],
        }

# ============================================
# LIVE PRICE TICKER (rendered HTML)
# ============================================

TICKER_SYMBOLS = [
    ("XAUUSD", "GC=F",      "Gold"),
    ("XAGUSD", "SI=F",      "Silver"),
    ("BTCUSD", "BTC-USD",   "Bitcoin"),
    ("SPX",    "ES=F",      "S&P 500"),
    ("NDX",    "NQ=F",      "NASDAQ"),
    ("USOIL",  "CL=F",      "Crude Oil"),
    ("EURUSD", "EURUSD=X",  "EUR/USD"),
    ("USDJPY", "USDJPY=X",  "USD/JPY"),
    ("GBPUSD", "GBPUSD=X",  "GBP/USD"),
    ("ETHUSD", "ETH-USD",   "Ethereum"),
]

def fetch_ticker_prices(engine: InstitutionalDataEngine) -> List[Dict]:
    results = []
    for name, sym, label in TICKER_SYMBOLS:
        d = engine.fetch_live_price(sym)
        results.append({
            'name': name,
            'label': label,
            'price': d['price'],
            'change': d['change_1d'],
        })
    return results

def render_live_ticker(engine: InstitutionalDataEngine):
    """Renders the scrolling price ticker strip below the header."""
    prices = fetch_ticker_prices(engine)
    
    items_html = ""
    for p in prices:
        chg = p['change']
        chg_class = "ticker-up" if chg > 0 else "ticker-down" if chg < 0 else "ticker-flat"
        arrow = "▲" if chg > 0 else "▼" if chg < 0 else "●"
        
        # Format price sensibly
        raw = p['price']
        if raw >= 1000:
            fmt_price = f"{raw:,.2f}"
        elif raw >= 1:
            fmt_price = f"{raw:.4f}"
        else:
            fmt_price = f"{raw:.6f}"
        
        items_html += f"""
            <span class="ticker-item">
                <span class="ticker-sym">{p['name']}</span>
                <span class="ticker-price">{fmt_price}</span>
                <span class="{chg_class}">{arrow}{abs(chg):.2f}%</span>
            </span>
        """
    
    st.markdown(f"""
        <div class="ticker-strip">
            {items_html}
        </div>
    """, unsafe_allow_html=True)

def render_sidebar_prices(engine: InstitutionalDataEngine):
    """Renders compact price cards in the sidebar."""
    prices = fetch_ticker_prices(engine)
    cards_html = ""
    for p in prices:
        chg = p['change']
        chg_class = "ticker-up" if chg > 0 else "ticker-down" if chg < 0 else "ticker-flat"
        arrow = "▲" if chg > 0 else "▼" if chg < 0 else "—"
        raw = p['price']
        if raw >= 1000:
            fmt_price = f"{raw:,.2f}"
        elif raw >= 1:
            fmt_price = f"{raw:.4f}"
        else:
            fmt_price = f"{raw:.6f}"
        
        cards_html += f"""
            <div class="price-card">
                <span class="price-card-sym">{p['name']}</span>
                <span class="price-card-val">{fmt_price}</span>
                <span class="price-card-chg {chg_class}">{arrow}{abs(chg):.2f}%</span>
            </div>
        """
    st.markdown(cards_html, unsafe_allow_html=True)

# ============================================
# SOVEREIGN BOARD OF GOVERNORS  ← UPGRADED
# ============================================

class SovereignBoardOfGovernors:
    def __init__(self):
        self.model = self._initialize_model()
        self.vote_history = deque(maxlen=500)
        self.directive_counter = 0
        
        # ── UPGRADED GOVERNOR PROFILES ──────────────────────────────────
        self.governors = {
            "CHAIRMAN_OSINACHI": {
                "id": "CHAIRMAN_OSINACHI",
                "title": "Chairman of the Board",
                "role": "Chief Investment Officer",
                "expertise": "Portfolio Strategy, Risk Management, Final Authority",
                "weight": 0.25,
                "background": (
                    "Former Federal Reserve Governor (12 years), PhD Economics MIT. "
                    "Managed $50B+ institutional AUM across multiple market cycles. "
                    "Led crisis response during 2008 and 2020 market dislocations. "
                    "Known for synthesizing conflicting board views into decisive, capital-preserving directives. "
                    "Believes deeply in asymmetric risk/reward — will never approve a trade where the RR is below 2:1."
                ),
                "decision_philosophy": (
                    "Capital preservation is the first law. Conviction without edge is gambling. "
                    "When board consensus is fractured, default to HOLD — the market will present clarity. "
                    "Position sizing is the most powerful tool a trader has. Risk the minimum, extract the maximum."
                ),
            },
            "GOVERNOR_MACRO": {
                "id": "GOVERNOR_MACRO",
                "title": "Governor of Macro Strategy",
                "role": "Head of Global Macro",
                "expertise": "Central Bank Policy, Yield Curve Analysis, Global Capital Flows, DXY Correlation",
                "weight": 0.15,
                "background": (
                    "Ex-IMF Chief Economist, 20 years advising G20 central banks. PhD Monetary Economics, LSE. "
                    "Constructed the macro overlay framework used by three sovereign wealth funds. "
                    "Specialist in USD liquidity cycles, gold-rate correlations, and Fed pivot timing. "
                    "Has accurately called every major macro regime shift since 2005."
                ),
                "decision_philosophy": (
                    "All price is downstream of liquidity. Before any trade, ask: is the macro regime aligned? "
                    "A technically perfect setup in a hostile macro environment is a trap. "
                    "DXY strength crushes gold; Fed dovishness is the most powerful tailwind gold can have."
                ),
            },
            "GOVERNOR_FLOW": {
                "id": "GOVERNOR_FLOW",
                "title": "Governor of Order Flow",
                "role": "Head of Order Flow Intelligence",
                "expertise": "Dark Pool Analysis, COT Positioning, Smart Money Footprints, Institutional Accumulation",
                "weight": 0.15,
                "background": (
                    "Former Goldman Sachs Partner and Head of Commodities Desk (25 years). "
                    "Pioneered dark pool tracking methodologies now used industry-wide. "
                    "Reads COT reports as primary signal — commercials vs. non-commercials positioning tells the real story. "
                    "Expert at identifying institutional absorption zones, stop hunts, and engineered liquidity sweeps."
                ),
                "decision_philosophy": (
                    "Price is manipulation. What matters is who is accumulating and who is distributing. "
                    "If commercials are net long while retail is net short, that is the setup. "
                    "A sweep of sell-side liquidity followed by a strong reclaim is the highest probability entry."
                ),
            },
            "GOVERNOR_QUANT": {
                "id": "GOVERNOR_QUANT",
                "title": "Governor of Quantitative Strategy",
                "role": "Chief Quantitative Officer",
                "expertise": "Statistical Edge, Probability Models, Regime Detection, Volatility Forecasting",
                "weight": 0.15,
                "background": (
                    "PhD Mathematical Finance, Stanford. Former Renaissance Technologies portfolio manager. "
                    "Built volatility forecasting models deployed across $15B+ in AUM. "
                    "Specialist in regime-detection algorithms — knows when a market is trending vs. mean-reverting. "
                    "Quantifies conviction using Bayesian probability updates on live data."
                ),
                "decision_philosophy": (
                    "Every trade is a probability distribution. My job is to identify when edge exceeds friction. "
                    "ATR-normalized targets, regime-adjusted position sizing, and expectancy-positive setups only. "
                    "If the math does not support the trade, no amount of narrative conviction justifies it."
                ),
            },
            "GOVERNOR_RISK": {
                "id": "GOVERNOR_RISK",
                "title": "Governor of Risk Management",
                "role": "Chief Risk Officer",
                "expertise": "VaR Modeling, Tail Risk, Drawdown Control, Correlation Risk, Black Swan Protocols",
                "weight": 0.15,
                "background": (
                    "Former Fed Risk Supervisor and Basel Committee Advisor. "
                    "Designed the systemic risk framework used by four major central banks. "
                    "Specialized in non-linear risk: scenarios where losses compound. "
                    "Has veto power over any directive that threatens more than 2% peak-to-valley drawdown. "
                    "Survived the 1998, 2008, and 2020 crises by identifying correlated risk before it cascaded."
                ),
                "decision_philosophy": (
                    "Risk is not a number — it is a story about what can go wrong. "
                    "The most dangerous moment is when everything seems to be working. "
                    "Never trade without knowing your maximum pain point. If a stop is ambiguous, the trade is off."
                ),
            },
            "GOVERNOR_SMC": {
                "id": "GOVERNOR_SMC",
                "title": "Governor of Smart Money Concepts",
                "role": "Head of Institutional Technical Analysis",
                "expertise": "Order Blocks, Fair Value Gaps, Break of Structure, Liquidity Sweeps, ICT Framework",
                "weight": 0.10,
                "background": (
                    "Trained under the Inner Circle Trader (ICT) methodology for 15 years. "
                    "Specialist in multi-timeframe Smart Money Concepts — reads the weekly draw on liquidity, "
                    "then executes on H1 and H4 order blocks. Expert at identifying manipulation candles, "
                    "Judas swings, and institutional entry models (OTE, NWOG, NDOG). "
                    "Has traded exclusively with limit orders from order blocks for a decade."
                ),
                "decision_philosophy": (
                    "Price always seeks liquidity. Identify where resting buy stops and sell stops are pooled, "
                    "then anticipate the institutional sweep before the true directional move. "
                    "The weekly chart determines the draw. The H4 chart identifies the order block. The H1 is the entry. "
                    "Never enter mid-range — only from premium or discount arrays."
                ),
            },
            "GOVERNOR_EXECUTION": {
                "id": "GOVERNOR_EXECUTION",
                "title": "Governor of Trading Operations",
                "role": "Head of Execution",
                "expertise": "Order Execution, Slippage Control, Limit Order Strategy, MT5 Execution Protocol",
                "weight": 0.05,
                "background": (
                    "Ex-Jump Trading and Citadel Execution. 20 years HFT and institutional execution. "
                    "Specialist in limit order placement, partial fill management, and slippage minimization. "
                    "Expert in MT5 execution mechanics — knows exact order types, pending order invalidation, "
                    "and how to size positions correctly given prop firm risk parameters. "
                    "Has never accepted a market order for a directional position."
                ),
                "decision_philosophy": (
                    "Execution is where edge is either preserved or destroyed. "
                    "A limit order at the exact order block is 10x better than a market order 5 points away. "
                    "On MT5: use buy limit / sell limit for OB entries. "
                    "Always define lot size before placement — never adjust after entry."
                ),
            },
        }
        # ─────────────────────────────────────────────────────────────────

    def _initialize_model(self):
        try:
            model = genai.GenerativeModel(
                'gemini-1.5-flash',
                generation_config={
                    'temperature': 0.2,
                    'top_p': 0.95,
                    'top_k': 40,
                    'max_output_tokens': 4096
                }
            )
            return model
        except Exception as e:
            return None
    
    def convene_board(self, asset: str, directive: str, market_data: Dict) -> BoardDirective:
        self.directive_counter += 1
        directive_id = f"SFC-{datetime.now().strftime('%Y%m%d')}-{self.directive_counter:04d}"
        
        governor_votes = []
        
        progress = st.progress(0)
        governors_list = list(self.governors.items())
        
        for idx, (gov_id, gov_info) in enumerate(governors_list):
            if gov_id == "CHAIRMAN_OSINACHI":
                continue
            
            progress.progress((idx + 1) / len(governors_list))
            
            with st.expander(f"🎓 **{gov_info['title']}** - {gov_info['role']}", expanded=(idx < 2)):
                vote = self._get_governor_vote(gov_id, gov_info, asset, directive, market_data)
                governor_votes.append(vote)
                
                signal_color = "#00C853" if vote.signal == SignalType.BUY else "#FF1744" if vote.signal == SignalType.SELL else "#FFD600"
                
                vote_html = f"""
                    <div style="border-left: 3px solid {signal_color}; padding: 10px; margin: 10px 0; background: #0A0A0A;">
                        <strong style="color: {signal_color};">VOTE: {vote.signal.value}</strong>
                        <span style="color: #666;"> | Conviction: {vote.conviction.value}/10</span>
                        <p style="margin: 10px 0; color: #CCC;">{vote.rationale}</p>
                        <small style="color: #888;">Risk Note: {vote.risk_assessment}</small>
                    </div>
                """
                st.markdown(vote_html, unsafe_allow_html=True)
        
        progress.empty()
        
        st.markdown("---")
        st.markdown("### 👑 CHAIRMAN OSINACHI - FINAL VERDICT")
        
        with st.spinner("Chairman synthesizing all analysis..."):
            final_directive = self._chairman_verdict(
                directive_id, asset, directive, market_data, governor_votes
            )
        
        self.vote_history.append(final_directive)
        
        return final_directive
    
    def _get_governor_vote(self, gov_id: str, gov_info: Dict, asset: str, 
                           directive: str, market_data: Dict) -> BoardVote:
        
        decision_philosophy = gov_info.get('decision_philosophy', '')
        
        prompt = f"""You are {gov_info['title']} at Sovereign Fund Capital, an elite private hedge fund.

CREDENTIALS & BACKGROUND:
{gov_info['background']}

YOUR DECISION PHILOSOPHY:
{decision_philosophy}

YOUR EXPERTISE: {gov_info['expertise']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOARD DIRECTIVE UNDER REVIEW: {directive}
ASSET: {asset}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LIVE MARKET DATA:
{json.dumps(market_data, indent=2)}

INSTRUCTIONS:
Analyse this directive strictly through the lens of YOUR expertise and philosophy.
Be direct, specific, and institutionally rigorous. Do NOT give generic analysis.
Reference the actual market data numbers in your rationale.
If you have concerns about the setup, state them with precision.

FORMAT (respond EXACTLY as shown — no extra text):
VOTE: [BUY/SELL/HOLD]
CONVICTION: [1-10]
RATIONALE: [3-4 sentences from YOUR specific expertise — cite actual data points]
RISK: [The single most important risk THIS specific setup carries from YOUR domain]
CONDITIONS: [Specific conditions that would change your vote — be precise]
"""
        
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                text = response.text
                
                vote_signal = self._extract_signal(text)
                conviction = self._extract_conviction(text)
                rationale = self._extract_field(text, 'RATIONALE')
                risk = self._extract_field(text, 'RISK')
                conditions = self._extract_field(text, 'CONDITIONS').split(',')
                
                return BoardVote(
                    governor_id=gov_id,
                    governor_role=gov_info['role'],
                    signal=vote_signal,
                    conviction=conviction,
                    rationale=rationale,
                    risk_assessment=risk,
                    conditions=conditions,
                    timestamp=datetime.now().isoformat()
                )
        except Exception as e:
            pass
        
        return self._fallback_vote(gov_id, gov_info, market_data)
    
    def _chairman_verdict(self, directive_id: str, asset: str, directive: str,
                          market_data: Dict, votes: List[BoardVote]) -> BoardDirective:
        
        buy_votes = sum(1 for v in votes if v.signal == SignalType.BUY)
        sell_votes = sum(1 for v in votes if v.signal == SignalType.SELL)
        hold_votes = sum(1 for v in votes if v.signal == SignalType.HOLD)
        avg_conviction = np.mean([v.conviction.value for v in votes]) if votes else 5

        chairman = self.governors["CHAIRMAN_OSINACHI"]
        
        prompt = f"""You are CHAIRMAN OSINACHI, CIO of Sovereign Fund Capital.

CREDENTIALS:
{chairman['background']}

YOUR DECISION PHILOSOPHY:
{chairman['decision_philosophy']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOARD VOTE TALLY:
  BUY: {buy_votes}  |  SELL: {sell_votes}  |  HOLD: {hold_votes}
  Average Conviction: {avg_conviction:.1f}/10

ASSET: {asset}
DIRECTIVE: {directive}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

LIVE MARKET DATA:
{json.dumps(market_data, indent=2)}

BOARD VOTES SUMMARY:
{json.dumps([{
    'role': v.governor_role,
    'vote': v.signal.value,
    'conviction': v.conviction.value,
    'rationale': v.rationale[:150],
    'risk': v.risk_assessment[:100]
} for v in votes], indent=2)}

FUND PARAMETERS:
  AUM: DNA Fund $4,995 | Sure Leverage $4,968 | Total: $9,963
  Max Risk Per Trade: 1% of account
  Order Type: Limit orders only (no market orders)
  Style: SMC / Institutional order block entries
  Objective: Disciplined growth toward multi-million dollar fund

YOUR TASK:
As Chairman, synthesize all board perspectives into ONE final directive.
You must weigh macro alignment, SMC structure, risk parameters, and order flow.
If the board is fractured or data is ambiguous, defend a HOLD with conviction.
Your entry/exit levels must be PRECISE and reference actual price data above.
Ensure RR is minimum 2:1. Never recommend >1% risk.

FORMAT (respond EXACTLY as shown):
SIGNAL: [BUY/SELL/HOLD]
CONVICTION: [1-10]
ENTRY_ZONE_LOW: [specific price]
ENTRY_ZONE_HIGH: [specific price]
STOP_LOSS: [specific price]
TARGET_1: [specific price]
TARGET_2: [specific price]
POSITION_SIZE: [0.1 to 1.0 — percent of per-account AUM]
TIMEFRAME: [SCALP/INTRADAY/SWING/POSITION/INVESTMENT]
RATIONALE: [4-5 sentences — reference board votes, cite data, explain decision with Chairman authority]
RISK_NOTE: [The most critical risk the fund faces on this specific trade]
"""
        
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                text = response.text
                
                signal = self._extract_signal(text)
                conviction = self._extract_conviction(text)
                price = market_data.get('price', 0)
                entry_low = self._extract_float(text, 'ENTRY_ZONE_LOW', price * 0.99)
                entry_high = self._extract_float(text, 'ENTRY_ZONE_HIGH', price * 1.01)
                stop_loss = self._extract_float(text, 'STOP_LOSS', entry_low * 0.98)
                target_1 = self._extract_float(text, 'TARGET_1', entry_high * 1.02)
                target_2 = self._extract_float(text, 'TARGET_2', entry_high * 1.04)
                position_size = self._extract_float(text, 'POSITION_SIZE', 0.5)
                timeframe = self._extract_timeframe(text)
                rationale = self._extract_field(text, 'RATIONALE')
                risk_note = self._extract_field(text, 'RISK_NOTE')
                
                return BoardDirective(
                    directive_id=directive_id,
                    asset=asset,
                    signal=signal,
                    conviction=conviction,
                    entry_zone=(entry_low, entry_high),
                    stop_loss=stop_loss,
                    targets=[target_1, target_2],
                    position_size_pct=min(position_size, 1.0),
                    risk_per_trade_pct=1.0,
                    timeframe=timeframe,
                    votes=votes,
                    macro_context="Board macro analysis completed",
                    fundamental_view="Board fundamental assessment completed",
                    technical_setup="Board technical analysis completed",
                    risk_assessment=risk_note,
                    execution_protocol=f"Limit orders in zone {entry_low}-{entry_high}",
                    chairman_statement=rationale,
                    timestamp=datetime.now().isoformat(),
                    expiry=(datetime.now() + timedelta(hours=24)).isoformat()
                )
        except Exception as e:
            pass
        
        return self._conservative_directive(directive_id, asset, votes)
    
    def _extract_signal(self, text: str) -> SignalType:
        for line in text.split('\n'):
            if 'VOTE:' in line.upper() or 'SIGNAL:' in line.upper():
                if 'BUY' in line.upper():
                    return SignalType.BUY
                elif 'SELL' in line.upper():
                    return SignalType.SELL
        return SignalType.HOLD
    
    def _extract_conviction(self, text: str) -> ConvictionLevel:
        for line in text.split('\n'):
            if 'CONVICTION:' in line.upper():
                try:
                    val = int(''.join(filter(str.isdigit, line.split(':')[1])))
                    return ConvictionLevel(max(1, min(10, val)))
                except:
                    pass
        return ConvictionLevel.MODERATE
    
    def _extract_field(self, text: str, field: str) -> str:
        for line in text.split('\n'):
            if field.upper() in line.upper():
                parts = line.split(':', 1)
                return parts[1].strip() if len(parts) > 1 else "Analysis pending"
        return "Analysis in progress"
    
    def _extract_float(self, text: str, field: str, default: float) -> float:
        for line in text.split('\n'):
            if field.upper() in line.upper():
                try:
                    return float(''.join(filter(lambda x: x.isdigit() or x == '.', line.split(':')[1])))
                except:
                    pass
        return default
    
    def _extract_timeframe(self, text: str) -> TimeFrame:
        for line in text.split('\n'):
            if 'TIMEFRAME:' in line.upper():
                for tf in TimeFrame:
                    if tf.value in line.upper():
                        return tf
        return TimeFrame.SWING
    
    def _fallback_vote(self, gov_id: str, gov_info: Dict, data: Dict) -> BoardVote:
        rsi = data.get('rsi_14', 50)
        trend = data.get('price_structure', 'CONSOLIDATION')
        sentiment = 0
        
        if 'BULLISH' in trend:
            sentiment = 0.3
        elif 'BEARISH' in trend:
            sentiment = -0.3
        
        if rsi < 30:
            sentiment += 0.2
        elif rsi > 70:
            sentiment -= 0.2
        
        signal = SignalType.HOLD
        if sentiment > 0.3:
            signal = SignalType.BUY
        elif sentiment < -0.3:
            signal = SignalType.SELL
        
        return BoardVote(
            governor_id=gov_id,
            governor_role=gov_info['role'],
            signal=signal,
            conviction=ConvictionLevel.MODERATE,
            rationale=f"Technical assessment: {trend}, RSI {rsi}. Systematic vote.",
            risk_assessment="Standard market risk",
            conditions=["Confirm with volume", "Check news calendar"],
            timestamp=datetime.now().isoformat()
        )
    
    def _conservative_directive(self, directive_id: str, asset: str, 
                                votes: List[BoardVote]) -> BoardDirective:
        return BoardDirective(
            directive_id=directive_id,
            asset=asset,
            signal=SignalType.HOLD,
            conviction=ConvictionLevel.LOW,
            entry_zone=(0, 0),
            stop_loss=0,
            targets=[0, 0],
            position_size_pct=0.0,
            risk_per_trade_pct=0.0,
            timeframe=TimeFrame.SWING,
            votes=votes,
            macro_context="Insufficient data for conviction",
            fundamental_view="Standing aside",
            technical_setup="No clear setup",
            risk_assessment="Elevated uncertainty - capital preservation priority",
            execution_protocol="NO EXECUTION - STANDING ASIDE",
            chairman_statement="Capital preservation is paramount. We wait for better opportunities.",
            timestamp=datetime.now().isoformat(),
            expiry=(datetime.now() + timedelta(hours=4)).isoformat()
        )

# ============================================
# HIGH PROBABILITY SETUP SCANNER
# ============================================

class InstitutionalSetupScanner:
    def __init__(self):
        self.data_engine = InstitutionalDataEngine()
        self.scan_universe = {
            "PRECIOUS_METALS": [
                ("XAUUSD", "GC=F", "Gold Futures"),
                ("XAGUSD", "SI=F", "Silver Futures"),
            ],
            "ENERGY": [
                ("USOIL", "CL=F", "Crude Oil Futures"),
            ],
            "INDICES": [
                ("SPX", "ES=F", "S&P 500 Futures"),
                ("NDX", "NQ=F", "NASDAQ Futures"),
            ],
            "CRYPTO": [
                ("BTC", "BTC-USD", "Bitcoin"),
                ("ETH", "ETH-USD", "Ethereum"),
            ],
            "FOREX": [
                ("EURUSD", "EURUSD=X", "Euro"),
                ("USDJPY", "USDJPY=X", "Yen"),
            ]
        }
    
    def scan_all_markets(self) -> List[Dict]:
        all_setups = []
        
        progress = st.progress(0)
        total = sum(len(assets) for assets in self.scan_universe.values())
        current = 0
        
        for sector, assets in self.scan_universe.items():
            for name, symbol, display in assets:
                current += 1
                progress.progress(current / total)
                
                data = self.data_engine.fetch_institutional_data(symbol)
                if data:
                    score = self._calculate_probability_score(data)
                    if score > 60:
                        all_setups.append({
                            'sector': sector,
                            'name': name,
                            'display': display,
                            'symbol': symbol,
                            'score': score,
                            'data': data,
                            'direction': self._determine_direction(data)
                        })
        
        progress.empty()
        all_setups.sort(key=lambda x: x['score'], reverse=True)
        return all_setups[:5]
    
    def _calculate_probability_score(self, data: Dict) -> float:
        score = 50
        
        if data['price_structure'] == 'BULLISH_STRUCTURE':
            score += 15
        elif data['price_structure'] == 'BEARISH_STRUCTURE':
            score += 10
        
        rsi = data['rsi_14']
        if 40 <= rsi <= 60:
            score += 10
        elif 30 <= rsi <= 70:
            score += 5
        
        if data['volume_ratio'] > 1.5:
            score += 15
        
        if data['macd_histogram'] > 0 and 'BULLISH' in data['price_structure']:
            score += 10
        elif data['macd_histogram'] < 0 and 'BEARISH' in data['price_structure']:
            score += 10
        
        atr_pct = data['atr_14'] / data['price'] * 100 if data['price'] > 0 else 0
        if 1 < atr_pct < 3:
            score += 5
        
        return min(100, score)
    
    def _determine_direction(self, data: Dict) -> str:
        if data['price_structure'] == 'BULLISH_STRUCTURE' and data['rsi_14'] < 60:
            return 'LONG'
        elif data['price_structure'] == 'BEARISH_STRUCTURE' and data['rsi_14'] > 40:
            return 'SHORT'
        return 'NEUTRAL'

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    if 'data_engine' not in st.session_state:
        st.session_state.data_engine = InstitutionalDataEngine()
    if 'board' not in st.session_state:
        st.session_state.board = SovereignBoardOfGovernors()
    if 'scanner' not in st.session_state:
        st.session_state.scanner = InstitutionalSetupScanner()
    if 'active_directives' not in st.session_state:
        st.session_state.active_directives = []
    if 'scan_results' not in st.session_state:
        st.session_state.scan_results = []
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("🔴 GOOGLE_API_KEY not configured!")
        st.code("export GOOGLE_API_KEY='your-api-key'")
        st.stop()
    
    genai.configure(api_key=api_key)
    
    # ============================================
    # SIDEBAR
    # ============================================
    with st.sidebar:
        st.markdown("""
            <div style="text-align:center; padding:20px 0;">
                <h2 style="color:#C8A84E; font-family:'Cormorant Garamond',serif; 
                           letter-spacing:4px; font-size:1.8rem;">SOVEREIGN</h2>
                <p style="color:#888; font-size:0.6rem; letter-spacing:3px;">FUND CAPITAL</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 💰 ASSETS UNDER MANAGEMENT")
        col1, col2 = st.columns(2)
        col1.metric("DNA Fund", "$4,995", "🔒")
        col2.metric("Sure Leverage", "$4,968", "🔒")
        st.metric("Total AUM", "$9,963", "🎯 Target: $1B+")
        
        st.divider()

        # ── LIVE PRICES IN SIDEBAR ───────────────────────────────────────
        st.markdown("### 📡 LIVE MARKET PRICES")
        with st.spinner("Fetching live prices..."):
            render_sidebar_prices(st.session_state.data_engine)
        # ─────────────────────────────────────────────────────────────────

        st.divider()
        
        st.markdown("### 📋 DIRECTIVES")
        page = st.radio(
            "Select Command",
            ["🏛️ Board Room", "🎯 Trading Terminal", "🔍 Market Scanner", "📊 Portfolio"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        ny_time = datetime.now(pytz.timezone('America/New_York'))
        st.markdown(f"""
            <div style="font-family:'JetBrains Mono',monospace; font-size:0.7rem; color:#666;">
            🇺🇸 NY: {ny_time.strftime('%H:%M:%S')} EST<br>
            📡 Data: LIVE<br>
            🔒 Security: ENCRYPTED
            </div>
        """, unsafe_allow_html=True)
    
    # ============================================
    # HEADER
    # ============================================
    st.markdown("""
        <h1 class="institutional-header">SOVEREIGN FUND CAPITAL</h1>
        <p style="text-align:center; color:#888; font-size:0.8rem; letter-spacing:2px;">
            INSTITUTIONAL AI BOARD OF GOVERNORS | PRIVATE HEDGE FUND
        </p>
    """, unsafe_allow_html=True)
    
    # ── LIVE TICKER STRIP BELOW HEADER ──────────────────────────────────
    with st.spinner("Loading live prices..."):
        render_live_ticker(st.session_state.data_engine)
    # ─────────────────────────────────────────────────────────────────────

    st.divider()
    
    # ============================================
    # PAGE ROUTING
    # ============================================
    if page == "🏛️ Board Room":
        render_board_room()
    elif page == "🎯 Trading Terminal":
        render_trading_terminal()
    elif page == "🔍 Market Scanner":
        render_market_scanner()
    elif page == "📊 Portfolio":
        render_portfolio()

def render_board_room():
    st.markdown("### 🏛️ BOARD OF GOVERNORS")
    st.markdown("*Federal Reserve Model — Seven Specialized Governors + Chairman Osinachi*")
    
    governors = st.session_state.board.governors
    cols = st.columns(4)
    
    for i, (gov_id, gov) in enumerate(governors.items()):
        with cols[i % 4]:
            is_chairman = gov_id == "CHAIRMAN_OSINACHI"
            border = "2px solid #C8A84E" if is_chairman else "1px solid #222"
            bg_color = "#C8A84E" if is_chairman else "#444"
            weight_pct = gov['weight'] * 100
            role_prefix = "👑 " if is_chairman else ""
            expertise_short = gov['expertise'][:55]
            font_size = "1rem" if is_chairman else "0.9rem"
            
            card_html = f"""
                <div class="governor-card" style="border: {border}; margin: 5px 0; padding: 15px;">
                    <div class="governor-role" style="font-size: {font_size};">{role_prefix}{gov['title']}</div>
                    <div class="governor-name">{gov['role']}</div>
                    <div style="font-size:0.65rem; color:#555; margin-top:8px;">{expertise_short}...</div>
                    <div style="margin-top:8px;">
                        <div style="background:#1A1A1A; height:2px;">
                            <div style="background:{bg_color}; width:{weight_pct}%; height:100%;"></div>
                        </div>
                    </div>
                </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 📋 SUBMIT DIRECTIVE TO BOARD")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        directive_text = st.text_area(
            "Presidential Directive:",
            placeholder="Example: 'Analyse XAUUSD for a strategic long position. Price is approaching a key H4 order block after sweeping sell-side liquidity below last week's low. Request full board analysis with entry, exit, and risk parameters.'",
            height=100,
            key="board_directive"
        )
        
        asset_select = st.selectbox(
            "Asset",
            ["XAUUSD (Gold)", "BTCUSD (Bitcoin)", "SPX500 (S&P 500)", 
             "USOIL (Crude Oil)", "EURUSD (Euro)", "USDJPY (Yen)"],
            key="board_asset"
        )
    
    with col2:
        st.markdown("#### Board Protocol")
        st.info("""
        **Process:**
        1. Intelligence Gathering
        2. Individual Governor Analysis
        3. Full Board Debate
        4. Chairman's Final Verdict
        
        **Output:**
        - Precise entry/exit
        - Position sizing
        - Risk parameters
        - Execution protocol
        """)
    
    if st.button("🏛️ CONVENE FULL BOARD", use_container_width=True, type="primary"):
        if directive_text:
            symbol_map = {
                "XAUUSD (Gold)": "GC=F",
                "BTCUSD (Bitcoin)": "BTC-USD",
                "SPX500 (S&P 500)": "ES=F",
                "USOIL (Crude Oil)": "CL=F",
                "EURUSD (Euro)": "EURUSD=X",
                "USDJPY (Yen)": "USDJPY=X"
            }
            
            symbol = symbol_map.get(asset_select, "GC=F")
            
            with st.spinner("📡 Fetching institutional data..."):
                market_data = st.session_state.data_engine.fetch_institutional_data(symbol)
            
            if market_data:
                directive = st.session_state.board.convene_board(
                    asset_select, directive_text, market_data
                )
                
                st.divider()
                display_board_directive(directive)
                
                st.session_state.active_directives.append(directive)
            else:
                st.error("Unable to fetch market data. Check symbol or try again.")
        else:
            st.error("Please enter a directive for the Board.")

def render_trading_terminal():
    st.markdown("### 🎯 EXECUTION TERMINAL")
    
    if st.button("🔍 AUTO-SCAN FOR HIGH PROBABILITY SETUPS", use_container_width=True):
        with st.spinner("Scanning institutional order flow..."):
            st.session_state.scan_results = st.session_state.scanner.scan_all_markets()
    
    if st.session_state.scan_results:
        st.success(f"Found {len(st.session_state.scan_results)} high-probability setups")
        
        for setup in st.session_state.scan_results:
            with st.expander(
                f"🎯 **{setup['display']}** | Score: {setup['score']}/100 | Direction: {setup['direction']}",
                expanded=True
            ):
                col1, col2, col3 = st.columns(3)
                data = setup['data']
                
                col1.metric("Price", f"${data['price']:,.2f}")
                col2.metric("RSI", f"{data['rsi_14']:.1f}")
                col3.metric("Structure", data['price_structure'].replace('_', ' '))
                
                if st.button(f"📊 Submit to Board", key=f"submit_{setup['symbol']}"):
                    st.session_state['pending_setup'] = setup
                    st.success(f"Setup submitted! Switch to Board Room for full analysis.")
    
    st.divider()
    
    st.markdown("### 📋 Manual Position Entry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        asset = st.selectbox("Asset", 
            ["XAUUSD", "BTCUSD", "SPX500", "USOIL", "EURUSD", "USDJPY"],
            key="manual_asset"
        )
        direction = st.radio("Direction", ["LONG", "SHORT"], horizontal=True)
        
        col_e, col_s, col_t = st.columns(3)
        entry = col_e.number_input("Entry", value=0.0, step=0.01)
        stop = col_s.number_input("Stop Loss", value=0.0, step=0.01)
        target = col_t.number_input("Target", value=0.0, step=0.01)
    
    with col2:
        risk = st.slider("Risk % of AUM", 0.1, 1.0, 0.5, 0.1)
        
        if entry > 0 and stop > 0:
            total_aum = 9963
            risk_amount = total_aum * (risk / 100)
            pos_size = risk_amount / abs(entry - stop)
            
            st.metric("Max Risk", f"${risk_amount:.2f}")
            st.metric("Position Size", f"{pos_size:.4f} units")
            st.metric("Notional", f"${pos_size * entry:,.2f}")
    
    if st.button("🔍 ANALYSE WITH BOARD", use_container_width=True):
        if entry > 0:
            with st.spinner("Board analysing..."):
                symbol_map = {
                    "XAUUSD": "GC=F", "BTCUSD": "BTC-USD", "SPX500": "ES=F",
                    "USOIL": "CL=F", "EURUSD": "EURUSD=X", "USDJPY": "USDJPY=X"
                }
                
                symbol = symbol_map.get(asset, "GC=F")
                market_data = st.session_state.data_engine.fetch_institutional_data(symbol)
                
                if market_data:
                    directive_text = f"Analyse {asset} for {direction} position. Entry: {entry}, Stop: {stop}, Target: {target}"
                    directive = st.session_state.board.convene_board(
                        asset, directive_text, market_data
                    )
                    
                    display_board_directive(directive)
                    st.session_state.active_directives.append(directive)

def render_market_scanner():
    st.markdown("### 🔍 INSTITUTIONAL SETUP SCANNER")
    st.markdown("*Autonomous detection of high-probability institutional trading opportunities*")
    
    if st.button("🚀 SCAN ALL MARKETS", use_container_width=True, type="primary"):
        with st.spinner("Scanning institutional data feeds..."):
            results = st.session_state.scanner.scan_all_markets()
            st.session_state.scan_results = results
    
    if st.session_state.scan_results:
        for setup in st.session_state.scan_results:
            with st.expander(
                f"{'🥇' if setup['score'] > 80 else '🥈' if setup['score'] > 70 else '📊'} "
                f"{setup['display']} | Score: {setup['score']}/100",
                expanded=setup['score'] > 75
            ):
                data = setup['data']
                
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Price", f"${data['price']:,.2f}")
                col2.metric("Direction", setup['direction'])
                col3.metric("RSI", f"{data['rsi_14']:.1f}")
                col4.metric("Volume", data['volume_trend'])
                
                sr = data['support_resistance']
                st.markdown(f"""
                    **Support:** S1: ${sr['support_1']} | S2: ${sr['support_2']}
                    **Resistance:** R1: ${sr['resistance_1']} | R2: ${sr['resistance_2']}
                    **ATR:** ${data['atr_14']:.2f} | **Volatility:** {data['volatility_30d']}%
                """)
                
                if st.button(f"📊 Full Board Analysis", key=f"scan_board_{setup['symbol']}"):
                    st.session_state['pending_scan'] = setup
                    st.success("Switching to Board Room...")

def render_portfolio():
    st.markdown("### 📊 SOVEREIGN PORTFOLIO")
    
    st.markdown("#### Active Positions")
    
    if st.session_state.active_directives:
        for directive in st.session_state.active_directives[-5:]:
            signal_color = "#00C853" if directive.signal == SignalType.BUY else "#FF1744"
            st.markdown(f"""
                <div style="border-left:3px solid {signal_color}; padding:10px; margin:10px 0; background:#0A0A0A;">
                    <strong>{directive.asset}</strong> - {directive.signal.value} | 
                    Conviction: {directive.conviction.value}/10 | Size: {directive.position_size_pct}%
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active positions. Submit directives to the Board.")
    
    st.divider()
    
    st.markdown("#### Fund Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("DNA Fund", "$4,995", "Active")
    col2.metric("Sure Leverage", "$4,968", "Active")
    col3.metric("Total AUM", "$9,963", "Growing")
    col4.metric("Target", "$1,000,000,000+", "🎯")
    
    st.markdown("""
        <div style="background:#0A0A0A; padding:20px; border:1px solid #222; border-radius:4px; margin-top:20px;">
            <h4 style="color:#C8A84E;">🎯 GROWTH OBJECTIVE</h4>
            <p style="color:#CCC;">
                Current AUM: <strong>$9,963</strong><br>
                Target: <strong>$1,000,000,000+</strong><br>
                Strategy: Institutional AI-driven trading with Federal Reserve Board governance model<br>
                Risk Management: Maximum 1% per trade, multi-governor approval required
            </p>
        </div>
    """, unsafe_allow_html=True)

def display_board_directive(directive: BoardDirective):
    signal_color = "#00C853" if directive.signal == SignalType.BUY else "#FF1744" if directive.signal == SignalType.SELL else "#FFD600"
    
    directive_html = f"""
        <div class="board-directive">
            <div class="classified-stamp">CLASSIFIED</div>
            
            <div class="decision-banner {directive.signal.value.lower()}">
                <h2 style="color:{signal_color}; font-size:2.5rem; margin:0;">
                    {directive.signal.value}
                </h2>
                <p style="color:#888; margin:10px 0;">
                    Directive #{directive.directive_id} | Conviction: {directive.conviction.value}/10
                </p>
            </div>
            
            <div class="param-grid">
                <div class="param-item">
                    <div class="param-label">Entry Zone</div>
                    <div class="param-value">${directive.entry_zone[0]:.2f} — ${directive.entry_zone[1]:.2f}</div>
                </div>
                <div class="param-item">
                    <div class="param-label">Stop Loss</div>
                    <div class="param-value" style="color:#FF1744;">${directive.stop_loss:.2f}</div>
                </div>
                <div class="param-item">
                    <div class="param-label">Target 1</div>
                    <div class="param-value" style="color:#00C853;">${directive.targets[0]:.2f}</div>
                </div>
                <div class="param-item">
                    <div class="param-label">Target 2</div>
                    <div class="param-value" style="color:#00C853;">${directive.targets[1]:.2f}</div>
                </div>
            </div>
            
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px; margin:15px 0;">
                <div>
                    <strong style="color:#C8A84E;">Position Size:</strong> {directive.position_size_pct}% of AUM
                </div>
                <div>
                    <strong style="color:#C8A84E;">Timeframe:</strong> {directive.timeframe.value}
                </div>
            </div>
            
            <div style="background:#0A0A0A; padding:20px; border-left:3px solid #C8A84E; margin:15px 0;">
                <strong style="color:#C8A84E;">👑 CHAIRMAN'S VERDICT:</strong>
                <p style="color:#CCC; margin:10px 0;">{directive.chairman_statement}</p>
            </div>
            
            <div style="color:#666; font-size:0.8rem;">
                <strong>Execution:</strong> {directive.execution_protocol}<br>
                <strong>Risk Note:</strong> {directive.risk_assessment}<br>
                <strong>Expiry:</strong> {directive.expiry}
            </div>
        </div>
    """
    st.markdown(directive_html, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
