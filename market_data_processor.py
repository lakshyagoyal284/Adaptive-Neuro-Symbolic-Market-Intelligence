"""
Market Data Processor for Adaptive Neuro-Symbolic Market Intelligence System
This module processes real stock market data from CSV files and integrates with the system
"""

import pandas as pd
import numpy as np
import os
import glob
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
import json
from dataclasses import dataclass
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TimeFrame(Enum):
    """Enumeration of available timeframes"""
    THREE_MINUTE = "3minute"
    FIVE_MINUTE = "5minute"
    TEN_MINUTE = "10minute"
    FIFTEEN_MINUTE = "15minute"

@dataclass
class MarketDataPoint:
    """Data class for market data point"""
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    timeframe: str

@dataclass
class MarketMetrics:
    """Data class for market metrics"""
    symbol: str
    current_price: float
    price_change: float
    price_change_pct: float
    volume: int
    volatility: float
    rsi: float
    moving_avg_20: float
    moving_avg_50: float
    trend_direction: str
    support_level: float
    resistance_level: float

class MarketDataProcessor:
    """
    Comprehensive market data processor for real stock data integration
    """
    
    def __init__(self, data_directory: str = None):
        self.data_directory = data_directory or "c:\\Users\\laksh\\Desktop\\adaptive_market_intelligence"
        self.market_data = {}
        self.processed_data = {}
        self.available_symbols = []
        self.timeframes = {}
        
    def load_market_data(self, timeframe: TimeFrame = TimeFrame.TEN_MINUTE) -> Dict[str, pd.DataFrame]:
        """Load market data from CSV files"""
        try:
            logger.info(f"Loading market data for {timeframe.value} timeframe...")
            
            # Construct path to data directory
            data_path = os.path.join(self.data_directory, f"temp_data_{timeframe.value}", timeframe.value)
            
            # Try alternative paths if the main one doesn't exist
            if not os.path.exists(data_path):
                alt_path = os.path.join(self.data_directory, f"temp_data_{timeframe.value}")
                if os.path.exists(alt_path):
                    data_path = alt_path
                else:
                    # Try direct path
                    direct_path = f"c:\\Users\\laksh\\Desktop\\adaptive_market_intelligence\\temp_data_{timeframe.value}\\{timeframe.value}"
                    if os.path.exists(direct_path):
                        data_path = direct_path
            
            if not os.path.exists(data_path):
                logger.error(f"Data path not found: {data_path}")
                return {}
            
            # Get all CSV files
            csv_files = glob.glob(os.path.join(data_path, "*.csv"))
            logger.info(f"Found {len(csv_files)} CSV files")
            
            market_data = {}
            
            for csv_file in csv_files:
                try:
                    # Extract symbol from filename
                    symbol = os.path.basename(csv_file).replace('.csv', '')
                    
                    # Load CSV data
                    df = pd.read_csv(csv_file)
                    
                    # Convert date column to datetime
                    df['date'] = pd.to_datetime(df['date'])
                    
                    # Sort by date
                    df = df.sort_values('date')
                    
                    # Store in dictionary
                    market_data[symbol] = df
                    
                except Exception as e:
                    logger.error(f"Error loading {csv_file}: {e}")
                    continue
            
            self.market_data[timeframe.value] = market_data
            self.available_symbols = list(market_data.keys())
            self.timeframes[timeframe.value] = timeframe
            
            logger.info(f"Successfully loaded {len(market_data)} symbols for {timeframe.value}")
            return market_data
            
        except Exception as e:
            logger.error(f"Error loading market data: {e}")
            return {}
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for market data"""
        try:
            df = df.copy()
            
            # Price changes
            df['price_change'] = df['close'] - df['open']
            df['price_change_pct'] = (df['price_change'] / df['open']) * 100
            
            # Moving averages
            df['ma_20'] = df['close'].rolling(window=20).mean()
            df['ma_50'] = df['close'].rolling(window=50).mean()
            
            # RSI (Relative Strength Index)
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # Bollinger Bands
            df['bb_middle'] = df['close'].rolling(window=20).mean()
            bb_std = df['close'].rolling(window=20).std()
            df['bb_upper'] = df['bb_middle'] + (bb_std * 2)
            df['bb_lower'] = df['bb_middle'] - (bb_std * 2)
            
            # Volatility (standard deviation of returns)
            df['returns'] = df['close'].pct_change()
            df['volatility'] = df['returns'].rolling(window=20).std() * 100
            
            # MACD
            exp1 = df['close'].ewm(span=12).mean()
            exp2 = df['close'].ewm(span=26).mean()
            df['macd'] = exp1 - exp2
            df['macd_signal'] = df['macd'].ewm(span=9).mean()
            df['macd_histogram'] = df['macd'] - df['macd_signal']
            
            # Support and Resistance levels
            df['resistance'] = df['high'].rolling(window=20).max()
            df['support'] = df['low'].rolling(window=20).min()
            
            return df
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
            return df
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate indicators (alias for calculate_technical_indicators)"""
        # This is an alias method to fix the missing method issue
        return self.calculate_technical_indicators(df)
    
    def identify_trends(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Identify market trends from technical indicators"""
        try:
            if len(df) < 50:
                return {"trend": "insufficient_data", "strength": 0}
            
            latest = df.iloc[-1]
            prev = df.iloc[-2]
            
            # Trend direction based on moving averages
            if latest['ma_20'] > latest['ma_50']:
                if latest['close'] > latest['ma_20']:
                    trend = "strong_uptrend"
                    strength = min(1.0, (latest['close'] - latest['ma_50']) / latest['ma_50'])
                else:
                    trend = "uptrend"
                    strength = 0.5
            elif latest['ma_20'] < latest['ma_50']:
                if latest['close'] < latest['ma_20']:
                    trend = "strong_downtrend"
                    strength = min(1.0, (latest['ma_50'] - latest['close']) / latest['ma_50'])
                else:
                    trend = "downtrend"
                    strength = 0.5
            else:
                trend = "sideways"
                strength = 0.3
            
            # RSI-based momentum
            if latest['rsi'] > 70:
                momentum = "overbought"
            elif latest['rsi'] < 30:
                momentum = "oversold"
            else:
                momentum = "neutral"
            
            # Volume analysis
            avg_volume = df['volume'].rolling(window=20).mean().iloc[-1]
            volume_signal = "high" if latest['volume'] > avg_volume * 1.5 else "normal"
            
            return {
                "trend": trend,
                "strength": strength,
                "momentum": momentum,
                "volume_signal": volume_signal,
                "rsi": latest['rsi'],
                "price_change_pct": latest['price_change_pct'],
                "volatility": latest['volatility']
            }
            
        except Exception as e:
            logger.error(f"Error identifying trends: {e}")
            return {"trend": "error", "strength": 0}
    
    def get_market_metrics(self, symbol: str, timeframe: TimeFrame = TimeFrame.TEN_MINUTE) -> Optional[MarketMetrics]:
        """Get comprehensive market metrics for a symbol"""
        try:
            if timeframe.value not in self.market_data:
                self.load_market_data(timeframe)
            
            if symbol not in self.market_data[timeframe.value]:
                logger.warning(f"Symbol {symbol} not found in market data")
                return None
            
            df = self.market_data[timeframe.value][symbol]
            
            # Calculate technical indicators
            df_with_indicators = self.calculate_technical_indicators(df)
            
            # Get latest data
            latest = df_with_indicators.iloc[-1]
            
            # Identify trends
            trend_analysis = self.identify_trends(df_with_indicators)
            
            # Create metrics object
            metrics = MarketMetrics(
                symbol=symbol,
                current_price=latest['close'],
                price_change=latest['price_change'],
                price_change_pct=latest['price_change_pct'],
                volume=int(latest['volume']),
                volatility=latest['volatility'],
                rsi=latest['rsi'],
                moving_avg_20=latest['ma_20'],
                moving_avg_50=latest['ma_50'],
                trend_direction=trend_analysis['trend'],
                support_level=latest['support'],
                resistance_level=latest['resistance']
            )
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error getting market metrics for {symbol}: {e}")
            return None
    
    def get_market_overview(self, timeframe: TimeFrame = TimeFrame.TEN_MINUTE) -> Dict[str, Any]:
        """Get market overview with top performers and market sentiment"""
        try:
            if timeframe.value not in self.market_data:
                self.load_market_data(timeframe)
            
            market_data = self.market_data[timeframe.value]
            overview = {
                "total_symbols": len(market_data),
                "top_gainers": [],
                "top_losers": [],
                "most_active": [],
                "market_sentiment": "neutral",
                "avg_volatility": 0,
                "trending_up": 0,
                "trending_down": 0,
                "timestamp": datetime.now().isoformat()
            }
            
            metrics_list = []
            
            # Calculate metrics for all symbols
            for symbol in list(market_data.keys())[:50]:  # Limit to top 50 for performance
                metrics = self.get_market_metrics(symbol, timeframe)
                if metrics:
                    metrics_list.append(metrics)
            
            if not metrics_list:
                return overview
            
            # Sort by different criteria
            top_gainers = sorted(metrics_list, key=lambda x: x.price_change_pct, reverse=True)[:10]
            top_losers = sorted(metrics_list, key=lambda x: x.price_change_pct)[:10]
            most_active = sorted(metrics_list, key=lambda x: x.volume, reverse=True)[:10]
            
            overview["top_gainers"] = [
                {
                    "symbol": m.symbol,
                    "price": m.current_price,
                    "change_pct": m.price_change_pct,
                    "volume": m.volume
                } for m in top_gainers
            ]
            
            overview["top_losers"] = [
                {
                    "symbol": m.symbol,
                    "price": m.current_price,
                    "change_pct": m.price_change_pct,
                    "volume": m.volume
                } for m in top_losers
            ]
            
            overview["most_active"] = [
                {
                    "symbol": m.symbol,
                    "price": m.current_price,
                    "change_pct": m.price_change_pct,
                    "volume": m.volume
                } for m in most_active
            ]
            
            # Calculate market sentiment
            positive_changes = sum(1 for m in metrics_list if m.price_change_pct > 0)
            negative_changes = sum(1 for m in metrics_list if m.price_change_pct < 0)
            
            if positive_changes > negative_changes * 1.5:
                overview["market_sentiment"] = "bullish"
            elif negative_changes > positive_changes * 1.5:
                overview["market_sentiment"] = "bearish"
            else:
                overview["market_sentiment"] = "neutral"
            
            # Calculate averages
            overview["avg_volatility"] = np.mean([m.volatility for m in metrics_list])
            overview["trending_up"] = sum(1 for m in metrics_list if "uptrend" in m.trend_direction)
            overview["trending_down"] = sum(1 for m in metrics_list if "downtrend" in m.trend_direction)
            
            return overview
            
        except Exception as e:
            logger.error(f"Error getting market overview: {e}")
            return {"error": str(e)}
    
    def generate_trading_signals(self, symbol: str, timeframe: TimeFrame = TimeFrame.TEN_MINUTE) -> Dict[str, Any]:
        """Generate trading signals based on technical analysis"""
        try:
            metrics = self.get_market_metrics(symbol, timeframe)
            if not metrics:
                return {"error": f"No data available for {symbol}"}
            
            signals = {
                "symbol": symbol,
                "current_price": metrics.current_price,
                "signals": [],
                "overall_signal": "hold",
                "confidence": 0.5,
                "timestamp": datetime.now().isoformat()
            }
            
            # RSI signals
            if metrics.rsi < 30:
                signals["signals"].append({
                    "type": "rsi_oversold",
                    "action": "buy",
                    "strength": "strong",
                    "reason": f"RSI ({metrics.rsi:.1f}) indicates oversold condition"
                })
            elif metrics.rsi > 70:
                signals["signals"].append({
                    "type": "rsi_overbought",
                    "action": "sell",
                    "strength": "strong",
                    "reason": f"RSI ({metrics.rsi:.1f}) indicates overbought condition"
                })
            
            # Moving average signals
            if metrics.current_price > metrics.moving_avg_20 > metrics.moving_avg_50:
                signals["signals"].append({
                    "type": "ma_crossover_bullish",
                    "action": "buy",
                    "strength": "medium",
                    "reason": "Price above both 20 and 50 period moving averages"
                })
            elif metrics.current_price < metrics.moving_avg_20 < metrics.moving_avg_50:
                signals["signals"].append({
                    "type": "ma_crossover_bearish",
                    "action": "sell",
                    "strength": "medium",
                    "reason": "Price below both 20 and 50 period moving averages"
                })
            
            # Trend signals
            if "strong_uptrend" in metrics.trend_direction:
                signals["signals"].append({
                    "type": "trend_follow",
                    "action": "buy",
                    "strength": "strong",
                    "reason": "Strong uptrend detected"
                })
            elif "strong_downtrend" in metrics.trend_direction:
                signals["signals"].append({
                    "type": "trend_follow",
                    "action": "sell",
                    "strength": "strong",
                    "reason": "Strong downtrend detected"
                })
            
            # Support/Resistance signals
            if abs(metrics.current_price - metrics.support_level) / metrics.current_price < 0.02:
                signals["signals"].append({
                    "type": "support_test",
                    "action": "buy",
                    "strength": "medium",
                    "reason": f"Price near support level at {metrics.support_level:.2f}"
                })
            elif abs(metrics.current_price - metrics.resistance_level) / metrics.current_price < 0.02:
                signals["signals"].append({
                    "type": "resistance_test",
                    "action": "sell",
                    "strength": "medium",
                    "reason": f"Price near resistance level at {metrics.resistance_level:.2f}"
                })
            
            # Determine overall signal
            buy_signals = sum(1 for s in signals["signals"] if s["action"] == "buy")
            sell_signals = sum(1 for s in signals["signals"] if s["action"] == "sell")
            
            if buy_signals > sell_signals:
                signals["overall_signal"] = "buy"
                signals["confidence"] = min(0.9, 0.5 + (buy_signals - sell_signals) * 0.1)
            elif sell_signals > buy_signals:
                signals["overall_signal"] = "sell"
                signals["confidence"] = min(0.9, 0.5 + (sell_signals - buy_signals) * 0.1)
            else:
                signals["overall_signal"] = "hold"
                signals["confidence"] = 0.5
            
            return signals
            
        except Exception as e:
            logger.error(f"Error generating trading signals for {symbol}: {e}")
            return {"error": str(e)}
    
    def get_symbol_list(self, timeframe: TimeFrame = TimeFrame.TEN_MINUTE) -> List[str]:
        """Get list of available symbols"""
        if timeframe.value not in self.market_data:
            self.load_market_data(timeframe)
        
        return self.available_symbols
    
    def export_processed_data(self, output_file: str = "processed_market_data.json"):
        """Export processed market data to JSON file"""
        try:
            processed_data = {
                "export_timestamp": datetime.now().isoformat(),
                "available_timeframes": list(self.timeframes.keys()),
                "total_symbols": len(self.available_symbols),
                "symbols": self.available_symbols,
                "market_overview": {}
            }
            
            # Generate overview for each timeframe
            for timeframe in self.timeframes.keys():
                try:
                    tf_enum = TimeFrame(timeframe)
                    overview = self.get_market_overview(tf_enum)
                    processed_data["market_overview"][timeframe] = overview
                except:
                    continue
            
            # Save to file
            with open(output_file, 'w') as f:
                json.dump(processed_data, f, indent=2, default=str)
            
            logger.info(f"Processed data exported to {output_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting processed data: {e}")
            return False

# Integration function for the Adaptive Market Intelligence System
def integrate_market_data_with_system():
    """Integrate real market data with the Adaptive Market Intelligence System"""
    try:
        print("🔄 Integrating Real Market Data with Adaptive Market Intelligence System")
        print("=" * 80)
        
        # Initialize processor
        processor = MarketDataProcessor()
        
        # Load 10-minute data
        print("📊 Loading 10-minute market data...")
        market_data = processor.load_market_data(TimeFrame.TEN_MINUTE)
        
        if not market_data:
            print("❌ Failed to load market data")
            return False
        
        print(f"✅ Loaded {len(market_data)} symbols")
        
        # Get market overview
        print("\n📈 Generating market overview...")
        overview = processor.get_market_overview(TimeFrame.TEN_MINUTE)
        
        print(f"📊 Market Sentiment: {overview.get('market_sentiment', 'unknown')}")
        print(f"📈 Average Volatility: {overview.get('avg_volatility', 0):.2f}%")
        print(f"⬆️ Trending Up: {overview.get('trending_up', 0)} symbols")
        print(f"⬇️ Trending Down: {overview.get('trending_down', 0)} symbols")
        
        # Show top gainers
        if overview.get('top_gainers'):
            print("\n🚀 Top Gainers:")
            for i, gainer in enumerate(overview['top_gainers'][:5], 1):
                print(f"  {i}. {gainer['symbol']}: +{gainer['change_pct']:.2f}% ({gainer['price']:.2f})")
        
        # Show top losers
        if overview.get('top_losers'):
            print("\n📉 Top Losers:")
            for i, loser in enumerate(overview['top_losers'][:5], 1):
                print(f"  {i}. {loser['symbol']}: {loser['change_pct']:.2f}% ({loser['price']:.2f})")
        
        # Generate trading signals for popular stocks
        popular_stocks = ['RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR']
        
        print("\n🎯 Trading Signals for Popular Stocks:")
        for symbol in popular_stocks:
            if symbol in market_data:
                signals = processor.generate_trading_signals(symbol, TimeFrame.TEN_MINUTE)
                if 'error' not in signals:
                    print(f"  {symbol}: {signals['overall_signal'].upper()} (Confidence: {signals['confidence']:.2f})")
                    if signals['signals']:
                        for signal in signals['signals'][:2]:  # Show top 2 signals
                            print(f"    - {signal['reason']}")
        
        # Export processed data
        print("\n💾 Exporting processed data...")
        processor.export_processed_data("integrated_market_data.json")
        
        print("\n✅ Market data integration completed successfully!")
        print("📄 Data exported to 'integrated_market_data.json'")
        
        return processor
        
    except Exception as e:
        logger.error(f"Error integrating market data: {e}")
        print(f"❌ Integration failed: {e}")
        return None

if __name__ == "__main__":
    integrate_market_data_with_system()
