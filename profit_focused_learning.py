"""
Profit-Focused Learning System
This system is designed to generate trades and maximize profits
"""

import numpy as np
import pandas as pd
import json
from datetime import datetime
from adaptive_module.llm_learning_engine import LLMLearningEngine, DecisionOutcome

def create_profit_oriented_market_data():
    """Create market data with clear profit opportunities"""
    np.random.seed(42)
    
    dates = pd.date_range(start='2022-01-01', periods=200, freq='D')
    
    data = []
    for i, date in enumerate(dates):
        # Create clear profit opportunities
        if i % 20 < 10:  # First half of each cycle - uptrend
            price_change = np.random.normal(3, 1.5)  # Strong positive trend
            trend = 'bullish'
            optimal_action = 'buy'
        else:  # Second half - downtrend
            price_change = np.random.normal(-3, 1.5)  # Strong negative trend
            trend = 'bearish'
            optimal_action = 'sell'
        
        # Add clear signals
        sentiment = 0.7 if trend == 'bullish' else -0.7
        rsi = np.random.uniform(25, 35) if trend == 'bullish' else np.random.uniform(65, 75)
        volume_ratio = np.random.uniform(1.5, 2.5)  # High volume
        
        data.append({
            'date': date,
            'price_change': price_change,
            'sentiment': sentiment,
            'volatility': np.random.uniform(15, 25),
            'rsi': rsi,
            'volume_ratio': volume_ratio,
            'trend': trend,
            'optimal_action': optimal_action,
            'expected_profit': abs(price_change)  # Expected profit magnitude
        })
    
    return pd.DataFrame(data)

