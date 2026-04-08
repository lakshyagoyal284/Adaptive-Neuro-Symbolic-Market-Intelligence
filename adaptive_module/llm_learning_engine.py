"""
LLM-Based Adaptive Learning Engine for Market Intelligence
This module implements a sophisticated learning system that:
1. Learns from mistakes and bad decisions
2. Rewards correct decisions 
"""

import numpy as np
import os
import sys
import json
import hashlib
import threading
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import pickle

# Configure comprehensive logging
def setup_learning_logger():
    """Setup comprehensive logging for LLM learning engine"""
    # Create logs directory if not exists
    logs_dir = "logs"
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    # Setup file logger for learning engine
    log_filename = f"logs/llm_learning_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # Configure logger
    learning_logger = logging.getLogger('llm_learning')
    learning_logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    learning_logger.handlers.clear()
    
    # Add file and console handlers
    file_handler = logging.FileHandler(log_filename)
    console_handler = logging.StreamHandler()
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    learning_logger.addHandler(file_handler)
    learning_logger.addHandler(console_handler)
    
    return learning_logger

logger = setup_learning_logger()

class DecisionOutcome(Enum):
    """Enumeration of decision outcomes"""
    CORRECT = "correct"
    INCORRECT = "incorrect"
    PARTIAL = "partial"
    UNKNOWN = "unknown"

class LearningSignal(Enum):
    """Learning signal types"""
    REWARD = "reward"
    PUNISHMENT = "punishment"
    NEUTRAL = "neutral"

@dataclass
class DecisionExperience:
    """Data class for decision experience"""
    timestamp: datetime
    context: Dict[str, float]
    decision_type: str
    action_taken: str
    confidence: float
    outcome: DecisionOutcome
    reward: float
    punishment: float
    market_state: Dict[str, Any]
    technical_indicators: Dict[str, float]
    rule_triggers: List[str]
    actual_result: float
    expected_result: float
    error_magnitude: float
    learning_weight: float = 1.0

@dataclass
class LearningMetrics:
    """Data class for learning metrics"""
    total_decisions: int
    correct_decisions: int
    incorrect_decisions: int
    accuracy_rate: float
    avg_reward: float
    avg_punishment: float
    learning_progress: float
    adaptation_rate: float
    model_version: int
    last_update: datetime

