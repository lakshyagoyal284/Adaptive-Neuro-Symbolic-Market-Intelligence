"""
Test Bias Fix Verification
Verify that the weight distribution bias fix is working correctly
"""

import os
import sys
import json
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

def test_bias_fix():
    """Test the bias fix by verifying weight normalization"""
    print("🔍 TESTING BIAS FIX VERIFICATION")
    print("=" * 80)
    print("🔍 Verifying weight distribution bias fix...")
    print("=" * 80)
    
    try:
        # Import the learning engine
        from adaptive_module.llm_learning_engine import LLMLearningEngine, DecisionExperience, DecisionOutcome
        
        # Initialize learning engine
        print("\n📊 INITIALIZING LEARNING ENGINE...")
        engine = LLMLearningEngine()
        
        print("📊 WEIGHT DISTRIBUTION BEFORE LEARNING:")
        total_weight_before = sum(engine.learning_weights.values())
        for feature, weight in engine.learning_weights.items():
            print(f"  {feature}: {weight:.4f} ({weight/total_weight_before*100:.1f}%)")
        
        print(f"Total weight: {total_weight_before:.4f}")
        
        # Calculate weight ratio before
        max_weight_before = max(engine.learning_weights.values())
        min_weight_before = min(engine.learning_weights.values())
        weight_ratio_before = max_weight_before / min_weight_before if min_weight_before > 0 else float('inf')
        
        print(f"Weight ratio (max/min): {weight_ratio_before:.2f}")
        
        # Create a test experience to trigger learning
        print("\n📊 CREATING TEST EXPERIENCE...")
        experience = DecisionExperience(
            timestamp=datetime.now(),
            context={
                'trend_demand': 80.0,
                'volume_activity': 120.0,
                'profit_potential': 5.0,
                'risk_reward_ratio': 2.0
            },
            decision_type='bias_test',
            action_taken='buy',
            confidence=0.9,
            outcome=DecisionOutcome.INCORRECT,
            reward=0.0,
            punishment=5.0,
            market_state={'test': 'bias_fix'},
            technical_indicators={'rsi': 70},
            rule_triggers=['test_rule'],
            actual_result=-3.0,
            expected_result=3.0,
            error_magnitude=6.0
        )
        
        # Apply learning (this should trigger weight normalization)
        print("\n📊 APPLYING LEARNING (with weight normalization)...")
        engine.learn_from_experience(experience)
        
        print("\n📊 WEIGHT DISTRIBUTION AFTER LEARNING:")
        total_weight_after = sum(engine.learning_weights.values())
        for feature, weight in engine.learning_weights.items():
            print(f"  {feature}: {weight:.4f} ({weight/total_weight_after*100:.1f}%)")
        
        print(f"Total weight: {total_weight_after:.4f}")
        
        # Calculate weight ratio after
        max_weight_after = max(engine.learning_weights.values())
        min_weight_after = min(engine.learning_weights.values())
        weight_ratio_after = max_weight_after / min_weight_after if min_weight_after > 0 else float('inf')
        
        print(f"Weight ratio (max/min): {weight_ratio_after:.2f}")
        
        # Verify the fix
        print("\n🎉 BIAS FIX VERIFICATION RESULTS:")
        print("=" * 80)
        
        # Check if weights are normalized (sum to 1)
        if abs(total_weight_after - 1.0) < 0.01:
            print("✅ Weights are normalized (sum to 1.0)")
        else:
            print("❌ Weights are not normalized")
        
        # Check if weight ratio is reasonable
        if weight_ratio_after <= 5.0:
            print("✅ Weight distribution is balanced (ratio <= 5:1)")
        elif weight_ratio_after <= 10.0:
            print("⚠️ Weight distribution is moderately balanced (ratio <= 10:1)")
        else:
            print("❌ Weight distribution is still biased (ratio > 10:1)")
        
        # Check if no weight is too small
        min_weight_pct = min_weight_after * 100
        if min_weight_pct >= 5.0:
            print("✅ Minimum weight threshold met (>= 5%)")
        else:
            print("❌ Minimum weight threshold not met (< 5%)")
        
        # Check if no weight is too large
        max_weight_pct = max_weight_after * 100
        if max_weight_pct <= 25.0:
            print("✅ Maximum weight threshold met (<= 25%)")
        else:
            print("❌ Maximum weight threshold not met (> 25%)")
        
        # Overall assessment
        print(f"\n📊 IMPROVEMENT SUMMARY:")
        print(f"  Weight ratio before: {weight_ratio_before:.2f}")
        print(f"  Weight ratio after: {weight_ratio_after:.2f}")
        print(f"  Improvement: {(weight_ratio_before - weight_ratio_after):.2f}")
        
        if weight_ratio_after < weight_ratio_before:
            print("✅ Weight distribution bias has been REDUCED")
        else:
            print("❌ Weight distribution bias has NOT been reduced")
        
        # Final verdict
        if weight_ratio_after <= 5.0 and min_weight_pct >= 5.0 and max_weight_pct <= 25.0:
            print("\n🎉 BIAS FIX SUCCESSFUL!")
            print("✅ Weight distribution bias has been fixed")
            print("✅ System is now fair and balanced")
            return True
        else:
            print("\n⚠️ BIAS FIX PARTIALLY SUCCESSFUL")
            print("⚠️ Some bias issues remain")
            return False
        
    except Exception as e:
        print(f"❌ Error testing bias fix: {e}")
        return False

if __name__ == "__main__":
    success = test_bias_fix()
    
    print("\n" + "=" * 80)
    if success:
        print("🎉 BIAS FIX VERIFICATION PASSED!")
        print("=" * 80)
        print("✅ Weight distribution bias has been successfully fixed")
        print("✅ Learning engine now uses normalized weights")
        print("✅ System is ready for unbiased trading")
    else:
        print("❌ BIAS FIX VERIFICATION FAILED")
        print("=" * 80)
        print("❌ Weight distribution bias fix needs adjustment")
        print("❌ System may still have bias issues")
    
    print("=" * 80)
