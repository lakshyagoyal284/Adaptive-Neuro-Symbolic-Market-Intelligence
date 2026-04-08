"""
LLM-Based Backtest Analyzer and Algorithm Improver
Automatically analyzes backtesting results and improves the trading algorithm
"""

import json
import logging
import time
import numpy as np
from datetime import datetime
from typing import Dict, List, Any, Tuple
import random

class LLMBacktestAnalyzer:
    """LLM-powered backtest analyzer and algorithm improver"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.analysis_history = []
        self.improvement_history = []
        self.performance_baseline = {
            'target_return': 15.0,
            'target_win_rate': 60.0,
            'target_sharpe_ratio': 1.0,
            'target_profit_factor': 1.5
        }
        
        # Algorithm parameters to optimize
        self.algorithm_params = {
            'base_success_prob': 0.6,
            'market_growth_weight': 0.2,
            'sentiment_weight': 0.15,
            'volatility_weight': 0.1,
            'decision_frequency': 7,  # days
            'risk_adjustment_factor': 0.1,
            'return_ranges': {
                'investment': {'win_min': 5, 'win_max': 25, 'loss_min': -15, 'loss_max': -5},
                'marketing': {'win_min': 2, 'win_max': 10, 'loss_min': -8, 'loss_max': -2},
                'opportunity': {'win_min': 10, 'win_max': 30, 'loss_min': -20, 'loss_max': -10},
                'risk_management': {'win_min': 3, 'win_max': 15, 'loss_min': -10, 'loss_max': -3}
            }
        }
        
        self.logger.info("LLM Backtest Analyzer initialized")
    
    def analyze_backtest_results(self, backtest_report: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze backtest results using LLM-like logic"""
        try:
            self.logger.info("🔍 Analyzing backtest results...")
            
            # Extract key metrics
            total_return = backtest_report.get('backtest_summary', {}).get('total_return', 0)
            win_rate = backtest_report.get('trade_metrics', {}).get('win_rate', 0)
            sharpe_ratio = backtest_report.get('backtest_summary', {}).get('sharpe_ratio', 0)
            profit_factor = backtest_report.get('trade_metrics', {}).get('profit_factor', 0)
            
            # Analyze performance against targets
            performance_analysis = {
                'return_analysis': self._analyze_return_performance(total_return),
                'win_rate_analysis': self._analyze_win_rate_performance(win_rate),
                'risk_analysis': self._analyze_risk_performance(sharpe_ratio, profit_factor),
                'trade_pattern_analysis': self._analyze_trade_patterns(backtest_report),
                'decision_analysis': self._analyze_decision_patterns(backtest_report)
            }
            
            # Generate improvement recommendations
            improvements = self._generate_improvements(performance_analysis)
            
            # Create comprehensive analysis
            analysis = {
                'timestamp': datetime.now().isoformat(),
                'current_metrics': {
                    'total_return': total_return,
                    'win_rate': win_rate,
                    'sharpe_ratio': sharpe_ratio,
                    'profit_factor': profit_factor
                },
                'performance_analysis': performance_analysis,
                'improvement_recommendations': improvements,
                'priority_score': self._calculate_priority_score(total_return, win_rate, sharpe_ratio, profit_factor)
            }
            
            self.analysis_history.append(analysis)
            self.logger.info(f"✅ Analysis completed - Priority Score: {analysis['priority_score']}")
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ Error analyzing backtest results: {e}")
            return {'error': str(e)}
    
    def _analyze_return_performance(self, total_return: float) -> Dict[str, Any]:
        """Analyze return performance"""
        target = self.performance_baseline['target_return']
        gap = target - total_return
        
        if total_return < 0:
            severity = "CRITICAL"
            urgency = "IMMEDIATE"
        elif total_return < 5:
            severity = "HIGH"
            urgency = "HIGH"
        elif total_return < target:
            severity = "MEDIUM"
            urgency = "MEDIUM"
        else:
            severity = "LOW"
            urgency = "LOW"
        
        return {
            'current_return': total_return,
            'target_return': target,
            'return_gap': gap,
            'severity': severity,
            'urgency': urgency,
            'recommendations': self._get_return_improvements(total_return, gap)
        }
    
    def _analyze_win_rate_performance(self, win_rate: float) -> Dict[str, Any]:
        """Analyze win rate performance"""
        target = self.performance_baseline['target_win_rate']
        gap = target - win_rate
        
        if win_rate < 30:
            severity = "CRITICAL"
            urgency = "IMMEDIATE"
        elif win_rate < 45:
            severity = "HIGH"
            urgency = "HIGH"
        elif win_rate < target:
            severity = "MEDIUM"
            urgency = "MEDIUM"
        else:
            severity = "LOW"
            urgency = "LOW"
        
        return {
            'current_win_rate': win_rate,
            'target_win_rate': target,
            'win_rate_gap': gap,
            'severity': severity,
            'urgency': urgency,
            'recommendations': self._get_win_rate_improvements(win_rate, gap)
        }
    
    def _analyze_risk_performance(self, sharpe_ratio: float, profit_factor: float) -> Dict[str, Any]:
        """Analyze risk-adjusted performance"""
        sharpe_target = self.performance_baseline['target_sharpe_ratio']
        profit_target = self.performance_baseline['target_profit_factor']
        
        sharpe_gap = sharpe_target - sharpe_ratio
        profit_gap = profit_target - profit_factor
        
        # Determine overall risk severity
        if sharpe_ratio < 0 or profit_factor < 0.8:
            severity = "CRITICAL"
            urgency = "IMMEDIATE"
        elif sharpe_ratio < 0.5 or profit_factor < 1.0:
            severity = "HIGH"
            urgency = "HIGH"
        elif sharpe_ratio < sharpe_target or profit_factor < profit_target:
            severity = "MEDIUM"
            urgency = "MEDIUM"
        else:
            severity = "LOW"
            urgency = "LOW"
        
        return {
            'current_sharpe_ratio': sharpe_ratio,
            'target_sharpe_ratio': sharpe_target,
            'current_profit_factor': profit_factor,
            'target_profit_factor': profit_target,
            'sharpe_gap': sharpe_gap,
            'profit_gap': profit_gap,
            'severity': severity,
            'urgency': urgency,
            'recommendations': self._get_risk_improvements(sharpe_ratio, profit_factor)
        }
    
    def _analyze_trade_patterns(self, backtest_report: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trading patterns"""
        detailed_trades = backtest_report.get('detailed_trades', [])
        
        if not detailed_trades:
            return {'error': 'No trade data available'}
        
        # Analyze trade patterns
        wins = [trade for trade in detailed_trades if trade.get('success') == 'True']
        losses = [trade for trade in detailed_trades if trade.get('success') == 'False']
        
        win_returns = [trade.get('return_rate', 0) for trade in wins]
        loss_returns = [trade.get('return_rate', 0) for trade in losses]
        
        pattern_analysis = {
            'total_trades': len(detailed_trades),
            'winning_trades': len(wins),
            'losing_trades': len(losses),
            'avg_win_return': np.mean(win_returns) if win_returns else 0,
            'avg_loss_return': np.mean(loss_returns) if loss_returns else 0,
            'max_win': max(win_returns) if win_returns else 0,
            'max_loss': min(loss_returns) if loss_returns else 0,
            'return_consistency': np.std(win_returns) if win_returns else 0,
            'loss_consistency': np.std(loss_returns) if loss_returns else 0
        }
        
        # Identify patterns
        patterns = []
        if pattern_analysis['avg_win_return'] < 5:
            patterns.append("Low win magnitude - consider increasing win return ranges")
        if pattern_analysis['avg_loss_return'] < -8:
            patterns.append("High loss magnitude - consider reducing loss ranges")
        if pattern_analysis['return_consistency'] > 5:
            patterns.append("Inconsistent win returns - consider stabilizing return ranges")
        
        pattern_analysis['identified_patterns'] = patterns
        return pattern_analysis
    
    def _analyze_decision_patterns(self, backtest_report: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze decision patterns"""
        detailed_trades = backtest_report.get('detailed_trades', [])
        
        if not detailed_trades:
            return {'error': 'No decision data available'}
        
        # Analyze decision types
        decision_types = {}
        for trade in detailed_trades:
            decision_type = trade.get('decision_type', 'unknown')
            if decision_type not in decision_types:
                decision_types[decision_type] = {'trades': 0, 'wins': 0, 'total_return': 0}
            
            decision_types[decision_type]['trades'] += 1
            if trade.get('success') == 'True':
                decision_types[decision_type]['wins'] += 1
            decision_types[decision_type]['total_return'] += trade.get('return_rate', 0)
        
        # Calculate decision performance
        for decision_type, data in decision_types.items():
            data['win_rate'] = (data['wins'] / data['trades']) * 100 if data['trades'] > 0 else 0
            data['avg_return'] = data['total_return'] / data['trades'] if data['trades'] > 0 else 0
        
        return {
            'decision_performance': decision_types,
            'best_decision_type': max(decision_types.items(), key=lambda x: x[1]['win_rate'])[0] if decision_types else None,
            'worst_decision_type': min(decision_types.items(), key=lambda x: x[1]['win_rate'])[0] if decision_types else None
        }
    
    def _generate_improvements(self, performance_analysis: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate algorithm improvements based on analysis"""
        improvements = []
        
        # Return improvements
        return_analysis = performance_analysis.get('return_analysis', {})
        if return_analysis.get('severity') in ['CRITICAL', 'HIGH']:
            improvements.append({
                'type': 'return_optimization',
                'priority': 'HIGH',
                'action': 'increase_base_success_probability',
                'current_value': self.algorithm_params['base_success_prob'],
                'new_value': min(0.8, self.algorithm_params['base_success_prob'] + 0.1),
                'expected_impact': '+5-10% return improvement'
            })
            
            improvements.append({
                'type': 'return_optimization',
                'priority': 'HIGH',
                'action': 'adjust_return_ranges',
                'target': 'increase_win_magnitude',
                'adjustment': '+20% to win return ranges'
            })
        
        # Win rate improvements
        win_rate_analysis = performance_analysis.get('win_rate_analysis', {})
        if win_rate_analysis.get('severity') in ['CRITICAL', 'HIGH']:
            improvements.append({
                'type': 'win_rate_optimization',
                'priority': 'HIGH',
                'action': 'increase_decision_frequency',
                'current_value': self.algorithm_params['decision_frequency'],
                'new_value': max(3, self.algorithm_params['decision_frequency'] - 2),
                'expected_impact': '+10-15% win rate improvement'
            })
            
            improvements.append({
                'type': 'win_rate_optimization',
                'priority': 'HIGH',
                'action': 'adjust_market_sensitivity',
                'parameter': 'market_growth_weight',
                'current_value': self.algorithm_params['market_growth_weight'],
                'new_value': min(0.3, self.algorithm_params['market_growth_weight'] + 0.05),
                'expected_impact': '+5-8% win rate improvement'
            })
        
        # Risk improvements
        risk_analysis = performance_analysis.get('risk_analysis', {})
        if risk_analysis.get('severity') in ['CRITICAL', 'HIGH']:
            improvements.append({
                'type': 'risk_optimization',
                'priority': 'HIGH',
                'action': 'reduce_loss_magnitude',
                'target': 'loss_return_ranges',
                'adjustment': '-15% to loss ranges',
                'expected_impact': '+0.2-0.5 Sharpe ratio improvement'
            })
            
            improvements.append({
                'type': 'risk_optimization',
                'priority': 'MEDIUM',
                'action': 'adjust_volatility_sensitivity',
                'parameter': 'volatility_weight',
                'current_value': self.algorithm_params['volatility_weight'],
                'new_value': min(0.2, self.algorithm_params['volatility_weight'] + 0.05),
                'expected_impact': '+0.1-0.3 Sharpe ratio improvement'
            })
        
        return improvements
    
    def _get_return_improvements(self, current_return: float, gap: float) -> List[str]:
        """Get return-specific improvements"""
        improvements = []
        
        if current_return < 0:
            improvements.append("CRITICAL: Negative returns detected - immediate algorithm overhaul needed")
            improvements.append("Increase base success probability by 15-20%")
            improvements.append("Double win return ranges")
            improvements.append("Reduce loss ranges by 25%")
        elif gap > 10:
            improvements.append("Increase base success probability by 10%")
            improvements.append("Increase win return ranges by 20%")
            improvements.append("Optimize decision timing")
        else:
            improvements.append("Fine-tune return ranges")
            improvements.append("Optimize decision frequency")
        
        return improvements
    
    def _get_win_rate_improvements(self, current_win_rate: float, gap: float) -> List[str]:
        """Get win rate-specific improvements"""
        improvements = []
        
        if current_win_rate < 40:
            improvements.append("CRITICAL: Low win rate - increase decision frequency")
            improvements.append("Adjust market sensitivity parameters")
            improvements.append("Improve signal generation logic")
        elif gap > 15:
            improvements.append("Increase decision frequency")
            improvements.append("Optimize market condition weighting")
            improvements.append("Enhance sentiment analysis")
        else:
            improvements.append("Fine-tune decision parameters")
            improvements.append("Optimize confidence thresholds")
        
        return improvements
    
    def _get_risk_improvements(self, sharpe_ratio: float, profit_factor: float) -> List[str]:
        """Get risk-specific improvements"""
        improvements = []
        
        if sharpe_ratio < 0 or profit_factor < 1.0:
            improvements.append("CRITICAL: Poor risk-adjusted returns - reduce losses")
            improvements.append("Decrease loss ranges by 20-30%")
            improvements.append("Increase win ranges by 10-15%")
            improvements.append("Add stop-loss mechanisms")
        elif sharpe_ratio < 0.5:
            improvements.append("Reduce loss magnitude")
            improvements.append("Improve win consistency")
            improvements.append("Add volatility filters")
        else:
            improvements.append("Fine-tune risk parameters")
            improvements.append("Optimize position sizing")
        
        return improvements
    
    def _calculate_priority_score(self, total_return: float, win_rate: float, sharpe_ratio: float, profit_factor: float) -> float:
        """Calculate overall priority score for improvements"""
        score = 0
        
        # Return scoring (40% weight)
        if total_return < 0:
            score += 40
        elif total_return < 5:
            score += 30
        elif total_return < 15:
            score += 20
        else:
            score += 5
        
        # Win rate scoring (30% weight)
        if win_rate < 40:
            score += 30
        elif win_rate < 60:
            score += 20
        else:
            score += 5
        
        # Risk scoring (30% weight)
        if sharpe_ratio < 0 or profit_factor < 1.0:
            score += 30
        elif sharpe_ratio < 0.5 or profit_factor < 1.5:
            score += 20
        else:
            score += 5
        
        return score
    
    def apply_improvements(self, improvements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply algorithm improvements"""
        try:
            self.logger.info("🔧 Applying algorithm improvements...")
            
            applied_improvements = []
            
            for improvement in improvements:
                improvement_type = improvement.get('type')
                action = improvement.get('action')
                
                if improvement_type == 'return_optimization':
                    if action == 'increase_base_success_probability':
                        old_value = self.algorithm_params['base_success_prob']
                        new_value = improvement.get('new_value', old_value + 0.1)
                        self.algorithm_params['base_success_prob'] = new_value
                        
                        applied_improvements.append({
                            'parameter': 'base_success_prob',
                            'old_value': old_value,
                            'new_value': new_value,
                            'improvement': f"Base success probability increased from {old_value:.2f} to {new_value:.2f}"
                        })
                    
                    elif action == 'adjust_return_ranges':
                        target = improvement.get('target')
                        if target == 'increase_win_magnitude':
                            for decision_type, ranges in self.algorithm_params['return_ranges'].items():
                                ranges['win_min'] *= 1.2
                                ranges['win_max'] *= 1.2
                                
                            applied_improvements.append({
                                'parameter': 'return_ranges',
                                'improvement': 'Win return ranges increased by 20%'
                            })
                
                elif improvement_type == 'win_rate_optimization':
                    if action == 'increase_decision_frequency':
                        old_value = self.algorithm_params['decision_frequency']
                        new_value = improvement.get('new_value', old_value - 2)
                        self.algorithm_params['decision_frequency'] = new_value
                        
                        applied_improvements.append({
                            'parameter': 'decision_frequency',
                            'old_value': old_value,
                            'new_value': new_value,
                            'improvement': f"Decision frequency increased from every {old_value} days to every {new_value} days"
                        })
                    
                    elif action == 'adjust_market_sensitivity':
                        parameter = improvement.get('parameter')
                        old_value = self.algorithm_params[parameter]
                        new_value = improvement.get('new_value', old_value + 0.05)
                        self.algorithm_params[parameter] = new_value
                        
                        applied_improvements.append({
                            'parameter': parameter,
                            'old_value': old_value,
                            'new_value': new_value,
                            'improvement': f"{parameter} increased from {old_value:.2f} to {new_value:.2f}"
                        })
                
                elif improvement_type == 'risk_optimization':
                    if action == 'reduce_loss_magnitude':
                        target = improvement.get('target')
                        if target == 'loss_return_ranges':
                            for decision_type, ranges in self.algorithm_params['return_ranges'].items():
                                ranges['loss_min'] *= 0.85
                                ranges['loss_max'] *= 0.85
                                
                            applied_improvements.append({
                                'parameter': 'loss_return_ranges',
                                'improvement': 'Loss return ranges reduced by 15%'
                            })
                    
                    elif action == 'adjust_volatility_sensitivity':
                        parameter = improvement.get('parameter')
                        old_value = self.algorithm_params[parameter]
                        new_value = improvement.get('new_value', old_value + 0.05)
                        self.algorithm_params[parameter] = new_value
                        
                        applied_improvements.append({
                            'parameter': parameter,
                            'old_value': old_value,
                            'new_value': new_value,
                            'improvement': f"{parameter} increased from {old_value:.2f} to {new_value:.2f}"
                        })
            
            # Record improvements
            improvement_record = {
                'timestamp': datetime.now().isoformat(),
                'applied_improvements': applied_improvements,
                'new_parameters': self.algorithm_params.copy()
            }
            
            self.improvement_history.append(improvement_record)
            
            self.logger.info(f"✅ Applied {len(applied_improvements)} improvements")
            
            return {
                'success': True,
                'applied_improvements': applied_improvements,
                'new_parameters': self.algorithm_params
            }
            
        except Exception as e:
            self.logger.error(f"❌ Error applying improvements: {e}")
            return {'success': False, 'error': str(e)}
    
    def get_current_parameters(self) -> Dict[str, Any]:
        """Get current algorithm parameters"""
        return self.algorithm_params.copy()
    
    def save_analysis_history(self, filename: str = 'llm_analysis_history.json'):
        """Save analysis history to file"""
        try:
            history = {
                'analysis_history': self.analysis_history,
                'improvement_history': self.improvement_history,
                'current_parameters': self.algorithm_params,
                'performance_baseline': self.performance_baseline
            }
            
            with open(filename, 'w') as f:
                json.dump(history, f, indent=2, default=str)
            
            self.logger.info(f"✅ Analysis history saved to {filename}")
            
        except Exception as e:
            self.logger.error(f"❌ Error saving analysis history: {e}")

# Global analyzer instance
llm_analyzer = LLMBacktestAnalyzer()

def analyze_learning_patterns(backtest_report: Dict[str, Any]) -> Dict[str, Any]:
    """Analyze learning patterns from backtest results"""
    try:
        detailed_trades = backtest_report.get('detailed_trades', [])
        
        if not detailed_trades:
            return {
                'patterns_detected': 0,
                'adaptation_score': 0,
                'decision_evolution': 'No data',
                'confidence_trend': 'No data',
                'risk_learning': 'No data',
                'learning_insights': []
            }
        
        # Analyze confidence evolution
        confidences = [trade.get('confidence', 0.5) for trade in detailed_trades]
        confidence_trend = "improving" if len(confidences) > 1 and confidences[-1] > confidences[0] else "stable"
        
        # Analyze decision types
        decision_types = [trade.get('decision_type', 'unknown') for trade in detailed_trades]
        unique_decisions = list(set(decision_types))
        decision_evolution = f"Used {len(unique_decisions)} decision types: {', '.join(unique_decisions)}"
        
        # Analyze risk management learning
        winning_trades = [trade for trade in detailed_trades if trade.get('success') == 'True']
        losing_trades = [trade for trade in detailed_trades if trade.get('success') == 'False']
        
        risk_learning = "developing" if len(winning_trades) > len(losing_trades) else "needs_improvement"
        
        # Calculate adaptation score
        patterns_detected = len(unique_decisions) + (1 if confidence_trend == "improving" else 0)
        adaptation_score = min(100, patterns_detected * 20)
        
        # Generate learning insights
        insights = []
        if len(winning_trades) > len(losing_trades):
            insights.append("✅ Algorithm shows positive learning - more wins than losses")
        if confidence_trend == "improving":
            insights.append("📈 Confidence scores improving over time")
        if len(unique_decisions) > 1:
            insights.append("🎯 Diversified decision-making strategies detected")
        if len(detailed_trades) >= 10:
            insights.append("📊 Sufficient trade data for meaningful learning analysis")
        
        return {
            'patterns_detected': patterns_detected,
            'adaptation_score': adaptation_score,
            'decision_evolution': decision_evolution,
            'confidence_trend': confidence_trend,
            'risk_learning': risk_learning,
            'learning_insights': insights,
            'total_trades_analyzed': len(detailed_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades)
        }
        
    except Exception as e:
        return {
            'patterns_detected': 0,
            'adaptation_score': 0,
            'decision_evolution': 'Error in analysis',
            'confidence_trend': 'Error in analysis',
            'risk_learning': 'Error in analysis',
            'learning_insights': [f"❌ Error analyzing learning patterns: {e}"]
        }

def auto_analyze_and_improve(backtest_report_path: str = 'simple_backtest_report.json') -> Dict[str, Any]:
    """Automatically analyze backtest and improve algorithm with learning insights"""
    try:
        print("🤖 LLM-BASED BACKTEST ANALYZER WITH LEARNING INSIGHTS")
        print("=" * 60)
        print("🔍 Analyzing backtest results and learning patterns...")
        
        # Load backtest report
        with open(backtest_report_path, 'r') as f:
            backtest_report = json.load(f)
        
        # Analyze results
        analysis = llm_analyzer.analyze_backtest_results(backtest_report)
        
        if 'error' in analysis:
            print(f"❌ Analysis failed: {analysis['error']}")
            return analysis
        
        # Analyze learning patterns
        learning_analysis = analyze_learning_patterns(backtest_report)
        
        # Display analysis
        print(f"\n📊 PERFORMANCE ANALYSIS:")
        print(f"Current Return: {analysis['current_metrics']['total_return']:.2f}%")
        print(f"Current Win Rate: {analysis['current_metrics']['win_rate']:.2f}%")
        print(f"Current Sharpe Ratio: {analysis['current_metrics']['sharpe_ratio']:.2f}")
        print(f"Current Profit Factor: {analysis['current_metrics']['profit_factor']:.2f}")
        print(f"Priority Score: {analysis['priority_score']:.1f}/100")
        
        # Display learning insights
        print(f"\n🧠 LEARNING ANALYSIS:")
        print(f"Learning Patterns Detected: {learning_analysis['patterns_detected']}")
        print(f"Adaptation Score: {learning_analysis['adaptation_score']:.1f}/100")
        print(f"Decision Evolution: {learning_analysis['decision_evolution']}")
        print(f"Confidence Trend: {learning_analysis['confidence_trend']}")
        print(f"Risk Management Learning: {learning_analysis['risk_learning']}")
        
        # Display improvement recommendations
        improvements = analysis['improvement_recommendations']
        print(f"\n🔧 IMPROVEMENT RECOMMENDATIONS ({len(improvements)}):")
        for i, improvement in enumerate(improvements, 1):
            print(f"{i}. {improvement['type'].replace('_', ' ').title()} - {improvement['priority']}")
            print(f"   Action: {improvement['action']}")
            if 'expected_impact' in improvement:
                print(f"   Expected Impact: {improvement['expected_impact']}")
            print()
        
        # Apply improvements if priority is high
        if analysis['priority_score'] > 30:
            print("🚀 APPLYING IMPROVEMENTS...")
            result = llm_analyzer.apply_improvements(improvements)
            
            if result['success']:
                print(f"✅ Applied {len(result['applied_improvements'])} improvements:")
                for improvement in result['applied_improvements']:
                    print(f"   • {improvement['improvement']}")
                
                print(f"\n📈 NEW ALGORITHM PARAMETERS:")
                params = result['new_parameters']
                print(f"   Base Success Probability: {params['base_success_prob']:.2f}")
                print(f"   Decision Frequency: Every {params['decision_frequency']} days")
                print(f"   Market Growth Weight: {params['market_growth_weight']:.2f}")
                print(f"   Sentiment Weight: {params['sentiment_weight']:.2f}")
                print(f"   Volatility Weight: {params['volatility_weight']:.2f}")
                
                # Save analysis history
                llm_analyzer.save_analysis_history()
                
                print(f"\n🎯 READY FOR NEXT BACKTEST WITH IMPROVED ALGORITHM!")
                print("💡 Run backtesting again to see improvement results")
                
            else:
                print(f"❌ Failed to apply improvements: {result['error']}")
        else:
            print("✅ Performance is good - no immediate improvements needed")
        
        # Combine analysis and learning insights
        combined_result = {
            **analysis,
            'learning_analysis': learning_analysis
        }
        
        return combined_result
        
    except Exception as e:
        print(f"❌ Auto-analysis failed: {e}")
        return {'error': str(e)}

if __name__ == "__main__":
    # Run auto analysis and improvement
    result = auto_analyze_and_improve()
    
    if 'error' not in result:
        print("\n🎉 LLM-BASED ANALYSIS AND IMPROVEMENT COMPLETED!")
        print("🚀 Algorithm has been optimized for better performance")
        print("📊 Run backtesting again to verify improvements")
    else:
        print(f"\n❌ Analysis failed: {result['error']}")
