"""
Deep Testing Round 2 - Testing each component 50 more times
"""

import os
import sys
import traceback
import importlib.util
import inspect
import json
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from pathlib import Path

class DeepTestRound2:
    """Second round of deep testing"""
    
    def __init__(self):
        self.test_results = {}
        self.error_log = []
        self.success_log = []
        self.test_count = 0
        self.max_tests = 50
        
        # Setup logging
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/deep_test_round2.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def run_round2_test(self):
        """Run second round of deep testing"""
        print("🔥 DEEP TESTING ROUND 2")
        print("=" * 80)
        print("🧪 Testing each component 50 more times")
        print("📊 Maximum validation continued")
        print("=" * 80)
        
        # Test each component 50 more times
        self.test_llm_engine_50x()
        self.test_rules_engine_50x()
        self.test_decision_engine_50x()
        self.test_backtester_50x()
        self.test_aggressive_backtester_50x()
        self.test_data_processor_50x()
        self.test_file_contents_50x()
        self.test_symbolic_logic_50x()
        self.test_learning_adaptation_50x()
        self.test_integration_flow_50x()
        
        # Generate final report
        self.generate_round2_report()
        
    def test_llm_engine_50x(self):
        """Test LLM engine 50 more times"""
        print("\n🤖 TESTING LLM ENGINE ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                from adaptive_module.llm_learning_engine import LLMLearningEngine, DecisionExperience, DecisionOutcome
                from datetime import datetime
                
                # Test initialization with different model paths
                engine = LLMLearningEngine(f"models/test_model_round2_{i}.pkl")
                
                # Test all core methods
                assert hasattr(engine, 'analyze_decision_outcome'), "Missing analyze_decision_outcome"
                assert hasattr(engine, 'get_learning_metrics'), "Missing get_learning_metrics"
                assert hasattr(engine, '_save_model'), "Missing _save_model"
                assert hasattr(engine, '_load_model'), "Missing _load_model"
                
                # Test weight structure
                assert len(engine.learning_weights) >= 5, "Insufficient learning weights"
                
                # Test each weight individually
                for weight_name, weight_value in engine.learning_weights.items():
                    assert isinstance(weight_value, (int, float)), f"Weight {weight_name} must be numeric"
                    assert 0 <= weight_value <= 1, f"Weight {weight_name} must be between 0 and 1"
                
                # Test experience creation with different outcomes
                outcomes = [DecisionOutcome.CORRECT, DecisionOutcome.INCORRECT, DecisionOutcome.PARTIAL]
                actions = ['buy', 'sell', 'hold']
                
                for outcome in outcomes:
                    for action in actions:
                        experience = DecisionExperience(
                            timestamp=datetime.now(),
                            context={
                                'market_growth': np.random.uniform(-5, 5),
                                'sentiment_score': np.random.uniform(-1, 1),
                                'market_volatility': np.random.uniform(10, 30),
                                'trend_demand': np.random.uniform(0, 100),
                                'volume_activity': np.random.uniform(0, 100)
                            },
                            decision_type=f'round2_test_{i}',
                            action_taken=action,
                            confidence=np.random.uniform(0.3, 0.9),
                            outcome=outcome,
                            reward=np.random.uniform(0, 3),
                            punishment=np.random.uniform(0, 5),
                            market_state={'test_round': 2},
                            technical_indicators={'rsi': np.random.uniform(20, 80)},
                            rule_triggers=[f'test_rule_{i}'],
                            actual_result=np.random.uniform(-5, 5),
                            expected_result=np.random.uniform(-5, 5),
                            error_magnitude=np.random.uniform(0, 5)
                        )
                        
                        # Test learning
                        old_version = engine.model_version
                        engine.learn_from_experience(experience)
                        
                        # Verify experience stored
                        assert len(engine.experiences) > 0, "Experience not stored"
                        
                        # Test metrics
                        metrics = engine.get_learning_metrics()
                        assert metrics is not None, "Metrics should not be None"
                        assert hasattr(metrics, 'total_decisions'), "Missing total_decisions"
                        assert hasattr(metrics, 'accuracy_rate'), "Missing accuracy_rate"
                
                self.success_log.append(f"LLM engine round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"LLM engine round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_rules_engine_50x(self):
        """Test rules engine 50 more times"""
        print("\n⚖️ TESTING RULES ENGINE ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                from symbolic_engine.rules import RuleEngine, MarketRule, RuleType, RulePriority, RuleStatus
                
                # Test initialization
                engine = RuleEngine()
                
                # Test all default rules exist
                expected_rules = [
                    'high_growth_investment',
                    'negative_sentiment_alert',
                    'competitor_price_response',
                    'high_demand_opportunity',
                    'low_market_share_alert',
                    'positive_sentiment_investment',
                    'volatility_risk_alert',
                    'competitor_activity_surge'
                ]
                
                for rule_id in expected_rules:
                    assert rule_id in engine.rules, f"Missing rule: {rule_id}"
                    rule = engine.rules[rule_id]
                    assert hasattr(rule, 'condition'), f"Rule {rule_id} missing condition"
                    assert hasattr(rule, 'action'), f"Rule {rule_id} missing action"
                    assert hasattr(rule, 'priority'), f"Rule {rule_id} missing priority"
                
                # Test rule evaluation with different contexts
                test_contexts = [
                    {
                        'market_growth': 35.0,
                        'sentiment_score': 0.8,
                        'market_volatility': 30.0,
                        'negative_sentiment': 50.0,
                        'trend_demand': 85.0,
                        'competitor_price_increase': 20.0,
                        'market_share': 12.0
                    },
                    {
                        'market_growth': -10.0,
                        'sentiment_score': -0.7,
                        'market_volatility': 40.0,
                        'negative_sentiment': 80.0,
                        'trend_demand': 25.0,
                        'competitor_price_increase': 5.0,
                        'market_share': 25.0
                    },
                    {
                        'market_growth': 15.0,
                        'sentiment_score': 0.2,
                        'market_volatility': 20.0,
                        'negative_sentiment': 30.0,
                        'trend_demand': 60.0,
                        'competitor_price_increase': 12.0,
                        'market_share': 18.0
                    }
                ]
                
                for context in test_contexts:
                    results = engine.evaluate_rules(context)
                    assert isinstance(results, list), "Rule results must be list"
                    
                    # Test each result
                    for result in results:
                        assert 'rule_id' in result, "Result missing rule_id"
                        assert 'action' in result, "Result missing action"
                        assert 'priority' in result, "Result missing priority"
                
                # Test rule statistics
                stats = engine.get_rule_statistics()
                assert stats is not None, "Statistics should not be None"
                assert 'total_rules' in stats, "Missing total_rules in statistics"
                
                # Test rule categories
                categories = engine.rule_categories
                assert isinstance(categories, dict), "Categories must be dict"
                
                self.success_log.append(f"Rules engine round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"Rules engine round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_decision_engine_50x(self):
        """Test decision engine 50 more times"""
        print("\n🧠 TESTING DECISION ENGINE ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                from symbolic_engine.decision_engine import DecisionEngine
                
                # Test initialization
                engine = DecisionEngine()
                
                # Test core methods
                assert hasattr(engine, 'make_decision'), "Missing make_decision method"
                assert hasattr(engine, 'rules_engine'), "Missing rules_engine"
                
                # Test decision making with different contexts
                test_contexts = [
                    {
                        'market_growth': 25.0,
                        'sentiment_score': 0.6,
                        'market_volatility': 18.0,
                        'negative_sentiment': 35.0,
                        'trend_demand': 70.0
                    },
                    {
                        'market_growth': -15.0,
                        'sentiment_score': -0.8,
                        'market_volatility': 35.0,
                        'negative_sentiment': 65.0,
                        'trend_demand': 20.0
                    }
                ]
                
                for context in test_contexts:
                    # Test AI insights generation
                    ai_insights = {
                        'sentiment_analysis': {
                            'average_sentiment': context['sentiment_score'],
                            'overall_trend': 'improving' if context['sentiment_score'] > 0 else 'declining'
                        },
                        'trend_analysis': {
                            'volatility': context['market_volatility'] / 100,
                            'growth_rate': context['market_growth']
                        }
                    }
                    
                    # Test decision making
                    decisions = engine.make_decision(context, ai_insights)
                    assert isinstance(decisions, list), "Decisions must be list"
                    
                    # Test each decision
                    for decision in decisions:
                        assert hasattr(decision, 'decision_type'), "Decision missing decision_type"
                        assert hasattr(decision, 'confidence'), "Decision missing confidence"
                        assert hasattr(decision, 'title'), "Decision missing title"
                        assert hasattr(decision, 'description'), "Decision missing description"
                        
                        # Test confidence range
                        assert 0 <= decision.confidence <= 1, "Confidence must be between 0 and 1"
                
                self.success_log.append(f"Decision engine round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"Decision engine round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_backtester_50x(self):
        """Test backtester 50 more times"""
        print("\n📈 TESTING BACKTESTER ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                from backtesting import MarketBacktester
                
                # Test initialization
                bt = MarketBacktester()
                
                # Test core attributes
                assert hasattr(bt, 'decision_history'), "Missing decision_history"
                assert hasattr(bt, 'market_data_history'), "Missing market_data_history"
                assert hasattr(bt, 'portfolio_value'), "Missing portfolio_value"
                assert hasattr(bt, 'trades'), "Missing trades"
                
                # Test historical data generation
                data = bt.generate_historical_data(days=20)
                assert isinstance(data, list), "Historical data must be list"
                assert len(data) == 20, f"Expected 20 days, got {len(data)}"
                
                # Test data structure
                for day_data in data:
                    assert isinstance(day_data, dict), "Each day must be dict"
                    assert 'date' in day_data, "Missing date"
                    assert 'market_growth' in day_data, "Missing market_growth"
                    assert 'sentiment_score' in day_data, "Missing sentiment_score"
                    assert 'market_volatility' in day_data, "Missing market_volatility"
                    
                    # Test data types
                    assert isinstance(day_data['market_growth'], (int, float)), "market_growth must be numeric"
                    assert isinstance(day_data['sentiment_score'], (int, float)), "sentiment_score must be numeric"
                    assert isinstance(day_data['market_volatility'], (int, float)), "market_volatility must be numeric"
                
                # Test backtest execution
                results = bt.run_backtest(days=5, initial_capital=5000)
                assert results is not None, "Backtest results cannot be None"
                
                # Test result attributes
                assert hasattr(results, 'total_decisions'), "Missing total_decisions"
                assert hasattr(results, 'successful_decisions'), "Missing successful_decisions"
                assert hasattr(results, 'failed_decisions'), "Missing failed_decisions"
                assert hasattr(results, 'success_rate'), "Missing success_rate"
                
                self.success_log.append(f"Backtester round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"Backtester round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_aggressive_backtester_50x(self):
        """Test aggressive backtester 50 more times"""
        print("\n💰 TESTING AGGRESSIVE BACKTESTER ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                import aggressive_profit_backtester
                
                # Test initialization
                backtester = aggressive_profit_backtester.AggressiveProfitBacktester()
                
                # Test signal generation
                import pandas as pd
                test_data = pd.DataFrame({
                    'close': [100 + j for j in range(10)],
                    'volume': [1000 + j*100 for j in range(10)],
                    'high': [101 + j for j in range(10)],
                    'low': [99 + j for j in range(10)],
                    'price_change_pct': [np.random.uniform(-2, 2) for _ in range(10)],
                    'rsi': [np.random.uniform(20, 80) for _ in range(10)],
                    'volume_ratio': [np.random.uniform(0.5, 2.0) for _ in range(10)],
                    'volatility': [np.random.uniform(10, 30) for _ in range(10)]
                })
                
                # Test signal generation for different indices
                for index in range(2, 8):
                    signal = backtester._generate_aggressive_signal("TEST", test_data, index)
                    assert isinstance(signal, dict), "Signal must be dict"
                    assert 'signal' in signal, "Signal missing 'signal' key"
                    assert 'confidence' in signal, "Signal missing 'confidence' key"
                    assert signal['signal'] in ['buy', 'sell', 'hold'], f"Invalid signal: {signal['signal']}"
                    assert 0 <= signal['confidence'] <= 1, f"Invalid confidence: {signal['confidence']}"
                
                # Test learning integration
                context = {
                    'market_growth': 1.5,
                    'sentiment_score': 0.5,
                    'market_volatility': 20.0,
                    'trend_demand': 60.0,
                    'volume_activity': 40.0,
                    'profit_potential': 2.0,
                    'risk_reward_ratio': 1.5
                }
                
                signal = {'signal': 'buy', 'confidence': 0.7}
                learning_result = backtester._learn_from_aggressive_decision(
                    "TEST", signal, 100.0, datetime.now(), test_data, 5, context
                )
                
                # Test learning result
                if learning_result:
                    assert hasattr(learning_result, 'outcome'), "Learning result missing outcome"
                    assert hasattr(learning_result, 'reward'), "Learning result missing reward"
                    assert hasattr(learning_result, 'punishment'), "Learning result missing punishment"
                
                self.success_log.append(f"Aggressive backtester round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"Aggressive backtester round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_data_processor_50x(self):
        """Test data processor 50 more times"""
        print("\n📊 TESTING DATA PROCESSOR ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                import market_data_processor
                
                # Test initialization
                processor = market_data_processor.MarketDataProcessor()
                
                # Test core methods
                assert hasattr(processor, 'load_market_data'), "Missing load_market_data method"
                assert hasattr(processor, 'get_market_overview'), "Missing get_market_overview method"
                
                # Test data loading
                market_data = processor.load_market_data()
                assert isinstance(market_data, dict), "Market data must be dict"
                
                # Test data structure
                for symbol, df in market_data.items():
                    assert isinstance(df, pd.DataFrame), f"Data for {symbol} must be DataFrame"
                    assert len(df) > 0, f"Data for {symbol} is empty"
                    
                    # Test required columns
                    required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
                    for col in required_columns:
                        assert col in df.columns, f"Missing column {col} in {symbol} data"
                
                # Test market overview
                overview = processor.get_market_overview()
                assert isinstance(overview, dict), "Overview must be dict"
                assert 'total_symbols' in overview, "Missing total_symbols in overview"
                assert 'total_data_points' in overview, "Missing total_data_points in overview"
                
                self.success_log.append(f"Data processor round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"Data processor round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_file_contents_50x(self):
        """Test file contents 50 more times"""
        print("\n📁 TESTING FILE CONTENTS ROUND 2 (50x)")
        print("-" * 60)
        
        key_files = [
            "backtesting.py",
            "adaptive_module/llm_learning_engine.py",
            "symbolic_engine/rules.py",
            "symbolic_engine/decision_engine.py",
            "aggressive_profit_backtester.py",
            "market_data_processor.py"
        ]
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                for file_path in key_files:
                    # Test file exists
                    assert os.path.exists(file_path), f"File {file_path} not found"
                    
                    # Test file content
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        # Test content not empty
                        assert len(content) > 0, f"File {file_path} is empty"
                        
                        # Test has Python code
                        assert 'def' in content or 'class' in content, f"File {file_path} has no functions or classes"
                        
                        # Test has imports
                        assert 'import' in content, f"File {file_path} has no imports"
                        
                        # Test basic Python syntax
                        try:
                            compile(content, file_path, 'exec')
                        except SyntaxError as e:
                            raise AssertionError(f"Syntax error in {file_path}: {e}")
                
                self.success_log.append(f"File contents round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"File contents round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_symbolic_logic_50x(self):
        """Test symbolic logic 50 more times"""
        print("\n🧮 TESTING SYMBOLIC LOGIC ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                from symbolic_engine.rules import RuleEngine
                
                engine = RuleEngine()
                
                # Test rule conditions
                test_conditions = [
                    "market_growth > 30",
                    "negative_sentiment > 40",
                    "competitor_price_increase > 10",
                    "trend_demand > 70",
                    "market_share < 15",
                    "market_growth > 15 and sentiment_score > 0.3",
                    "market_volatility > 25"
                ]
                
                # Test each rule condition
                for rule_id, rule in engine.rules.items():
                    condition = rule.condition
                    
                    # Test condition is valid Python
                    try:
                        # Create safe namespace for evaluation
                        safe_namespace = {
                            'market_growth': 25.0,
                            'negative_sentiment': 35.0,
                            'competitor_price_increase': 12.0,
                            'trend_demand': 65.0,
                            'market_share': 18.0,
                            'sentiment_score': 0.5,
                            'market_volatility': 20.0
                        }
                        
                        # Evaluate condition
                        result = eval(condition, {"__builtins__": {}}, safe_namespace)
                        assert isinstance(result, bool), f"Condition {condition} must return boolean"
                        
                    except Exception as e:
                        raise AssertionError(f"Error evaluating condition {condition}: {e}")
                
                # Test rule actions
                for rule_id, rule in engine.rules.items():
                    action = rule.action
                    assert isinstance(action, str), f"Action for {rule_id} must be string"
                    assert len(action) > 0, f"Action for {rule_id} cannot be empty"
                
                self.success_log.append(f"Symbolic logic round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"Symbolic logic round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_learning_adaptation_50x(self):
        """Test learning adaptation 50 more times"""
        print("\n🔄 TESTING LEARNING ADAPTATION ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                from adaptive_module.llm_learning_engine import LLMLearningEngine, DecisionExperience, DecisionOutcome
                from datetime import datetime
                
                # Initialize engine
                engine = LLMLearningEngine()
                
                # Test initial weights
                initial_weights = engine.learning_weights.copy()
                assert len(initial_weights) >= 5, "Insufficient initial weights"
                
                # Test weight sum
                initial_sum = sum(initial_weights.values())
                assert abs(initial_sum - 1.0) < 0.01, f"Initial weights should sum to 1.0, got {initial_sum}"
                
                # Test learning with different scenarios
                scenarios = [
                    {
                        'context': {'market_growth': 3.0, 'sentiment_score': 0.8},
                        'outcome': DecisionOutcome.CORRECT,
                        'reward': 2.0,
                        'punishment': 0.0
                    },
                    {
                        'context': {'market_growth': -2.0, 'sentiment_score': -0.6},
                        'outcome': DecisionOutcome.INCORRECT,
                        'reward': 0.0,
                        'punishment': 3.0
                    },
                    {
                        'context': {'market_growth': 0.5, 'sentiment_score': 0.1},
                        'outcome': DecisionOutcome.PARTIAL,
                        'reward': 0.5,
                        'punishment': 0.5
                    }
                ]
                
                for scenario in scenarios:
                    experience = DecisionExperience(
                        timestamp=datetime.now(),
                        context=scenario['context'],
                        decision_type='adaptation_test',
                        action_taken='buy',
                        confidence=0.8,
                        outcome=scenario['outcome'],
                        reward=scenario['reward'],
                        punishment=scenario['punishment'],
                        market_state={},
                        technical_indicators={},
                        rule_triggers=['test'],
                        actual_result=1.0,
                        expected_result=1.0,
                        error_magnitude=0.0
                    )
                    
                    old_weights = engine.learning_weights.copy()
                    engine.learn_from_experience(experience)
                    new_weights = engine.learning_weights
                    
                    # Test weights changed
                    if scenario['reward'] > scenario['punishment']:
                        # For correct decisions, weights should be adjusted
                        assert new_weights != old_weights, "Weights should change after learning"
                    
                    # Test weights still sum to 1
                    new_sum = sum(new_weights.values())
                    assert abs(new_sum - 1.0) < 0.01, f"Weights should still sum to 1.0, got {new_sum}"
                
                # Test model evolution
                final_version = engine.model_version
                assert final_version >= 1, "Model version should be >= 1"
                
                # Test experience storage
                assert len(engine.experiences) > 0, "Experiences should be stored"
                
                # Test metrics
                metrics = engine.get_learning_metrics()
                assert metrics is not None, "Metrics should not be None"
                
                self.success_log.append(f"Learning adaptation round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"Learning adaptation round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def test_integration_flow_50x(self):
        """Test integration flow 50 more times"""
        print("\n🔗 TESTING INTEGRATION FLOW ROUND 2 (50x)")
        print("-" * 60)
        
        for i in range(self.max_tests):
            self.test_count += 1
            try:
                # Test complete integration
                from adaptive_module.llm_learning_engine import LLMLearningEngine
                from symbolic_engine.rules import RuleEngine
                from symbolic_engine.decision_engine import DecisionEngine
                from backtesting import MarketBacktester
                import market_data_processor
                
                # Initialize all components
                learning_engine = LLMLearningEngine()
                rules_engine = RuleEngine()
                decision_engine = DecisionEngine()
                backtester = MarketBacktester()
                data_processor = market_data_processor.MarketDataProcessor()
                
                # Test data flow
                market_data = data_processor.load_market_data()
                assert isinstance(market_data, dict), "Market data must be dict"
                
                # Test context creation
                if market_data:
                    first_symbol = list(market_data.keys())[0]
                    first_data = market_data[first_symbol]
                    
                    if len(first_data) > 0:
                        # Create context from real data
                        context = {
                            'market_growth': np.random.uniform(-5, 5),
                            'sentiment_score': np.random.uniform(-1, 1),
                            'market_volatility': np.random.uniform(10, 30),
                            'negative_sentiment': max(0, (1 - np.random.uniform(-1, 1)) * 50),
                            'trend_demand': np.random.uniform(0, 100),
                            'competitor_price_increase': np.random.uniform(0, 25),
                            'market_share': np.random.uniform(5, 35)
                        }
                        
                        # Test rule evaluation
                        rule_results = rules_engine.evaluate_rules(context)
                        assert isinstance(rule_results, list), "Rule results must be list"
                        
                        # Test decision making
                        ai_insights = {
                            'sentiment_analysis': {
                                'average_sentiment': context['sentiment_score'],
                                'overall_trend': 'improving' if context['sentiment_score'] > 0 else 'declining'
                            },
                            'trend_analysis': {
                                'volatility': context['market_volatility'] / 100,
                                'growth_rate': context['market_growth']
                            }
                        }
                        
                        decisions = decision_engine.make_decision(context, ai_insights)
                        assert isinstance(decisions, list), "Decisions must be list"
                        
                        # Test learning integration
                        if decisions:
                            decision = decisions[0]
                            experience = learning_engine.analyze_decision_outcome(
                                context=context,
                                decision_type='integration_test',
                                action_taken='buy',
                                confidence=0.7,
                                market_state={},
                                technical_indicators={},
                                rule_triggers=[rule['rule_id'] for rule in rule_results],
                                actual_result=1.0,
                                expected_result=0.8,
                                error_magnitude=0.2
                            )
                            
                            if experience:
                                learning_engine.learn_from_experience(experience)
                                assert len(learning_engine.experiences) > 0, "Experience not stored"
                
                # Test backtesting integration
                historical_data = backtester.generate_historical_data(days=5)
                assert isinstance(historical_data, list), "Historical data must be list"
                assert len(historical_data) == 5, "Should have 5 days of data"
                
                # Test complete flow success
                assert learning_engine.model_version >= 1, "Learning engine should have version"
                assert len(rules_engine.rules) > 0, "Rules engine should have rules"
                
                self.success_log.append(f"Integration flow round2 test {i+1}: PASSED")
                
            except Exception as e:
                error_msg = f"Integration flow round2 test {i+1}: FAILED - {str(e)}"
                self.error_log.append(error_msg)
                self.logger.error(error_msg)
                
    def generate_round2_report(self):
        """Generate round 2 report"""
        print("\n" + "=" * 80)
        print("🎯 DEEP TESTING ROUND 2 FINAL REPORT")
        print("=" * 80)
        
        total_tests = self.max_tests * 10  # 10 test categories * 50 tests each
        success_count = len(self.success_log)
        error_count = len(self.error_log)
        
        print(f"\n📊 ROUND 2 TEST SUMMARY:")
        print(f"  Total Tests Run: {self.test_count}")
        print(f"  Expected Tests: {total_tests}")
        print(f"  Successful Tests: {success_count}")
        print(f"  Failed Tests: {error_count}")
        print(f"  Success Rate: {(success_count / max(self.test_count, 1)) * 100:.2f}%")
        
        if error_count > 0:
            print(f"\n❌ ERRORS ENCOUNTERED:")
            for i, error in enumerate(self.error_log[:5]):  # Show first 5 errors
                print(f"  {i+1}. {error}")
            if len(self.error_log) > 5:
                print(f"  ... and {len(self.error_log) - 5} more errors")
        
        print(f"\n✅ SUCCESSFUL TESTS:")
        for i, success in enumerate(self.success_log[:5]):  # Show first 5 successes
            print(f"  {i+1}. {success}")
        if len(self.success_log) > 5:
            print(f"  ... and {len(self.success_log) - 5} more successes")
        
        # Save detailed report
        report = {
            'round': 2,
            'test_summary': {
                'total_tests': self.test_count,
                'expected_tests': total_tests,
                'successful_tests': success_count,
                'failed_tests': error_count,
                'success_rate': (success_count / max(self.test_count, 1)) * 100
            },
            'errors': self.error_log,
            'successes': self.success_log,
            'test_timestamp': datetime.now().isoformat()
        }
        
        with open('logs/deep_test_round2_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n📄 Detailed report saved to: logs/deep_test_round2_report.json")
        
        print(f"\n🎯 ROUND 2 ASSESSMENT:")
        if error_count == 0:
            print("  ✅ ALL TESTS PASSED - System is PERFECT!")
        elif error_count < 10:
            print("  ⚠️ MINOR ISSUES - System is mostly functional")
        elif error_count < 50:
            print("  🔶 MODERATE ISSUES - System needs attention")
        else:
            print("  ❌ MAJOR ISSUES - System requires significant fixes")
        
        print("=" * 80)

if __name__ == "__main__":
    # Create logs directory if not exists
    os.makedirs("logs", exist_ok=True)
    
    # Run round 2 test
    tester = DeepTestRound2()
    tester.run_round2_test()
