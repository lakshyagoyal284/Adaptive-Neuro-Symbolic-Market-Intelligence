"""
Real Market Data Backtester for Adaptive Neuro-Symbolic Market Intelligence System
This module uses real stock market data for comprehensive backtesting
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

# Import system components
from symbolic_engine.decision_engine import DecisionEngine
from symbolic_engine.rules import RuleEngine
from adaptive_module.learning import AdaptiveLearningEngine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class BacktestTrade:
    """Data class for backtest trade"""
    symbol: str
    entry_date: datetime
    exit_date: datetime
    entry_price: float
    exit_price: float
    quantity: int
    trade_type: str  # 'long' or 'short'
    pnl: float
    pnl_pct: float
    decision_type: str
    confidence: float
    holding_period: int  # in minutes

@dataclass
class BacktestResults:
    """Data class for backtest results"""
    initial_capital: float
    final_capital: float
    total_return: float
    total_return_pct: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    total_trades: int
    winning_trades: int
    losing_trades: int
    avg_win: float
    avg_loss: float
    profit_factor: float
    trades: List[BacktestTrade]

class RealMarketBacktester:
    """
    Backtester using real market data from CSV files
    """
    
    def __init__(self, data_directory: str = None):
        self.data_directory = data_directory or "c:\\Users\\laksh\\Desktop\\adaptive_market_intelligence"
        self.market_data = {}
        self.decision_engine = DecisionEngine()
        self.learning_engine = AdaptiveLearningEngine()
        self.current_capital = 100000  # Starting capital
        self.positions = {}
        self.trades = []
        
    def load_market_data(self) -> Dict[str, pd.DataFrame]:
        """Load real market data from CSV files"""
        try:
            logger.info("Loading real market data...")
            
            # Path to 10-minute data
            data_path = os.path.join(self.data_directory, "temp_data_10min", "10minute")
            
            if not os.path.exists(data_path):
                logger.error(f"Data path not found: {data_path}")
                return {}
            
            # Get all CSV files
            csv_files = glob.glob(os.path.join(data_path, "*.csv"))
            logger.info(f"Found {len(csv_files)} CSV files")
            
            market_data = {}
            
            # Load major stocks for backtesting
            major_stocks = [
                'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'HINDUNILVR',
                'ICICIBANK', 'KOTAKBANK', 'SBIN', 'BHARTIARTL', 'ASIANPAINT'
            ]
            
            for csv_file in csv_files:
                try:
                    symbol = os.path.basename(csv_file).replace('.csv', '')
                    
                    # Focus on major stocks for performance
                    if symbol in major_stocks:
                        df = pd.read_csv(csv_file)
                        
                        # Convert and sort
                        df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)  # Remove timezone
                        df = df.sort_values('date')
                        
                        # Calculate technical indicators
                        df = self.calculate_indicators(df)
                        
                        # Filter for recent data (use last 3 months of available data)
                        if len(df) > 1000:  # Ensure sufficient data
                            # Take last 3 months of data
                            df = df.tail(len(df) // 4)  # Approximate last quarter
                            market_data[symbol] = df
                            logger.info(f"Loaded {symbol}: {len(df)} rows")
                        
                except Exception as e:
                    logger.error(f"Error loading {csv_file}: {e}")
                    continue
            
            self.market_data = market_data
            logger.info(f"Successfully loaded {len(market_data)} symbols for backtesting")
            return market_data
            
        except Exception as e:
            logger.error(f"Error loading market data: {e}")
            return {}
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators for trading signals"""
        try:
            df = df.copy()
            
            # Price changes
            df['price_change'] = df['close'] - df['open']
            df['price_change_pct'] = (df['price_change'] / df['open']) * 100
            
            # Moving averages
            df['ma_20'] = df['close'].rolling(window=20).mean()
            df['ma_50'] = df['close'].rolling(window=50).mean()
            
            # RSI
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df['rsi'] = 100 - (100 / (1 + rs))
            
            # Volatility
            df['returns'] = df['close'].pct_change()
            df['volatility'] = df['returns'].rolling(window=20).std() * 100
            
            # Support/Resistance
            df['resistance'] = df['high'].rolling(window=20).max()
            df['support'] = df['low'].rolling(window=20).min()
            
            # Volume indicators
            df['volume_ma'] = df['volume'].rolling(window=20).mean()
            df['volume_ratio'] = df['volume'] / df['volume_ma']
            
            return df
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
            return df
    
    def generate_trading_signals(self, symbol: str, df: pd.DataFrame, current_index: int) -> Dict[str, Any]:
        """Generate trading signals using system components"""
        try:
            if current_index < 50:  # Need enough history
                return {"signal": "hold", "confidence": 0.5}
            
            current_data = df.iloc[current_index]
            
            # Create context for decision engine
            context = {
                'market_growth': current_data['price_change_pct'],
                'sentiment_score': np.clip(current_data['price_change_pct'] / 100, -1, 1),
                'market_volatility': current_data['volatility'],
                'negative_sentiment': max(0, (1 - current_data['rsi']/100) * 100),
                'trend_demand': current_data['volume_ratio'] * 50,
                'competitor_price_increase': np.random.uniform(0, 20),  # Simulated
                'market_share': np.random.uniform(10, 30)  # Simulated
            }
            
            # Generate AI insights
            ai_insights = {
                'sentiment_analysis': {
                    'average_sentiment': context['sentiment_score'],
                    'overall_trend': 'improving' if context['sentiment_score'] > 0 else 'declining'
                },
                'trend_analysis': {
                    'volatility': current_data['volatility'] / 100,
                    'growth_rate': context['market_growth']
                }
            }
            
            # Make decisions using system
            decisions = self.decision_engine.make_decision(context, ai_insights)
            
            if not decisions:
                return {"signal": "hold", "confidence": 0.5}
            
            # Analyze decisions to determine trading signal
            buy_signals = sum(1 for d in decisions if hasattr(d, 'decision_type') and 
                           d.decision_type.value in ['investment', 'opportunity'])
            sell_signals = sum(1 for d in decisions if hasattr(d, 'decision_type') and 
                            d.decision_type.value in ['risk_management'])
            
            # Calculate confidence
            total_confidence = sum(getattr(d, 'confidence_score', 0.5) for d in decisions if hasattr(d, 'confidence_score'))
            avg_confidence = total_confidence / len(decisions) if decisions else 0.5
            
            # Determine signal
            if buy_signals > sell_signals and buy_signals > 0:
                return {"signal": "buy", "confidence": avg_confidence, "decisions": decisions}
            elif sell_signals > buy_signals and sell_signals > 0:
                return {"signal": "sell", "confidence": avg_confidence, "decisions": decisions}
            else:
                return {"signal": "hold", "confidence": avg_confidence}
                
        except Exception as e:
            logger.error(f"Error generating signals for {symbol}: {e}")
            return {"signal": "hold", "confidence": 0.5}
    
    def execute_trade(self, symbol: str, signal: Dict[str, Any], price: float, timestamp: datetime):
        """Execute trade based on signal"""
        try:
            if signal["signal"] == "hold":
                return
            
            # Position sizing (2% risk per trade)
            risk_amount = self.current_capital * 0.02
            quantity = int(risk_amount / price)
            
            if signal["signal"] == "buy" and symbol not in self.positions:
                # Open long position
                self.positions[symbol] = {
                    'entry_price': price,
                    'quantity': quantity,
                    'entry_date': timestamp,
                    'signal': signal
                }
                
            elif signal["signal"] == "sell" and symbol in self.positions:
                # Close position
                position = self.positions[symbol]
                exit_price = price
                pnl = (exit_price - position['entry_price']) * position['quantity']
                pnl_pct = (exit_price - position['entry_price']) / position['entry_price'] * 100
                
                # Update capital
                self.current_capital += pnl
                
                # Get decision info safely
                decisions = position['signal'].get('decisions', [])
                decision_type = 'unknown'
                confidence = 0.5
                
                if decisions and len(decisions) > 0:
                    if hasattr(decisions[0], 'decision_type'):
                        decision_type = decisions[0].decision_type.value
                    if hasattr(decisions[0], 'confidence_score'):
                        confidence = decisions[0].confidence_score
                
                # Record trade
                trade = BacktestTrade(
                    symbol=symbol,
                    entry_date=position['entry_date'],
                    exit_date=timestamp,
                    entry_price=position['entry_price'],
                    exit_price=exit_price,
                    quantity=position['quantity'],
                    trade_type='long',
                    pnl=pnl,
                    pnl_pct=pnl_pct,
                    decision_type=decision_type,
                    confidence=confidence,
                    holding_period=int((timestamp - position['entry_date']).total_seconds() / 60)
                )
                
                self.trades.append(trade)
                del self.positions[symbol]
                
        except Exception as e:
            logger.error(f"Error executing trade for {symbol}: {e}")
    
    def run_backtest(self, start_date: datetime = None, end_date: datetime = None) -> BacktestResults:
        """Run comprehensive backtest on real market data"""
        try:
            logger.info("Starting real market data backtest...")
            
            # Load data
            self.load_market_data()
            
            if not self.market_data:
                raise ValueError("No market data loaded")
            
            # Set date range based on available data
            if not start_date:
                start_date = pd.Timestamp.now() - pd.Timedelta(days=365)  # Use available data
            if not end_date:
                end_date = pd.Timestamp.now() - pd.Timedelta(days=1)
            
            logger.info(f"Backtesting period: {start_date} to {end_date}")
            
            # Initialize
            self.current_capital = 100000
            self.positions = {}
            self.trades = []
            
            # Process each symbol
            for symbol, df in self.market_data.items():
                logger.info(f"Backtesting {symbol}...")
                
                # Use actual data range
                df_filtered = df.copy()
                
                # Process each time period (sample every 100th period for performance)
                for i in range(0, len(df_filtered), 100):
                    current_row = df_filtered.iloc[i]
                    current_time = current_row['date']
                    current_price = current_row['close']
                    
                    # Generate trading signal
                    signal = self.generate_trading_signals(symbol, df_filtered, i)
                    
                    # Execute trade
                    self.execute_trade(symbol, signal, current_price, current_time)
            
            # Close any remaining positions
            for symbol in list(self.positions.keys()):
                position = self.positions[symbol]
                self.execute_trade(symbol, {"signal": "sell"}, position['entry_price'], end_date)
            
            # Calculate results
            results = self.calculate_results()
            
            logger.info(f"Backtest completed. Final capital: ${results.final_capital:,.2f}")
            logger.info(f"Total return: {results.total_return_pct:.2f}%")
            
            return results
            
        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            raise
    
    def calculate_results(self) -> BacktestResults:
        """Calculate backtest results"""
        try:
            if not self.trades:
                return BacktestResults(
                    initial_capital=100000,
                    final_capital=self.current_capital,
                    total_return=0,
                    total_return_pct=0,
                    max_drawdown=0,
                    sharpe_ratio=0,
                    win_rate=0,
                    total_trades=0,
                    winning_trades=0,
                    losing_trades=0,
                    avg_win=0,
                    avg_loss=0,
                    profit_factor=0,
                    trades=[]
                )
            
            # Basic metrics
            initial_capital = 100000
            final_capital = self.current_capital
            total_return = final_capital - initial_capital
            total_return_pct = (total_return / initial_capital) * 100
            
            # Trade metrics
            total_trades = len(self.trades)
            winning_trades = sum(1 for t in self.trades if t.pnl > 0)
            losing_trades = total_trades - winning_trades
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            # Average win/loss
            wins = [t.pnl for t in self.trades if t.pnl > 0]
            losses = [t.pnl for t in self.trades if t.pnl < 0]
            avg_win = np.mean(wins) if wins else 0
            avg_loss = np.mean(losses) if losses else 0
            
            # Profit factor
            total_wins = sum(wins)
            total_losses = abs(sum(losses))
            profit_factor = total_wins / total_losses if total_losses > 0 else float('inf')
            
            # Calculate drawdown
            equity_curve = [initial_capital]
            for trade in self.trades:
                equity_curve.append(equity_curve[-1] + trade.pnl)
            
            peak = initial_capital
            max_drawdown = 0
            for equity in equity_curve:
                if equity > peak:
                    peak = equity
                drawdown = (peak - equity) / peak * 100
                max_drawdown = max(max_drawdown, drawdown)
            
            # Sharpe ratio
            if len(equity_curve) > 1:
                returns = np.diff(equity_curve) / equity_curve[:-1]
                sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
            else:
                sharpe_ratio = 0
            
            return BacktestResults(
                initial_capital=initial_capital,
                final_capital=final_capital,
                total_return=total_return,
                total_return_pct=total_return_pct,
                max_drawdown=max_drawdown,
                sharpe_ratio=sharpe_ratio,
                win_rate=win_rate,
                total_trades=total_trades,
                winning_trades=winning_trades,
                losing_trades=losing_trades,
                avg_win=avg_win,
                avg_loss=avg_loss,
                profit_factor=profit_factor,
                trades=self.trades
            )
            
        except Exception as e:
            logger.error(f"Error calculating results: {e}")
            raise
    
    def generate_report(self, results: BacktestResults) -> Dict[str, Any]:
        """Generate comprehensive backtest report"""
        try:
            report = {
                "backtest_summary": {
                    "initial_capital": results.initial_capital,
                    "final_capital": results.final_capital,
                    "total_return": results.total_return,
                    "total_return_pct": results.total_return_pct,
                    "max_drawdown": results.max_drawdown,
                    "sharpe_ratio": results.sharpe_ratio,
                    "backtest_period": "Real Market Data (3 months)"
                },
                "performance_metrics": {
                    "total_trades": results.total_trades,
                    "winning_trades": results.winning_trades,
                    "losing_trades": results.losing_trades,
                    "win_rate": results.win_rate,
                    "avg_win": results.avg_win,
                    "avg_loss": results.avg_loss,
                    "profit_factor": results.profit_factor
                },
                "trade_analysis": self.analyze_trades(results.trades),
                "recommendations": self.generate_recommendations(results),
                "detailed_trades": [
                    {
                        "symbol": t.symbol,
                        "entry_date": t.entry_date.isoformat(),
                        "exit_date": t.exit_date.isoformat(),
                        "entry_price": t.entry_price,
                        "exit_price": t.exit_price,
                        "pnl": t.pnl,
                        "pnl_pct": t.pnl_pct,
                        "decision_type": t.decision_type,
                        "confidence": t.confidence,
                        "holding_period_minutes": t.holding_period
                    } for t in results.trades[-20:]  # Last 20 trades
                ],
                "generated_at": datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating report: {e}")
            return {"error": str(e)}
    
    def analyze_trades(self, trades: List[BacktestTrade]) -> Dict[str, Any]:
        """Analyze trades for insights"""
        try:
            if not trades:
                return {}
            
            # Performance by symbol
            symbol_performance = {}
            for trade in trades:
                if trade.symbol not in symbol_performance:
                    symbol_performance[trade.symbol] = {
                        'trades': 0,
                        'wins': 0,
                        'total_pnl': 0,
                        'avg_pnl': 0
                    }
                
                symbol_performance[trade.symbol]['trades'] += 1
                symbol_performance[trade.symbol]['total_pnl'] += trade.pnl
                if trade.pnl > 0:
                    symbol_performance[trade.symbol]['wins'] += 1
            
            # Calculate averages
            for symbol, data in symbol_performance.items():
                if data['trades'] > 0:
                    data['avg_pnl'] = data['total_pnl'] / data['trades']
                    data['win_rate'] = (data['wins'] / data['trades']) * 100
            
            # Performance by decision type
            decision_performance = {}
            for trade in trades:
                decision_type = trade.decision_type
                if decision_type not in decision_performance:
                    decision_performance[decision_type] = {
                        'trades': 0,
                        'wins': 0,
                        'total_pnl': 0
                    }
                
                decision_performance[decision_type]['trades'] += 1
                decision_performance[decision_type]['total_pnl'] += trade.pnl
                if trade.pnl > 0:
                    decision_performance[decision_type]['wins'] += 1
            
            # Calculate win rates
            for decision, data in decision_performance.items():
                if data['trades'] > 0:
                    data['win_rate'] = (data['wins'] / data['trades']) * 100
            
            # Holding period analysis
            holding_periods = [t.holding_period for t in trades]
            
            return {
                "symbol_performance": symbol_performance,
                "decision_type_performance": decision_performance,
                "holding_period_stats": {
                    "avg_minutes": np.mean(holding_periods),
                    "median_minutes": np.median(holding_periods),
                    "max_minutes": max(holding_periods),
                    "min_minutes": min(holding_periods)
                }
            }
            
        except Exception as e:
            logger.error(f"Error analyzing trades: {e}")
            return {}
    
    def generate_recommendations(self, results: BacktestResults) -> List[str]:
        """Generate recommendations based on backtest results"""
        recommendations = []
        
        # Return analysis
        if results.total_return_pct > 20:
            recommendations.append("🎉 Excellent returns! Strategy is highly effective")
        elif results.total_return_pct > 10:
            recommendations.append("✅ Good returns! Strategy is working well")
        elif results.total_return_pct > 0:
            recommendations.append("📈 Positive returns. Strategy shows promise")
        else:
            recommendations.append("⚠️ Negative returns. Strategy needs optimization")
        
        # Risk analysis
        if results.max_drawdown > 20:
            recommendations.append("🛑 High drawdown detected. Implement better risk management")
        elif results.max_drawdown > 10:
            recommendations.append("⚡ Moderate drawdown. Consider position sizing")
        
        # Win rate analysis
        if results.win_rate > 60:
            recommendations.append("🎯 Excellent win rate! Strategy is very accurate")
        elif results.win_rate > 50:
            recommendations.append("✅ Good win rate. Strategy is effective")
        elif results.win_rate > 40:
            recommendations.append("📊 Moderate win rate. Room for improvement")
        else:
            recommendations.append("❌ Low win rate. Review entry/exit criteria")
        
        # Profit factor analysis
        if results.profit_factor > 2:
            recommendations.append("💰 Excellent profit factor. Strong risk/reward ratio")
        elif results.profit_factor > 1.5:
            recommendations.append("💵 Good profit factor. Positive expectancy")
        elif results.profit_factor > 1:
            recommendations.append("📈 Positive profit factor. Slightly profitable")
        else:
            recommendations.append("📉 Negative profit factor. Losers outweigh winners")
        
        # Sharpe ratio analysis
        if results.sharpe_ratio > 2:
            recommendations.append("⭐ Excellent risk-adjusted returns")
        elif results.sharpe_ratio > 1:
            recommendations.append("🌟 Good risk-adjusted returns")
        elif results.sharpe_ratio > 0.5:
            recommendations.append("💫 Moderate risk-adjusted returns")
        else:
            recommendations.append("🌙 Low risk-adjusted returns. Improve consistency")
        
        return recommendations

def main():
    """Main function to run real market data backtesting"""
    try:
        print("🚀 Real Market Data Backtesting - Adaptive Neuro-Symbolic Market Intelligence")
        print("=" * 90)
        
        # Initialize backtester
        backtester = RealMarketBacktester()
        
        # Run backtest
        print("📊 Running backtest on real market data...")
        results = backtester.run_backtest()
        
        # Display results
        print("\n📈 BACKTEST RESULTS")
        print("=" * 50)
        print(f"Initial Capital: ${results.initial_capital:,.2f}")
        print(f"Final Capital: ${results.final_capital:,.2f}")
        print(f"Total Return: ${results.total_return:,.2f}")
        print(f"Total Return %: {results.total_return_pct:.2f}%")
        print(f"Maximum Drawdown: {results.max_drawdown:.2f}%")
        print(f"Sharpe Ratio: {results.sharpe_ratio:.2f}")
        
        print(f"\n🎯 TRADE METRICS")
        print("=" * 50)
        print(f"Total Trades: {results.total_trades}")
        print(f"Winning Trades: {results.winning_trades}")
        print(f"Losing Trades: {results.losing_trades}")
        print(f"Win Rate: {results.win_rate:.2f}%")
        print(f"Average Win: ${results.avg_win:.2f}")
        print(f"Average Loss: ${results.avg_loss:.2f}")
        print(f"Profit Factor: {results.profit_factor:.2f}")
        
        # Generate and save report
        print("\n📋 Generating detailed report...")
        report = backtester.generate_report(results)
        
        with open('real_market_backtest_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Show recommendations
        if 'recommendations' in report:
            print("\n💡 RECOMMENDATIONS")
            print("=" * 50)
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"{i}. {rec}")
        
        # Show top performing symbols
        if 'trade_analysis' in report and 'symbol_performance' in report['trade_analysis']:
            print("\n🏆 TOP PERFORMING SYMBOLS")
            print("=" * 50)
            symbol_perf = report['trade_analysis']['symbol_performance']
            top_symbols = sorted(symbol_perf.items(), key=lambda x: x[1]['total_pnl'], reverse=True)[:5]
            
            for i, (symbol, perf) in enumerate(top_symbols, 1):
                print(f"{i}. {symbol}: ${perf['total_pnl']:.2f} ({perf['trades']} trades, {perf.get('win_rate', 0):.1f}% win rate)")
        
        print(f"\n✅ Backtest completed successfully!")
        print(f"📄 Detailed report saved to 'real_market_backtest_report.json'")
        
        return backtester, results
        
    except Exception as e:
        logger.error(f"Backtest failed: {e}")
        print(f"❌ Backtest failed: {e}")
        return None, None

if __name__ == "__main__":
    main()