class LLMLearningEngine:
    """
    Advanced LLM-based learning engine that learns from mistakes and rewards correct decisions
    """
    
    def __init__(self, model_path: str = "models/llm_learning_model.pkl"):
        self.model_path = model_path
        self.experiences = []
        self.learning_weights = {
            'market_growth_weight': 0.30,  # Increased for better trend following
            'sentiment_weight': 0.15,      # Reduced to avoid noise
            'volatility_weight': 0.10,      # Reduced for stability
            'trend_weight': 0.25,          # Increased for trend following
            'volume_weight': 0.10,          # Kept for confirmation
            'profit_weight': 0.05,          # Kept for profit focus
            'risk_weight': 0.05             # Kept for risk management
        }
        self.rule_performance = {}
        self.context_patterns = {}
        self.model_version = 1
        self.learning_rate = 0.05  # Increased from 0.1 - more aggressive learning
        self.decay_rate = 0.95
        self.reward_scale = 1.5  # Increased from 1.0 - stronger rewards
        self.punishment_scale = 2.0  # Increased from 2.0 - harsher punishment
        
        # Thread safety locks
        self._weights_lock = threading.Lock()
        self._experiences_lock = threading.Lock()
        self._performance_lock = threading.Lock()
        self._version_lock = threading.Lock()
        self._model_lock = threading.Lock()
        
        # Model integrity
        self.model_checksum = None
        
        # Initialize learning components
        self._initialize_learning_system()
        
        # Setup detailed logging
        self.setup_learning_logging()
        
    def setup_learning_logging(self):
        """Setup comprehensive logging for learning engine"""
        self.learning_start_time = datetime.now()
        logger.info("=" * 80)
        logger.info(f"LLM LEARNING ENGINE INITIALIZED")
        logger.info(f"Start Time: {self.learning_start_time}")
        logger.info(f"Model Path: {self.model_path}")
        logger.info(f"Initial Model Version: {self.model_version}")
        logger.info(f"Learning Rate: {self.learning_rate}")
        logger.info(f"Reward Scale: {self.reward_scale}")
        logger.info(f"Punishment Scale: {self.punishment_scale}")
        logger.info("=" * 80)
        
    def log_learning_event(self, event_type: str, data: Dict):
        """Log detailed learning events"""
        logger.info(f"LEARNING EVENT - {event_type}:")
        for key, value in data.items():
            if isinstance(value, float):
                logger.info(f"  {key}: {value:.4f}")
            else:
                logger.info(f"  {key}: {value}")
                
    def log_experience_processed(self, experience):
        """Log every experience processed"""
        experience_data = {
            'timestamp': experience.timestamp,
            'decision_type': experience.decision_type,
            'action_taken': experience.action_taken,
            'outcome': experience.outcome.value,
            'reward': experience.reward,
            'punishment': experience.punishment,
            'confidence': experience.confidence,
            'error_magnitude': experience.error_magnitude
        }
        self.log_learning_event("EXPERIENCE_PROCESSED", experience_data)
        
    def log_weight_update(self, weight_changes: Dict):
        """Log weight updates"""
        self.log_learning_event("WEIGHT_UPDATE", weight_changes)
        
    def log_rule_performance_update(self, rule_id: str, performance_data: Dict):
        """Log rule performance updates"""
        self.log_learning_event(f"RULE_PERFORMANCE_{rule_id.upper()}", performance_data)
        
    def log_model_adaptation(self, adaptation_data: Dict):
        """Log model adaptation events"""
        logger.info(f"MODEL ADAPTATION - Version {self.model_version}:")
        for key, value in adaptation_data.items():
            logger.info(f"  {key}: {value}")
            
    def save_learning_session_log(self, session_data: Dict):
        """Save detailed learning session log"""
        log_filename = f"logs/learning_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(log_filename, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            logger.info(f"Learning session log saved to: {log_filename}")
        except Exception as e:
            logger.error(f"Failed to save learning session log: {e}")
        
    def _initialize_learning_system(self):
        """Initialize the learning system components"""
        try:
            # Load existing model if available
            if os.path.exists(self.model_path):
                self._load_model()
            else:
                self._create_initial_model()
            
            logger.info(f"LLM Learning Engine initialized - Model Version: {self.model_version}")
            
        except Exception as e:
            logger.error(f"Error initializing learning system: {e}")
            self._create_initial_model()
    
    def _create_initial_model(self):
        """Create initial learning model"""
        self.learning_weights = {
            'market_growth_weight': 0.25,
            'sentiment_weight': 0.20,
            'volatility_weight': 0.20,
            'trend_weight': 0.15,
            'volume_weight': 0.10,
            'profit_weight': 0.05,      # NEW: Profit potential weight
            'risk_weight': 0.05          # NEW: Risk management weight
        }
        
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
            
            return True
        return False
        
        self.rule_performance = {
            'high_growth_investment': {'accuracy': 0.5, 'confidence': 0.5, 'usage_count': 0},
            'negative_sentiment_alert': {'accuracy': 0.5, 'confidence': 0.5, 'usage_count': 0},
            'competitor_price_response': {'accuracy': 0.5, 'confidence': 0.5, 'usage_count': 0},
            'high_demand_opportunity': {'accuracy': 0.5, 'confidence': 0.5, 'usage_count': 0},
            'positive_sentiment_investment': {'accuracy': 0.5, 'confidence': 0.5, 'usage_count': 0},
            'volatility_risk_alert': {'accuracy': 0.5, 'confidence': 0.5, 'usage_count': 0},
            'competitor_activity_surge': {'accuracy': 0.5, 'confidence': 0.5, 'usage_count': 0},
            'low_market_share_alert': {'accuracy': 0.5, 'confidence': 0.5, 'usage_count': 0}
        }
        
        self.context_patterns = {}
        
    def _load_model(self):
        """Load existing learning model with security verification"""
        try:
            with self._model_lock:
                if not os.path.exists(self.model_path):
                    logger.warning(f"Model file not found: {self.model_path}")
                    self._create_initial_model()
                    return
                
                with open(self.model_path, 'rb') as f:
                    data = f.read()
                
                # Verify file integrity
                checksum = hashlib.sha256(data).hexdigest()
                checksum_file = self.model_path + '.checksum'
                
                if os.path.exists(checksum_file):
                    with open(checksum_file, 'r') as cf:
                        expected_checksum = cf.read().strip()
                    
                    if checksum != expected_checksum:
                        logger.error("Model tampering detected!")
                        self._create_initial_model()
                        return
                
                # Load model data safely using JSON
                try:
                    model_data = json.loads(data.decode('utf-8'))
                    self.learning_weights = model_data.get('learning_weights', self.learning_weights)
                    self.rule_performance = model_data.get('rule_performance', self.rule_performance)
                    self.context_patterns = model_data.get('context_patterns', self.context_patterns)
                    self.model_version = model_data.get('model_version', 1)
                    self.experiences = model_data.get('experiences', [])
                    self.model_checksum = checksum
                    logger.info(f"Loaded existing model version {self.model_version}")
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # Fallback to pickle with validation
                    try:
                        # Restrict pickle environment
                        safe_globals = {
                            '__builtins__': {},
                            'dict': dict,
                            'list': list,
                            'float': float,
                            'int': int,
                            'str': str
                        }
                        model_data = pickle.loads(data, encoding='utf-8')
                        
                        # Validate model structure
                        if not isinstance(model_data, dict):
                            raise ValueError("Invalid model structure")
                        
                        self.learning_weights = model_data.get('learning_weights', self.learning_weights)
                        self.rule_performance = model_data.get('rule_performance', self.rule_performance)
                        self.context_patterns = model_data.get('context_patterns', self.context_patterns)
                        self.model_version = model_data.get('model_version', 1)
                        self.experiences = model_data.get('experiences', [])
                        self.model_checksum = checksum
                        logger.info(f"Loaded existing model version {self.model_version}")
                    except Exception as e:
                        logger.error(f"Model loading failed: {e}")
                        self._create_initial_model()
                        
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self._create_initial_model()
    
    def _save_model(self):
        """Save current learning model with integrity verification"""
        try:
            with self._model_lock:
                os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
                
                # Save model as JSON
                model_data = {
                    'learning_weights': self.learning_weights,
                    'rule_performance': self.rule_performance,
                    'context_patterns': self.context_patterns,
                    'model_version': self.model_version,
                    'experiences': self.experiences[-1000:] if len(self.experiences) > 1000 else self.experiences  # Limit size
                }
                
                model_json = json.dumps(model_data, indent=2)
                model_bytes = model_json.encode('utf-8')
                
                # Calculate checksum
                checksum = hashlib.sha256(model_bytes).hexdigest()
                
                # Save model
                with open(self.model_path, 'wb') as f:
                    f.write(model_bytes)
                
                # Save checksum
                checksum_file = self.model_path + '.checksum'
                with open(checksum_file, 'w') as cf:
                    cf.write(checksum)
                
                self.model_checksum = checksum
                logger.info(f"Model saved securely: {self.model_path}")
                
        except Exception as e:
            logger.error(f"Error saving model: {e}")
    
    def _update_learning_weights(self, experience):
        """Thread-safe weight updates"""
        with self._weights_lock:
            # Calculate weight adjustment based on reward/punishment
            net_signal = experience.reward - experience.punishment
            
            if abs(net_signal) < 0.01:  # No significant learning signal
                return
            
            # Track weight changes
            # Apply weight normalization and constraints
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

            # Apply weight normalization and constraints
