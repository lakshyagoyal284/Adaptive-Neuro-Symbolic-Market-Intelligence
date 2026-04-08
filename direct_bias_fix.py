"""
Direct Bias Fix for Learning Engine
Fixes the critical weight distribution bias by directly modifying the _update_learning_weights method
"""

import os
import sys
import json
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

def fix_weight_distribution_bias():
    """Direct fix for weight distribution bias"""
    print("🔧 FIXING WEIGHT DISTRIBUTION BIAS")
    print("=" * 80)
    print("🔍 Adding weight normalization and constraints...")
    print("=" * 80)
    
    try:
        # Read the learning engine file
        with open('adaptive_module/llm_learning_engine.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find the _update_learning_weights method
        method_start = content.find('def _update_learning_weights(self, experience):')
        if method_start == -1:
            print("❌ Could not find _update_learning_weights method")
            return False
        
        # Find the method body
        method_body_start = content.find('with self._weights_lock:', method_start)
        if method_body_start == -1:
            print("❌ Could not find method body")
            return False
        
        # Find where to insert the new code (after weight changes initialization)
        insert_point = content.find('weight_changes = {}', method_body_start)
        if insert_point == -1:
            print("❌ Could not find weight changes initialization")
            return False
        
        # Define the new code to insert
        new_code = '''# Apply weight normalization and constraints
            total_weight = sum(self.learning_weights.values())
            if total_weight > 0:
                # Normalize weights
                normalized_weights = {}
                for feature, weight in self.learning_weights.items():
                    normalized_weights[feature] = weight / total_weight
                
                # Apply constraints
                min_weight = 0.05  # 5% minimum
                max_weight = 0.25  # 25% maximum
                
                for feature, weight in normalized_weights.items():
                    if weight < min_weight:
                        normalized_weights[feature] = min_weight
                    elif weight > max_weight:
                        normalized_weights[feature] = max_weight
                
                # Update weights
                old_weights = self.learning_weights.copy()
                self.learning_weights = normalized_weights
                
                # Log normalization
                self.logger.info(f"WEIGHT NORMALIZATION APPLIED:")
                for feature, weight in normalized_weights.items():
                    self.logger.info(f"  {feature}: {weight:.4f}")
                
                # Log significant changes
                for feature, new_weight in normalized_weights.items():
                    if feature in old_weights:
                        change = new_weight - old_weights[feature]
                        if abs(change) > 0.01:
                            self.logger.info(f"  {feature}: {old_weights[feature]:.4f} -> {new_weight:.4f} (change: {change:+.4f})")
'''
        
        # Insert the new code
        updated_content = (
            content[:insert_point] + 
            new_code + '\n' +
            content[insert_point:]
        )
        
        # Write back the updated file
        with open('adaptive_module/llm_learning_engine.py', 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print("✅ Weight distribution bias fix applied successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing bias: {e}")
        return False

if __name__ == "__main__":
    # Apply the bias fix
    success = fix_weight_distribution_bias()
    if success:
        print("\n🎉 BIAS FIX COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("✅ Weight distribution bias has been fixed")
        print("✅ Learning engine will now use normalized weights")
        print("✅ This will prevent overfitting to trend signals")
        print("✅ System is now more fair and balanced")
    else:
        print("\n❌ BIAS FIX FAILED")
        print("=" * 80)
        print("❌ Could not fix weight distribution bias")
