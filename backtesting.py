"""
Backtesting Module for Adaptive Neuro-Symbolic Market Intelligence System
This module provides comprehensive backtesting capabilities for the system
WITH SECURITY GUARD PROTECTION AGAINST BIASING AND CHEATING
"""

import numpy as np
import pandas as pd
import logging
import os
import threading
import hashlib
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple
import json
from dataclasses import dataclass
from enum import Enum

# Configure comprehensive logging
def setup_comprehensive_logger():
    """Setup comprehensive logging system"""
    # Create logs directory if not exists
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Setup file logger for backtesting
    log_filename = f"logs/backtesting_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

logger = setup_comprehensive_logger()

class SecurityGuard:
    """Security guard to prevent biasing and cheating during backtesting"""
    
    def __init__(self):
        self.baseline_weights = None
        self.baseline_learning_rate = None
        self.threats_detected = []
        self.lock = threading.Lock()
        self._establish_baseline()
    
    def _establish_baseline(self):
        """Establish baseline values for security monitoring"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            engine = LLMLearningEngine()
            self.baseline_weights = engine.learning_weights.copy()
            self.baseline_learning_rate = engine.learning_rate
            logger.info("🔒 Security baseline established")
        except Exception as e:
            logger.error(f"❌ Error establishing baseline: {e}")
    
    def check_weight_bias(self) -> bool:
        """Check for weight biasing"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            engine = LLMLearningEngine()
            weights = engine.learning_weights
            
            # Check for extreme concentration
            max_weight = max(weights.values())
            min_weight = min(weights.values())
            weight_ratio = max_weight / min_weight if min_weight > 0 else float('inf')
            
            if weight_ratio > 10:  # More than 10:1 ratio
                logger.warning(f"🚨 WEIGHT BIAS DETECTED: ratio {weight_ratio:.2f}")
                return False
            
            # Check for zero weights
            zero_weights = [k for k, v in weights.items() if v < 0.01]
            if zero_weights:
                logger.warning(f"🚨 ZERO WEIGHTS DETECTED: {zero_weights}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error checking weight bias: {e}")
            return False
    
    def check_parameter_tampering(self) -> bool:
        """Check for parameter tampering"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            engine = LLMLearningEngine()
            
            # Check learning rate
            if engine.learning_rate > 0.2:  # More than 0.2 is suspicious
                logger.warning(f"🚨 LEARNING RATE TAMPERING: {engine.learning_rate}")
                return False
            
            # Check reward/punishment scales
            if engine.reward_scale > 3.0 or engine.punishment_scale > 5.0:
                logger.warning(f"🚨 REWARD/PUNISHMENT TAMPERING")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error checking parameter tampering: {e}")
            return False
    
    def check_result_validity(self, result) -> bool:
        """Check result validity"""
        try:
            if not result:
                return False
            
            # Check for reasonable returns
            if 'total_return' in result:
                total_return = result['total_return']
                if abs(total_return) > 100:  # More than 100% is suspicious
                    logger.warning(f"🚨 UNUSUAL RETURN: {total_return}%")
                    return False
            
            # Check for reasonable win rate
            if 'win_rate' in result:
                win_rate = result['win_rate']
                if win_rate > 95:  # More than 95% is suspicious
                    logger.warning(f"🚨 UNUSUAL WIN RATE: {win_rate}%")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error checking result validity: {e}")
            return False

# Global security guard instance
security_guard = SecurityGuard()

class BacktestResult(Enum):
    """Enumeration of backtest result types"""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"

@dataclass
class BacktestMetrics:
    """Data class for backtest performance metrics"""
    total_decisions: int
    successful_decisions: int
    failed_decisions: int
    success_rate: float
    avg_confidence: float
    total_return: float
    max_drawdown: float
    sharpe_ratio: float
    win_rate: float
    avg_win: float
    avg_loss: float
    profit_factor: float
    total_trades: int
    winning_trades: int
    losing_trades: int

class MarketBacktester:
    """
    Comprehensive backtesting system for market intelligence decisions
    """
    
    def __init__(self):
        self.decision_history = []
        self.market_data_history = []
        self.portfolio_value = []
        self.trades = []
        self.metrics = None
        
        # Setup detailed logging for this instance
        self.setup_instance_logging()
        
    def setup_instance_logging(self):
        """Setup instance-specific logging"""
        self.log_start_time = datetime.now()
        logger.info("=" * 80)
        logger.info(f"MARKET BACKTESTER INITIALIZED")
        logger.info(f"Start Time: {self.log_start_time}")
        logger.info(f"Instance ID: {id(self)}")
        logger.info("=" * 80)
        
    def log_test_start(self, test_name: str, parameters: Dict = None):
        """Log the start of a test with all parameters"""
        logger.info(f"\n{'='*60}")
        logger.info(f"TEST STARTED: {test_name}")
        logger.info(f"Timestamp: {datetime.now()}")
        if parameters:
            logger.info("PARAMETERS:")
            for key, value in parameters.items():
                logger.info(f"  {key}: {value}")
        logger.info(f"{'='*60}")
        
    def log_decision_made(self, decision_data: Dict):
        """Log every decision made during testing"""
        logger.info(f"DECISION MADE:")
        for key, value in decision_data.items():
            logger.info(f"  {key}: {value}")
            
    def log_trade_executed(self, trade_data: Dict):
        """Log every trade executed"""
        logger.info(f"TRADE EXECUTED:")
        for key, value in trade_data.items():
            logger.info(f"  {key}: {value}")
            
    def log_market_data_point(self, data_point: Dict):
        """Log market data points"""
        logger.debug(f"MARKET DATA: {data_point}")
        
    def log_performance_update(self, current_capital: float, trade_count: int, win_rate: float):
        """Log performance updates"""
        logger.info(f"PERFORMANCE UPDATE:")
        logger.info(f"  Current Capital: ${current_capital:,.2f}")
        logger.info(f"  Trade Count: {trade_count}")
        logger.info(f"  Win Rate: {win_rate:.2f}%")
        
    def log_error(self, error_type: str, error_message: str, context: Dict = None):
        """Log errors with full context"""
        logger.error(f"ERROR - {error_type}: {error_message}")
        if context:
            logger.error(f"CONTEXT: {context}")
            
    def log_test_completion(self, test_name: str, results: Dict):
        """Log test completion with full results"""
        logger.info(f"\n{'='*60}")
        logger.info(f"TEST COMPLETED: {test_name}")
        logger.info(f"Timestamp: {datetime.now()}")
        logger.info("FINAL RESULTS:")
        for key, value in results.items():
            if isinstance(value, float):
                logger.info(f"  {key}: {value:.4f}")
            else:
                logger.info(f"  {key}: {value}")
        logger.info(f"{'='*60}\n")
        
    def save_detailed_log(self, test_name: str, all_data: Dict):
        """Save detailed log to separate file"""
        log_filename = f"logs/detailed_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(log_filename, 'w') as f:
                json.dump(all_data, f, indent=2, default=str)
            logger.info(f"Detailed log saved to: {log_filename}")
        except Exception as e:
            logger.error(f"Failed to save detailed log: {e}")
        
    def generate_historical_data(self, days: int = 365) -> List[Dict]:
        """Generate synthetic historical market data for backtesting"""
        try:
            logger.info(f"Generating {days} days of historical market data...")
            
            historical_data = []
            base_date = datetime.now() - timedelta(days=days)
            
            # Generate realistic market data with trends and volatility
            for i in range(days):
                current_date = base_date + timedelta(days=i)
                
                # Simulate market conditions with some randomness
                market_growth = np.random.normal(0, 2)  # Daily growth with volatility
                sentiment_score = np.random.normal(0, 0.3)  # Sentiment with noise
                market_volatility = abs(np.random.normal(15, 10))  # Volatility
                
                # Add some trend and seasonality
                trend_factor = np.sin(i / 30) * 5  # Monthly cycle
                market_growth += trend_factor
                
                # Create market data point
                data_point = {
                    'date': current_date,
                    'market_growth': round(market_growth, 2),
                    'sentiment_score': round(np.clip(sentiment_score, -1, 1), 3),
                    'market_volatility': round(market_volatility, 2),
                    'negative_sentiment': max(0, (1 - sentiment_score) * 100),
                    'trend_demand': round(np.random.uniform(30, 90), 1),
                    'competitor_price_increase': round(np.random.uniform(0, 20), 1),
                    'market_share': round(np.random.uniform(10, 30), 1),
                    'competitor_activity_count': np.random.randint(1, 10)
                }
                
                historical_data.append(data_point)
            
            logger.info(f"Generated {len(historical_data)} historical data points")
            return historical_data
            
        except Exception as e:
            logger.error(f"Error generating historical data: {e}")
            return []
    
    def simulate_decision_execution(self, context: Dict, decision_type: str) -> Dict:
        """Simulate the outcome of a decision based on historical context"""
        try:
            # Simulate decision execution with realistic outcomes
            base_success_prob = 0.6
            
            # Adjust success probability based on market conditions
            if context.get('market_growth', 0) > 20:
                base_success_prob += 0.2
            elif context.get('market_growth', 0) < -10:
                base_success_prob -= 0.2
            
            if context.get('sentiment_score', 0) > 0.3:
                base_success_prob += 0.15
            elif context.get('sentiment_score', 0) < -0.3:
                base_success_prob -= 0.15
            
            if context.get('market_volatility', 0) > 25:
                base_success_prob -= 0.1
            
            # Ensure probability stays within bounds
            base_success_prob = np.clip(base_success_prob, 0.1, 0.9)
            
            # Determine success
            is_successful = np.random.random() < base_success_prob
            
            # Calculate return based on decision type and market conditions
            if decision_type == "investment":
                if is_successful:
                    return_rate = np.random.uniform(5, 25)  # 5-25% return
                else:
                    return_rate = np.random.uniform(-15, -5)  # -15 to -5% loss
            elif decision_type == "marketing":
                if is_successful:
                    return_rate = np.random.uniform(2, 10)  # 2-10% improvement
                else:
                    return_rate = np.random.uniform(-8, -2)  # -8 to -2% loss
            elif decision_type == "opportunity":
                if is_successful:
                    return_rate = np.random.uniform(10, 30)  # 10-30% return
                else:
                    return_rate = np.random.uniform(-20, -10)  # -20 to -10% loss
            else:
                # Default for other decision types
                if is_successful:
                    return_rate = np.random.uniform(3, 15)
                else:
                    return_rate = np.random.uniform(-10, -3)
            
            return {
                'success': is_successful,
                'return_rate': round(return_rate, 2),
                'confidence': base_success_prob,
                'decision_type': decision_type,
                'execution_time': datetime.now()
            }
            
        except Exception as e:
            logger.error(f"Error simulating decision execution: {e}")
            return {'success': False, 'return_rate': 0, 'confidence': 0}
    
    def run_backtest(self, days: int = 365, initial_capital: float = 10000) -> BacktestMetrics:
        """Run comprehensive backtest simulation"""
        try:
            # Log test start with all parameters
            test_params = {
                'days': days,
                'initial_capital': initial_capital,
                'test_type': 'comprehensive_backtest'
            }
            self.log_test_start("COMPREHENSIVE BACKTEST", test_params)
            
            logger.info(f"Starting backtest for {days} days with ${initial_capital:,.2f} initial capital")
            
            # Generate historical data
            historical_data = self.generate_historical_data(days)
            
            if not historical_data:
                raise ValueError("No historical data generated")
            
            # Initialize backtracking variables
            current_capital = initial_capital
            portfolio_values = [initial_capital]
            decisions = []
            trades = []
            
            # Import system components
            from symbolic_engine.decision_engine import DecisionEngine
            from symbolic_engine.rules import RuleEngine
            from adaptive_module.learning import AdaptiveLearningEngine
            
            decision_engine = DecisionEngine()
            learning_engine = AdaptiveLearningEngine()
            
            # Run backtest day by day
            for i, data_point in enumerate(historical_data):
                try:
                    # Every 7 days, make decisions
                    if i % 7 == 0:
                        # Create context for decision making
                        context = {
                            'market_growth': data_point['market_growth'],
                            'sentiment_score': data_point['sentiment_score'],
                            'negative_sentiment': data_point['negative_sentiment'],
                            'trend_demand': data_point['trend_demand'],
                            'market_volatility': data_point['market_volatility']
                        }
                        
                        # Generate AI insights
                        ai_insights = {
                            'sentiment_analysis': {
                                'average_sentiment': data_point['sentiment_score'],
                                'overall_trend': 'improving' if data_point['sentiment_score'] > 0 else 'declining'
                            },
                            'trend_analysis': {
                                'volatility': data_point['market_volatility'] / 100,
                                'growth_rate': data_point['market_growth']
                            }
                        }
                        
                        # Make decisions
                        daily_decisions = decision_engine.make_decision(context, ai_insights)
                        
                        # Log decisions made
                        if daily_decisions:
                            decision_data = {
                                'date': data_point['date'],
                                'num_decisions': len(daily_decisions),
                                'market_growth': context['market_growth'],
                                'sentiment_score': context['sentiment_score']
                            }
                            self.log_decision_made(decision_data)
                        
                        # Execute decisions and track performance
                        for decision in daily_decisions:
                            if hasattr(decision, 'decision_type'):
                                # Simulate decision execution
                                execution_result = self.simulate_decision_execution(
                                    context, decision.decision_type.value
                                )
                                
                                # Calculate capital change
                                capital_change = current_capital * (execution_result['return_rate'] / 100)
                                current_capital += capital_change
                                
                                # Record trade
                                trade = {
                                    'date': data_point['date'],
                                    'decision_type': decision.decision_type.value,
                                    'decision_title': decision.title,
                                    'return_rate': execution_result['return_rate'],
                                    'capital_change': capital_change,
                                    'capital_before': current_capital - capital_change,
                                    'capital_after': current_capital,
                                    'success': execution_result['success'],
                                    'confidence': execution_result['confidence']
                                }
                                trades.append(trade)
                                
                                # Log trade executed
                                self.log_trade_executed(trade)
                                
                                # Log performance update
                                win_rate = len([t for t in trades if t['success']]) / len(trades) * 100 if trades else 0
                                self.log_performance_update(current_capital, len(trades), win_rate)
                                
                                # Record decision
                                decisions.append({
                                    'date': data_point['date'],
                                    'decision': decision,
                                    'execution': execution_result
                                })
                    
                    # Record portfolio value
                    portfolio_values.append(current_capital)
                    
                except Exception as e:
                    logger.error(f"Error processing day {i}: {e}")
                    portfolio_values.append(current_capital)
                    continue
            
            # Calculate backtest metrics
            metrics = self._calculate_metrics(
                decisions, trades, portfolio_values, initial_capital
            )
            
            self.decision_history = decisions
            self.trades = trades
            self.portfolio_value = portfolio_values
            self.metrics = metrics
            
            # Log final results
            final_results = {
                'final_capital': current_capital,
                'total_return': metrics.total_return,
                'success_rate': metrics.success_rate,
                'total_trades': metrics.total_trades,
                'win_rate': metrics.win_rate,
                'profit_factor': metrics.profit_factor,
                'sharpe_ratio': metrics.sharpe_ratio,
                'max_drawdown': metrics.max_drawdown
            }
            self.log_test_completion("COMPREHENSIVE BACKTEST", final_results)
            
            # Save detailed log
            all_data = {
                'test_parameters': test_params,
                'decisions': decisions,
                'trades': trades,
                'portfolio_values': portfolio_values,
                'metrics': metrics.__dict__,
                'final_results': final_results
            }
            self.save_detailed_log("comprehensive_backtest", all_data)
            
            logger.info(f"Backtest completed. Final capital: ${current_capital:,.2f}")
            logger.info(f"Total return: {metrics.total_return:.2f}%")
            logger.info(f"Success rate: {metrics.success_rate:.2f}%")
            
            return metrics
            
        except Exception as e:
            logger.error(f"Backtest failed: {e}")
            raise
    
    def _calculate_metrics(self, decisions: List[Dict], trades: List[Dict], 
                          portfolio_values: List[float], initial_capital: float) -> BacktestMetrics:
        """Calculate comprehensive backtest metrics"""
        try:
            if not trades:
                # Return default metrics if no trades
                return BacktestMetrics(
                    total_decisions=0, successful_decisions=0, failed_decisions=0,
                    success_rate=0, avg_confidence=0, total_return=0, max_drawdown=0,
                    sharpe_ratio=0, win_rate=0, avg_win=0, avg_loss=0, profit_factor=0,
                    total_trades=0, winning_trades=0, losing_trades=0
                )
            
            # Basic metrics
            total_decisions = len(decisions)
            successful_decisions = sum(1 for d in decisions if d.get('execution', {}).get('success', False))
            failed_decisions = total_decisions - successful_decisions
            success_rate = (successful_decisions / total_decisions * 100) if total_decisions > 0 else 0
            
            avg_confidence = np.mean([d.get('execution', {}).get('confidence', 0) for d in decisions])
            
            # Portfolio metrics
            final_capital = portfolio_values[-1] if portfolio_values else initial_capital
            total_return = ((final_capital - initial_capital) / initial_capital * 100)
            
            # Calculate maximum drawdown
            peak = initial_capital
            max_drawdown = 0
            for value in portfolio_values:
                if value > peak:
                    peak = value
                drawdown = (peak - value) / peak * 100
                max_drawdown = max(max_drawdown, drawdown)
            
            # Calculate Sharpe ratio (simplified)
            if len(portfolio_values) > 1:
                returns = np.diff(portfolio_values) / portfolio_values[:-1]
                sharpe_ratio = np.mean(returns) / np.std(returns) * np.sqrt(252) if np.std(returns) > 0 else 0
            else:
                sharpe_ratio = 0
            
            # Trade metrics
            total_trades = len(trades)
            winning_trades = sum(1 for t in trades if t.get('success', False))
            losing_trades = total_trades - winning_trades
            win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
            
            # Calculate average win/loss
            winning_returns = [t['return_rate'] for t in trades if t.get('success', False)]
            losing_returns = [t['return_rate'] for t in trades if not t.get('success', False)]
            
            avg_win = np.mean(winning_returns) if winning_returns else 0
            avg_loss = np.mean(losing_returns) if losing_returns else 0
            
            # Calculate profit factor
            total_wins = sum(winning_returns) if winning_returns else 0
            total_losses = abs(sum(losing_returns)) if losing_returns else 1
            profit_factor = total_wins / total_losses if total_losses > 0 else 0
            
            return BacktestMetrics(
                total_decisions=total_decisions,
                successful_decisions=successful_decisions,
                failed_decisions=failed_decisions,
                success_rate=success_rate,
                avg_confidence=avg_confidence,
                total_return=total_return,
                max_drawdown=max_drawdown,
                sharpe_ratio=sharpe_ratio,
                win_rate=win_rate,
                avg_win=avg_win,
                avg_loss=avg_loss,
                profit_factor=profit_factor,
                total_trades=total_trades,
                winning_trades=winning_trades,
                losing_trades=losing_trades
            )
            
        except Exception as e:
            logger.error(f"Error calculating metrics: {e}")
            return BacktestMetrics(
                total_decisions=0, successful_decisions=0, failed_decisions=0,
                success_rate=0, avg_confidence=0, total_return=0, max_drawdown=0,
                sharpe_ratio=0, win_rate=0, avg_win=0, avg_loss=0, profit_factor=0,
                total_trades=0, winning_trades=0, losing_trades=0
            )
    
    def generate_backtest_report(self) -> Dict[str, Any]:
        """Generate comprehensive backtest report"""
        try:
            if not self.metrics:
                return {"error": "No backtest data available. Run backtest first."}
            
            report = {
                "backtest_summary": {
                    "initial_capital": 10000,
                    "final_capital": self.portfolio_value[-1] if self.portfolio_value else 10000,
                    "total_return": self.metrics.total_return,
                    "max_drawdown": self.metrics.max_drawdown,
                    "sharpe_ratio": self.metrics.sharpe_ratio,
                    "backtest_period": f"{len(self.portfolio_value)} days"
                },
                "decision_metrics": {
                    "total_decisions": self.metrics.total_decisions,
                    "successful_decisions": self.metrics.successful_decisions,
                    "failed_decisions": self.metrics.failed_decisions,
                    "success_rate": self.metrics.success_rate,
                    "avg_confidence": self.metrics.avg_confidence
                },
                "trade_metrics": {
                    "total_trades": self.metrics.total_trades,
                    "winning_trades": self.metrics.winning_trades,
                    "losing_trades": self.metrics.losing_trades,
                    "win_rate": self.metrics.win_rate,
                    "avg_win": self.metrics.avg_win,
                    "avg_loss": self.metrics.avg_loss,
                    "profit_factor": self.metrics.profit_factor
                },
                "performance_analysis": self._analyze_performance(),
                "recommendations": self._generate_recommendations(),
                "detailed_trades": self.trades[:10],  # First 10 trades
                "generated_at": datetime.now().isoformat()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error generating backtest report: {e}")
            return {"error": str(e)}
    
    def _analyze_performance(self) -> Dict[str, Any]:
        """Analyze performance patterns"""
        try:
            if not self.trades:
                return {}
            
            # Analyze performance by decision type
            performance_by_type = {}
            for trade in self.trades:
                decision_type = trade.get('decision_type', 'unknown')
                if decision_type not in performance_by_type:
                    performance_by_type[decision_type] = {
                        'trades': 0,
                        'wins': 0,
                        'total_return': 0,
                        'avg_return': 0
                    }
                
                performance_by_type[decision_type]['trades'] += 1
                performance_by_type[decision_type]['total_return'] += trade.get('return_rate', 0)
                if trade.get('success', False):
                    performance_by_type[decision_type]['wins'] += 1
            
            # Calculate averages
            for decision_type, data in performance_by_type.items():
                if data['trades'] > 0:
                    data['avg_return'] = data['total_return'] / data['trades']
                    data['win_rate'] = (data['wins'] / data['trades']) * 100
            
            # Analyze monthly performance
            monthly_performance = {}
            for trade in self.trades:
                trade_date = trade.get('date')
                if isinstance(trade_date, str):
                    trade_date = datetime.fromisoformat(trade_date.replace('Z', '+00:00'))
                
                month_key = trade_date.strftime('%Y-%m')
                if month_key not in monthly_performance:
                    monthly_performance[month_key] = {'returns': [], 'count': 0}
                
                monthly_performance[month_key]['returns'].append(trade.get('return_rate', 0))
                monthly_performance[month_key]['count'] += 1
            
            # Calculate monthly averages
            for month, data in monthly_performance.items():
                if data['returns']:
                    data['avg_return'] = np.mean(data['returns'])
                    data['total_return'] = np.sum(data['returns'])
            
            return {
                'performance_by_decision_type': performance_by_type,
                'monthly_performance': monthly_performance
            }
            
        except Exception as e:
            logger.error(f"Error analyzing performance: {e}")
            return {}
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations based on backtest results"""
        try:
            recommendations = []
            
            if not self.metrics:
                return ["No recommendations available - run backtest first"]
            
            # Success rate recommendations
            if self.metrics.success_rate < 50:
                recommendations.append("Consider reviewing and optimizing decision rules - success rate is below 50%")
            elif self.metrics.success_rate > 75:
                recommendations.append("Excellent success rate! Consider scaling up the strategy")
            
            # Risk recommendations
            if self.metrics.max_drawdown > 20:
                recommendations.append("High maximum drawdown detected - consider implementing risk management")
            elif self.metrics.max_drawdown < 5:
                recommendations.append("Low drawdown - good risk management")
            
            # Return recommendations
            if self.metrics.total_return < 0:
                recommendations.append("Negative returns - strategy needs optimization")
            elif self.metrics.total_return > 20:
                recommendations.append("Strong positive returns - strategy is performing well")
            
            # Sharpe ratio recommendations
            if self.metrics.sharpe_ratio < 1:
                recommendations.append("Low Sharpe ratio - improve risk-adjusted returns")
            elif self.metrics.sharpe_ratio > 2:
                recommendations.append("Excellent risk-adjusted returns")
            
            # Win rate recommendations
            if self.metrics.win_rate < 40:
                recommendations.append("Low win rate - review entry/exit criteria")
            elif self.metrics.win_rate > 60:
                recommendations.append("Good win rate - strategy is effective")
            
            # Profit factor recommendations
            if self.metrics.profit_factor < 1:
                recommendations.append("Profit factor below 1 - losing more than winning")
            elif self.metrics.profit_factor > 2:
                recommendations.append("Excellent profit factor - strategy is profitable")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Error generating recommendations"]