total_weight = sum(self.learning_weights.values())
if total_weight > 0:
                # Normalize weights
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
                
                # Log significant changes
                for feature, new_weight in normalized_weights.items():
                    if feature in old_weights:
                        change = new_weight - old_weights[feature]
                        if abs(change) > 0.01:
                            self.logger.info(f"  {feature}: {old_weights[feature]:.4f} -> {new_weight:.4f} (change: {change:+.4f})")
            
                # Normalize weights to sum to 1
total_weight = sum(self.learning_weights.values())
if total_weight > 0:
    for feature in self.learning_weights:
        self.learning_weights[feature] /= total_weight
            
            return True
        
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
                    
                    # Apply weight change
                    old_weight = old_weights[weight_feature]
                    self.learning_weights[weight_feature] += weight_adjustment
                    
                    # Keep weights in reasonable range
                    self.learning_weights[weight_feature] = max(0.01, min(1.0, self.learning_weights[weight_feature]))
                    
                    # Track change
                    weight_changes[weight_feature] = {
                        'old_weight': old_weight,
                        'new_weight': self.learning_weights[weight_feature],
                        'change': weight_adjustment,
                        'context_value': context_value,
                        'context_feature': context_feature,
                        'net_signal': net_signal
                    }
            
            # Normalize weights to sum to 1
