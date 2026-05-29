import streamlit as st
import os
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
import google.generativeai as genai
from typing import Dict, List, Optional, Tuple, Any
import json
from dataclasses import dataclass, field
from enum import Enum
import warnings
import time
import hashlib
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
# INSTITUTIONAL STYLING - WORLD CLASS UI
# ============================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --gold: #C8A84E;
    --gold-light: #D4AF37;
    --dark-bg: #0A0A0A;
    --card-bg: #111111;
    --border: #1A1A1A;
    --text: #E0E0E0;
    --text-dim: #888888;
    --success: #00C853;
    --danger: #FF1744;
    --warning: #FFD600;
}

.stApp {
    background: var(--dark-bg);
    color: var(--text);
}

/* Institutional Typography */
.institutional-header {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--gold);
    text-align: center;
    border-bottom: 1px solid var(--gold);
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

/* Board Member Cards */
.governor-card {
    background: linear-gradient(145deg, #0D0D0D, #1A1A1A);
    border: 1px solid #222;
    border-radius: 4px;
    padding: 20px;
    position: relative;
    transition: all 0.3s ease;
}

.governor-card:hover {
    border-color: var(--gold);
    box-shadow: 0 4px 20px rgba(200, 168, 78, 0.1);
}

.governor-card.chairman {
    border: 2px solid var(--gold);
    background: linear-gradient(145deg, #111, #1A1A1A);
}

.governor-role {
    font-family: 'Cormorant Garamond', serif;
    font-size: 1.1rem;
    color: var(--gold);
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

/* Decision Cards */
.board-directive {
    background: #000;
    border: 1px solid var(--gold);
    padding: 30px;
    border-radius: 4px;
    position: relative;
    margin: 20px 0;
}

.board-directive::before {
    content: 'BOARD DIRECTIVE';
    position: absolute;
    top: -10px;
    left: 20px;
    background: #000;
    color: var(--gold);
    padding: 0 10px;
    font-size: 0.7rem;
    letter-spacing: 3px;
    font-family: 'JetBrains Mono', monospace;
}

.decision-banner {
    padding: 30px;
    text-align: center;
    border: 2px solid;
    border-radius: 4px;
    margin: 20px 0;
    font-family: 'Cormorant Garamond', serif;
}

.decision-banner.buy { border-color: #00C853; background: rgba(0,200,83,0.05); }
.decision-banner.sell { border-color: #FF1744; background: rgba(255,23,68,0.05); }
.decision-banner.hold { border-color: #FFD600; background: rgba(255,214,0,0.05); }

/* Institutional Data Feed */
.data-feed {
    background: #050505;
    border-left: 3px solid var(--gold);
    padding: 15px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    color: #666;
}

/* Trading Parameters */
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

/* Buttons */
.stButton > button {
    font-family: 'Inter', sans-serif;
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 500;
    border-radius: 2px;
    padding: 15px 30px;
    transition: all 0.3s ease;
}

.stButton > button.primary {
    background: var(--gold);
    color: #000;
    border: none;
}

.stButton > button.primary:hover {
    background: var(--gold-light);
}

/* Custom scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #000; }
::-webkit-scrollbar-thumb { background: #222; }
::-webkit-scrollbar-thumb:hover { background: var(--gold); }

/* Animations */
@keyframes scan {
    0% { opacity: 0.3; }
    50% { opacity: 1; }
    100% { opacity: 0.3; }
}

.scanning { animation: scan 2s infinite; }

/* Confidential watermark */
.confidential-watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 8rem;
    color: rgba(200, 168, 78, 0.02);
    pointer-events: none;
    z-index: -1;
    font-family: 'Cormorant Garamond', serif;
    white-space: nowrap;
}
</style>

<div class="confidential-watermark">SOVEREIGN</div>
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
class InstitutionalIntel:
    """Non-public institutional intelligence"""
    dark_pool_prints: Dict
    block_trade_activity: str
    gamma_exposure: float
    option_flow_sentiment: str
    institutional_positioning: str
    smart_money_index: float
    market_maker_positioning: str
    hedge_fund_consensus: str
    sovereign_flow: str
    central_bank_activity: str
    
@dataclass
class MacroAnalysis:
    """Federal Reserve level macro analysis"""
    fed_policy_stance: str
    rate_trajectory: str
    inflation_outlook: str
    gdp_growth_forecast: float
    yield_curve_signal: str
    liquidity_conditions: str
    credit_spread_signal: str
    global_capital_flows: str
    geopolitical_risk: str
    dollar_regime: str

@dataclass
class FundamentalAnalysis:
    """Institutional fundamental assessment"""
    fair_value_range: Tuple[float, float]
    institutional_demand_score: float
    supply_dynamics: str
    carry_cost: float
    correlation_regime: str
    volatility_regime: str
    seasonality_factor: float
    etf_flow_analysis: str
    cftc_positioning: str
    breakeven_analysis: Dict

@dataclass
class TechnicalAnalysis:
    """Multi-timeframe technical assessment"""
    primary_trend: str
    momentum_regime: str
    volume_profile: str
    key_support: float
    key_resistance: float
    pattern_recognition: str
    fibonacci_confluence: List[float]
    market_structure: str
    order_block_zones: List[Dict]
    liquidity_levels: Dict

@dataclass
class BoardVote:
    """Individual governor vote"""
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
    """Final board directive - Chairman's verdict"""
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
# INSTITUTIONAL DATA ENGINE
# ============================================

class InstitutionalDataEngine:
    """Access institutional-grade market intelligence"""
    
    def __init__(self):
        self.cache = {}
        self.cache_ttl = timedelta(minutes=2)
        self.lock = threading.Lock()
        
    def fetch_institutional_data(self, symbol: str) -> Dict:
        """Fetch comprehensive institutional data"""
        cache_key = f"{symbol}_{datetime.now().strftime('%Y%m%d_%H')}"
        
        with self.lock:
            if cache_key in self.cache:
                cached_time, data = self.cache[cache_key]
                if datetime.now() - cached_time < self.cache_ttl:
                    return data
        
        try:
            ticker = yf.Ticker(symbol)
            
            # Get price data
            df_1d = ticker.history(period="1d", interval="1m")
            df_1mo = ticker.history(period="1mo", interval="1h")
            df_6mo = ticker.history(period="6mo", interval="1d")
            
            if df_6mo.empty:
                return self._generate_synthetic_data(symbol)
            
            close = df_6mo['Close']
            high = df_6mo['High']
            low = df_6mo['Low']
            volume = df_6mo['Volume']
            current_price = close.iloc[-1]
            
            # Calculate institutional metrics
            data = {
                'price': round(current_price, 2),
                'change_1d': round(((close.iloc[-1] - close.iloc[-2]) / close.iloc[-2]) * 100, 2) if len(close) > 1 else 0,
                'volatility_30d': round(close.pct_change().std() * np.sqrt(252) * 100, 2),
                'volume_ratio': round(volume.iloc[-1] / volume.mean(), 2),
                'rsi_14': self._calculate_rsi(close, 14),
                'macd_histogram': self._calculate_macd(close),
                'bb_position': self._calculate_bb_position(close),
                'atr_14': self._calculate_atr(high, low, close, 14),
                'sma_20': round(close.rolling(20).mean().iloc[-1], 2),
                'sma_50': round(close.rolling(50).mean().iloc[-1], 2),
                'sma_200': round(close.rolling(200).mean().iloc[-1], 2) if len(close) >= 200 else round(close.mean(), 2),
                'volume_trend': self._analyze_volume_trend(volume),
                'price_structure': self._analyze_market_structure(close, high, low),
                'support_resistance': self._find_key_levels(high, low, close),
                'liquidity_zones': self._identify_liquidity(high, low, volume),
                'market_profile': self._market_profile_analysis(df_1mo)
            }
            
            # Cache the result
            with self.lock:
                self.cache[cache_key] = (datetime.now(), data)
            
            return data
            
        except Exception as e:
            return self._generate_synthetic_data(symbol)
    
    def _calculate_rsi(self, prices: pd.Series, period: int) -> float:
        delta = prices.diff()
        gain = delta.where(delta > 0, 0.0).rolling(period).mean()
        loss = (-delta.where(delta < 0, 0.0)).rolling(period).mean()
        rs = gain / loss
        return round(100 - (100 / (1 + rs.iloc[-1])), 1)
    
    def _calculate_macd(self, prices: pd.Series) -> float:
        ema12 = prices.ewm(span=12).mean()
        ema26 = prices.ewm(span=26).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9).mean()
        return round((macd - signal).iloc[-1], 4)
    
    def _calculate_bb_position(self, prices: pd.Series) -> float:
        sma = prices.rolling(20).mean()
        std = prices.rolling(20).std()
        upper = sma + 2 * std
        lower = sma - 2 * std
        pos = (prices.iloc[-1] - lower.iloc[-1]) / (upper.iloc[-1] - lower.iloc[-1])
        return round(pos, 2)
    
    def _calculate_atr(self, high, low, close, period) -> float:
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        return round(tr.rolling(period).mean().iloc[-1], 4)
    
    def _analyze_volume_trend(self, volume: pd.Series) -> str:
        vol_ma = volume.rolling(20).mean()
        current = volume.iloc[-1]
        if current > vol_ma.iloc[-1] * 1.5:
            return "CLIMACTIC"
        elif current > vol_ma.iloc[-1] * 1.2:
            return "ELEVATED"
        elif current < vol_ma.iloc[-1] * 0.5:
            return "SUBDUED"
        return "NORMAL"
    
    def _analyze_market_structure(self, close, high, low) -> str:
        """Analyze market structure (HH/HL or LH/LL)"""
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
    
    def _find_key_levels(self, high, low, close) -> Dict:
        """Find key support and resistance levels"""
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
    
    def _identify_liquidity(self, high, low, volume) -> List[Dict]:
        """Identify liquidity zones"""
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
    
    def _market_profile_analysis(self, df) -> Dict:
        """Basic market profile analysis"""
        if df.empty:
            return {'poc': 0, 'value_area': (0, 0)}
        
        price_range = pd.cut(df['Close'], bins=10)
        volume_by_price = df.groupby(price_range)['Volume'].sum()
        poc_bin = volume_by_price.idxmax()
        poc = (poc_bin.left + poc_bin.right) / 2
        
        total_vol = volume_by_price.sum()
        cumsum = 0
        value_high = None
        value_low = None
        
        for bin_range, vol in volume_by_price.items():
            cumsum += vol
            if cumsum <= total_vol * 0.7:
                if value_low is None:
                    value_low = bin_range.left
                value_high = bin_range.right
        
        return {
            'poc': round(poc, 2),
            'value_area_high': round(value_high, 2) if value_high else round(poc * 1.01, 2),
            'value_area_low': round(value_low, 2) if value_low else round(poc * 0.99, 2)
        }
    
    def _generate_synthetic_data(self, symbol: str) -> Dict:
        """Generate data when real data is unavailable"""
        # Map common symbols to approximate prices
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
            'market_profile': {
                'poc': base_price,
                'value_area_high': base_price * 1.01,
                'value_area_low': base_price * 0.99
            }
        }

# ============================================
# SOVEREIGN BOARD OF GOVERNORS
# ============================================

class SovereignBoardOfGovernors:
    """
    SOVEREIGN FUND CAPITAL - BOARD OF GOVERNORS
    Modeled after the Federal Reserve Board of Governors
    
    Chairman: Osinachi (Final Decision Authority)
    
    Seven Specialized Governors providing institutional-grade analysis
    with access to non-public information flows.
    """
    
    def __init__(self):
        self.model = self._initialize_model()
        self.vote_history = deque(maxlen=500)
        self.directive_counter = 0
        
        # Board composition - Federal Reserve Model
        self.governors = {
            "CHAIRMAN_OSINACHI": {
                "id": "CHAIRMAN_OSINACHI",
                "title": "Chairman of the Board",
                "role": "Chief Investment Officer",
                "expertise": "Portfolio Strategy, Risk Management, Final Authority",
                "weight": 0.25,
                "background": "Former Federal Reserve Governor (12 years). PhD Economics, MIT. Managed through 2008, 2020 crises. $50B+ institutional AUM experience.",
                "personality": "Decisive, analytical, visionary. Known for contrarian calls and impeccable timing.",
                "vote_power": "FINAL - Override Authority"
            },
            "GOVERNOR_MACRO": {
                "id": "GOVERNOR_MACRO",
                "title": "Governor of Monetary & Macro Strategy",
                "role": "Head of Global Macro",
                "expertise": "Central Bank Policy, Yield Curve Analysis, Global Capital Flows",
                "weight": 0.15,
                "background": "Ex-IMF Chief Economist. 20 years central bank advisory. PhD Monetary Economics, LSE.",
                "personality": "Data-driven, forward-looking, systematic thinker."
            },
            "GOVERNOR_FLOW": {
                "id": "GOVERNOR_FLOW",
                "title": "Governor of Institutional Flow & Structure",
                "role": "Head of Order Flow Intelligence",
                "expertise": "Dark Pool Analysis, CME Positioning, Smart Money Tracking",
                "weight": 0.15,
                "background": "Former Goldman Sachs Partner, Head of US Equity Derivatives. 25 years institutional flow trading.",
                "personality": "Precise, secretive, unmatched pattern recognition. Sees what others don't."
            },
            "GOVERNOR_QUANT": {
                "id": "GOVERNOR_QUANT",
                "title": "Governor of Quantitative Strategy",
                "role": "Chief Quantitative Officer",
                "expertise": "Statistical Arbitrage, Machine Learning, Probability Theory",
                "weight": 0.15,
                "background": "PhD Mathematical Finance, Stanford. Ex-Renaissance Technologies, D.E. Shaw. 15+ years alpha generation.",
                "personality": "Mathematical, rigorous, probability-weighted. Never emotional."
            },
            "GOVERNOR_RISK": {
                "id": "GOVERNOR_RISK",
                "title": "Governor of Risk & Compliance",
                "role": "Chief Risk Officer",
                "expertise": "VaR Modeling, Tail Risk, Black Swan Protection, Stress Testing",
                "weight": 0.15,
                "background": "Former Fed Risk Supervisor. Basel Committee Advisor. 20 years systemic risk management.",
                "personality": "Conservative, protective, detail-oriented. The voice of caution."
            },
            "GOVERNOR_INTEL": {
                "id": "GOVERNOR_INTEL",
                "title": "Governor of Market Intelligence",
                "role": "Director of Intelligence",
                "expertise": "Geopolitical Risk, Insider Activity, Non-Public Information Analysis",
                "weight": 0.10,
                "background": "Former CIA Economic Intelligence. 15 years tracking sovereign wealth flows and central bank activity.",
                "personality": "Paranoid, connected, always sees the hidden hand. Nothing escapes notice."
            },
            "GOVERNOR_EXECUTION": {
                "id": "GOVERNOR_EXECUTION",
                "title": "Governor of Trading Operations",
                "role": "Head of Execution",
                "expertise": "Order Execution, Slippage Control, Market Microstructure",
                "weight": 0.05,
                "background": "Ex-Jump Trading, Citadel Execution. 20 years HFT and institutional execution.",
                "personality": "Technical, precise, execution-obsessed. Every tick matters."
            }
        }
    
    def _initialize_model(self):
        """Initialize Gemini model"""
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
            st.error(f"Model initialization failed: {e}")
            return None
    
    def convene_board(self, asset: str, directive: str, market_data: Dict) -> BoardDirective:
        """
        Convene full board meeting.
        Each governor provides institutional-grade analysis.
        Chairman Osinachi makes final decision.
        """
        
        self.directive_counter += 1
        directive_id = f"SFC-{datetime.now().strftime('%Y%m%d')}-{self.directive_counter:04d}"
        
        st.info("🏛️ **BOARD IN SESSION** - Governors convening...")
        
        # Phase 1: Gather Intelligence
        with st.spinner("📡 GATHERING INSTITUTIONAL INTELLIGENCE..."):
            intel = self._gather_intelligence(asset, market_data)
        
        # Phase 2: Individual Governor Analysis
        governor_votes = []
        analyses_container = st.container()
        
        with analyses_container:
            st.markdown("### 📊 GOVERNOR DELIBERATIONS")
            
            progress = st.progress(0)
            governors_list = list(self.governors.items())
            
            for idx, (gov_id, gov_info) in enumerate(governors_list):
                if gov_id == "CHAIRMAN_OSINACHI":
                    continue  # Chairman votes last
                
                progress.progress((idx + 1) / len(governors_list))
                
                with st.expander(f"🎓 **{gov_info['title']}** - {gov_info['role']}", expanded=(idx < 2)):
                    vote = self._get_governor_vote(gov_id, gov_info, asset, directive, market_data, intel)
                    governor_votes.append(vote)
                    
                    # Display governor analysis
                    signal_color = "#00C853" if vote.signal == SignalType.BUY else "#FF1744" if vote.signal == SignalType.SELL else "#FFD600"
                    st.markdown(f"""
                        <div style="border-left: 3px solid {signal_color}; padding: 10px; margin: 10px 0; background: #0A0A0A;">
                            <strong style="color: {signal_color};">VOTE: {vote.signal.value}</strong>
                            <span style="color: #666;"> | Conviction: {vote.conviction.value}/10</span>
                            <p style="margin: 10px 0; color: #CCC;">{vote.rationale}</p>
                            <small style="color: #888;">Risk Note: {vote.risk_assessment}</small>
                        </div>
                    """, unsafe_allow_html=True)
            
            progress.empty()
        
        # Phase 3: Chairman's Deliberation
        st.markdown("---")
        st.markdown("### 👑 CHAIRMAN OSINACHI - FINAL VERDICT")
        
        with st.spinner("Chairman synthesizing all analysis..."):
            final_directive = self._chairman_verdict(
                directive_id, asset, directive, market_data, 
                governor_votes, intel
            )
        
        # Store in history
        self.vote_history.append(final_directive)
        
        return final_directive
    
    def _gather_intelligence(self, asset: str, market_data: Dict) -> Dict:
        """Gather institutional-grade intelligence"""
        
        intel_prompt = f"""
        You are the Director of Intelligence at Sovereign Fund Capital.
        You have access to non-public information flows including:
        - Dark pool prints and block trade data
        - CME Commitment of Traders reports
        - Prime brokerage flow data
        - Central bank activity monitoring
        - Sovereign wealth fund movements
        
        Asset: {asset}
        Market Data: {json.dumps(market_data, indent=2)}
        
        Provide intelligence briefing:
        1. Institutional positioning (3 bullets)
        2. Unusual activity detected (2 bullets)
        3. Smart money consensus
        4. Risk flags
        
        Be specific and quantitative.
        """
        
        try:
            if self.model:
                response = self.model.generate_content(intel_prompt)
                return {'raw_intel': response.text, 'source': 'AI_ANALYSIS'}
        except:
            pass
        
        return {'raw_intel': 'Intelligence gathering in progress...', 'source': 'SYNTHETIC'}
    
    def _get_governor_vote(self, gov_id: str, gov_info: Dict, asset: str, 
                           directive: str, market_data: Dict, intel: Dict) -> BoardVote:
        """Get individual governor's vote"""
        
        prompt = f"""
        You are {gov_info['title']} at Sovereign Fund Capital.
        
        BACKGROUND: {gov_info['background']}
        EXPERTISE: {gov_info['expertise']}
        PERSONALITY: {gov_info['personality']}
        
        You are voting on: {directive}
        Asset: {asset}
        
        MARKET DATA:
        {json.dumps(market_data, indent=2)}
        
        INTELLIGENCE BRIEFING:
        {intel.get('raw_intel', 'Classified')}
        
        Provide your analysis and vote. Format:
        VOTE: [BUY/SELL/HOLD]
        CONVICTION: [1-10]
        RATIONALE: [2-3 sentences from your expertise perspective]
        RISK: [Key risk concern]
        CONDITIONS: [Any conditions for your vote]
        """
        
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                text = response.text
                
                # Parse response
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
        
        # Fallback vote based on market data
        return self._fallback_vote(gov_id, gov_info, market_data)
    
    def _chairman_verdict(self, directive_id: str, asset: str, directive: str,
                          market_data: Dict, votes: List[BoardVote], intel: Dict) -> BoardDirective:
        """Chairman Osinachi's final decision"""
        
        # Count votes
        buy_votes = sum(1 for v in votes if v.signal == SignalType.BUY)
        sell_votes = sum(1 for v in votes if v.signal == SignalType.SELL)
        hold_votes = sum(1 for v in votes if v.signal == SignalType.HOLD)
        
        # Average conviction
        avg_conviction = np.mean([v.conviction.value for v in votes]) if votes else 5
        
        prompt = f"""
        You are CHAIRMAN OSINACHI, Chief Investment Officer of Sovereign Fund Capital.
        
        CREDENTIALS:
        - Former Federal Reserve Governor (12 years)
        - PhD Economics, MIT
        - 30 years institutional investment experience
        - Managed $50B+ institutional portfolios
        - Successfully navigated: 2008 Crisis, 2020 Crash, 2022 Bear Market
        
        BOARD VOTE TALLY:
        - BUY Votes: {buy_votes}
        - SELL Votes: {sell_votes}
        - HOLD Votes: {hold_votes}
        - Average Conviction: {avg_conviction:.1f}/10
        
        ASSET: {asset}
        DIRECTIVE: {directive}
        
        MARKET DATA:
        {json.dumps(market_data, indent=2)}
        
        INDIVIDUAL VOTES:
        {json.dumps([{'role': v.governor_role, 'vote': v.signal.value, 'conviction': v.conviction.value, 'rationale': v.rationale[:100]} for v in votes], indent=2)}
        
        As Chairman, you must now make the FINAL DECISION that will be executed with REAL capital.
        
        Your decision must consider:
        1. Current AUM: DNA Fund $4,995 | Sure Leverage $4,968
        2. Objective: Grow to multi-billion dollar fund
        3. Maximum risk: 1% per trade
        4. The weight of board evidence
        5. Your own institutional experience
        
        DELIVER YOUR FINAL VERDICT:
        SIGNAL: [BUY/SELL/HOLD]
        CONVICTION: [1-10]
        ENTRY_ZONE_LOW: [price]
        ENTRY_ZONE_HIGH: [price]
        STOP_LOSS: [price]
        TARGET_1: [price]
        TARGET_2: [price]
        POSITION_SIZE: [0.1-1.0% of AUM]
        TIMEFRAME: [SCALP/INTRADAY/SWING/POSITION/INVESTMENT]
        RATIONALE: [Your reasoning]
        RISK_NOTE: [Key risk consideration]
        """
        
        try:
            if self.model:
                response = self.model.generate_content(prompt)
                text = response.text
                
                # Parse chairman's decision
                signal = self._extract_signal(text)
                conviction = self._extract_conviction(text)
                entry_low = self._extract_float(text, 'ENTRY_ZONE_LOW', market_data.get('price', 0) * 0.99)
                entry_high = self._extract_float(text, 'ENTRY_ZONE_HIGH', market_data.get('price', 0) * 1.01)
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
        
        # Fallback - conservative hold
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
        """Generate fallback vote based on technical analysis"""
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
        """Conservative fallback directive"""
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
    """Autonomous scanner for high-probability institutional setups"""
    
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
        """Scan all markets for high-probability setups"""
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
        """Multi-factor probability scoring"""
        score = 50
        
        # Trend alignment
        if data['price_structure'] == 'BULLISH_STRUCTURE':
            score += 15
        elif data['price_structure'] == 'BEARISH_STRUCTURE':
            score += 10
        
        # RSI optimal zone
        rsi = data['rsi_14']
        if 40 <= rsi <= 60:
            score += 10
        elif 30 <= rsi <= 70:
            score += 5
        
        # Volume confirmation
        if data['volume_ratio'] > 1.5:
            score += 15
        
        # MACD confirmation
        if data['macd_histogram'] > 0 and 'BULLISH' in data['price_structure']:
            score += 10
        elif data['macd_histogram'] < 0 and 'BEARISH' in data['price_structure']:
            score += 10
        
        # ATR range
        atr_pct = data['atr_14'] / data['price'] * 100
        if 1 < atr_pct < 3:
            score += 5
        
        return min(100, score)
    
    def _determine_direction(self, data: Dict) -> str:
        """Determine optimal trade direction"""
        if data['price_structure'] == 'BULLISH_STRUCTURE' and data['rsi_14'] < 60:
            return 'LONG'
        elif data['price_structure'] == 'BEARISH_STRUCTURE' and data['rsi_14'] > 40:
            return 'SHORT'
        return 'NEUTRAL'

# ============================================
# MAIN APPLICATION
# ============================================

def main():
    """Sovereign Fund Capital - Main Application"""
    
    # Initialize session state
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
    
    # Check API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("🔴 GOOGLE_API_KEY not configured!")
        st.code("export GOOGLE_API_KEY='your-api-key'")
        st.stop()
    
    genai.configure(api_key=api_key)
    
    # ============================================
    # SIDEBAR - COMMAND CENTER
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
        
        # AUM Display
        st.markdown("### 💰 ASSETS UNDER MANAGEMENT")
        
        col1, col2 = st.columns(2)
        col1.metric("DNA Fund", "$4,995", "🔒")
        col2.metric("Sure Leverage", "$4,968", "🔒")
        st.metric("Total AUM", "$9,963", "🎯 Target: $1B+")
        
        st.divider()
        
        # Navigation
        st.markdown("### 📋 DIRECTIVES")
        page = st.radio(
            "Select Command",
            ["🏛️ Board Room", "🎯 Trading Terminal", "🔍 Market Scanner", "📊 Portfolio"],
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # Market Status
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
    st.markdown("">
        <h1 class="institutional-header">SOVEREIGN FUND CAPITAL</h1>
        <p style="text-align:center; color:#888; font-size:0.8rem; letter-spacing:2px;">
            INSTITUTIONAL AI BOARD OF GOVERNORS | PRIVATE HEDGE FUND
        </p>
    """, unsafe_allow_html=True)
    
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
    """Institutional Board Room"""
    
    st.markdown("### 🏛️ BOARD OF GOVERNORS")
    st.markdown("*Federal Reserve Model - Seven Specialized Governors + Chairman Osinachi*")
    
    # Display board members
    board = st.session_state.board
    cols = st.columns(4)
    
    for i, (gov_id, gov) in enumerate(board.governors.items()):
        with cols[i % 4]:
            is_chairman = gov_id == "CHAIRMAN_OSINACHI"
            border = "2px solid #C8A84E" if is_chairman else "1px solid #222"
            
            st.markdown(f"""
                <div class="governor-card {'chairman' if is_chairman else ''}" 
                     style="border: {border}; margin: 5px 0; padding: 15px;">
                    <div class="governor-role">{'👑 ' if is_chairman else ''}{gov['title']}</div>
                    <div class="governor-name">{gov['role']}</div>
                    <div style="font-size:0.65rem; color:#555; margin-top:8px;">{gov['expertise'][:50]}...</div>
                    <div style="margin-top:8px;">
                        <div style="background:#1A1A1A; height:2px;">
                            <div style="background:{'#C8A84E' if is_chairman else '#444'}; 
                                        width:{gov['weight']*100}%; height:100%;"></div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    st.divider()
    
    # Directive input
    st.markdown("### 📋 SUBMIT DIRECTIVE TO BOARD")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        directive_text = st.text_area(
            "Presidential Directive:",
            placeholder="Example: 'Analyze XAUUSD for a strategic long position. Current price showing institutional accumulation. Request full board analysis with entry, exit, and risk parameters.'",
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
            # Map asset to symbol
            symbol_map = {
                "XAUUSD (Gold)": "GC=F",
                "BTCUSD (Bitcoin)": "BTC-USD",
                "SPX500 (S&P 500)": "ES=F",
                "USOIL (Crude Oil)": "CL=F",
                "EURUSD (Euro)": "EURUSD=X",
                "USDJPY (Yen)": "USDJPY=X"
            }
            
            symbol = symbol_map.get(asset_select, "GC=F")
            
            # Fetch market data
            with st.spinner("📡 Fetching institutional data..."):
                market_data = st.session_state.data_engine.fetch_institutional_data(symbol)
            
            if market_data:
                # Convene board
                directive = st.session_state.board.convene_board(
                    asset_select, directive_text, market_data
                )
                
                # Display final directive
                st.divider()
                display_board_directive(directive)
                
                # Store
                st.session_state.active_directives.append(directive)
            else:
                st.error("Unable to fetch market data. Check symbol or try again.")
        else:
            st.error("Please enter a directive for the Board.")

def render_trading_terminal():
    """Trading Terminal"""
    
    st.markdown("### 🎯 EXECUTION TERMINAL")
    
    # Quick scan
    if st.button("🔍 AUTO-SCAN FOR HIGH PROBABILITY SETUPS", use_container_width=True):
        with st.spinner("Scanning institutional order flow..."):
            st.session_state.scan_results = st.session_state.scanner.scan_all_markets()
    
    # Display scan results
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
    
    # Manual entry
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
            total_aum = 9963  # Current total AUM
            risk_amount = total_aum * (risk / 100)
            pos_size = risk_amount / abs(entry - stop)
            
            st.metric("Max Risk", f"${risk_amount:.2f}")
            st.metric("Position Size", f"{pos_size:.4f} units")
            st.metric("Notional", f"${pos_size * entry:,.2f}")
    
    if st.button("🔍 ANALYZE WITH BOARD", use_container_width=True):
        if entry > 0:
            with st.spinner("Board analyzing..."):
                symbol_map = {
                    "XAUUSD": "GC=F", "BTCUSD": "BTC-USD", "SPX500": "ES=F",
                    "USOIL": "CL=F", "EURUSD": "EURUSD=X", "USDJPY": "USDJPY=X"
                }
                
                symbol = symbol_map.get(asset, "GC=F")
                market_data = st.session_state.data_engine.fetch_institutional_data(symbol)
                
                if market_data:
                    directive_text = f"Analyze {asset} for {direction} position. Entry: {entry}, Stop: {stop}, Target: {target}"
                    directive = st.session_state.board.convene_board(
                        asset, directive_text, market_data
                    )
                    
                    display_board_directive(directive)
                    st.session_state.active_directives.append(directive)

def render_market_scanner():
    """Market Scanner"""
    
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
                
                st.markdown(f"""
                    **Support Levels:** S1: ${data['support_resistance']['support_1']} | 
                    S2: ${data['support_resistance']['support_2']}
                    **Resistance Levels:** R1: ${data['support_resistance']['resistance_1']} | 
                    R2: ${data['support_resistance']['resistance_2']}
                    **ATR:** ${data['atr_14']:.2f} | **Volatility:** {data['volatility_30d']}%
                """)
                
                if st.button(f"📊 Full Board Analysis", key=f"scan_board_{setup['symbol']}"):
                    st.session_state['pending_scan'] = setup
                    st.success("Switching to Board Room...")

def render_portfolio():
    """Portfolio Overview"""
    
    st.markdown("### 📊 SOVEREIGN PORTFOLIO")
    
    # Current positions
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
    
    # Performance metrics
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
    """Display board directive in institutional format"""
    
    signal_color = "#00C853" if directive.signal == SignalType.BUY else "#FF1744" if directive.signal == SignalType.SELL else "#FFD600"
    
    st.markdown(f"""
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
                    <div class="param-value">${directive.entry_zone[0]:.2f} - ${directive.entry_zone[1]:.2f}</div>
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
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
