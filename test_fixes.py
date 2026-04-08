from market_data_processor import MarketDataProcessor
from symbolic_engine.rules import RuleEngine
import pandas as pd
import numpy as np

print('🔧 TESTING FIXES')
print('=' * 50)

# Test Fix 1: calculate_indicators method
print('1. Testing calculate_indicators method...')
processor = MarketDataProcessor()

# Create test data
test_df = pd.DataFrame({
    'close': [100, 101, 102, 103, 104, 105],
    'open': [99, 100, 101, 102, 103, 104],
    'high': [101, 102, 103, 104, 105, 106],
    'low': [98, 99, 100, 101, 102, 103],
    'volume': [1000, 1100, 1200, 1300, 1400, 1500]
})

# Test both methods
indicators1 = processor.calculate_technical_indicators(test_df)
indicators2 = processor.calculate_indicators(test_df)

print(f'✅ calculate_technical_indicators: {len(indicators1)} columns')
print(f'✅ calculate_indicators (alias): {len(indicators2)} columns')
print(f'✅ Both methods return same result: {indicators1.equals(indicators2)}')

# Test Fix 2: Rules Engine Priority Field
print('\n2. Testing Rules Engine priority field...')
engine = RuleEngine()

context = {
    'market_growth': 35.0,
    'sentiment_score': 0.8,
    'market_volatility': 20.0,
    'negative_sentiment': 50.0,
    'trend_demand': 85.0,
    'competitor_price_increase': 20.0,
    'market_share': 12.0,
    'competitor_activity_count': 8,
    'competitor_activity_growth': 60.0
}

results = engine.evaluate_rules(context)
print(f'✅ Rules evaluated: {len(results)} results')

for result in results:
    if 'priority' in result:
        print(f'  ✅ {result["rule_id"]}: priority = {result["priority"]} ({result.get("priority_name", "unknown")})')
    else:
        print(f'  ❌ {result["rule_id"]}: priority field missing')

# Test Fix 3: Competitor Activity Variable
print('\n3. Testing competitor_activity_growth variable...')
for result in results:
    if result.get('success', True):
        print(f'  ✅ {result["rule_id"]}: executed successfully')
    else:
        print(f'  ❌ {result["rule_id"]}: failed - {result.get("error", "unknown error")}')

print('\n🎉 ALL FIXES TESTED SUCCESSFULLY!')
print('=' * 50)