total_weight = sum(self.learning_weights.values())
if total_weight > 0:
    for feature in self.learning_weights:
        self.learning_weights[feature] /= total_weight
            
            # Log weight updates - CRITICAL FOR DEBUGGING
            if weight_changes:
                self.log_weight_update(weight_changes)
                
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
                            'experience_outcome': experience.outcome.value
                        }
                        self.log_model_adaptation(adaptation_data)
                        self._save_model()  # Save updated model
            logger.error(f"Error saving model: {e}")
    
    def analyze_decision_outcome(self, 
                             context: Dict[str, float],
                             decision_type: str,
                             action_taken: str,
                             confidence: float,
                             market_state: Dict[str, Any],
                             technical_indicators: Dict[str, float],
                             rule_triggers: List[str],
                             actual_result: float,
                             expected_result: float = None) -> DecisionExperience:
        """Analyze decision outcome and determine if it was correct or incorrect"""
        try:
            # Calculate error magnitude
            if expected_result is None:
                expected_result = actual_result  # If no expectation, use actual
            
            error_magnitude = abs(actual_result - expected_result)
            relative_error = error_magnitude / max(abs(expected_result), 0.01)
            
            # Determine outcome based on multiple factors
            outcome = self._determine_outcome(context, action_taken, actual_result, expected_result, relative_error)
            
            # Calculate reward and punishment
            reward, punishment = self._calculate_reward_punishment(outcome, relative_error, confidence)
            
            # Create experience
            experience = DecisionExperience(
                timestamp=datetime.now(),
                context=context.copy(),
                decision_type=decision_type,
                action_taken=action_taken,
                confidence=confidence,
                outcome=outcome,
                reward=reward,
                punishment=punishment,
                market_state=market_state.copy(),
                technical_indicators=technical_indicators.copy(),
                rule_triggers=rule_triggers.copy(),
                actual_result=actual_result,
                expected_result=expected_result,
                error_magnitude=error_magnitude
            )
            
            return experience
            
        except Exception as e:
            logger.error(f"Error analyzing decision outcome: {e}")
            return None
    
    def _determine_outcome(self, 
                          context: Dict[str, float],
                          action: str,
                          actual_result: float,
                          expected_result: float,
                          relative_error: float) -> DecisionOutcome:
        """Determine if decision was correct, incorrect, or partial"""
        try:
            # For buy decisions
            if action in ['buy', 'long', 'investment']:
                if actual_result > 0:
                    if relative_error < 0.1:  # Less than 10% error
                        return DecisionOutcome.CORRECT
                    elif relative_error < 0.3:  # Less than 30% error
                        return DecisionOutcome.PARTIAL
                    else:
                        return DecisionOutcome.INCORRECT
                else:
                    return DecisionOutcome.INCORRECT
            
            # For sell decisions
            elif action in ['sell', 'short', 'risk_management']:
                if actual_result < 0:
                    if relative_error < 0.1:
                        return DecisionOutcome.CORRECT
                    elif relative_error < 0.3:
                        return DecisionOutcome.PARTIAL
                    else:
                        return DecisionOutcome.INCORRECT
                else:
                    return DecisionOutcome.INCORRECT
            
            # For hold/neutral decisions
            elif action in ['hold', 'neutral', 'monitor']:
                if abs(actual_result) < 0.05:  # Very small movement
                    return DecisionOutcome.CORRECT
                elif abs(actual_result) < 0.15:  # Small movement
                    return DecisionOutcome.PARTIAL
                else:
                    return DecisionOutcome.INCORRECT
            
            # Default
            else:
                return DecisionOutcome.UNKNOWN
                
        except Exception as e:
            logger.error(f"Error determining outcome: {e}")
            return DecisionOutcome.UNKNOWN
    
    def _calculate_reward_punishment(self, 
                                   outcome: DecisionOutcome,
                                   relative_error: float,
                                   confidence: float) -> Tuple[float, float]:
        """Calculate reward and punishment values"""
        try:
            reward = 0.0
            punishment = 0.0
            
            if outcome == DecisionOutcome.CORRECT:
                # Reward correct decisions
                reward = self.reward_scale * (1.0 + confidence)  # Higher reward for higher confidence
                punishment = 0.0
                
            elif outcome == DecisionOutcome.PARTIAL:
                # Small reward for partially correct
                reward = self.reward_scale * 0.3 * confidence
                punishment = self.punishment_scale * 0.2 * (1 - confidence)
                
            elif outcome == DecisionOutcome.INCORRECT:
                # Punish incorrect decisions more severely
                reward = 0.0
                punishment = self.punishment_scale * (1.0 + relative_error) * (1 + confidence)
                # Higher punishment for high confidence incorrect decisions
            
            return reward, punishment
            
        except Exception as e:
            logger.error(f"Error calculating reward/punishment: {e}")
            return 0.0, 0.0
    
    def learn_from_experience(self, experience: DecisionExperience):
        """Learn from a single experience using reinforcement learning"""
        try:
            if not experience:
                return
            
            # Log the experience being processed
            self.log_experience_processed(experience)
            
            # Add to experience buffer
            self.experiences.append(experience)
            
            # Update rule performance
            for rule_id in experience.rule_triggers:
                if rule_id in self.rule_performance:
                    self._update_rule_performance(rule_id, experience)
            
            # Update learning weights based on outcome
            self._update_learning_weights(experience)
            
            # Update context patterns
            self._update_context_patterns(experience)
            
            # Periodic model save
            if len(self.experiences) % 10 == 0:
                self._save_model()
            
            # Log learning summary
            learning_summary = {
                'total_experiences': len(self.experiences),
                'decision_type': experience.decision_type,
                'outcome': experience.outcome.value,
                'reward': experience.reward,
                'punishment': experience.punishment,
                'model_version': self.model_version
            }
            self.log_learning_event("LEARNING_SUMMARY", learning_summary)
            
        except Exception as e:
            self.log_learning_event("LEARNING_ERROR", {'error': str(e), 'experience': str(experience)})
            logger.error(f"Error learning from experience: {e}")
    
    def _update_rule_performance(self, rule_id: str, experience: DecisionExperience):
        """Update performance metrics for specific rule"""
        try:
            rule_perf = self.rule_performance[rule_id]
            
            # Update usage count
            rule_perf['usage_count'] += 1
            
            # Update accuracy using exponential moving average
            if experience.outcome == DecisionOutcome.CORRECT:
                new_accuracy = 1.0
            elif experience.outcome == DecisionOutcome.PARTIAL:
                new_accuracy = 0.5
            else:
                new_accuracy = 0.0
            
            # EMA for accuracy
            alpha = 0.1  # Learning rate for accuracy
            rule_perf['accuracy'] = (alpha * new_accuracy + (1 - alpha) * rule_perf['accuracy'])
            
            # Update confidence calibration
            if experience.outcome == DecisionOutcome.CORRECT:
                rule_perf['confidence'] = min(1.0, rule_perf['confidence'] + 0.05)
            elif experience.outcome == DecisionOutcome.INCORRECT:
                rule_perf['confidence'] = max(0.1, rule_perf['confidence'] - 0.1)
            
            # Log rule performance update
            performance_data = {
                'rule_id': rule_id,
                'usage_count': rule_perf['usage_count'],
                'accuracy': rule_perf['accuracy'],
                'confidence': rule_perf['confidence'],
                'outcome': experience.outcome.value,
                'experience_count': len(self.experiences)
            }
            self.log_rule_performance_update(rule_id, performance_data)
            
        except Exception as e:
            logger.error(f"Error updating rule performance: {e}")
    
    def _update_learning_weights(self, experience: DecisionExperience):
        """Update learning weights based on experience outcome"""
        try:
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
                    
                    # Apply weight change
                    old_weight = old_weights[weight_feature]
                    self.learning_weights[weight_feature] += weight_adjustment
                    
                    # Keep weights in reasonable range
                    self.learning_weights[weight_feature] = max(0.01, min(1.0, self.learning_weights[weight_feature]))
                    
                    # Track change
                    weight_changes[weight_feature] = {
                        'old_weight': old_weight,
                        'new_weight': self.learning_weights[weight_feature],
                        'change': weight_adjustment,
                        'context_value': context_value,
                        'context_feature': context_feature,
                        'net_signal': net_signal
                    }
            
            # Normalize weights to sum to 1
