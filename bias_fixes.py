"""
Critical Bias Fixes - Weight Distribution Normalization
Fixes the critical weight distribution bias identified in bias analysis
"""

import os
import sys
import json
import numpy as np
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional

class BiasFixes:
    """Fix critical weight distribution bias"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def apply_critical_bias_fixes(self):
        """Apply critical bias fixes to learning engine"""
        print("🔧 APPLYING CRITICAL BIAS FIXES")
        print("=" * 80)
        print("🔍 Fixing weight distribution bias...")
        print("=" * 80)
        
        # Fix 1: Add weight normalization to learning engine
        self._add_weight_normalization()
        
        # Fix 2: Add weight constraints
        self._add_weight_constraints()
        
        # Fix 3: Add weight rebalancing
        self._add_weight_rebalancing()
        
        # Fix 4: Add learning rate adjustment
        self._add_adaptive_learning_rate()
        
        print("\n🎉 CRITICAL BIAS FIXES APPLIED!")
        print("=" * 80)
        
    def _add_weight_normalization(self):
        """Add weight normalization to prevent concentration"""
        print("\n🔧 Adding weight normalization...")
        
        # Define the normalization code directly
    def _normalize_learning_weights(self):
        """Normalize weights to prevent extreme concentration"""
        total_weight = sum(self.learning_weights.values())
        if total_weight > 0:
            # Apply softmax normalization
            normalized_weights = {}
            for feature, weight in self.learning_weights.items():
                normalized_weights[feature] = weight / total_weight
            
            # Apply minimum weight threshold (5%)
            min_weight = 0.05
            max_weight = 0.25
            
            for feature, weight in normalized_weights.items():
                if weight < min_weight:
                    normalized_weights[feature] = min_weight
                elif weight > max_weight:
                    normalized_weights[feature] = max_weight
            
            # Update weights
            self.learning_weights = normalized_weights
            
            # Log normalization
            self.logger.info(f"WEIGHT NORMALIZATION APPLIED:")
            for feature, weight in normalized_weights.items():
                self.logger.info(f"  {feature}: {weight:.4f}")
            
            return True
        return False
    '''
    
    def _add_weight_constraints(self):
        """Add weight constraints to prevent extreme changes"""
        print("\n🔧 Adding weight constraints...")
        
        constraints_code = '''
    def _update_learning_weights_constrained(self, experience):
        """Update weights with constraints to prevent extreme changes"""
        with self._weights_lock:
            # Calculate weight adjustment based on reward/punishment
            net_signal = experience.reward - experience.punishment
            
            if abs(net_signal) < 0.01:  # No significant learning signal
                return
            
            # Track weight changes
            weight_changes = {}
            old_weights = self.learning_weights.copy()
            
            # Feature mapping - CRITICAL FIX
            feature_mapping = {
                'trend_demand': 'trend_weight',
                'volume_activity': 'volume_weight',
                'profit_potential': 'profit_weight',
                'risk_reward_ratio': 'risk_weight'
            }
            
            # Update weights for context features that contributed to decision
            for context_feature, context_value in experience.context.items():
                # Map context feature to weight feature
                weight_feature = feature_mapping.get(context_feature, context_feature)
                
                if weight_feature in self.learning_weights:
                    # Gradient descent-like update
                    weight_adjustment = self.learning_rate * net_signal * context_value
                    
                    # Apply weight change with constraints
                    max_change = 0.05  # Maximum 5% change per update
                    min_weight = 0.01  # Minimum weight threshold
                    max_weight = 0.40  # Maximum weight threshold
                    
                    # Apply weight change with constraints
                    old_weight = old_weights[weight_feature]
                    new_weight = old_weight + weight_adjustment
                    
                    # Apply constraints
                    new_weight = max(min_weight, min(max_weight, new_weight))
                    
                    # Apply maximum change constraint
                    if abs(new_weight - old_weight) > max_change:
                        new_weight = old_weight + (max_change if weight_adjustment > 0 else -max_change)
                    
                    # Update weight
                    self.learning_weights[weight_feature] = new_weight
                    
                    # Track change
                    weight_changes[weight_feature] = {
                        'old_weight': old_weight,
                        'new_weight': new_weight,
                        'change': new_weight - old_weight,
                        'context_value': context_value,
                        'context_feature': context_feature,
                        'net_signal': net_signal,
                        'constrained': True
                    }
            
            # Normalize weights to sum to 1
            total_weight = sum(self.learning_weights.values())
            if total_weight > 0:
                for feature in self.learning_weights:
                    self.learning_weights[feature] /= total_weight
            
            # Log constrained weight updates
            if weight_changes:
                self.logger.info(f"CONSTRAINED WEIGHT UPDATE:")
                for feature, change in weight_changes.items():
                    self.logger.info(f"  {feature}: {change['old_weight']:.4f} -> {change['new_weight']:.4f} (change: {change['change']:+.4f}) [CONSTRAINED]")
            
            # Force model version increment when significant changes occur
            total_change = sum(abs(change['change']) for change in weight_changes.values())
            if total_change > 0.05:  # Significant change
                with self._version_lock:
                    self.model_version += 1
                    adaptation_data = {
                        'version_increment': True,
                        'total_weight_change': total_change,
                        'num_features_updated': len(weight_changes),
                        'net_signal': net_signal,
                        'experience_outcome': experience.outcome.value,
                        'bias_correction': 'weight_distribution'
                    }
                    self.log_model_adaptation(adaptation_data)
                    self._save_model()  # Save updated model
            
            return True
        return False
'''
        
        # Apply to learning engine
        self._apply_code_fix_to_learning_engine(normalization_code, "weight_normalization")
        
        # Apply constraints code
        self._apply_code_fix_to_learning_engine(constraints_code, "weight_constraints")
        
        print("✅ Weight normalization and constraints added")
        
    def _add_weight_rebalancing(self):
        """Add weight rebalancing mechanism"""
        print("\n🔧 Adding weight rebalancing...")
        
        rebalancing_code = '''
    def _rebalance_weights_if_needed(self):
        """Rebalance weights if distribution is too concentrated"""
        with self._weights_lock:
            # Calculate weight distribution metrics
            weights = list(self.learning_weights.values())
            weights_array = np.array(weights)
            
            # Calculate concentration metrics
            gini_coefficient = self._calculate_gini_coefficient(weights_array)
            max_weight = np.max(weights_array)
            min_weight = np.min(weights_array)
            weight_ratio = max_weight / min_weight if min_weight > 0 else float('inf')
            
            # Check if rebalancing is needed
            needs_rebalancing = (
                gini_coefficient > 0.4 or  # High inequality
                weight_ratio > 5.0 or  # Extreme concentration
                max_weight > 0.3 or  # Single weight > 30%
                min_weight < 0.01  # Weights too small
            )
            
            if needs_rebalancing:
                self.logger.warning(f"WEIGHT REBALANCING TRIGGERED: Gini={gini_coefficient:.3f}, Ratio={weight_ratio:.2f}")
                
                # Apply equal weight rebalancing
                num_features = len(self.learning_weights)
                equal_weight = 1.0 / num_features
                
                # Apply rebalancing with smoothing
                rebalanced_weights = {}
                for feature in self.learning_weights:
                    # Smooth transition to equal weights
                    old_weight = self.learning_weights[feature]
                    rebalanced_weights[feature] = 0.7 * old_weight + 0.3 * equal_weight
                
                self.learning_weights = rebalanced_weights
                
                # Normalize after rebalancing
                total_weight = sum(rebalanced_weights.values())
                for feature in rebalanced_weights:
                    rebalanced_weights[feature] /= total_weight
                
                # Log rebalancing
                self.logger.info(f"WEIGHTS REBALANCED:")
                for feature, weight in rebalanced_weights.items():
                    self.logger.info(f"  {feature}: {weight:.4f}")
                
                # Increment model version
                with self._version_lock:
                    self.model_version += 1
                    adaptation_data = {
                        'version_increment': True,
                        'rebalancing_applied': True,
                        'gini_before': gini_coefficient,
                        'gini_after': self._calculate_gini_coefficient(np.array(list(rebalanced_weights.values()))),
                        'bias_correction': 'weight_rebalancing'
                    }
                    self.log_model_adaptation(adaptation_data)
                    self._save_model()
                
                return True
        return False
    
    def _calculate_gini_coefficient(self, weights):
        """Calculate Gini coefficient for weight inequality"""
        try:
            # Sort weights
            sorted_weights = np.sort(weights)
            n = len(weights)
            if n == 0:
                return 0.0
            
            # Calculate Gini coefficient
            cumsum = np.cumsum(sorted_weights)
            sum_weights = np.sum(weights)
            gini = (n + 1) - 2 * np.sum(cumsum) / (n * sum_weights)
            return max(0, gini)
        except:
            return 0.0
'''
        
        # Apply rebalancing code
        self._apply_code_fix_to_learning_engine(rebalancing_code, "weight_rebalancing")
        
        print("✅ Weight rebalancing mechanism added")
        
    def _add_adaptive_learning_rate(self):
        """Add adaptive learning rate to prevent overfitting"""
        print("\n🔧 Adding adaptive learning rate...")
        
        adaptive_lr_code = '''
    def _get_adaptive_learning_rate(self, experience):
        """Get adaptive learning rate based on performance"""
        # Base learning rate
        base_lr = 0.1
        
        # Calculate recent performance
        recent_experiences = self.experiences[-50:] if len(self.experiences) >= 50 else self.experiences
        
        if len(recent_experiences) >= 10:
            # Calculate recent accuracy
            correct_experiences = [exp for exp in recent_experiences if exp.outcome.value == 'correct']
            recent_accuracy = len(correct_experiences) / len(recent_experiences)
            
            # Adjust learning rate based on performance
            if recent_accuracy > 0.7:  # Good performance
                return base_lr * 0.5  # Reduce learning rate
            elif recent_accuracy < 0.3:  # Poor performance
                return base_lr * 1.5  # Increase learning rate
            else:  # Average performance
                return base_lr
        
        return base_lr
    
    def _update_learning_weights_adaptive(self, experience):
        """Update weights with adaptive learning rate"""
        with self._weights_lock:
            # Get adaptive learning rate
            adaptive_lr = self._get_adaptive_learning_rate(experience)
            
            # Calculate weight adjustment
            net_signal = experience.reward - experience.punishment
            
            if abs(net_signal) < 0.01:  # No significant learning signal
                return
            
            # Feature mapping
            feature_mapping = {
                'trend_demand': 'trend_weight',
                'volume_activity': 'volume_weight',
                'profit_potential': 'profit_weight',
                'risk_reward_ratio': 'risk_weight'
            }
            
            # Update weights with adaptive learning rate
            weight_changes = {}
            old_weights = self.learning_weights.copy()
            
            for context_feature, context_value in experience.context.items():
                weight_feature = feature_mapping.get(context_feature, context_feature)
                
                if weight_feature in self.learning_weights:
                    weight_adjustment = adaptive_lr * net_signal * context_value
                    old_weight = old_weights[weight_feature]
                    new_weight = old_weight + weight_adjustment
                    
                    # Apply constraints
                    max_weight = 0.30  # Maximum 30% per feature
                    min_weight = 0.01  # Minimum 1% per feature
                    new_weight = max(min_weight, min(max_weight, new_weight))
                    
                    self.learning_weights[weight_feature] = new_weight
                    
                    weight_changes[weight_feature] = {
                        'old_weight': old_weight,
                        'new_weight': new_weight,
                        'change': new_weight - old_weight,
                        'adaptive_lr': adaptive_lr,
                        'context_value': context_value,
                        'context_feature': context_feature,
                        'net_signal': net_signal
                    }
            
            # Normalize weights
            total_weight = sum(self.learning_weights.values())
            if total_weight > 0:
                for feature in self.learning_weights:
                    self.learning_weights[feature] /= total_weight
            
            # Log adaptive update
            if weight_changes:
                self.logger.info(f"ADAPTIVE WEIGHT UPDATE (LR={adaptive_lr:.3f}):")
                for feature, change in weight_changes.items():
                    self.logger.info(f"  {feature}: {change['old_weight']:.4f} -> {change['new_weight']:.4f} (change: {change['change']:+.4f})")
            
            return True
        return False
'''
        
        # Apply adaptive learning rate code
        self._apply_code_fix_to_learning_engine(adaptive_lr_code, "adaptive_learning_rate")
        
        print("✅ Adaptive learning rate mechanism added")
        
    def _apply_code_fix_to_learning_engine(self, fix_code, fix_name):
        """Apply code fix to learning engine file"""
        try:
            # Read current learning engine
            with open('adaptive_module/llm_learning_engine.py', 'r') as f:
                current_code = f.read()
            
            # Find the _update_learning_weights method
            method_start = current_code.find('def _update_learning_weights(self, experience):')
            if method_start == -1:
                print(f"❌ Could not find _update_learning_weights method")
                return
            
            # Find the end of the method
            method_end = current_code.find('\n    def ', method_start + 1)
            if method_end == -1:
                method_end = current_code.find('\n    def ', method_start + 2)
            
            # Insert the fix code before the method
            insertion_point = method_start
            updated_code = (
                current_code[:insertion_point] + 
                fix_code + '\n\n' +
                current_code[method_start:]
            )
            
            # Write updated code
            with open('adaptive_module/llm_learning_engine.py', 'w') as f:
                f.write(updated_code)
            
            print(f"✅ Applied {fix_name} to learning engine")
            
        except Exception as e:
            print(f"❌ Error applying {fix_name}: {e}")

if __name__ == "__main__":
    # Apply critical bias fixes
    fixer = BiasFixes()
    fixer.apply_critical_bias_fixes()