# Main backtesting function
def run_comprehensive_backtest():
    """Run comprehensive backtesting demonstration WITH SECURITY PROTECTION"""
    try:
        print("🧪 Adaptive Neuro-Symbolic Market Intelligence - Backtesting")
        print("🔒 SECURITY GUARD ACTIVE - Preventing biasing and cheating...")
        print("=" * 70)
        
        # PRE-SECURITY CHECKS
        print("\n🔒 PRE-SECURITY CHECKS:")
        if not security_guard.check_weight_bias():
            logger.error("❌ WEIGHT BIAS DETECTED - BACKTESTING BLOCKED")
            return
        if not security_guard.check_parameter_tampering():
            logger.error("❌ PARAMETER TAMPERING DETECTED - BACKTESTING BLOCKED")
            return
        
        print("✅ All security checks passed")
        
        # Initialize backtester
        backtester = MarketBacktester()
        
        # Run backtest with monitoring
        print("📊 Running secure backtest simulation...")
        metrics = backtester.run_backtest(days=365, initial_capital=10000)
        
        # Create result dictionary for validation
        result = {
            'total_return': metrics.total_return,
            'win_rate': metrics.win_rate,
            'sharpe_ratio': metrics.sharpe_ratio,
            'max_drawdown': metrics.max_drawdown,
            'total_trades': metrics.total_trades,
            'winning_trades': metrics.winning_trades,
            'losing_trades': metrics.losing_trades
        }
        
        # POST-SECURITY CHECKS
        print("\n🔒 POST-SECURITY CHECKS:")
        if not security_guard.check_result_validity(result):
            logger.error("❌ RESULT VALIDATION FAILED - RESULTS INVALID")
            return
        
        print("✅ Result validation passed")
        
        # Display results
        print("\n📈 Backtest Results:")
        print(f"Initial Capital: $10,000.00")
        print(f"Final Capital: ${backtester.portfolio_value[-1]:,.2f}")
        print(f"Total Return: {metrics.total_return:.2f}%")
        print(f"Maximum Drawdown: {metrics.max_drawdown:.2f}%")
        print(f"Sharpe Ratio: {metrics.sharpe_ratio:.2f}")
        
        print("\n🎯 Decision Metrics:")
        print(f"Total Decisions: {metrics.total_decisions}")
        print(f"Successful Decisions: {metrics.successful_decisions}")
        print(f"Success Rate: {metrics.success_rate:.2f}%")
        print(f"Average Confidence: {metrics.avg_confidence:.2f}")
        
        print("\n💰 Trade Metrics:")
        print(f"Total Trades: {metrics.total_trades}")
        print(f"Winning Trades: {metrics.winning_trades}")
        print(f"Losing Trades: {metrics.losing_trades}")
        print(f"Win Rate: {metrics.win_rate:.2f}%")
        print(f"Average Win: {metrics.avg_win:.2f}%")
        print(f"Average Loss: {metrics.avg_loss:.2f}%")
        print(f"Profit Factor: {metrics.profit_factor:.2f}")
        
        # Generate and save report
        print("\n📋 Generating detailed report...")
        report = backtester.generate_backtest_report()
        
        # Add security status to report
        report['security_status'] = 'SECURE'
        report['security_checks'] = {
            'weight_bias_check': 'PASSED',
            'parameter_tampering_check': 'PASSED',
            'result_validity_check': 'PASSED'
        }
        
        # Save report to file
        with open('backtest_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print("✅ Backtest completed successfully!")
        print("📄 Detailed report saved to 'backtest_report.json'")
        print("🔒 SECURITY STATUS: SECURE - No biasing or cheating detected")
        
        # Display recommendations
        if 'recommendations' in report:
            print("\n💡 Recommendations:")
            for i, rec in enumerate(report['recommendations'], 1):
                print(f"{i}. {rec}")
        
        return backtester, report
        
    except Exception as e:
        logger.error(f"Backtest failed: {e}")
        print(f"❌ Backtest failed: {e}")
        print("🔒 SECURITY STATUS: ERROR - Check security logs")
        return None, None

if __name__ == "__main__":
    run_comprehensive_backtest()

# Basic Risk Management
def apply_risk_management(self, trade_result, entry_price, current_price):
    """Apply basic risk management"""
    try:
        # 2% stop loss
        stop_loss_pct = 0.02
        
        # Calculate loss percentage
        loss_pct = (entry_price - current_price) / entry_price
        
        # Apply stop loss
        if loss_pct > stop_loss_pct:
            return True  # Stop loss triggered
        
        return False  # No stop loss
        
    except Exception as e:
        return False


class AdvancedSecurityGuard(SecurityGuard):
    """Enhanced security guard with advanced biasing prevention"""
    
    def __init__(self):
        super().__init__()
        self.biasing_attempts_blocked = 0
        self.security_alerts = []
        
    def advanced_bias_detection(self) -> bool:
        """Advanced biasing detection algorithms"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            engine = LLMLearningEngine()
            
            # Advanced check 1: Weight entropy analysis
            weights = list(engine.learning_weights.values())
            if weights:
                import math
                entropy = -sum(w * math.log2(w) for w in weights if w > 0)
                if entropy < 1.0:  # Low entropy indicates bias
                    self._log_security_alert("LOW_ENTROPY", f"Weight entropy: {entropy:.3f}")
                    return False
            
            # Advanced check 2: Learning rate stability
            if hasattr(engine, 'learning_rate_history'):
                recent_rates = engine.learning_rate_history[-10:]  # Last 10 rates
                rate_variance = sum((r - sum(recent_rates)/len(recent_rates))**2 for r in recent_rates) / len(recent_rates)
                if rate_variance > 0.01:  # High variance indicates tampering
                    self._log_security_alert("RATE_VOLATILITY", f"Learning rate variance: {rate_variance:.6f}")
                    return False
            
            # Advanced check 3: Decision pattern analysis
            if hasattr(engine, 'decision_history'):
                decisions = engine.decision_history[-50:]  # Last 50 decisions
                decision_types = [d.get('type', '') for d in decisions]
                type_counts = {dt: decision_types.count(dt) for dt in set(decision_types)}
                
                # Check for abnormal decision patterns
                if len(type_counts) > 0:
                    max_count = max(type_counts.values())
                    total_count = sum(type_counts.values())
                    if max_count > total_count * 0.8:  # 80% same type
                        self._log_security_alert("DECISION_BIAS", f"Decision bias: {max_count/total_count:.2%}")
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Advanced bias detection error: {e}")
            return False
    
    def _log_security_alert(self, alert_type, details):
        """Log security alert"""
        alert = {
            'timestamp': datetime.now().isoformat(),
            'alert_type': alert_type,
            'details': details,
            'severity': 'HIGH'
        }
        self.security_alerts.append(alert)
        self.logger.warning(f"🚨 SECURITY ALERT: {alert_type} - {details}")
        
        # Block operation if too many alerts
        if len(self.security_alerts) > 5:
            self.biasing_attempts_blocked += 1
            raise Exception("🚨 MULTIPLE SECURITY ALERTS - OPERATION BLOCKED")
    
    def get_enhanced_security_report(self) -> dict:
        """Get enhanced security report"""
        base_report = super().get_security_report()
        
        enhanced_report = base_report.copy()
        enhanced_report.update({
            'advanced_security_active': True,
            'biasing_attempts_blocked': self.biasing_attempts_blocked,
            'security_alerts': self.security_alerts,
            'enhanced_threat_detection': True
        })
        
        return enhanced_report

# Replace the global security guard with enhanced version
try:
    advanced_guard = AdvancedSecurityGuard()
    security_guard = advanced_guard
    print("  ✅ Enhanced security guard activated")
except Exception as e:
    print(f"  ⚠️ Could not activate enhanced guard: {e}")
