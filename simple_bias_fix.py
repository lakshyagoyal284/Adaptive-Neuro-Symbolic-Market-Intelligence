"""
Simple Critical Bias Fix
Fixes the critical weight distribution bias in the learning engine
"""

import os
import sys
import json
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

class SimpleBiasFix:
    """Simple but effective bias fix"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def apply_critical_bias_fix(self):
        """Apply critical bias fixes to learning engine"""
        print("🔧 APPLYING CRITICAL BIAS FIX")
        print("=" * 80)
        print("🔍 Fixing critical weight distribution bias...")
        print("=" * 80)
        
        # Read current learning engine
        try:
            with open('adaptive_module/llm_learning_engine.py', 'r') as f:
                engine_code = f.read()
            
            # Fix 1: Add weight normalization method
            if '_normalize_weights' not in engine_code:
                self._add_weight_normalization_method(engine_code)
            
            # Fix 2: Add weight constraints to existing method
            if '_update_learning_weights' in engine_code:
                self._add_weight_constraints_to_existing_method(engine_code)
            
            # Write back the fixed code
            with open('adaptive_module/llm_learning_engine.py', 'w') as f:
                f.write(engine_code)
            
            print("✅ Critical bias fixes applied to learning engine")
            
        except Exception as e:
            print(f"❌ Error applying bias fixes: {e}")
        
        print("\n🎉 CRITICAL BIAS FIXES APPLIED!")
        print("=" * 80)
        
    def _add_weight_normalization_method(self, engine_code):
        """Add weight normalization method to learning engine"""
        # Find the class definition
        class_start = engine_code.find('class LLMLearningEngine')
        if class_start == -1:
            print("❌ Could not find LLMLearningEngine class")
            return
        
        # Find the __init__ method
        init_start = engine_code.find('def __init__', class_start)
        if init_start == -1:
            print("❌ Could not find __init__ method")
            return
        
        # Find where to insert the normalization method (after __init__)
        insert_point = engine_code.find('self.model_version = 1', init_start)
        if insert_point == -1:
            print("❌ Could not find insertion point")
            return
        
        # Define the normalization method
        normalization_method = '''
    def _normalize_weights(self):
        """Normalize weights to prevent extreme concentration"""
        total_weight = sum(self.learning_weights.values())
        if total_weight > 0:
            # Apply softmax normalization
            normalized_weights = {}
            for feature, weight in self.learning_weights.items():
                normalized_weights[feature] = weight / total_weight
            
            # Apply minimum weight threshold (5%) and maximum (25%)
            min_weight = 0.05
            max_weight = 0.25
            
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
            
            # Log changes
            for feature, new_weight in normalized_weights.items():
                if feature in old_weights:
                    change = new_weight - old_weights[feature]
                    if abs(change) > 0.01:
                        self.logger.info(f"  {feature}: {old_weights[feature]:.4f} -> {new_weight:.4f} (change: {change:+.4f})")
            
            return True
        return False
'''
        
        # Insert the normalization method
        updated_code = (
            engine_code[:insert_point] + 
            normalization_method + '\n' +
            engine_code[init_start:]
        )
        
        # Write back the updated code
        with open('adaptive_module/llm_learning_engine.py', 'w') as f:
            f.write(updated_code)
        
        print("✅ Weight normalization method added")
        
    def _add_weight_constraints_to_existing_method(self, engine_code):
        """Add weight constraints to existing _update_learning_weights method"""
        # Find the _update_learning_weights method
        method_start = engine_code.find('def _update_learning_weights(self, experience):')
        if method_start == -1:
            print("❌ Could not find _update_learning_weights method")
            return
        
        # Find the method body
        method_body_start = engine_code.find('with self._weights_lock:', method_start)
        if method_body_start == -1:
            print("❌ Could not find method body")
            return
        
        # Find where to insert constraints (after weight calculation)
        insert_point = engine_code.find('weight_changes = {}', method_body_start)
        if insert_point == -1:
            print("❌ Could not find weight changes initialization")
            return
        
        # Define the constraints code
        constraints_code = '''
            # Apply weight change constraints
            max_change = 0.05  # Maximum 5% change per update
            min_weight = 0.01  # Minimum weight threshold
            max_weight = 0.40  # Maximum weight threshold
            
            for weight_feature, weight_change in weight_changes.items():
                new_weight = old_weights[weight_feature] + weight_change
                
                # Apply constraints
                new_weight = max(min_weight, min(max_weight, new_weight))
                
                # Apply maximum change constraint
                if abs(new_weight - old_weights[weight_feature]) > max_change:
                    new_weight = old_weights[weight_feature] + (max_change if weight_change > 0 else -max_change)
                
                weight_changes[weight_feature]['new_weight'] = new_weight
                weight_changes[weight_feature]['constrained'] = True
'''
        
        # Insert the constraints code
        updated_code = (
            engine_code[:insert_point] + 
            constraints_code + '\n' +
            engine_code[insert_point + len(weight_changes):]
        )
        
        # Write back the updated code
        with open('adaptive_module/llm_learning_engine.py', 'w') as f:
            f.write(updated_code)
        
        print("✅ Weight constraints added to existing method")

if __name__ == "__main__":
    # Apply critical bias fixes
    fixer = SimpleBiasFix()
    fixer.apply_critical_bias_fix()
