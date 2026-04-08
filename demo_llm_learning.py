"""
Demonstration of LLM Learning System with Visible Learning Events
This script shows the learning system actively learning from decisions
"""

import numpy as np
import pandas as pd
import json
from datetime import datetime
from adaptive_module.llm_learning_engine import LLMLearningEngine, DecisionOutcome

def create_demo_market_data():
    """Create demonstration market data for learning"""
    np.random.seed(42)
    
    # Generate 100 data points with different market conditions
    dates = pd.date_range(start='2022-01-01', periods=100, freq='D')
    
    data = []
    for i, date in enumerate(dates):
        # Create different market scenarios
        if i < 25:
            # Bull market - good for buy decisions
            price_change = np.random.normal(2, 1)  # Positive returns
            sentiment = np.random.uniform(0.3, 0.8)
            volatility = np.random.uniform(10, 20)
        elif i < 50:
            # Bear market - good for sell decisions  
            price_change = np.random.normal(-2, 1)  # Negative returns
            sentiment = np.random.uniform(-0.8, -0.3)
            volatility = np.random.uniform(20, 30)
        elif i < 75:
            # Sideways market - good for hold decisions
            price_change = np.random.normal(0, 0.5)  # Small returns
            sentiment = np.random.uniform(-0.2, 0.2)
            volatility = np.random.uniform(15, 25)
        else:
            # Volatile market - mixed conditions
            price_change = np.random.normal(0, 3)  # High volatility
            sentiment = np.random.uniform(-0.5, 0.5)
            volatility = np.random.uniform(25, 40)
        
        data.append({
            'date': date,
            'price_change': price_change,
            'sentiment': sentiment,
            'volatility': volatility,
            'rsi': np.random.uniform(20, 80),
            'volume_ratio': np.random.uniform(0.5, 2.0)
        })
    
    return pd.DataFrame(data)

