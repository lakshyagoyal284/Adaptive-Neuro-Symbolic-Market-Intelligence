"""
Aggressive Profit-Focused Backtester
This system actively generates trades and maximizes profits with real market data
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

# Import existing components
from real_market_backtester import RealMarketBacktester, BacktestResults, BacktestTrade
from adaptive_module.llm_learning_engine import LLMLearningEngine, DecisionOutcome

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AggressiveProfitBacktester:
    """
    Aggressive backtester focused on generating trades and maximizing profits
    """
    
    def __init__(self, data_directory: str = None):
        self.data_directory = data_directory or "c:\\Users\\laksh\\Desktop\\adaptive_market_intelligence"
        self.backtester = RealMarketBacktester(data_directory)
        self.learning_engine = LLMLearningEngine()
        
        # Aggressive profit settings
        self.learning_engine.reward_scale = 10.0  # Very high rewards for profits
        self.learning_engine.punishment_scale = 0.5  # Low punishment to encourage trading
        self.learning_engine.learning_rate = 0.3  # Fast learning
        
        # Trading parameters
        self.min_trade_threshold = 0.02  # 2% minimum movement to trigger trade
        self.max_positions = 5  # Maximum concurrent positions
        self.position_size = 0.2  # 20% of capital per position
        
    def run_aggressive_profit_backtest(self) -> Tuple[BacktestResults, Dict[str, Any]]:
        """Run aggressive profit-focused backtest"""
        try:
            print("💰 Aggressive Profit-Focused Backtesting")
            print("=" * 70)
            print("🎯 Objective: Generate maximum trades and profits")
            
            # Load market data
            print("📊 Loading real market data...")
            market_data = self.backtester.load_market_data()
            
            if not market_data:
                raise ValueError("No market data loaded")
            
            print(f"✅ Loaded {len(market_data)} symbols")
            
            # Initialize aggressive trading
            initial_capital = 100000
            self.backtester.current_capital = initial_capital
            self.backtester.positions = {}
            self.backtester.trades = []
            
            # Track aggressive trading stats
            trading_stats = {
                'total_opportunities': 0,
                'trades_taken': 0,
                'profitable_trades': 0,
                'losing_trades': 0,
                'total_profit': 0,
                'total_loss': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'max_positions_held': 0,
                'avg_holding_period': 0,
                'learning_events': []
            }
            
            # Process each symbol with aggressive trading
            for symbol, df in market_data.items():
                print(f"\n🚀 Aggressive Trading {symbol}...")
                
                # Sample data for performance
                df_sample = df.copy()
                
                for i in range(0, len(df_sample), 10):  # Every 10th point for more trades
                    current_row = df_sample.iloc[i]
                    current_time = current_row['date']
                    current_price = current_row['close']
                    
                    trading_stats['total_opportunities'] += 1
                    
                    # Aggressive signal generation
                    signal = self._generate_aggressive_signal(symbol, df_sample, i)
                    
                    # Execute trade if signal is strong enough
                    if signal["signal"] != "hold" and signal["confidence"] > 0.6:
                        # Check position limits
                        if len(self.backtester.positions) < self.max_positions:
                            old_capital = self.backtester.current_capital
                            self.backtester.execute_trade(symbol, signal, current_price, current_time)
                            
                            # Track trade execution
                            if old_capital != self.backtester.current_capital:
                                trading_stats['trades_taken'] += 1
                                
                                # Calculate profit/loss for closed trades
                                if len(self.backtester.trades) > 0:
                                    last_trade = self.backtester.trades[-1]
                                    if last_trade.pnl > 0:
                                        trading_stats['profitable_trades'] += 1
                                        trading_stats['total_profit'] += last_trade.pnl
                                    else:
                                        trading_stats['losing_trades'] += 1
                                        trading_stats['total_loss'] += abs(last_trade.pnl)
                    
                    # Learn from aggressive decisions
                    if signal["signal"] != "hold":
                        # Create context for learning - CRITICAL FIX
                        context = {
                            'market_growth': current_row.get('price_change_pct', 0),
                            'sentiment_score': np.clip(current_row.get('price_change_pct', 0) / 100, -1, 1),
                            'market_volatility': current_row.get('volatility', 20),
                            # Map to learning weights - CRITICAL
                            'trend_demand': current_row.get('volume_ratio', 1.0) * 30,  # Maps to trend_weight
                            'volume_activity': current_row.get('volume_ratio', 1.0) * 50,  # Maps to volume_weight
                            'profit_potential': abs(current_row.get('price_change_pct', 0)),  # Maps to profit_weight
                            'risk_reward_ratio': abs(current_row.get('price_change_pct', 0)) / max(abs(current_row.get('rsi', 50) - 50), 1),  # Maps to risk_weight
                            # Additional context
                            'negative_sentiment': max(0, (1 - (current_row.get('price_change_pct', 0) / 100 + 1)) * 100),
                            'trend_strength': abs(current_row.get('price_change_pct', 0)),
                            'competitor_price_increase': np.random.uniform(0, 25),
                            'market_share': np.random.uniform(10, 30),
                            'competitor_activity_count': np.random.randint(1, 10)
                        }
                        
                        learning_result = self._learn_from_aggressive_decision(
                            symbol, signal, current_price, current_time, df_sample, i, context
                        )
                        
                        if learning_result:
                            trading_stats['learning_events'].append({
                                'timestamp': current_time.isoformat(),
                                'symbol': symbol,
                                'signal': signal["signal"],
                                'confidence': signal["confidence"],
                                'outcome': learning_result.outcome.value,
                                'reward': learning_result.reward,
                                'punishment': learning_result.punishment
                            })
                    
                    # Track positions
                    current_positions = len(self.backtester.positions)
                    trading_stats['max_positions_held'] = max(trading_stats['max_positions_held'], current_positions)
            
            # Close all remaining positions
            print("\n🔄 Closing all positions...")
            for symbol in list(self.backtester.positions.keys()):
                position = self.backtester.positions[symbol]
                self.backtester.execute_trade(symbol, {"signal": "sell"}, position['entry_price'], datetime.now())
            
            # Calculate final results
            results = self.backtester.calculate_results()
            
            # Calculate final trading statistics
            if trading_stats['trades_taken'] > 0:
                trading_stats['win_rate'] = (trading_stats['profitable_trades'] / trading_stats['trades_taken']) * 100
                
                if trading_stats['total_loss'] > 0:
                    trading_stats['profit_factor'] = trading_stats['total_profit'] / trading_stats['total_loss']
                else:
                    trading_stats['profit_factor'] = float('inf') if trading_stats['total_profit'] > 0 else 0
                
                # Calculate average holding period
                if self.backtester.trades:
                    holding_periods = [trade.holding_period for trade in self.backtester.trades]
                    trading_stats['avg_holding_period'] = np.mean(holding_periods)
            
            # Generate comprehensive report
            profit_report = self._generate_profit_report(trading_stats, results)
            
            print(f"\n💰 AGGRESSIVE TRADING RESULTS")
            print("=" * 60)
            print(f"Initial Capital: ${initial_capital:,.2f}")
            print(f"Final Capital: ${results.final_capital:,.2f}")
            print(f"Total Return: ${results.total_return:,.2f}")
            print(f"Return %: {results.total_return_pct:.2f}%")
            
            print(f"\n🎯 TRADING ACTIVITY")
            print("=" * 60)
            print(f"Total Opportunities: {trading_stats['total_opportunities']}")
            print(f"Trades Taken: {trading_stats['trades_taken']}")
            print(f"Trade Participation: {trading_stats['trades_taken']/trading_stats['total_opportunities']*100:.1f}%")
            print(f"Max Positions Held: {trading_stats['max_positions_held']}")
            
            print(f"\n📈 PROFITABILITY")
            print("=" * 60)
            print(f"Win Rate: {trading_stats['win_rate']:.1f}%")
            print(f"Profitable Trades: {trading_stats['profitable_trades']}")
            print(f"Losing Trades: {trading_stats['losing_trades']}")
            print(f"Total Profit: ${trading_stats['total_profit']:.2f}")
            print(f"Total Loss: ${trading_stats['total_loss']:.2f}")
            print(f"Net Profit: ${trading_stats['total_profit'] - trading_stats['total_loss']:.2f}")
            print(f"Profit Factor: {trading_stats['profit_factor']:.2f}")
            
            if trading_stats['avg_holding_period'] > 0:
                print(f"Avg Holding Period: {trading_stats['avg_holding_period']:.1f} minutes")
            
            print(f"\n🧠 LEARNING SYSTEM")
            print("=" * 60)
            print(f"Model Version: {self.learning_engine.model_version}")
            print(f"Learning Events: {len(trading_stats['learning_events'])}")
            
            return results, profit_report
            
        except Exception as e:
            logger.error(f"Aggressive profit backtest failed: {e}")
            raise
    
    def _generate_aggressive_signal(self, symbol: str, df: pd.DataFrame, index: int) -> Dict[str, Any]:
        """Generate aggressive trading signals"""
        try:
            if index < 10:
                return {"signal": "hold", "confidence": 0.5}
            
            current_data = df.iloc[index]
            
            # Calculate aggressive indicators
            price_change_pct = current_data.get('price_change_pct', 0)
            rsi = current_data.get('rsi', 50)
            volume_ratio = current_data.get('volume_ratio', 1.0)
            
            # Aggressive signal criteria
            signal_strength = 0
            signal_type = "hold"
            
            # Strong buy signals
            if price_change_pct > 1.0 and rsi < 70 and volume_ratio > 1.2:
                signal_strength = min(1.0, (price_change_pct / 3.0) + (volume_ratio - 1.0) * 0.3)
                signal_type = "buy"
            
            # Strong sell signals
            elif price_change_pct < -1.0 and rsi > 30 and volume_ratio > 1.2:
                signal_strength = min(1.0, (abs(price_change_pct) / 3.0) + (volume_ratio - 1.0) * 0.3)
                signal_type = "sell"
            
            # Moderate signals (more aggressive)
            elif abs(price_change_pct) > 0.5 and volume_ratio > 1.5:
                signal_strength = min(1.0, abs(price_change_pct) / 2.0)
                signal_type = "buy" if price_change_pct > 0 else "sell"
            
            # Create signal
            if signal_strength > 0.3:  # Lower threshold for more trades
                return {
                    "signal": signal_type,
                    "confidence": signal_strength,
                    "strength": signal_strength,
                    "price_change": price_change_pct,
                    "rsi": rsi,
                    "volume": volume_ratio
                }
            else:
                return {"signal": "hold", "confidence": 0.5}
                
        except Exception as e:
            logger.error(f"Error generating aggressive signal: {e}")
            return {"signal": "hold", "confidence": 0.5}
    
    def _learn_from_aggressive_decision(self, symbol: str, signal: Dict[str, Any], entry_price: float,
                                     entry_time: datetime, df: pd.DataFrame, index: int, context: Dict[str, Any]) -> Optional[Any]:
        """Learn from aggressive trading decisions"""
        try:
            # Simulate outcome with lookahead
            if index + 20 < len(df):
                future_price = df.iloc[index + 20]['close']
                price_change = (future_price - entry_price) / entry_price * 100
            else:
                # Use last available price
                future_price = df.iloc[-1]['close']
                price_change = (future_price - entry_price) / entry_price * 100
            
            # Determine outcome based on signal and result
            if signal["signal"] == "buy" and price_change > 0:
                outcome = DecisionOutcome.CORRECT
            elif signal["signal"] == "sell" and price_change < 0:
                outcome = DecisionOutcome.CORRECT
            elif abs(price_change) < 0.5:
                outcome = DecisionOutcome.PARTIAL
            else:
                outcome = DecisionOutcome.INCORRECT
            
            # Create experience
            experience = self.learning_engine.analyze_decision_outcome(
                context=context,
                decision_type="aggressive_trading",
                action_taken=signal["signal"],
                confidence=signal.get("confidence", 0.5),
                market_state={"symbol": symbol, "signal_strength": signal.get('strength', 0.5)},
                technical_indicators={
                    'rsi': signal.get('rsi', 50),
                    'price_change': signal.get('price_change', 0)
                },
                rule_triggers=[f"aggressive_{signal['signal']}_signal"],
                actual_result=price_change,
                expected_result=abs(price_change) * 0.8  # Expect 80% of potential
            )
            
            if experience:
                self.learning_engine.learn_from_experience(experience)
                return experience
            
            return None
            
        except Exception as e:
            logger.error(f"Error learning from aggressive decision: {e}")
            return None
    
    def _generate_profit_report(self, trading_stats: Dict[str, Any], results: BacktestResults) -> Dict[str, Any]:
        """Generate comprehensive profit report"""
        try:
            # Get learning metrics
            metrics = self.learning_engine.get_learning_metrics()
            
            report = {
                "aggressive_trading_summary": {
                    "total_opportunities": trading_stats['total_opportunities'],
                    "trades_taken": trading_stats['trades_taken'],
                    "trade_participation_pct": trading_stats['trades_taken'] / trading_stats['total_opportunities'] * 100,
                    "max_positions_held": trading_stats['max_positions_held'],
                    "avg_holding_period": trading_stats['avg_holding_period']
                },
                "profitability_metrics": {
                    "win_rate": trading_stats['win_rate'],
                    "profitable_trades": trading_stats['profitable_trades'],
                    "losing_trades": trading_stats['losing_trades'],
                    "total_profit": trading_stats['total_profit'],
                    "total_loss": trading_stats['total_loss'],
                    "net_profit": trading_stats['total_profit'] - trading_stats['total_loss'],
                    "profit_factor": trading_stats['profit_factor']
                },
                "backtest_performance": {
                    "initial_capital": results.initial_capital,
                    "final_capital": results.final_capital,
                    "total_return": results.total_return,
                    "total_return_pct": results.total_return_pct,
                    "max_drawdown": results.max_drawdown,
                    "sharpe_ratio": results.sharpe_ratio
                },
                "learning_system": {
                    "model_version": self.learning_engine.model_version,
                    "learning_events": len(trading_stats['learning_events']),
                    "accuracy_rate": metrics.accuracy_rate if metrics else 0,
                    "learning_progress": metrics.learning_progress if metrics else 0
                },
                "adaptive_weights": self.learning_engine.learning_weights,
                "recommendations": self._generate_profit_recommendations(trading_stats, results),
                "generated_at": datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating profit report: {e}")
            return {"error": str(e)}
    
    def _generate_profit_recommendations(self, trading_stats: Dict[str, Any], results: BacktestResults) -> List[str]:
        """Generate profit-focused recommendations"""
        recommendations = []
        
        # Trade participation recommendations
        participation = trading_stats['trades_taken'] / trading_stats['total_opportunities'] * 100
        if participation > 70:
            recommendations.append("🚀 Excellent trade participation! System is actively engaging the market.")
        elif participation > 50:
            recommendations.append("⚡ Good trade participation. Consider being more aggressive for higher returns.")
        else:
            recommendations.append("🐢 Low trade participation. Reduce thresholds to generate more trades.")
        
        # Win rate recommendations
        if trading_stats['win_rate'] > 60:
            recommendations.append("🎉 Outstanding win rate! Current strategy is highly effective.")
        elif trading_stats['win_rate'] > 50:
            recommendations.append("✅ Good win rate. Strategy is working well.")
        elif trading_stats['win_rate'] > 40:
            recommendations.append("📊 Moderate win rate. Fine-tune entry criteria for better accuracy.")
        else:
            recommendations.append("⚠️ Low win rate. Review signal generation and market analysis.")
        
        # Profit factor recommendations
        if trading_stats['profit_factor'] > 2:
            recommendations.append("💰 Exceptional profit factor! Excellent risk/reward management.")
        elif trading_stats['profit_factor'] > 1.5:
            recommendations.append("💵 Strong profit factor. Positive trading expectancy.")
        elif trading_stats['profit_factor'] > 1:
            recommendations.append("📈 Positive profit factor. System is profitable.")
        else:
            recommendations.append("📉 Negative profit factor. Improve trade selection and risk management.")
        
        # Return recommendations
        if results.total_return_pct > 10:
            recommendations.append("🚀 Strong returns! System is generating significant profits.")
        elif results.total_return_pct > 5:
            recommendations.append("📈 Positive returns. Strategy is working.")
        elif results.total_return_pct > 0:
            recommendations.append("💡 Small positive returns. Room for improvement.")
        else:
            recommendations.append("⚠️ Negative returns. Review strategy and market conditions.")
        
        return recommendations

def main():
    """Main function to run aggressive profit backtesting"""
    try:
        print("💰 Aggressive Profit-Focused Backtesting System")
        print("=" * 70)
        
        # Initialize aggressive backtester
        aggressive_backtester = AggressiveProfitBacktester()
        
        # Run aggressive backtest
        results, profit_report = aggressive_backtester.run_aggressive_profit_backtest()
        
        # Save results
        with open('aggressive_profit_results.json', 'w') as f:
            json.dump(profit_report, f, indent=2, default=str)
        
        # Show recommendations
        if 'recommendations' in profit_report:
            print(f"\n💡 Profit-Focused Recommendations:")
            for i, rec in enumerate(profit_report['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        print(f"\n🎉 Aggressive Profit Backtesting Completed!")
        print(f"💰 Net Profit: ${profit_report['profitability_metrics']['net_profit']:.2f}")
        print(f"🎯 Win Rate: {profit_report['profitability_metrics']['win_rate']:.1f}%")
        print(f"📈 Trade Participation: {profit_report['aggressive_trading_summary']['trade_participation_pct']:.1f}%")
        print(f"📄 Results saved to 'aggressive_profit_results.json'")
        
        return aggressive_backtester, results
        
    except Exception as e:
        logger.error(f"Aggressive profit backtest failed: {e}")
        print(f"❌ Failed: {e}")
        return None, None

if __name__ == "__main__":
    main()
