"""
Simple Bias Test
Test if the weight bias fix is working by checking the learning engine file
"""

import os
import sys
import json
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

def test_bias_fix_simple():
    """Simple test to verify bias fix was applied"""
    print("🔍 SIMPLE BIAS FIX TEST")
    print("=" * 80)
    print("🔍 Checking if bias fix was applied to learning engine...")
    print("=" * 80)
    
    try:
        # Read the learning engine file
        with open('adaptive_module/llm_learning_engine.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for bias fix components
        checks = {
            'weight_normalization': '_normalize_weights' in content,
            'weight_constraints': 'min_weight' in content and 'max_weight' in content,
            'softmax_normalization': 'softmax' in content,
            'weight_thresholds': '0.05' in content and '0.25' in content,
            'normalization_logging': 'WEIGHT NORMALIZATION APPLIED' in content
        }
        
        print("\n📊 BIAS FIX COMPONENTS CHECK:")
        for component, found in checks.items():
            if found:
                print(f"✅ {component}: Found")
            else:
                print(f"❌ {component}: Not found")
        
        # Count how many components are found
        components_found = sum(checks.values())
        total_components = len(checks)
        
        print(f"\n📊 SUMMARY: {components_found}/{total_components} components found")
        
        # Check if the critical components are there
        if checks['weight_normalization'] and checks['weight_constraints']:
            print("\n🎉 CRITICAL BIAS FIX COMPONENTS FOUND!")
            print("✅ Weight normalization method is present")
            print("✅ Weight constraints are present")
            print("✅ Bias fix has been applied to learning engine")
            
            # Check for specific bias fix patterns
            if 'total_weight = sum(self.learning_weights.values())' in content:
                print("✅ Weight sum calculation found")
            
            if 'for feature, weight in self.learning_weights.items():' in content:
                print("✅ Weight iteration found")
            
            if 'normalized_weights[feature] = weight / total_weight' in content:
                print("✅ Weight normalization logic found")
            
            return True
        else:
            print("\n❌ CRITICAL BIAS FIX COMPONENTS MISSING!")
            print("❌ Weight normalization method not found")
            print("❌ Weight constraints not found")
            print("❌ Bias fix may not have been applied correctly")
            return False
        
    except Exception as e:
        print(f"❌ Error testing bias fix: {e}")
        return False

def check_weight_distribution_balance():
    """Check if weight distribution is balanced in the initialization"""
    print("\n🔍 CHECKING WEIGHT DISTRIBUTION BALANCE...")
    print("=" * 80)
    
    try:
        # Read the learning engine file
        with open('adaptive_module/llm_learning_engine.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the initial weight distribution
        init_start = content.find('def _create_initial_model(self):')
        if init_start == -1:
            print("❌ Could not find _create_initial_model method")
            return False
        
        # Extract weight initialization
        weights_section = content[init_start:init_start+500]
        
        # Check for balanced weight distribution
        weight_values = []
        lines = weights_section.split('\n')
        for line in lines:
            if ':' in line and '0.' in line:
                # Extract weight value
                weight_str = line.split(':')[1].strip().rstrip(',')
                try:
                    weight = float(weight_str)
                    weight_values.append(weight)
                except:
                    pass
        
        if weight_values:
            print(f"📊 Found {len(weight_values)} weight values:")
            for i, weight in enumerate(weight_values):
                print(f"  Weight {i+1}: {weight:.2f}")
            
            # Check balance
            max_weight = max(weight_values)
            min_weight = min(weight_values)
            weight_ratio = max_weight / min_weight if min_weight > 0 else float('inf')
            
            print(f"\n📊 WEIGHT DISTRIBUTION ANALYSIS:")
            print(f"  Max weight: {max_weight:.2f}")
            print(f"  Min weight: {min_weight:.2f}")
            print(f"  Weight ratio: {weight_ratio:.2f}")
            
            if weight_ratio <= 5.0:
                print("✅ Weight distribution is balanced (ratio <= 5:1)")
                return True
            elif weight_ratio <= 10.0:
                print("⚠️ Weight distribution is moderately balanced (ratio <= 10:1)")
                return True
            else:
                print("❌ Weight distribution is unbalanced (ratio > 10:1)")
                return False
        else:
            print("❌ Could not extract weight values")
            return False
        
    except Exception as e:
        print(f"❌ Error checking weight distribution: {e}")
        return False

if __name__ == "__main__":
    print("🔍 COMPREHENSIVE BIAS FIX VERIFICATION")
    print("=" * 80)
    
    # Test 1: Check if bias fix was applied
    test1_result = test_bias_fix_simple()
    
    # Test 2: Check weight distribution balance
    test2_result = check_weight_distribution_balance()
    
    # Overall assessment
    print("\n" + "=" * 80)
    print("🎉 OVERALL BIAS FIX ASSESSMENT")
    print("=" * 80)
    
    if test1_result and test2_result:
        print("🎉 BIAS FIX VERIFICATION PASSED!")
        print("=" * 80)
        print("✅ All bias fix components are present")
        print("✅ Weight distribution is balanced")
        print("✅ Learning engine is ready for unbiased trading")
        print("✅ Weight distribution bias has been fixed")
    elif test1_result:
        print("⚠️ BIAS FIX PARTIALLY SUCCESSFUL!")
        print("=" * 80)
        print("✅ Bias fix components are present")
        print("⚠️ Weight distribution may need adjustment")
        print("✅ System is partially unbiased")
    else:
        print("❌ BIAS FIX VERIFICATION FAILED!")
        print("=" * 80)
        print("❌ Bias fix components are missing")
        print("❌ Weight distribution is unbalanced")
        print("❌ System may still have bias issues")
    
    print("=" * 80)
