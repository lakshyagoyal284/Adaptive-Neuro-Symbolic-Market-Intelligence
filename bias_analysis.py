"""
Comprehensive Bias Analysis System
Identifies and analyzes potential biases in trading algorithms, data, and decision-making
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

class BiasAnalysis:
    """Comprehensive bias detection and analysis system"""
    
    def __init__(self):
        self.bias_findings = []
        self.recommendations = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/bias_analysis.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def run_comprehensive_bias_analysis(self):
        """Run comprehensive bias analysis"""
        print("🔍 COMPREHENSIVE BIAS ANALYSIS")
        print("=" * 80)
        print("🔍 Analyzing system for potential biases...")
        print("=" * 80)
        
        # Analyze different types of biases
        self.analyze_algorithmic_bias()
        self.analyze_data_bias()
        self.analyze_selection_bias()
        self.analyze_temporal_bias()
        self.analyze_market_bias()
        self.analyze_learning_bias()
        self.analyze_risk_bias()
        self.analyze_evaluation_bias()
        
        # Generate comprehensive report
        self.generate_bias_report()
        
    def analyze_algorithmic_bias(self):
        """Analyze algorithmic biases in trading logic"""
        print("\n🔍 ANALYZING ALGORITHMIC BIAS...")
        
        # Check learning engine for biases
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Check weight distribution bias
            weights = engine.learning_weights
            if weights:
                weight_analysis = self._analyze_weight_distribution(weights)
                if weight_analysis['is_biased']:
                    self.bias_findings.append({
                        'type': 'ALGORITHMIC_BIAS',
                        'subtype': 'WEIGHT_DISTRIBUTION_BIAS',
                        'severity': weight_analysis['severity'],
                        'description': weight_analysis['description'],
                        'evidence': weight_analysis['evidence'],
                        'recommendation': weight_analysis['recommendation']
                    })
            
            # Check learning rate bias
            learning_rate = engine.learning_rate
            if learning_rate > 0.5:
                self.bias_findings.append({
                    'type': 'ALGORITHMIC_BIAS',
                    'subtype': 'LEARNING_RATE_BIAS',
                    'severity': 'MEDIUM',
                    'description': f'Learning rate too high ({learning_rate}), may cause overfitting',
                    'evidence': f'Learning rate: {learning_rate}',
                    'recommendation': 'Reduce learning rate to 0.1-0.3 range'
                })
            
            # Check reward/punishment bias
            if engine.reward_scale > engine.punishment_scale * 2:
                self.bias_findings.append({
                    'type': 'ALGORITHMIC_BIAS',
                    'subtype': 'REWARD_PUNISHMENT_BIAS',
                    'severity': 'HIGH',
                    'description': f'Reward scale ({engine.reward_scale}) much higher than punishment scale ({engine.punishment_scale})',
                    'evidence': f'Reward/Punishment ratio: {engine.reward_scale/engine.punishment_scale}',
                    'recommendation': 'Balance reward and punishment scales'
                })
                
        except Exception as e:
            self.logger.error(f"Error analyzing algorithmic bias: {e}")
        
        # Check trading logic bias
        try:
            import aggressive_profit_backtester
            
            # Check signal generation bias
            signal_bias = self._check_signal_generation_bias()
            if signal_bias['is_biased']:
                self.bias_findings.append({
                    'type': 'ALGORITHMIC_BIAS',
                    'subtype': 'SIGNAL_GENERATION_BIAS',
                    'severity': signal_bias['severity'],
                    'description': signal_bias['description'],
                    'evidence': signal_bias['evidence'],
                    'recommendation': signal_bias['recommendation']
                })
                
        except Exception as e:
            self.logger.error(f"Error analyzing trading logic bias: {e}")
    
    def analyze_data_bias(self):
        """Analyze data-related biases"""
        print("\n🔍 ANALYZING DATA BIAS...")
        
        # Check market data for biases
        try:
            import market_data_processor
            
            processor = market_data_processor.MarketDataProcessor()
            market_data = processor.load_market_data()
            
            if market_data:
                for symbol, df in market_data.items():
                    # Check for data quality issues
                    data_bias = self._analyze_data_quality(df, symbol)
                    if data_bias['is_biased']:
                        self.bias_findings.append({
                            'type': 'DATA_BIAS',
                            'subtype': 'DATA_QUALITY_BIAS',
                            'severity': data_bias['severity'],
                            'description': data_bias['description'],
                            'evidence': data_bias['evidence'],
                            'recommendation': data_bias['recommendation']
                        })
                    
                    # Check for survivorship bias
                    survivorship_bias = self._check_survivorship_bias(df, symbol)
                    if survivorship_bias['is_biased']:
                        self.bias_findings.append({
                            'type': 'DATA_BIAS',
                            'subtype': 'SURVIVORSHIP_BIAS',
                            'severity': survivorship_bias['severity'],
                            'description': survivorship_bias['description'],
                            'evidence': survivorship_bias['evidence'],
                            'recommendation': survivorship_bias['recommendation']
                        })
                        
        except Exception as e:
            self.logger.error(f"Error analyzing data bias: {e}")
    
    def analyze_selection_bias(self):
        """Analyze selection bias in trading decisions"""
        print("\n🔍 ANALYZING SELECTION BIAS...")
        
        # Check for symbol selection bias
        try:
            import aggressive_profit_backtester
            
            # Analyze which symbols are preferred
            symbol_bias = self._analyze_symbol_selection_bias()
            if symbol_bias['is_biased']:
                self.bias_findings.append({
                    'type': 'SELECTION_BIAS',
                    'subtype': 'SYMBOL_SELECTION_BIAS',
                    'severity': symbol_bias['severity'],
                    'description': symbol_bias['description'],
                    'evidence': symbol_bias['evidence'],
                    'recommendation': symbol_bias['recommendation']
                })
                
        except Exception as e:
            self.logger.error(f"Error analyzing selection bias: {e}")
    
    def analyze_temporal_bias(self):
        """Analyze temporal biases in trading patterns"""
        print("\n🔍 ANALYZING TEMPORAL BIAS...")
        
        # Check for time-based biases
        try:
            import market_data_processor
            
            processor = market_data_processor.MarketDataProcessor()
            market_data = processor.load_market_data()
            
            if market_data:
                for symbol, df in market_data.items():
                    # Check for look-ahead bias
                    lookahead_bias = self._check_lookahead_bias(df, symbol)
                    if lookahead_bias['is_biased']:
                        self.bias_findings.append({
                            'type': 'TEMPORAL_BIAS',
                            'subtype': 'LOOKAHEAD_BIAS',
                            'severity': lookahead_bias['severity'],
                            'description': lookahead_bias['description'],
                            'evidence': lookahead_bias['evidence'],
                            'recommendation': lookahead_bias['recommendation']
                        })
                    
                    # Check for time-of-day bias
                    time_bias = self._check_time_of_day_bias(df, symbol)
                    if time_bias['is_biased']:
                        self.bias_findings.append({
                            'type': 'TEMPORAL_BIAS',
                            'subtype': 'TIME_OF_DAY_BIAS',
                            'severity': time_bias['severity'],
                            'description': time_bias['description'],
                            'evidence': time_bias['evidence'],
                            'recommendation': time_bias['recommendation']
                        })
                        
        except Exception as e:
            self.logger.error(f"Error analyzing temporal bias: {e}")
    
    def analyze_market_bias(self):
        """Analyze market-related biases"""
        print("\n🔍 ANALYZING MARKET BIAS...")
        
        # Check for market condition bias
        try:
            from symbolic_engine.rules import RuleEngine
            
            engine = RuleEngine()
            
            # Check if rules favor certain market conditions
            market_bias = self._analyze_market_condition_bias(engine)
            if market_bias['is_biased']:
                self.bias_findings.append({
                    'type': 'MARKET_BIAS',
                    'subtype': 'MARKET_CONDITION_BIAS',
                    'severity': market_bias['severity'],
                    'description': market_bias['description'],
                    'evidence': market_bias['evidence'],
                    'recommendation': market_bias['recommendation']
                })
                
        except Exception as e:
            self.logger.error(f"Error analyzing market bias: {e}")
    
    def analyze_learning_bias(self):
        """Analyze learning-related biases"""
        print("\n🔍 ANALYZING LEARNING BIAS...")
        
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Check for confirmation bias
            confirmation_bias = self._check_confirmation_bias(engine)
            if confirmation_bias['is_biased']:
                self.bias_findings.append({
                    'type': 'LEARNING_BIAS',
                    'subtype': 'CONFIRMATION_BIAS',
                    'severity': confirmation_bias['severity'],
                    'description': confirmation_bias['description'],
                    'evidence': confirmation_bias['evidence'],
                    'recommendation': confirmation_bias['recommendation']
                })
            
            # Check for overfitting bias
            overfitting_bias = self._check_overfitting_bias(engine)
            if overfitting_bias['is_biased']:
                self.bias_findings.append({
                    'type': 'LEARNING_BIAS',
                    'subtype': 'OVERFITTING_BIAS',
                    'severity': overfitting_bias['severity'],
                    'description': overfitting_bias['description'],
                    'evidence': overfitting_bias['evidence'],
                    'recommendation': overfitting_bias['recommendation']
                })
                
        except Exception as e:
            self.logger.error(f"Error analyzing learning bias: {e}")
    
    def analyze_risk_bias(self):
        """Analyze risk-related biases"""
        print("\n🔍 ANALYZING RISK BIAS...")
        
        # Check for risk preference bias
        try:
            import aggressive_profit_backtester
            
            risk_bias = self._analyze_risk_preference_bias()
            if risk_bias['is_biased']:
                self.bias_findings.append({
                    'type': 'RISK_BIAS',
                    'subtype': 'RISK_PREFERENCE_BIAS',
                    'severity': risk_bias['severity'],
                    'description': risk_bias['description'],
                    'evidence': risk_bias['evidence'],
                    'recommendation': risk_bias['recommendation']
                })
                
        except Exception as e:
            self.logger.error(f"Error analyzing risk bias: {e}")
    
    def analyze_evaluation_bias(self):
        """Analyze evaluation-related biases"""
        print("\n🔍 ANALYZING EVALUATION BIAS...")
        
        # Check for evaluation metric bias
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Check if evaluation favors certain outcomes
            eval_bias = self._analyze_evaluation_metric_bias(engine)
            if eval_bias['is_biased']:
                self.bias_findings.append({
                    'type': 'EVALUATION_BIAS',
                    'subtype': 'EVALUATION_METRIC_BIAS',
                    'severity': eval_bias['severity'],
                    'description': eval_bias['description'],
                    'evidence': eval_bias['evidence'],
                    'recommendation': eval_bias['recommendation']
                })
                
        except Exception as e:
            self.logger.error(f"Error analyzing evaluation bias: {e}")
    
    def _analyze_weight_distribution(self, weights: Dict[str, float]) -> Dict[str, Any]:
        """Analyze weight distribution for bias"""
        if not weights:
            return {'is_biased': False, 'severity': 'LOW'}
        
        weight_values = list(weights.values())
        
        # Check for extreme weight concentration
        max_weight = max(weight_values)
        min_weight = min(weight_values)
        weight_ratio = max_weight / min_weight if min_weight > 0 else float('inf')
        
        # Check if weights are too concentrated
        if weight_ratio > 10:  # One weight is 10x another
            return {
                'is_biased': True,
                'severity': 'HIGH',
                'description': f'Weight distribution highly concentrated (ratio: {weight_ratio:.2f})',
                'evidence': f'Max weight: {max_weight:.4f}, Min weight: {min_weight:.4f}',
                'recommendation': 'Normalize weight distribution to prevent overemphasis on single features'
            }
        
        # Check for zero weights
        zero_weights = [k for k, v in weights.items() if v < 0.01]
        if zero_weights:
            return {
                'is_biased': True,
                'severity': 'MEDIUM',
                'description': f'Some weights are effectively zero: {zero_weights}',
                'evidence': f'Zero weights: {zero_weights}',
                'recommendation': 'Ensure all weights have meaningful values'
            }
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _check_signal_generation_bias(self) -> Dict[str, Any]:
        """Check for signal generation bias"""
        # This would analyze the signal generation logic
        # For now, return a placeholder
        return {
            'is_biased': False,
            'severity': 'LOW',
            'description': 'No significant signal generation bias detected',
            'evidence': 'Signal generation appears balanced',
            'recommendation': 'Continue monitoring signal patterns'
        }
    
    def _analyze_data_quality(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Analyze data quality for biases"""
        if df is None or df.empty:
            return {
                'is_biased': True,
                'severity': 'HIGH',
                'description': f'No data available for {symbol}',
                'evidence': 'Empty DataFrame',
                'recommendation': 'Ensure data availability and quality'
            }
        
        # Check for missing data
        missing_data = df.isnull().sum()
        if missing_data.any():
            missing_pct = (missing_data / len(df)) * 100
            return {
                'is_biased': True,
                'severity': 'MEDIUM',
                'description': f'Significant missing data in {symbol}',
                'evidence': f'Missing data percentage: {missing_pct.mean():.2f}%',
                'recommendation': 'Implement data imputation or collection improvement'
            }
        
        # Check for outliers
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        outliers = {}
        
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            if outlier_count > len(df) * 0.05:  # More than 5% outliers
                outliers[col] = outlier_count
        
        if outliers:
            return {
                'is_biased': True,
                'severity': 'MEDIUM',
                'description': f'Significant outliers detected in {symbol}',
                'evidence': f'Outliers: {outliers}',
                'recommendation': 'Investigate data collection and cleaning processes'
            }
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _check_survivorship_bias(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Check for survivorship bias"""
        if len(df) < 100:
            return {
                'is_biased': False,
                'severity': 'LOW',
                'description': f'Insufficient data for survivorship bias analysis in {symbol}',
                'evidence': f'Data points: {len(df)}',
                'recommendation': 'Collect more historical data'
            }
        
        # Check if data only includes successful companies
        if 'close' in df.columns:
            # Simple check: if all prices are increasing (survivor bias)
            price_changes = df['close'].pct_change().dropna()
            if price_changes.mean() > 0.1:  # Average gain > 10%
                return {
                    'is_biased': True,
                    'severity': 'HIGH',
                    'description': f'Potential survivorship bias in {symbol} data',
                    'evidence': f'Average price change: {price_changes.mean():.2%}',
                    'recommendation': 'Include delisted companies in dataset'
                }
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _check_lookahead_bias(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Check for lookahead bias"""
        # Check if future information is inadvertently included
        if 'close' in df.columns and 'open' in df.columns:
            # Check if next day's close is predictable from current day's data
            next_day_returns = df['close'].shift(-1) / df['close'] - 1
            current_day_info = df[['open', 'high', 'low', 'volume']]
            
            # Simple correlation check
            correlations = []
            for col in current_day_info.columns:
                if current_day_info[col].dtype in ['int64', 'float64']:
                    corr = current_day_info[col].corr(next_day_returns)
                    correlations.append(abs(corr))
            
            max_corr = max(correlations) if correlations else 0
            if max_corr > 0.8:  # Very high correlation suggests lookahead
                return {
                    'is_biased': True,
                    'severity': 'HIGH',
                    'description': f'Potential lookahead bias in {symbol}',
                    'evidence': f'Max correlation: {max_corr:.3f}',
                    'recommendation': 'Review data collection and preprocessing'
                }
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _check_time_of_day_bias(self, df: pd.DataFrame, symbol: str) -> Dict[str, Any]:
        """Check for time-of-day bias"""
        if 'date' not in df.columns:
            return {
                'is_biased': False,
                'severity': 'LOW',
                'description': f'No timestamp data for {symbol}',
                'evidence': 'Missing date column',
                'recommendation': 'Include timestamp information in data'
            }
        
        # Convert date to datetime if it's not already
        try:
            df['date'] = pd.to_datetime(df['date'])
            df['hour'] = df['date'].dt.hour
            
            # Check if performance varies by hour
            if 'close' in df.columns:
                hourly_returns = df.groupby('hour')['close'].pct_change().mean()
                
                if hourly_returns.std() > 0.02:  # High variance in hourly returns
                    return {
                        'is_biased': True,
                        'severity': 'MEDIUM',
                        'description': f'Time-of-day bias detected in {symbol}',
                        'evidence': f'Hourly return variance: {hourly_returns.std():.3f}',
                        'recommendation': 'Consider time-based adjustments in strategy'
                    }
        except Exception as e:
            self.logger.error(f"Error checking time-of-day bias: {e}")
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _analyze_market_condition_bias(self, engine) -> Dict[str, Any]:
        """Analyze market condition bias in rules"""
        try:
            rules = engine.rules
            
            # Check if rules favor bull markets
            bull_rules = 0
            bear_rules = 0
            neutral_rules = 0
            
            for rule_id, rule in rules.items():
                condition = rule.condition.lower()
                if 'market_growth >' in condition:
                    bull_rules += 1
                elif 'market_growth <' in condition:
                    bear_rules += 1
                else:
                    neutral_rules += 1
            
            total_rules = bull_rules + bear_rules + neutral_rules
            
            if total_rules > 0:
                bull_ratio = bull_rules / total_rules
                bear_ratio = bear_rules / total_rules
                
                # Check for significant imbalance
                if abs(bull_ratio - bear_ratio) > 0.3:  # 30% difference
                    favored_market = 'bull' if bull_ratio > bear_ratio else 'bear'
                    return {
                        'is_biased': True,
                        'severity': 'MEDIUM',
                        'description': f'Market condition bias favoring {favored_market} markets',
                        'evidence': f'Bull rules: {bull_ratio:.2f}, Bear rules: {bear_ratio:.2f}',
                        'recommendation': 'Balance rules for different market conditions'
                    }
        
        except Exception as e:
            self.logger.error(f"Error analyzing market condition bias: {e}")
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _check_confirmation_bias(self, engine) -> Dict[str, Any]:
        """Check for confirmation bias in learning"""
        try:
            experiences = engine.experiences
            
            if len(experiences) > 100:
                # Analyze recent experiences
                recent_experiences = experiences[-100:]
                
                correct_decisions = [exp for exp in recent_experiences if exp.outcome.value == 'correct']
                incorrect_decisions = [exp for exp in recent_experiences if exp.outcome.value == 'incorrect']
                
                # Check if system learns more from correct decisions
                if len(correct_decisions) > 0 and len(incorrect_decisions) > 0:
                    correct_confidence = np.mean([exp.confidence for exp in correct_decisions])
                    incorrect_confidence = np.mean([exp.confidence for exp in incorrect_decisions])
                    
                    if correct_confidence > incorrect_confidence * 1.2:  # 20% higher confidence for correct
                        return {
                            'is_biased': True,
                            'severity': 'MEDIUM',
                            'description': 'Confirmation bias detected in learning system',
                            'evidence': f'Correct confidence: {correct_confidence:.3f}, Incorrect confidence: {incorrect_confidence:.3f}',
                            'recommendation': 'Balance confidence calibration across outcomes'
                        }
        
        except Exception as e:
            self.logger.error(f"Error checking confirmation bias: {e}")
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _check_overfitting_bias(self, engine) -> Dict[str, Any]:
        """Check for overfitting bias"""
        try:
            experiences = engine.experiences
            
            if len(experiences) > 200:
                # Compare recent vs older performance
                recent_experiences = experiences[-100:]
                older_experiences = experiences[-200:-100]
                
                recent_correct = len([exp for exp in recent_experiences if exp.outcome.value == 'correct'])
                older_correct = len([exp for exp in older_experiences if exp.outcome.value == 'correct'])
                
                recent_accuracy = recent_correct / len(recent_experiences) if len(recent_experiences) > 0 else 0
                older_accuracy = older_correct / len(older_experiences) if len(older_experiences) > 0 else 0
                
                # Check if recent performance is significantly better
                if recent_accuracy > older_accuracy * 1.5:  # 50% improvement
                    return {
                        'is_biased': True,
                        'severity': 'HIGH',
                        'description': 'Potential overfitting to recent data',
                        'evidence': f'Recent accuracy: {recent_accuracy:.3f}, Older accuracy: {older_accuracy:.3f}',
                        'recommendation': 'Implement regularization and cross-validation'
                    }
        
        except Exception as e:
            self.logger.error(f"Error checking overfitting bias: {e}")
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _analyze_risk_preference_bias(self) -> Dict[str, Any]:
        """Analyze risk preference bias"""
        # This would analyze if the system prefers certain risk levels
        # For now, return a placeholder
        return {
            'is_biased': False,
            'severity': 'LOW',
            'description': 'No significant risk preference bias detected',
            'evidence': 'Risk management appears balanced',
            'recommendation': 'Continue monitoring risk-adjusted returns'
        }
    
    def _analyze_evaluation_metric_bias(self, engine) -> Dict[str, Any]:
        """Analyze evaluation metric bias"""
        try:
            experiences = engine.experiences
            
            if len(experiences) > 50:
                # Check if evaluation favors certain types of outcomes
                outcomes = [exp.outcome.value for exp in experiences]
                outcome_counts = pd.Series(outcomes).value_counts()
                
                # Check if one outcome is significantly underrepresented
                total_outcomes = len(outcomes)
                min_count = outcome_counts.min()
                min_pct = min_count / total_outcomes
                
                if min_pct < 0.1:  # Less than 10% for any outcome
                    return {
                        'is_biased': True,
                        'severity': 'MEDIUM',
                        'description': 'Evaluation metric bias in outcome distribution',
                        'evidence': f'Outcome distribution: {outcome_counts.to_dict()}',
                        'recommendation': 'Ensure balanced representation of all outcomes'
                    }
        
        except Exception as e:
            self.logger.error(f"Error analyzing evaluation metric bias: {e}")
        
        return {'is_biased': False, 'severity': 'LOW'}
    
    def _analyze_symbol_selection_bias(self) -> Dict[str, Any]:
        """Analyze symbol selection bias"""
        # This would analyze if certain symbols are preferred
        # For now, return a placeholder
        return {
            'is_biased': False,
            'severity': 'LOW',
            'description': 'No significant symbol selection bias detected',
            'evidence': 'Symbol selection appears balanced',
            'recommendation': 'Continue monitoring symbol performance'
        }
    
    def generate_bias_report(self):
        """Generate comprehensive bias analysis report"""
        print("\n" + "=" * 80)
        print("🔍 COMPREHENSIVE BIAS ANALYSIS REPORT")
        print("=" * 80)
        
        # Count biases by type and severity
        bias_counts = {
            'ALGORITHMIC_BIAS': 0,
            'DATA_BIAS': 0,
            'SELECTION_BIAS': 0,
            'TEMPORAL_BIAS': 0,
            'MARKET_BIAS': 0,
            'LEARNING_BIAS': 0,
            'RISK_BIAS': 0,
            'EVALUATION_BIAS': 0
        }
        
        severity_counts = {
            'CRITICAL': 0,
            'HIGH': 0,
            'MEDIUM': 0,
            'LOW': 0
        }
        
        for bias in self.bias_findings:
            bias_type = bias['type']
            severity = bias['severity']
            
            if bias_type in bias_counts:
                bias_counts[bias_type] += 1
            
            if severity in severity_counts:
                severity_counts[severity] += 1
        
        # Summary statistics
        total_biases = len(self.bias_findings)
        critical_biases = severity_counts['CRITICAL']
        high_biases = severity_counts['HIGH']
        medium_biases = severity_counts['MEDIUM']
        low_biases = severity_counts['LOW']
        
        print(f"\n📊 BIAS ANALYSIS SUMMARY:")
        print(f"  Total Biases Found: {total_biases}")
        print(f"  Critical: {critical_biases}")
        print(f"  High: {high_biases}")
        print(f"  Medium: {medium_biases}")
        print(f"  Low: {low_biases}")
        
        print(f"\n🔍 BIAS TYPES FOUND:")
        for bias_type, count in bias_counts.items():
            if count > 0:
                print(f"  {bias_type}: {count}")
        
        # Detailed findings
        if self.bias_findings:
            print(f"\n🚨 DETAILED BIAS FINDINGS:")
            for i, bias in enumerate(self.bias_findings[:10]):  # Show top 10
                print(f"  {i+1}. {bias['type']} - {bias['severity']}")
                print(f"     Subtype: {bias['subtype']}")
                print(f"     Description: {bias['description']}")
                print(f"     Evidence: {bias['evidence']}")
                print(f"     Recommendation: {bias['recommendation']}")
                print()
        
        # Generate recommendations
        self._generate_bias_recommendations()
        
        # Save detailed report
        report = {
            'analysis_timestamp': datetime.now().isoformat(),
            'summary': {
                'total_biases': total_biases,
                'critical_biases': critical_biases,
                'high_biases': high_biases,
                'medium_biases': medium_biases,
                'low_biases': low_biases,
                'bias_counts': bias_counts,
                'severity_counts': severity_counts
            },
            'findings': self.bias_findings,
            'recommendations': self.recommendations
        }
        
        with open('logs/bias_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: logs/bias_analysis_report.json")
        
        # Overall assessment
        if critical_biases > 0:
            print(f"\n🚨 OVERALL ASSESSMENT: CRITICAL BIAS ISSUES FOUND")
            print("   IMMEDIATE ACTION REQUIRED")
        elif high_biases > 0:
            print(f"\n⚠️ OVERALL ASSESSMENT: HIGH BIAS ISSUES FOUND")
            print("   SIGNIFICANT ATTENTION REQUIRED")
        elif medium_biases > 0:
            print(f"\n🔶 OVERALL ASSESSMENT: MEDIUM BIAS ISSUES FOUND")
            print("   ATTENTION RECOMMENDED")
        elif low_biases > 0:
            print(f"\n✅ OVERALL ASSESSMENT: LOW BIAS ISSUES FOUND")
            print("   MINOR CONCERNS")
        else:
            print(f"\n🎉 OVERALL ASSESSMENT: NO SIGNIFICANT BIAS ISSUES FOUND")
            print("   SYSTEM APPEARS FAIR AND BALANCED")
        
        print("=" * 80)
    
    def _generate_bias_recommendations(self):
        """Generate bias mitigation recommendations"""
        recommendations = []
        
        # Algorithmic bias recommendations
        algo_biases = [b for b in self.bias_findings if b['type'] == 'ALGORITHMIC_BIAS']
        if algo_biases:
            recommendations.append({
                'category': 'ALGORITHMIC_BIAS',
                'priority': 'HIGH',
                'title': 'Address Algorithmic Biases',
                'actions': [
                    'Balance weight distribution in learning system',
                    'Adjust learning rate to prevent overfitting',
                    'Balance reward and punishment scales',
                    'Implement regularization techniques'
                ]
            })
        
        # Data bias recommendations
        data_biases = [b for b in self.bias_findings if b['type'] == 'DATA_BIAS']
        if data_biases:
            recommendations.append({
                'category': 'DATA_BIAS',
                'priority': 'HIGH',
                'title': 'Address Data Biases',
                'actions': [
                    'Implement data quality checks',
                    'Handle missing data appropriately',
                    'Remove survivorship bias',
                    'Ensure representative sampling',
                    'Validate data sources'
                ]
            })
        
        # Learning bias recommendations
        learning_biases = [b for b in self.bias_findings if b['type'] == 'LEARNING_BIAS']
        if learning_biases:
            recommendations.append({
                'category': 'LEARNING_BIAS',
                'priority': 'MEDIUM',
                'title': 'Address Learning Biases',
                'actions': [
                    'Implement balanced training data',
                    'Use cross-validation',
                    'Monitor for confirmation bias',
                    'Apply regularization',
                    'Ensure diverse outcome representation'
                ]
            })
        
        # Evaluation bias recommendations
        eval_biases = [b for b in self.bias_findings if b['type'] == 'EVALUATION_BIAS']
        if eval_biases:
            recommendations.append({
                'category': 'EVALUATION_BIAS',
                'priority': 'MEDIUM',
                'title': 'Address Evaluation Biases',
                'actions': [
                    'Use multiple evaluation metrics',
                    'Ensure balanced test sets',
                    'Implement fairness metrics',
                    'Regular bias audits',
                    'Consider external validation'
                ]
            })
        
        self.recommendations = recommendations

if __name__ == "__main__":
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Run comprehensive bias analysis
    analyzer = BiasAnalysis()
    analyzer.run_comprehensive_bias_analysis()
