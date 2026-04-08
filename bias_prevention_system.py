
"""
Bias Prevention System
Comprehensive system to prevent biasing and ensure fair trading
"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any

class BiasPreventionSystem:
    """Comprehensive bias prevention system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.bias_prevention_active = True
        self.prevention_logs = []
        
    def enable_continuous_monitoring(self):
        """Enable continuous bias monitoring"""
        print("🔒 ENABLING CONTINUOUS BIAS MONITORING")
        
        # Monitor weight distribution every 5 seconds
        import threading
        import time
        
        def monitor_weights():
            while self.bias_prevention_active:
                try:
                    self._check_weight_distribution()
                    self._check_learning_parameters()
                    time.sleep(5)
                except Exception as e:
                    self.logger.error(f"Monitoring error: {e}")
        
        monitor_thread = threading.Thread(target=monitor_weights, daemon=True)
        monitor_thread.start()
        
        print("  ✅ Continuous monitoring enabled")
    
    def _check_weight_distribution(self):
        """Check weight distribution for bias"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            engine = LLMLearningEngine()
            weights = engine.learning_weights
            
            # Check for bias indicators
            max_weight = max(weights.values())
            min_weight = min(weights.values())
            ratio = max_weight / min_weight if min_weight > 0 else float('inf')
            
            if ratio > 10:
                self._log_prevention_event("WEIGHT_BIAS", f"Weight ratio: {ratio:.2f}")
                self._auto_correct_weights(engine)
            
        except Exception as e:
            self.logger.error(f"Weight distribution check error: {e}")
    
    def _check_learning_parameters(self):
        """Check learning parameters for tampering"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            engine = LLMLearningEngine()
            
            # Check for suspicious parameters
            if engine.learning_rate > 0.5:
                self._log_prevention_event("LEARNING_RATE_TAMPERING", f"Rate: {engine.learning_rate}")
                engine.learning_rate = 0.1  # Auto-correct
                self.logger.info("Auto-corrected learning rate to 0.1")
            
        except Exception as e:
            self.logger.error(f"Learning parameter check error: {e}")
    
    def _auto_correct_weights(self, engine):
        """Auto-correct biased weights"""
        try:
            # Normalize weights to fair distribution
            total_weight = sum(engine.learning_weights.values())
            if total_weight > 0:
                for feature in engine.learning_weights:
                    engine.learning_weights[feature] = 1.0 / len(engine.learning_weights)
                
                self.logger.info("Auto-corrected weights to fair distribution")
                self._log_prevention_event("WEIGHT_AUTO_CORRECTION", "Weights normalized")
            
        except Exception as e:
            self.logger.error(f"Weight auto-correction error: {e}")
    
    def _log_prevention_event(self, event_type, details):
        """Log bias prevention event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'event_type': event_type,
            'details': details,
            'action_taken': 'AUTO_CORRECTED'
        }
        self.prevention_logs.append(event)
        
        self.logger.warning(f"🛡️ BIAS PREVENTION: {event_type} - {details}")
    
    def get_prevention_report(self) -> dict:
        """Get bias prevention report"""
        return {
            'prevention_active': self.bias_prevention_active,
            'events_logged': len(self.prevention_logs),
            'recent_events': self.prevention_logs[-10:],
            'system_status': 'PROTECTED'
        }

# Global bias prevention system
bias_prevention = BiasPreventionSystem()