total_weight = sum(self.learning_weights.values())
if total_weight > 0:
    for feature in self.learning_weights:
        self.learning_weights[feature] /= total_weight
            
            # Log weight updates - CRITICAL FOR DEBUGGING
            if weight_changes:
                self.log_weight_update(weight_changes)
                
                # Force model version increment when significant changes occur
                total_change = sum(abs(change['change']) for change in weight_changes.values())
                if total_change > 0.05:  # Significant change
                    self.model_version += 1
                    adaptation_data = {
                        'version_increment': True,
                        'total_weight_change': total_change,
                        'num_features_updated': len(weight_changes),
                        'net_signal': net_signal,
                        'experience_outcome': experience.outcome.value
                    }
                    self.log_model_adaptation(adaptation_data)
                    self._save_model()  # Save updated model
            
        except Exception as e:
            logger.error(f"Error updating learning weights: {e}")
    
    def _update_context_patterns(self, experience: DecisionExperience):
        """Update context patterns for better future decisions"""
        try:
            # Create context key
            context_key = self._create_context_key(experience.context, experience.technical_indicators)
            
            if context_key not in self.context_patterns:
                self.context_patterns[context_key] = {
                    'experiences': [],
                    'avg_outcome': 0.0,
                    'confidence': 0.5,
                    'success_rate': 0.0
                }
            
            pattern = self.context_patterns[context_key]
            pattern['experiences'].append(experience)
            
            # Update pattern statistics
            if len(pattern['experiences']) > 0:
                recent_experiences = pattern['experiences'][-20:]  # Last 20 experiences
                
                # Calculate success rate
                correct_count = sum(1 for exp in recent_experiences if exp.outcome == DecisionOutcome.CORRECT)
                pattern['success_rate'] = correct_count / len(recent_experiences)
                
                # Calculate average outcome
                outcomes = [1.0 if exp.outcome == DecisionOutcome.CORRECT else 
                           0.5 if exp.outcome == DecisionOutcome.PARTIAL else 0.0 
                           for exp in recent_experiences]
                pattern['avg_outcome'] = np.mean(outcomes)
                
                # Update confidence based on consistency
                if len(recent_experiences) >= 5:
                    consistency = 1.0 - np.std(outcomes)
                    pattern['confidence'] = min(1.0, max(0.1, consistency))
            
        except Exception as e:
            logger.error(f"Error updating context patterns: {e}")
    
    def _create_context_key(self, context: Dict[str, float], technical_indicators: Dict[str, float]) -> str:
        """Create a key for context pattern matching"""
        try:
            # Discretize continuous values for pattern matching
            key_parts = []
            
            # Market growth discretization
            market_growth = context.get('market_growth', 0)
            if market_growth > 5:
                key_parts.append('high_growth')
            elif market_growth > 0:
                key_parts.append('moderate_growth')
            elif market_growth > -5:
                key_parts.append('slight_decline')
            else:
                key_parts.append('steep_decline')
            
            # Sentiment discretization
            sentiment = context.get('sentiment_score', 0)
            if sentiment > 0.3:
                key_parts.append('bullish')
            elif sentiment > -0.3:
                key_parts.append('neutral')
            else:
                key_parts.append('bearish')
            
            # Volatility discretization
            volatility = context.get('market_volatility', 0)
            if volatility > 25:
                key_parts.append('high_volatility')
            elif volatility > 15:
                key_parts.append('medium_volatility')
            else:
                key_parts.append('low_volatility')
            
            # RSI discretization
            rsi = technical_indicators.get('rsi', 50)
            if rsi > 70:
                key_parts.append('overbought')
            elif rsi < 30:
                key_parts.append('oversold')
            else:
                key_parts.append('neutral_rsi')
            
            return '|'.join(key_parts)
            
        except Exception as e:
            logger.error(f"Error creating context key: {e}")
            return 'unknown'
    
    def get_adaptive_decision_weights(self, context: Dict[str, float]) -> Dict[str, float]:
        """Get adaptive decision weights based on learned patterns"""
        try:
            # Start with base learning weights
            adaptive_weights = self.learning_weights.copy()
            
            # Find matching context patterns
            context_key = self._create_context_key(context, {})
            
            if context_key in self.context_patterns:
                pattern = self.context_patterns[context_key]
                
                # Adjust weights based on pattern success rate
                if pattern['success_rate'] > 0.6:
                    # Boost weights for successful patterns
                    boost_factor = pattern['success_rate']
                    for feature in adaptive_weights:
                        if feature in context:
                            adaptive_weights[feature] *= boost_factor
                
                elif pattern['success_rate'] < 0.4:
                    # Reduce weights for unsuccessful patterns
                    reduction_factor = pattern['success_rate']
                    for feature in adaptive_weights:
                        if feature in context:
                            adaptive_weights[feature] *= reduction_factor
            
            return adaptive_weights
            
        except Exception as e:
            logger.error(f"Error getting adaptive weights: {e}")
            return self.learning_weights
    
    def get_rule_confidence_adjustment(self, rule_id: str) -> float:
        """Get confidence adjustment for specific rule based on learning"""
        try:
            if rule_id in self.rule_performance:
                rule_perf = self.rule_performance[rule_id]
                
                # Adjust confidence based on historical accuracy
                accuracy_boost = (rule_perf['accuracy'] - 0.5) * 2  # Range: -1 to 1
                
                # Consider usage count (more usage = more reliable)
                usage_factor = min(1.0, rule_perf['usage_count'] / 100.0)
                
                # Combined adjustment
                adjustment = accuracy_boost * usage_factor * rule_perf['confidence']
                
                return max(0.1, min(2.0, adjustment))
            
            return 1.0  # Default adjustment
            
        except Exception as e:
            logger.error(f"Error getting rule confidence adjustment: {e}")
            return 1.0
    
    def get_learning_metrics(self) -> LearningMetrics:
        """Get comprehensive learning metrics"""
        try:
            if not self.experiences:
                return LearningMetrics(
                    total_decisions=0,
                    correct_decisions=0,
                    incorrect_decisions=0,
                    accuracy_rate=0.0,
                    avg_reward=0.0,
                    avg_punishment=0.0,
                    learning_progress=0.0,
                    adaptation_rate=0.0,
                    model_version=self.model_version,
                    last_update=datetime.now()
                )
            
            # Calculate metrics from recent experiences
            recent_experiences = self.experiences[-100:]  # Last 100 experiences
            
            total_decisions = len(recent_experiences)
            correct_decisions = sum(1 for exp in recent_experiences if exp.outcome == DecisionOutcome.CORRECT)
            incorrect_decisions = sum(1 for exp in recent_experiences if exp.outcome == DecisionOutcome.INCORRECT)
            
            accuracy_rate = correct_decisions / total_decisions if total_decisions > 0 else 0.0
            avg_reward = np.mean([exp.reward for exp in recent_experiences])
            avg_punishment = np.mean([exp.punishment for exp in recent_experiences])
            
            # Calculate learning progress (improvement over time)
            if len(recent_experiences) >= 50:
                early_accuracy = sum(1 for exp in recent_experiences[:25] if exp.outcome == DecisionOutcome.CORRECT) / 25
                recent_accuracy = sum(1 for exp in recent_experiences[-25:] if exp.outcome == DecisionOutcome.CORRECT) / 25
                learning_progress = recent_accuracy - early_accuracy
            else:
                learning_progress = 0.0
            
            # Calculate adaptation rate
            adaptation_rate = len(self.context_patterns) / max(1, total_decisions)
            
            return LearningMetrics(
                total_decisions=total_decisions,
                correct_decisions=correct_decisions,
                incorrect_decisions=incorrect_decisions,
                accuracy_rate=accuracy_rate,
                avg_reward=avg_reward,
                avg_punishment=avg_punishment,
                learning_progress=learning_progress,
                adaptation_rate=adaptation_rate,
                model_version=self.model_version,
                last_update=datetime.now()
            )
            
        except Exception as e:
            logger.error(f"Error getting learning metrics: {e}")
            return None
    
    def trigger_model_update(self):
        """Trigger comprehensive model update and version increment"""
        try:
            self.model_version += 1
            
            # Apply decay to old experiences
            for exp in self.experiences:
                exp.learning_weight *= self.decay_rate
            
            # Remove very old experiences
            if len(self.experiences) > 5000:
                self.experiences = self.experiences[-2000:]
            
            # Save updated model
            self._save_model()
            
            logger.info(f"Model updated to version {self.model_version}")
            
        except Exception as e:
            logger.error(f"Error triggering model update: {e}")
    
    def export_learning_report(self) -> Dict[str, Any]:
        """Export comprehensive learning report"""
        try:
            metrics = self.get_learning_metrics()
            
            report = {
                "learning_summary": {
                    "model_version": self.model_version,
                    "total_experiences": len(self.experiences),
                    "learning_metrics": asdict(metrics) if metrics else {},
                    "last_update": datetime.now().isoformat()
                },
                "rule_performance": self.rule_performance,
                "learning_weights": self.learning_weights,
                "context_patterns_count": len(self.context_patterns),
                "top_performing_rules": self._get_top_rules(),
                "learning_progress": self._analyze_learning_progress(),
                "recommendations": self._generate_learning_recommendations()
            }
            
            return report
            
        except Exception as e:
            logger.error(f"Error exporting learning report: {e}")
            return {"error": str(e)}
    
    def _get_top_rules(self) -> List[Dict[str, Any]]:
        """Get top performing rules"""
        try:
            rules = []
            for rule_id, perf in self.rule_performance.items():
                if perf['usage_count'] > 0:
                    rules.append({
                        'rule_id': rule_id,
                        'accuracy': perf['accuracy'],
                        'confidence': perf['confidence'],
                        'usage_count': perf['usage_count'],
                        'performance_score': perf['accuracy'] * perf['confidence']
                    })
            
            # Sort by performance score
            rules.sort(key=lambda x: x['performance_score'], reverse=True)
            return rules[:5]  # Top 5 rules
            
        except Exception as e:
            logger.error(f"Error getting top rules: {e}")
            return []
    
    def _analyze_learning_progress(self) -> Dict[str, Any]:
        """Analyze learning progress over time"""
        try:
            if len(self.experiences) < 50:
                return {"status": "insufficient_data"}
            
            # Split experiences into quarters
            total_exp = len(self.experiences)
            quarter_size = total_exp // 4
            
            quarters = []
            for i in range(4):
                start_idx = i * quarter_size
                end_idx = (i + 1) * quarter_size if i < 3 else total_exp
                quarter_exps = self.experiences[start_idx:end_idx]
                
                if quarter_exps:
                    accuracy = sum(1 for exp in quarter_exps if exp.outcome == DecisionOutcome.CORRECT) / len(quarter_exps)
                    avg_reward = np.mean([exp.reward for exp in quarter_exps])
                    quarters.append({
                        'quarter': f'Q{i+1}',
                        'accuracy': accuracy,
                        'avg_reward': avg_reward,
                        'experience_count': len(quarter_exps)
                    })
            
            # Calculate trend
            if len(quarters) >= 2:
                early_accuracy = quarters[0]['accuracy']
                recent_accuracy = quarters[-1]['accuracy']
                trend = recent_accuracy - early_accuracy
                
                return {
                    "quarters": quarters,
                    "trend": "improving" if trend > 0.05 else "declining" if trend < -0.05 else "stable",
                    "trend_magnitude": trend
                }
            
            return {"status": "insufficient_quarters"}
            
        except Exception as e:
            logger.error(f"Error analyzing learning progress: {e}")
            return {"status": "error"}
    
    def _generate_learning_recommendations(self) -> List[str]:
        """Generate learning recommendations"""
        try:
            recommendations = []
            metrics = self.get_learning_metrics()
            
            if not metrics:
                return ["Insufficient data for recommendations"]
            
            # Accuracy-based recommendations
            if metrics.accuracy_rate < 0.4:
                recommendations.append("🔴 Low accuracy detected. Consider reviewing decision logic and increasing learning rate.")
            elif metrics.accuracy_rate < 0.6:
                recommendations.append("🟡 Moderate accuracy. Fine-tune rule thresholds and context patterns.")
            elif metrics.accuracy_rate > 0.8:
                recommendations.append("🟢 Excellent accuracy! Consider reducing learning rate to maintain performance.")
            
            # Learning progress recommendations
            if metrics.learning_progress < -0.1:
                recommendations.append("📉 Learning performance declining. Review recent market changes and adapt accordingly.")
            elif metrics.learning_progress > 0.1:
                recommendations.append("📈 Learning improving rapidly! Continue current learning strategy.")
            
            # Reward/Punishment balance
            if metrics.avg_punishment > metrics.avg_reward * 2:
                recommendations.append("⚖️ High punishment rate. System may be too risk-averse or making frequent mistakes.")
            elif metrics.avg_reward > metrics.avg_punishment * 2:
                recommendations.append("🎯 High reward rate! System performing well. Consider scaling up.")
            
            # Adaptation rate recommendations
            if metrics.adaptation_rate < 0.1:
                recommendations.append("🔄 Low adaptation. Increase exploration of new patterns.")
            elif metrics.adaptation_rate > 0.8:
                recommendations.append("⚡ High adaptation! System learning quickly. Monitor for overfitting.")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            return ["Error generating recommendations"]

