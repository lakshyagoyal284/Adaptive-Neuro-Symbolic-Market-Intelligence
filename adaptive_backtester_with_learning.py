"""
Adaptive Backtester with LLM Learning System
This module combines real market backtesting with continuous learning from mistakes and rewards
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

class AdaptiveBacktesterWithLearning:
    """
    Advanced backtester that continuously learns from trading decisions
    """
    
    def __init__(self, data_directory: str = None):
        self.data_directory = data_directory or "c:\\Users\\laksh\\Desktop\\adaptive_market_intelligence"
        self.backtester = RealMarketBacktester(data_directory)
        self.learning_engine = LLMLearningEngine()
        self.learning_experiences = []
        self.adaptation_enabled = True
        
    def run_adaptive_backtest(self, enable_learning: bool = True) -> Tuple[BacktestResults, Dict[str, Any]]:
        """Run backtest with continuous learning from outcomes"""
        try:
            print("🚀 Running Adaptive Backtest with LLM Learning System")
            print("=" * 70)
            
            self.adaptation_enabled = enable_learning
            
            # Load market data
            print("📊 Loading real market data...")
            market_data = self.backtester.load_market_data()
            
            if not market_data:
                raise ValueError("No market data loaded")
            
            print(f"✅ Loaded {len(market_data)} symbols")
            
            # Initialize backtest
            self.backtester.current_capital = 100000
            self.backtester.positions = {}
            self.backtester.trades = []
            
            # Track learning progress
            learning_stats = {
                'total_decisions': 0,
                'correct_decisions': 0,
                'incorrect_decisions': 0,
                'learning_events': [],
                'adaptation_points': []
            }
            
            # Process each symbol with learning
            for symbol, df in market_data.items():
                print(f"\n🔄 Processing {symbol} with learning...")
                
                # Sample data points for performance
                df_sample = df.copy()
                
                for i in range(0, len(df_sample), 50):  # Every 50th point
                    current_row = df_sample.iloc[i]
                    current_time = current_row['date']
                    current_price = current_row['close']
                    
                    # Get adaptive weights from learning engine
                    context = self._extract_context(current_row, df_sample, i)
                    adaptive_weights = self.learning_engine.get_adaptive_decision_weights(context)
                    
                    # Generate trading signal with adaptive weights
                    signal = self._generate_adaptive_signal(symbol, df_sample, i, adaptive_weights)
                    
                    # Execute trade
                    old_capital = self.backtester.current_capital
                    self.backtester.execute_trade(symbol, signal, current_price, current_time)
                    
                    # Learn from the decision if enabled
                    if enable_learning and signal["signal"] != "hold":
                        learning_result = self._learn_from_decision(
                            symbol, signal, current_price, current_time, context, df_sample, i
                        )
                        
                        if learning_result:
                            learning_stats['total_decisions'] += 1
                            if learning_result.outcome == DecisionOutcome.CORRECT:
                                learning_stats['correct_decisions'] += 1
                            else:
                                learning_stats['incorrect_decisions'] += 1
                            
                            learning_stats['learning_events'].append({
                                'timestamp': current_time.isoformat(),
                                'symbol': symbol,
                                'decision': signal["signal"],
                                'outcome': learning_result.outcome.value,
                                'reward': learning_result.reward,
                                'punishment': learning_result.punishment
                            })
                    
                    # Periodic adaptation
                    if i % 500 == 0 and enable_learning:
                        self._trigger_adaptation(symbol, learning_stats)
            
            # Close remaining positions
            for symbol in list(self.backtester.positions.keys()):
                position = self.backtester.positions[symbol]
                self.backtester.execute_trade(symbol, {"signal": "sell"}, position['entry_price'], datetime.now())
            
            # Calculate results
            results = self.backtester.calculate_results()
            
            # Generate learning report
            learning_report = self._generate_learning_report(learning_stats)
            
            print(f"\n📈 BACKTEST RESULTS")
            print("=" * 50)
            print(f"Initial Capital: ${results.initial_capital:,.2f}")
            print(f"Final Capital: ${results.final_capital:,.2f}")
            print(f"Total Return: {results.total_return_pct:.2f}%")
            print(f"Total Trades: {results.total_trades}")
            print(f"Win Rate: {results.win_rate:.2f}%")
            
            print(f"\n🧠 LEARNING RESULTS")
            print("=" * 50)
            print(f"Total Learning Events: {learning_stats['total_decisions']}")
            print(f"Correct Decisions: {learning_stats['correct_decisions']}")
            print(f"Incorrect Decisions: {learning_stats['incorrect_decisions']}")
            
            if learning_stats['total_decisions'] > 0:
                learning_accuracy = learning_stats['correct_decisions'] / learning_stats['total_decisions'] * 100
                print(f"Learning Accuracy: {learning_accuracy:.2f}%")
            
            return results, learning_report
            
        except Exception as e:
            logger.error(f"Adaptive backtest failed: {e}")
            raise
    
    def _extract_context(self, current_row: pd.Series, df: pd.DataFrame, index: int) -> Dict[str, float]:
        """Extract market context for learning"""
        try:
            context = {}
            
            # Basic market metrics
            context['market_growth'] = current_row.get('price_change_pct', 0)
            context['sentiment_score'] = np.clip(context['market_growth'] / 100, -1, 1)
            context['market_volatility'] = current_row.get('volatility', 20)
            
            # Trend indicators
            if index > 20:
                recent_changes = df['price_change_pct'].iloc[index-20:index].mean()
                context['trend_demand'] = max(0, recent_changes + 50)
            
            # Volume analysis
            volume_ratio = current_row.get('volume_ratio', 1.0)
            context['volume_activity'] = min(100, volume_ratio * 50)
            
            # RSI-based sentiment
            rsi = current_row.get('rsi', 50)
            context['negative_sentiment'] = max(0, (100 - rsi) / 100 * 100)
            context['positive_sentiment'] = max(0, rsi / 100 * 100)
            
            # Simulated market conditions
            context['competitor_price_increase'] = np.random.uniform(0, 25)
            context['market_share'] = np.random.uniform(10, 35)
            context['competitor_activity_count'] = np.random.randint(1, 10)
            
            return context
            
        except Exception as e:
            logger.error(f"Error extracting context: {e}")
            return {}
    
    def _generate_adaptive_signal(self, symbol: str, df: pd.DataFrame, index: int, adaptive_weights: Dict[str, float]) -> Dict[str, Any]:
        """Generate trading signal using adaptive weights"""
        try:
            if index < 50:
                return {"signal": "hold", "confidence": 0.5}
            
            current_data = df.iloc[index]
            
            # Create weighted context
            context = self._extract_context(current_data, df, index)
            
            # Apply adaptive weights to context
            weighted_context = {}
            for key, value in context.items():
                weight_key = f"{key}_weight"
                if weight_key in adaptive_weights:
                    weighted_context[key] = value * adaptive_weights[weight_key]
                else:
                    weighted_context[key] = value
            
            # Generate AI insights with adaptive context
            ai_insights = {
                'sentiment_analysis': {
                    'average_sentiment': weighted_context.get('sentiment_score', 0),
                    'overall_trend': 'improving' if weighted_context.get('sentiment_score', 0) > 0 else 'declining'
                },
                'trend_analysis': {
                    'volatility': weighted_context.get('market_volatility', 20) / 100,
                    'growth_rate': weighted_context.get('market_growth', 0)
                }
            }
            
            # Make decisions with adaptive context
            decisions = self.backtester.decision_engine.make_decision(weighted_context, ai_insights)
            
            if not decisions:
                return {"signal": "hold", "confidence": 0.5}
            
            # Apply rule confidence adjustments
            adjusted_decisions = []
            for decision in decisions:
                if hasattr(decision, 'decision_type'):
                    rule_id = decision.decision_type.value
                    confidence_adj = self.learning_engine.get_rule_confidence_adjustment(rule_id)
                    
                    # Adjust decision confidence
                    if hasattr(decision, 'confidence_score'):
                        original_confidence = decision.confidence_score
                        decision.confidence_score = min(1.0, original_confidence * confidence_adj)
                
                adjusted_decisions.append(decision)
            
            # Determine signal from adjusted decisions
            buy_signals = sum(1 for d in adjusted_decisions if hasattr(d, 'decision_type') and 
                           d.decision_type.value in ['investment', 'opportunity'])
            sell_signals = sum(1 for d in adjusted_decisions if hasattr(d, 'decision_type') and 
                            d.decision_type.value in ['risk_management'])
            
            # Calculate average confidence
            total_confidence = sum(getattr(d, 'confidence_score', 0.5) for d in adjusted_decisions if hasattr(d, 'confidence_score'))
            avg_confidence = total_confidence / len(adjusted_decisions) if adjusted_decisions else 0.5
            
            # Determine signal
            if buy_signals > sell_signals and buy_signals > 0:
                return {"signal": "buy", "confidence": avg_confidence, "decisions": adjusted_decisions}
            elif sell_signals > buy_signals and sell_signals > 0:
                return {"signal": "sell", "confidence": avg_confidence, "decisions": adjusted_decisions}
            else:
                return {"signal": "hold", "confidence": avg_confidence}
                
        except Exception as e:
            logger.error(f"Error generating adaptive signal: {e}")
            return {"signal": "hold", "confidence": 0.5}
    
    def _learn_from_decision(self, symbol: str, signal: Dict[str, Any], entry_price: float, 
                           entry_time: datetime, context: Dict[str, float], 
                           df: pd.DataFrame, index: int) -> Optional[Any]:
        """Learn from trading decision outcome"""
        try:
            # Simulate outcome (in real system, this would come from actual market movement)
            if index + 100 < len(df):
                future_price = df.iloc[index + 100]['close']
                price_change = (future_price - entry_price) / entry_price * 100
            else:
                # Use last available price if can't look ahead
                future_price = df.iloc[-1]['close']
                price_change = (future_price - entry_price) / entry_price * 100
            
            # Create experience for learning
            experience = self.learning_engine.analyze_decision_outcome(
                context=context,
                decision_type="trading",
                action_taken=signal["signal"],
                confidence=signal.get("confidence", 0.5),
                market_state={"symbol": symbol, "entry_price": entry_price},
                technical_indicators={
                    'rsi': df.iloc[index].get('rsi', 50),
                    'ma_20': df.iloc[index].get('ma_20', entry_price),
                    'ma_50': df.iloc[index].get('ma_50', entry_price)
                },
                rule_triggers=[d.decision_type.value for d in signal.get('decisions', []) if hasattr(d, 'decision_type')],
                actual_result=price_change,
                expected_result=5.0 if signal["signal"] == "buy" else -5.0 if signal["signal"] == "sell" else 0.0
            )
            
            if experience:
                self.learning_engine.learn_from_experience(experience)
                self.learning_experiences.append(experience)
                
                return experience
            
            return None
            
        except Exception as e:
            logger.error(f"Error learning from decision: {e}")
            return None
    
    def _trigger_adaptation(self, symbol: str, learning_stats: Dict[str, Any]):
        """Trigger model adaptation"""
        try:
            if len(self.learning_experiences) % 20 == 0:  # Adapt every 20 experiences
                self.learning_engine.trigger_model_update()
                
                learning_stats['adaptation_points'].append({
                    'timestamp': datetime.now().isoformat(),
                    'symbol': symbol,
                    'model_version': self.learning_engine.model_version,
                    'total_experiences': len(self.learning_experiences)
                })
                
                print(f"  🔄 Model adapted to version {self.learning_engine.model_version}")
                
        except Exception as e:
            logger.error(f"Error triggering adaptation: {e}")
    
    def _generate_learning_report(self, learning_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive learning report"""
        try:
            # Get learning metrics
            metrics = self.learning_engine.get_learning_metrics()
            
            # Get learning engine report
            engine_report = self.learning_engine.export_learning_report()
            
            # Combine with backtest-specific stats
            report = {
                "backtest_learning_summary": {
                    "total_learning_events": learning_stats['total_decisions'],
                    "correct_decisions": learning_stats['correct_decisions'],
                    "incorrect_decisions": learning_stats['incorrect_decisions'],
                    "adaptation_points": learning_stats['adaptation_points'],
                    "learning_enabled": self.adaptation_enabled
                },
                "learning_engine_metrics": {
                    "model_version": self.learning_engine.model_version,
                    "total_experiences": len(self.learning_experiences),
                    "accuracy_rate": metrics.accuracy_rate if metrics else 0,
                    "learning_progress": metrics.learning_progress if metrics else 0,
                    "avg_reward": metrics.avg_reward if metrics else 0,
                    "avg_punishment": metrics.avg_punishment if metrics else 0
                },
                "rule_performance": engine_report.get('rule_performance', {}),
                "adaptive_weights": self.learning_engine.learning_weights,
                "learning_events": learning_stats['learning_events'][-10:],  # Last 10 events
                "recommendations": engine_report.get('recommendations', []),
                "generated_at": datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating learning report: {e}")
            return {"error": str(e)}
    
    def save_adaptive_results(self, results: BacktestResults, learning_report: Dict[str, Any]):
        """Save adaptive backtest results"""
        try:
            # Save backtest results
            backtest_data = {
                "initial_capital": results.initial_capital,
                "final_capital": results.final_capital,
                "total_return": results.total_return,
                "total_return_pct": results.total_return_pct,
                "max_drawdown": results.max_drawdown,
                "sharpe_ratio": results.sharpe_ratio,
                "win_rate": results.win_rate,
                "total_trades": results.total_trades,
                "avg_win": results.avg_win,
                "avg_loss": results.avg_loss,
                "profit_factor": results.profit_factor,
                "learning_enabled": self.adaptation_enabled,
                "generated_at": datetime.now().isoformat()
            }
            
            with open('adaptive_backtest_results.json', 'w') as f:
                json.dump(backtest_data, f, indent=2, default=str)
            
            # Save learning report
            with open('adaptive_learning_report.json', 'w') as f:
                json.dump(learning_report, f, indent=2, default=str)
            
            print(f"✅ Results saved to 'adaptive_backtest_results.json'")
            print(f"✅ Learning report saved to 'adaptive_learning_report.json'")
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")

def main():
    """Main function to run adaptive backtesting"""
    try:
        print("🧠 Adaptive Backtesting with LLM Learning System")
        print("=" * 70)
        
        # Initialize adaptive backtester
        adaptive_backtester = AdaptiveBacktesterWithLearning()
        
        # Run backtest with learning enabled
        print("\n🚀 Running Backtest WITH Learning...")
        results_with_learning, learning_report = adaptive_backtester.run_adaptive_backtest(enable_learning=True)
        
        # Save results
        adaptive_backtester.save_adaptive_results(results_with_learning, learning_report)
        
        # Show learning insights
        if 'recommendations' in learning_report:
            print(f"\n💡 Learning Recommendations:")
            for i, rec in enumerate(learning_report['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        # Show adaptive weights
        if 'adaptive_weights' in learning_report:
            print(f"\n⚖️ Final Adaptive Weights:")
            weights = learning_report['adaptive_weights']
            for feature, weight in weights.items():
                print(f"  {feature}: {weight:.3f}")
        
        print(f"\n🎉 Adaptive Backtesting Completed!")
        print(f"📊 Model Version: {adaptive_backtester.learning_engine.model_version}")
        print(f"🧠 Total Learning Experiences: {len(adaptive_backtester.learning_experiences)}")
        
        return adaptive_backtester, results_with_learning
        
    except Exception as e:
        logger.error(f"Adaptive backtest failed: {e}")
        print(f"❌ Failed: {e}")
        return None, None

if __name__ == "__main__":
    main()