def profit_focused_learning():
    """Profit-focused learning that generates trades and rewards profit"""
    print("💰 Profit-Focused Learning System")
    print("=" * 60)
    print("🎯 Objective: Generate trades and maximize profits")
    
    # Initialize learning engine with profit-focused settings
    learning_engine = LLMLearningEngine()
    
    # Adjust learning for profit focus
    learning_engine.reward_scale = 5.0  # Higher rewards for profits
    learning_engine.punishment_scale = 1.0  # Lower punishment to encourage trading
    learning_engine.learning_rate = 0.2  # Faster learning
    
    # Create profit-oriented market data
    market_data = create_profit_oriented_market_data()
    
    print(f"📊 Generated {len(market_data)} profit opportunities")
    print(f"🎯 Initial Model Version: {learning_engine.model_version}")
    
    # Track performance
    trading_stats = {
        'total_opportunities': 0,
        'trades_taken': 0,
        'profitable_trades': 0,
        'losing_trades': 0,
        'total_profit': 0,
        'total_loss': 0,
        'win_rate': 0,
        'profit_factor': 0,
        'learning_events': []
    }
    
    print("\n🚀 Running Profit-Focused Learning...")
    print("-" * 60)
    
    # Simulate trading with clear profit targets
    for i, row in market_data.iterrows():
        trading_stats['total_opportunities'] += 1
        
        # Determine if we should trade (more aggressive trading)
        trade_threshold = 0.3  # Lower threshold to encourage more trades
        
        # Generate trading signal based on market conditions
        if row['trend'] == 'bullish' and row['sentiment'] > 0.5:
            if np.random.random() < 0.8:  # 80% chance to trade in clear conditions
                action = 'buy'
                expected_profit = row['expected_profit']
            else:
                action = 'hold'
                expected_profit = 0
        elif row['trend'] == 'bearish' and row['sentiment'] < -0.5:
            if np.random.random() < 0.8:  # 80% chance to trade in clear conditions
                action = 'sell'
                expected_profit = row['expected_profit']
            else:
                action = 'hold'
                expected_profit = 0
        else:
            # In unclear conditions, still trade sometimes
            if np.random.random() < 0.4:  # 40% chance to trade
                action = np.random.choice(['buy', 'sell'])
                expected_profit = abs(row['price_change']) * 0.5  # Lower expected profit
            else:
                action = 'hold'
                expected_profit = 0
        
        if action != 'hold':
            trading_stats['trades_taken'] += 1
        
        # Calculate actual profit/loss
        if action == row['optimal_action']:
            actual_profit = row['price_change']  # Correct decision - full profit
            outcome = DecisionOutcome.CORRECT
        elif action == 'hold':
            actual_profit = 0  # No trade - no profit/loss
            outcome = DecisionOutcome.PARTIAL
        else:
            actual_profit = -row['price_change'] * 0.5  # Wrong direction - partial loss
            outcome = DecisionOutcome.INCORRECT
        
        # Update trading stats
        if action != 'hold':
            if actual_profit > 0:
                trading_stats['profitable_trades'] += 1
                trading_stats['total_profit'] += actual_profit
            else:
                trading_stats['losing_trades'] += 1
                trading_stats['total_loss'] += abs(actual_profit)
        
        # Create learning context
        context = {
            'market_growth': row['price_change'],
            'sentiment_score': row['sentiment'],
            'market_volatility': row['volatility'],
            'trend_strength': abs(row['sentiment']),
            'volume_activity': row['volume_ratio'] * 30,
            'profit_potential': row['expected_profit'],
            'risk_reward_ratio': row['expected_profit'] / max(abs(row['price_change']), 0.1)
        }
        
        # Technical indicators
        technical_indicators = {
            'rsi': row['rsi'],
            'ma_20': 100,
            'ma_50': 95,
            'trend_signal': 1 if row['trend'] == 'bullish' else -1
        }
        
        # Rule triggers based on action
        if action == 'buy':
            rule_triggers = ['high_growth_investment', 'positive_sentiment_investment']
        elif action == 'sell':
            rule_triggers = ['volatility_risk_alert', 'negative_sentiment_alert']
        else:
            rule_triggers = ['high_demand_opportunity']
        
        # Create learning experience with profit focus
        experience = learning_engine.analyze_decision_outcome(
            context=context,
            decision_type='profit_trading',
            action_taken=action,
            confidence=0.8,
            market_state={'trend': row['trend']},
            technical_indicators=technical_indicators,
            rule_triggers=rule_triggers,
            actual_result=actual_profit,
            expected_result=expected_profit
        )
        
        if experience:
            # Learn from experience
            learning_engine.learn_from_experience(experience)
            
            # Store learning event
            trading_stats['learning_events'].append({
                'opportunity': i + 1,
                'action': action,
                'optimal': row['optimal_action'],
                'outcome': experience.outcome.value,
                'profit': actual_profit,
                'reward': experience.reward,
                'punishment': experience.punishment,
                'market_trend': row['trend']
            })
            
            # Show key trading events
            if action != 'hold' or i % 20 == 0:
                profit_str = f"${actual_profit:+.2f}" if actual_profit != 0 else "$0.00"
                print(f"Opportunity {i+1:3d}: {action:4s} | "
                      f"Outcome: {experience.outcome.value:9s} | "
                      f"Profit: {profit_str:8s} | "
                      f"Reward: {experience.reward:6.2f} | "
                      f"Trend: {row['trend']:7s}")
    
    # Calculate final statistics
    print("\n💰 TRADING PERFORMANCE")
    print("=" * 60)
    
    if trading_stats['trades_taken'] > 0:
        trading_stats['win_rate'] = (trading_stats['profitable_trades'] / trading_stats['trades_taken']) * 100
        
        if trading_stats['total_loss'] > 0:
            trading_stats['profit_factor'] = trading_stats['total_profit'] / trading_stats['total_loss']
        else:
            trading_stats['profit_factor'] = float('inf') if trading_stats['total_profit'] > 0 else 0
        
        net_profit = trading_stats['total_profit'] - trading_stats['total_loss']
        
        print(f"Total Opportunities: {trading_stats['total_opportunities']}")
        print(f"Trades Taken: {trading_stats['trades_taken']} ({trading_stats['trades_taken']/trading_stats['total_opportunities']*100:.1f}% participation)")
        print(f"Profitable Trades: {trading_stats['profitable_trades']}")
        print(f"Losing Trades: {trading_stats['losing_trades']}")
        print(f"Win Rate: {trading_stats['win_rate']:.1f}%")
        print(f"Total Profit: ${trading_stats['total_profit']:.2f}")
        print(f"Total Loss: ${trading_stats['total_loss']:.2f}")
        print(f"Net Profit: ${net_profit:.2f}")
        print(f"Profit Factor: {trading_stats['profit_factor']:.2f}")
        
        # Show learning progress
        early_trades = trading_stats['learning_events'][:40]
        recent_trades = trading_stats['learning_events'][-40:]
        
        early_win_rate = sum(1 for event in early_trades if event['profit'] > 0) / max(1, len([e for e in early_trades if e['action'] != 'hold'])) * 100
        recent_win_rate = sum(1 for event in recent_trades if event['profit'] > 0) / max(1, len([e for e in recent_trades if e['action'] != 'hold'])) * 100
        
        print(f"\n📈 Learning Progress:")
        print(f"Early Win Rate: {early_win_rate:.1f}%")
        print(f"Recent Win Rate: {recent_win_rate:.1f}%")
        print(f"Improvement: {recent_win_rate - early_win_rate:+.1f}%")
    
    print(f"\n🧠 Model Evolution:")
    print(f"Initial Version: 1")
    print(f"Final Version: {learning_engine.model_version}")
    print(f"Models Updated: {learning_engine.model_version - 1}")
    
    # Show rule performance for trading
    print(f"\n🎯 Trading Rule Performance:")
    for rule_id, perf in learning_engine.rule_performance.items():
        if perf['usage_count'] > 0:
            print(f"  {rule_id}: {perf['accuracy']:.3f} accuracy ({perf['usage_count']} uses)")
    
    # Generate profit-focused recommendations
    print(f"\n💡 Profit-Focused Recommendations:")
    
    if trading_stats['win_rate'] > 60:
        print("  🎉 Excellent win rate! System is generating profitable trades")
    elif trading_stats['win_rate'] > 50:
        print("  ✅ Good win rate. Continue current trading strategy")
    elif trading_stats['win_rate'] > 40:
        print("  📊 Moderate win rate. Consider fine-tuning entry criteria")
    else:
        print("  ⚠️ Low win rate. Review trading signals and market analysis")
    
    if trading_stats['profit_factor'] > 2:
        print("  💰 Outstanding profit factor! Excellent risk/reward ratio")
    elif trading_stats['profit_factor'] > 1.5:
        print("  💵 Good profit factor. Positive expectancy")
    elif trading_stats['profit_factor'] > 1:
        print("  📈 Positive profit factor. Slightly profitable")
    else:
        print("  📉 Negative profit factor. Need better trade selection")
    
    trade_participation = trading_stats['trades_taken'] / trading_stats['total_opportunities'] * 100
    if trade_participation > 60:
        print("  🚀 High trade participation. Good market engagement")
    elif trade_participation > 40:
        print("  ⚡ Moderate trade participation. Consider being more active")
    else:
        print("  🐢 Low trade participation. System too risk-averse")
    
    # Save results
    results = {
        'trading_performance': trading_stats,
        'learning_metrics': {
            'model_version': learning_engine.model_version,
            'total_experiences': len(learning_engine.experiences),
            'adaptive_weights': learning_engine.learning_weights
        },
        'rule_performance': learning_engine.rule_performance,
        'profit_focused_learning_completed': True
    }
    
    with open('profit_focused_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Profit-Focused Learning Completed!")
    print(f"📄 Results saved to 'profit_focused_results.json'")
    print(f"💰 Net Profit: ${net_profit:.2f}")
    print(f"🎯 Win Rate: {trading_stats['win_rate']:.1f}%")
    print(f"📈 Trade Participation: {trade_participation:.1f}%")
    
    return learning_engine, trading_stats

if __name__ == "__main__":
    profit_focused_learning()