def demo_llm_learning():
    """Demonstrate LLM learning system with visible learning events"""
    print("🧠 LLM Learning System Demonstration")
    print("=" * 60)
    
    # Initialize learning engine
    learning_engine = LLMLearningEngine()
    
    # Create demo market data
    market_data = create_demo_market_data()
    
    print(f"📊 Generated {len(market_data)} market scenarios for learning")
    print(f"🎯 Initial Model Version: {learning_engine.model_version}")
    
    # Track learning progress
    learning_stats = {
        'total_decisions': 0,
        'correct_decisions': 0,
        'incorrect_decisions': 0,
        'partial_decisions': 0,
        'learning_events': []
    }
    
    print("\n🔄 Running Learning Demonstration...")
    print("-" * 60)
    
    # Process each market scenario
    for i, row in market_data.iterrows():
        # Determine optimal action based on market conditions
        if row['price_change'] > 1.5 and row['sentiment'] > 0.3:
            optimal_action = 'buy'
            expected_result = row['price_change']
        elif row['price_change'] < -1.5 and row['sentiment'] < -0.3:
            optimal_action = 'sell'
            expected_result = row['price_change']
        else:
            optimal_action = 'hold'
            expected_result = 0
        
        # Make decision (simulate algorithm decision)
        if i < 33:
            # Phase 1: Algorithm makes mistakes
            algorithm_action = 'sell' if optimal_action == 'buy' else 'buy' if optimal_action == 'sell' else 'buy'
        elif i < 66:
            # Phase 2: Algorithm starts learning
            if np.random.random() < 0.7:  # 70% chance of correct action
                algorithm_action = optimal_action
            else:
                algorithm_action = 'sell' if optimal_action == 'buy' else 'buy' if optimal_action == 'sell' else 'buy'
        else:
            # Phase 3: Algorithm has learned
            algorithm_action = optimal_action
        
        # Create context for learning
        context = {
            'market_growth': row['price_change'],
            'sentiment_score': row['sentiment'],
            'market_volatility': row['volatility'],
            'negative_sentiment': max(0, (1 - (row['sentiment'] + 1) / 2) * 100),
            'trend_demand': row['volume_ratio'] * 50,
            'competitor_price_increase': np.random.uniform(0, 20),
            'market_share': np.random.uniform(10, 30),
            'competitor_activity_count': np.random.randint(1, 10)
        }
        
        # Create technical indicators
        technical_indicators = {
            'rsi': row['rsi'],
            'ma_20': 100,
            'ma_50': 95
        }
        
        # Simulate rule triggers
        if algorithm_action == 'buy' and row['sentiment'] > 0.3:
            rule_triggers = ['high_growth_investment', 'positive_sentiment_investment']
        elif algorithm_action == 'sell' and row['sentiment'] < -0.3:
            rule_triggers = ['volatility_risk_alert', 'negative_sentiment_alert']
        else:
            rule_triggers = ['high_demand_opportunity']
        
        # Analyze decision outcome
        experience = learning_engine.analyze_decision_outcome(
            context=context,
            decision_type='trading',
            action_taken=algorithm_action,
            confidence=0.8,
            market_state={'scenario': i},
            technical_indicators=technical_indicators,
            rule_triggers=rule_triggers,
            actual_result=row['price_change'],
            expected_result=expected_result
        )
        
        if experience:
            # Learn from experience
            learning_engine.learn_from_experience(experience)
            
            # Update stats
            learning_stats['total_decisions'] += 1
            if experience.outcome == DecisionOutcome.CORRECT:
                learning_stats['correct_decisions'] += 1
            elif experience.outcome == DecisionOutcome.INCORRECT:
                learning_stats['incorrect_decisions'] += 1
            else:
                learning_stats['partial_decisions'] += 1
            
            # Store learning event
            learning_stats['learning_events'].append({
                'scenario': i + 1,
                'optimal_action': optimal_action,
                'algorithm_action': algorithm_action,
                'outcome': experience.outcome.value,
                'reward': experience.reward,
                'punishment': experience.punishment,
                'market_condition': row['price_change']
            })
            
            # Show key learning events
            if experience.outcome != DecisionOutcome.PARTIAL or i % 10 == 0:
                print(f"Scenario {i+1:3d}: {algorithm_action:4s} | "
                      f"Outcome: {experience.outcome.value:9s} | "
                      f"Reward: {experience.reward:6.2f} | "
                      f"Punishment: {experience.punishment:7.2f} | "
                      f"Market: {row['price_change']:+6.2f}")
    
    # Calculate learning metrics
    print("\n📊 LEARNING RESULTS")
    print("=" * 60)
    
    total = learning_stats['total_decisions']
    if total > 0:
        accuracy = learning_stats['correct_decisions'] / total * 100
        print(f"Total Decisions: {total}")
        print(f"Correct Decisions: {learning_stats['correct_decisions']} ({accuracy:.1f}%)")
        print(f"Incorrect Decisions: {learning_stats['incorrect_decisions']} ({learning_stats['incorrect_decisions']/total*100:.1f}%)")
        print(f"Partial Decisions: {learning_stats['partial_decisions']} ({learning_stats['partial_decisions']/total*100:.1f}%)")
        
        # Show learning progress
        early_correct = sum(1 for event in learning_stats['learning_events'][:20] 
                           if event['outcome'] == 'correct')
        recent_correct = sum(1 for event in learning_stats['learning_events'][-20:] 
                            if event['outcome'] == 'correct')
        
        early_accuracy = early_correct / min(20, len(learning_stats['learning_events'][:20])) * 100
        recent_accuracy = recent_correct / min(20, len(learning_stats['learning_events'][-20:])) * 100
        
        print(f"\n📈 Learning Progress:")
        print(f"Early Accuracy (first 20): {early_accuracy:.1f}%")
        print(f"Recent Accuracy (last 20): {recent_accuracy:.1f}%")
        print(f"Improvement: {recent_accuracy - early_accuracy:+.1f}%")
    
    print(f"\n🧠 Model Evolution:")
    print(f"Initial Version: 1")
    print(f"Final Version: {learning_engine.model_version}")
    print(f"Models Updated: {learning_engine.model_version - 1}")
    
    # Show final adaptive weights
    print(f"\n⚖️ Final Adaptive Weights:")
    for feature, weight in learning_engine.learning_weights.items():
        print(f"  {feature}: {weight:.3f}")
    
    # Show rule performance
    print(f"\n🎯 Rule Performance:")
    for rule_id, perf in learning_engine.rule_performance.items():
        if perf['usage_count'] > 0:
            print(f"  {rule_id}: {perf['accuracy']:.3f} accuracy ({perf['usage_count']} uses)")
    
    # Generate learning recommendations
    metrics = learning_engine.get_learning_metrics()
    if metrics:
        print(f"\n💡 Learning Recommendations:")
        recommendations = learning_engine._generate_learning_recommendations()
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"  {i}. {rec}")
    
    # Save detailed results
    results = {
        'learning_statistics': learning_stats,
        'learning_metrics': {
            'accuracy_rate': metrics.accuracy_rate if metrics else 0,
            'learning_progress': metrics.learning_progress if metrics else 0,
            'model_version': learning_engine.model_version,
            'total_experiences': len(learning_engine.experiences)
        },
        'adaptive_weights': learning_engine.learning_weights,
        'rule_performance': learning_engine.rule_performance,
        'demonstration_completed': True
    }
    
    with open('llm_learning_demo_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Learning Demonstration Completed!")
    print(f"📄 Results saved to 'llm_learning_demo_results.json'")
    print(f"🧠 Model learned from {learning_stats['total_decisions']} decisions")
    print(f"🎯 Final accuracy: {accuracy:.1f}%")
    
    return learning_engine, learning_stats

if __name__ == "__main__":
    demo_llm_learning()