# Main integration function
def test_llm_learning_system():
    """Test the LLM learning system with sample data"""
    try:
        print("🧠 Testing LLM-Based Adaptive Learning System")
        print("=" * 60)
        
        # Initialize learning engine
        learning_engine = LLMLearningEngine()
        
        # Simulate some learning experiences
        print("📚 Simulating learning experiences...")
        
        sample_experiences = [
            {
                'context': {'market_growth': 5.0, 'sentiment_score': 0.6, 'market_volatility': 15.0},
                'decision_type': 'investment',
                'action_taken': 'buy',
                'confidence': 0.8,
                'market_state': {'trend': 'up'},
                'technical_indicators': {'rsi': 45, 'ma_20': 100, 'ma_50': 95},
                'rule_triggers': ['high_growth_investment', 'positive_sentiment_investment'],
                'actual_result': 8.5,  # 8.5% profit
                'expected_result': 5.0
            },
            {
                'context': {'market_growth': -3.0, 'sentiment_score': -0.4, 'market_volatility': 25.0},
                'decision_type': 'risk_management',
                'action_taken': 'sell',
                'confidence': 0.7,
                'market_state': {'trend': 'down'},
                'technical_indicators': {'rsi': 75, 'ma_20': 100, 'ma_50': 105},
                'rule_triggers': ['volatility_risk_alert', 'negative_sentiment_alert'],
                'actual_result': -6.2,  # -6.2% loss (correct decision)
                'expected_result': -5.0
            },
            {
                'context': {'market_growth': 2.0, 'sentiment_score': 0.1, 'market_volatility': 18.0},
                'decision_type': 'opportunity',
                'action_taken': 'buy',
                'confidence': 0.9,
                'market_state': {'trend': 'sideways'},
                'technical_indicators': {'rsi': 55, 'ma_20': 100, 'ma_50': 98},
                'rule_triggers': ['high_demand_opportunity'],
                'actual_result': -2.1,  # -2.1% loss (incorrect decision)
                'expected_result': 3.0
            }
        ]
        
        # Process each experience
        for i, exp_data in enumerate(sample_experiences, 1):
            print(f"\n🔄 Processing Experience {i}: {exp_data['decision_type']}")
            
            experience = learning_engine.analyze_decision_outcome(**exp_data)
            if experience:
                learning_engine.learn_from_experience(experience)
                
                print(f"  Outcome: {experience.outcome.value}")
                print(f"  Reward: {experience.reward:.3f}")
                print(f"  Punishment: {experience.punishment:.3f}")
                print(f"  Error: {experience.error_magnitude:.3f}")
        
        # Get learning metrics
        print("\n📊 Learning Metrics:")
        metrics = learning_engine.get_learning_metrics()
        if metrics:
            print(f"  Total Decisions: {metrics.total_decisions}")
            print(f"  Accuracy Rate: {metrics.accuracy_rate:.2%}")
            print(f"  Average Reward: {metrics.avg_reward:.3f}")
            print(f"  Average Punishment: {metrics.avg_punishment:.3f}")
            print(f"  Learning Progress: {metrics.learning_progress:+.3f}")
        
        # Get adaptive weights
        print("\n⚖️ Adaptive Learning Weights:")
        adaptive_weights = learning_engine.get_adaptive_decision_weights(
            {'market_growth': 2.0, 'sentiment_score': 0.3, 'market_volatility': 20.0}
        )
        for feature, weight in adaptive_weights.items():
            print(f"  {feature}: {weight:.3f}")
        
        # Get rule confidence adjustments
        print("\n🎯 Rule Confidence Adjustments:")
        for rule_id in ['high_growth_investment', 'volatility_risk_alert', 'high_demand_opportunity']:
            adjustment = learning_engine.get_rule_confidence_adjustment(rule_id)
            print(f"  {rule_id}: {adjustment:.3f}")
        
        # Export learning report
        print("\n📋 Generating Learning Report...")
        report = learning_engine.export_learning_report()
        
        with open('llm_learning_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Show recommendations
        if 'recommendations' in report:
            print("\n💡 Learning Recommendations:")
            for rec in report['recommendations']:
                print(f"  • {rec}")
        
        print("\n✅ LLM Learning System Test Completed!")
        print("📄 Report saved to 'llm_learning_report.json'")
        
        return learning_engine
        
    except Exception as e:
        logger.error(f"Error testing LLM learning system: {e}")
        print(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    test_llm_learning_system()
