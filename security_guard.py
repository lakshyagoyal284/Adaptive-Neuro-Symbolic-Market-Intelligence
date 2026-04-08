"""
Security Guard System
Prevents biasing and cheating during backtesting operations
"""

import os
import sys
import json
import hashlib
import logging
import time
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

class SecurityLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class ThreatType(Enum):
    BIAS_MANIPULATION = "bias_manipulation"
    WEIGHT_TAMPERING = "weight_tampering"
    DATA_INJECTION = "data_injection"
    PARAMETER_TAMPERING = "parameter_tampering"
    RESULT_FABRICATION = "result_fabrication"
    MEMORY_CORRUPTION = "memory_corruption"
    THREAD_MANIPULATION = "thread_manipulation"
    CACHE_POISONING = "cache_poisoning"

@dataclass
class SecurityThreat:
    threat_type: ThreatType
    severity: SecurityLevel
    description: str
    evidence: Dict[str, Any]
    timestamp: datetime
    blocked: bool = False

class SecurityGuard:
    """Comprehensive security guard for backtesting operations"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.threats_detected = []
        self.security_logs = []
        self.lock = threading.Lock()
        
        # Security parameters
        self.max_weight_change = 0.1  # Maximum 10% change per update
        self.max_learning_rate = 0.2  # Maximum learning rate
        self.min_confidence = 0.1     # Minimum confidence threshold
        self.max_position_size = 0.3  # Maximum 30% position size
        
        # Baseline values for comparison
        self.baseline_weights = None
        self.baseline_learning_rate = None
        self.baseline_reward_scale = None
        self.baseline_punishment_scale = None
        
        # Initialize security
        self._initialize_security()
    
    def _initialize_security(self):
        """Initialize security monitoring"""
        self.logger.info("🔒 SECURITY GUARD INITIALIZED")
        self.logger.info("🔒 Monitoring for biasing and cheating attempts...")
        
        # Establish baseline values
        self._establish_baseline()
        
        # Start monitoring thread
        self._start_monitoring()
    
    def _establish_baseline(self):
        """Establish baseline values for security monitoring"""
        try:
            # Import learning engine to get baseline
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            self.baseline_weights = engine.learning_weights.copy()
            self.baseline_learning_rate = engine.learning_rate
            self.baseline_reward_scale = engine.reward_scale
            self.baseline_punishment_scale = engine.punishment_scale
            
            self.logger.info("🔒 BASELINE ESTABLISHED:")
            self.logger.info(f"  Learning Rate: {self.baseline_learning_rate}")
            self.logger.info(f"  Reward Scale: {self.baseline_reward_scale}")
            self.logger.info(f"  Punishment Scale: {self.baseline_punishment_scale}")
            
            # Calculate baseline checksum
            self.baseline_checksum = self._calculate_system_checksum()
            self.logger.info(f"  Baseline Checksum: {self.baseline_checksum}")
            
        except Exception as e:
            self.logger.error(f"❌ Error establishing baseline: {e}")
    
    def _start_monitoring(self):
        """Start continuous security monitoring"""
        def monitor():
            while True:
                try:
                    self._perform_security_check()
                    time.sleep(5)  # Check every 5 seconds
                except Exception as e:
                    self.logger.error(f"❌ Security monitoring error: {e}")
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
        self.logger.info("🔒 Security monitoring started")
    
    def protect_backtesting(self, backtesting_function):
        """Protect backtesting function from biasing and cheating"""
        def protected_backtesting(*args, **kwargs):
            self.logger.info("🔒 STARTING PROTECTED BACKTESTING")
            
            # Pre-execution security check
            if not self._pre_execution_check():
                raise SecurityException("Pre-execution security check failed")
            
            # Execute backtesting with monitoring
            try:
                start_time = time.time()
                result = backtesting_function(*args, **kwargs)
                execution_time = time.time() - start_time
                
                # Post-execution security check
                if not self._post_execution_check(result, execution_time):
                    raise SecurityException("Post-execution security check failed")
                
                self.logger.info("🔒 BACKTESTING COMPLETED SECURELY")
                return result
                
            except Exception as e:
                self._handle_security_violation("BACKTESTING_EXECUTION", str(e))
                raise
        
        return protected_backtesting
    
    def _pre_execution_check(self) -> bool:
        """Perform pre-execution security checks"""
        self.logger.info("🔒 PERFORMING PRE-EXECUTION SECURITY CHECK")
        
        # Check 1: Learning parameters
        if not self._check_learning_parameters():
            return False
        
        # Check 2: Weight distribution
        if not self._check_weight_distribution():
            return False
        
        # Check 3: System integrity
        if not self._check_system_integrity():
            return False
        
        # Check 4: Memory state
        if not self._check_memory_state():
            return False
        
        self.logger.info("✅ PRE-EXECUTION SECURITY CHECK PASSED")
        return True
    
    def _post_execution_check(self, result, execution_time: float) -> bool:
        """Perform post-execution security checks"""
        self.logger.info("🔒 PERFORMING POST-EXECUTION SECURITY CHECK")
        
        # Check 1: Result validity
        if not self._check_result_validity(result):
            return False
        
        # Check 2: Execution time
        if not self._check_execution_time(execution_time):
            return False
        
        # Check 3: Learning changes
        if not self._check_learning_changes():
            return False
        
        # Check 4: System state
        if not self._check_system_state():
            return False
        
        self.logger.info("✅ POST-EXECUTION SECURITY CHECK PASSED")
        return True
    
    def _check_learning_parameters(self) -> bool:
        """Check learning parameters for tampering"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Check learning rate
            if engine.learning_rate > self.max_learning_rate:
                threat = SecurityThreat(
                    threat_type=ThreatType.PARAMETER_TAMPERING,
                    severity=SecurityLevel.HIGH,
                    description="Learning rate exceeds maximum allowed",
                    evidence={"learning_rate": engine.learning_rate, "max_allowed": self.max_learning_rate},
                    timestamp=datetime.now()
                )
                self._handle_threat(threat)
                return False
            
            # Check reward/punishment scales
            if engine.reward_scale > self.baseline_reward_scale * 2:
                threat = SecurityThreat(
                    threat_type=ThreatType.PARAMETER_TAMPERING,
                    severity=SecurityLevel.MEDIUM,
                    description="Reward scale appears tampered",
                    evidence={"reward_scale": engine.reward_scale, "baseline": self.baseline_reward_scale},
                    timestamp=datetime.now()
                )
                self._handle_threat(threat)
            
            if engine.punishment_scale > self.baseline_punishment_scale * 2:
                threat = SecurityThreat(
                    threat_type=ThreatType.PARAMETER_TAMPERING,
                    severity=SecurityLevel.MEDIUM,
                    description="Punishment scale appears tampered",
                    evidence={"punishment_scale": engine.punishment_scale, "baseline": self.baseline_punishment_scale},
                    timestamp=datetime.now()
                )
                self._handle_threat(threat)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking learning parameters: {e}")
            return False
    
    def _check_weight_distribution(self) -> bool:
        """Check weight distribution for biasing"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            weights = engine.learning_weights
            
            # Check for extreme concentration
            max_weight = max(weights.values())
            min_weight = min(weights.values())
            weight_ratio = max_weight / min_weight if min_weight > 0 else float('inf')
            
            if weight_ratio > 10:  # More than 10:1 ratio
                threat = SecurityThreat(
                    threat_type=ThreatType.WEIGHT_TAMPERING,
                    severity=SecurityLevel.HIGH,
                    description="Weight distribution shows extreme bias",
                    evidence={"weight_ratio": weight_ratio, "max_weight": max_weight, "min_weight": min_weight},
                    timestamp=datetime.now()
                )
                self._handle_threat(threat)
                return False
            
            # Check for zero weights
            zero_weights = [k for k, v in weights.items() if v < 0.01]
            if zero_weights:
                threat = SecurityThreat(
                    threat_type=ThreatType.WEIGHT_TAMPERING,
                    severity=SecurityLevel.MEDIUM,
                    description="Some weights are effectively zero",
                    evidence={"zero_weights": zero_weights},
                    timestamp=datetime.now()
                )
                self._handle_threat(threat)
            
            # Check against baseline
            if self.baseline_weights:
                for feature, weight in weights.items():
                    if feature in self.baseline_weights:
                        change = abs(weight - self.baseline_weights[feature])
                        if change > self.max_weight_change:
                            threat = SecurityThreat(
                                threat_type=ThreatType.WEIGHT_TAMPERING,
                                severity=SecurityLevel.MEDIUM,
                                description=f"Weight for {feature} changed significantly",
                                evidence={"feature": feature, "change": change, "baseline": self.baseline_weights[feature]},
                                timestamp=datetime.now()
                            )
                            self._handle_threat(threat)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking weight distribution: {e}")
            return False
    
    def _check_system_integrity(self) -> bool:
        """Check system integrity"""
        try:
            current_checksum = self._calculate_system_checksum()
            
            if current_checksum != self.baseline_checksum:
                threat = SecurityThreat(
                    threat_type=ThreatType.MEMORY_CORRUPTION,
                    severity=SecurityLevel.CRITICAL,
                    description="System checksum changed - possible tampering",
                    evidence={"current_checksum": current_checksum, "baseline_checksum": self.baseline_checksum},
                    timestamp=datetime.now()
                )
                self._handle_threat(threat)
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking system integrity: {e}")
            return False
    
    def _check_memory_state(self) -> bool:
        """Check memory state for corruption"""
        try:
            import psutil
            import gc
            
            # Check memory usage
            process = psutil.Process()
            memory_info = process.memory_info()
            
            # Check for unusual memory patterns
            if memory_info.rss > 1024 * 1024 * 1024:  # More than 1GB
                threat = SecurityThreat(
                    threat_type=ThreatType.MEMORY_CORRUPTION,
                    severity=SecurityLevel.MEDIUM,
                    description="Unusual memory usage detected",
                    evidence={"memory_rss": memory_info.rss},
                    timestamp=datetime.now()
                )
                self._handle_threat(threat)
            
            # Force garbage collection
            gc.collect()
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking memory state: {e}")
            return False
    
    def _check_result_validity(self, result) -> bool:
        """Check result validity"""
        try:
            # Check if result is reasonable
            if hasattr(result, 'get'):
                # Check for reasonable returns
                if 'total_return' in result:
                    total_return = result['total_return']
                    if abs(total_return) > 100:  # More than 100% return is suspicious
                        threat = SecurityThreat(
                            threat_type=ThreatType.RESULT_FABRICATION,
                            severity=SecurityLevel.HIGH,
                            description="Unusually high return detected",
                            evidence={"total_return": total_return},
                            timestamp=datetime.now()
                        )
                        self._handle_threat(threat)
                        return False
                
                # Check for reasonable win rate
                if 'win_rate' in result:
                    win_rate = result['win_rate']
                    if win_rate > 95:  # More than 95% win rate is suspicious
                        threat = SecurityThreat(
                            threat_type=ThreatType.RESULT_FABRICATION,
                            severity=SecurityLevel.HIGH,
                            description="Unusually high win rate detected",
                            evidence={"win_rate": win_rate},
                            timestamp=datetime.now()
                        )
                        self._handle_threat(threat)
                        return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking result validity: {e}")
            return False
    
    def _check_execution_time(self, execution_time: float) -> bool:
        """Check execution time"""
        if execution_time > 300:  # More than 5 minutes is suspicious
            threat = SecurityThreat(
                threat_type=ThreatType.THREAD_MANIPULATION,
                severity=SecurityLevel.MEDIUM,
                description="Unusually long execution time",
                evidence={"execution_time": execution_time},
                timestamp=datetime.now()
            )
            self._handle_threat(threat)
        
        return True
    
    def _check_learning_changes(self) -> bool:
        """Check learning changes for biasing"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Check model version
            if hasattr(engine, 'model_version'):
                version_change = engine.model_version - getattr(engine, '_initial_model_version', engine.model_version)
                if version_change > 100:  # More than 100 versions is suspicious
                    threat = SecurityThreat(
                        threat_type=ThreatType.BIAS_MANIPULATION,
                        severity=SecurityLevel.MEDIUM,
                        description="Excessive model version changes",
                        evidence={"version_change": version_change},
                        timestamp=datetime.now()
                    )
                    self._handle_threat(threat)
            
            # Check experience count
            if hasattr(engine, 'experiences'):
                experience_count = len(engine.experiences)
                if experience_count > 10000:  # More than 10k experiences is suspicious
                    threat = SecurityThreat(
                        threat_type=ThreatType.DATA_INJECTION,
                        severity=SecurityLevel.MEDIUM,
                        description="Unusually high experience count",
                        evidence={"experience_count": experience_count},
                        timestamp=datetime.now()
                    )
                    self._handle_threat(threat)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking learning changes: {e}")
            return False
    
    def _check_system_state(self) -> bool:
        """Check overall system state"""
        try:
            # Check thread count
            thread_count = threading.active_count()
            if thread_count > 50:  # More than 50 threads is suspicious
                threat = SecurityThreat(
                    threat_type=ThreatType.THREAD_MANIPULATION,
                    severity=SecurityLevel.MEDIUM,
                    description="Unusually high thread count",
                    evidence={"thread_count": thread_count},
                    timestamp=datetime.now()
                )
                self._handle_threat(threat)
            
            return True
            
        except Exception as e:
            self.logger.error(f"❌ Error checking system state: {e}")
            return False
    
    def _perform_security_check(self):
        """Perform periodic security check"""
        with self.lock:
            try:
                # Check weight distribution
                self._check_weight_distribution()
                
                # Check learning parameters
                self._check_learning_parameters()
                
                # Check system integrity
                self._check_system_integrity()
                
                # Check memory state
                self._check_memory_state()
                
            except Exception as e:
                self.logger.error(f"❌ Error in periodic security check: {e}")
    
    def _calculate_system_checksum(self) -> str:
        """Calculate system checksum"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Create checksum from key parameters
            checksum_data = {
                'learning_rate': engine.learning_rate,
                'reward_scale': engine.reward_scale,
                'punishment_scale': engine.punishment_scale,
                'weights': engine.learning_weights,
                'model_version': getattr(engine, 'model_version', 1)
            }
            
            checksum_str = json.dumps(checksum_data, sort_keys=True)
            return hashlib.sha256(checksum_str.encode()).hexdigest()
            
        except Exception as e:
            self.logger.error(f"❌ Error calculating checksum: {e}")
            return "ERROR"
    
    def _handle_threat(self, threat: SecurityThreat):
        """Handle security threat"""
        with self.lock:
            self.threats_detected.append(threat)
            
            # Log threat
            self.logger.warning(f"🚨 SECURITY THREAT DETECTED: {threat.threat_type.value}")
            self.logger.warning(f"   Severity: {threat.severity.value}")
            self.logger.warning(f"   Description: {threat.description}")
            self.logger.warning(f"   Evidence: {threat.evidence}")
            
            # Take action based on severity
            if threat.severity == SecurityLevel.CRITICAL:
                self._block_operation(threat)
            elif threat.severity == SecurityLevel.HIGH:
                self._warn_user(threat)
            elif threat.severity == SecurityLevel.MEDIUM:
                self._log_threat(threat)
            
            # Save to security log
            self._save_security_log(threat)
    
    def _block_operation(self, threat: SecurityThreat):
        """Block operation due to critical threat"""
        threat.blocked = True
        self.logger.error(f"🚨 OPERATION BLOCKED: {threat.description}")
        
        # Could implement more sophisticated blocking here
        raise SecurityException(f"Operation blocked due to security threat: {threat.description}")
    
    def _warn_user(self, threat: SecurityThreat):
        """Warn user about high-level threat"""
        self.logger.warning(f"⚠️ SECURITY WARNING: {threat.description}")
    
    def _log_threat(self, threat: SecurityThreat):
        """Log medium-level threat"""
        self.logger.info(f"📋 SECURITY LOG: {threat.description}")
    
    def _save_security_log(self, threat: SecurityThreat):
        """Save security threat to log"""
        log_entry = {
            'timestamp': threat.timestamp.isoformat(),
            'threat_type': threat.threat_type.value,
            'severity': threat.severity.value,
            'description': threat.description,
            'evidence': threat.evidence,
            'blocked': threat.blocked
        }
        
        self.security_logs.append(log_entry)
        
        # Save to file
        try:
            with open('logs/security_guard_log.json', 'w') as f:
                json.dump(self.security_logs, f, indent=2, default=str)
        except Exception as e:
            self.logger.error(f"❌ Error saving security log: {e}")
    
    def _handle_security_violation(self, operation: str, details: str):
        """Handle security violation"""
        threat = SecurityThreat(
            threat_type=ThreatType.BIAS_MANIPULATION,
            severity=SecurityLevel.HIGH,
            description=f"Security violation in {operation}",
            evidence={"details": details},
            timestamp=datetime.now()
        )
        self._handle_threat(threat)
    
    def get_security_report(self) -> Dict[str, Any]:
        """Get comprehensive security report"""
        with self.lock:
            return {
                'timestamp': datetime.now().isoformat(),
                'threats_detected': len(self.threats_detected),
                'threats_blocked': len([t for t in self.threats_detected if t.blocked]),
                'security_level': self._calculate_security_level(),
                'threats_by_type': self._get_threats_by_type(),
                'threats_by_severity': self._get_threats_by_severity(),
                'recent_threats': [self._threat_to_dict(t) for t in self.threats_detected[-10:]],
                'system_status': 'SECURE' if len([t for t in self.threats_detected if t.blocked]) == 0 else 'COMPROMISED'
            }
    
    def _calculate_security_level(self) -> str:
        """Calculate current security level"""
        blocked_threats = len([t for t in self.threats_detected if t.blocked])
        total_threats = len(self.threats_detected)
        
        if blocked_threats > 0:
            return "COMPROMISED"
        elif total_threats > 10:
            return "MEDIUM"
        elif total_threats > 5:
            return "GOOD"
        else:
            return "EXCELLENT"
    
    def _get_threats_by_type(self) -> Dict[str, int]:
        """Get threats count by type"""
        threats_by_type = {}
        for threat in self.threats_detected:
            threat_type = threat.threat_type.value
            threats_by_type[threat_type] = threats_by_type.get(threat_type, 0) + 1
        return threats_by_type
    
    def _get_threats_by_severity(self) -> Dict[str, int]:
        """Get threats count by severity"""
        threats_by_severity = {}
        for threat in self.threats_detected:
            severity = threat.severity.value
            threats_by_severity[severity] = threats_by_severity.get(severity, 0) + 1
        return threats_by_severity
    
    def _threat_to_dict(self, threat: SecurityThreat) -> Dict[str, Any]:
        """Convert threat to dictionary"""
        return {
            'timestamp': threat.timestamp.isoformat(),
            'threat_type': threat.threat_type.value,
            'severity': threat.severity.value,
            'description': threat.description,
            'evidence': threat.evidence,
            'blocked': threat.blocked
        }

class SecurityException(Exception):
    """Security exception for security violations"""
    pass

# Global security guard instance
security_guard = SecurityGuard()

def protect_backtesting(backtesting_function):
    """Decorator to protect backtesting function"""
    return security_guard.protect_backtesting(backtesting_function)

def get_security_report() -> Dict[str, Any]:
    """Get current security report"""
    return security_guard.get_security_report()

def check_system_security() -> bool:
    """Check overall system security"""
    report = get_security_report()
    return report['system_status'] == 'SECURE'

if __name__ == "__main__":
    # Test security guard
    print("🔒 TESTING SECURITY GUARD")
    print("=" * 80)
    
    # Get security report
    report = get_security_report()
    
    print(f"📊 Security Level: {report['security_level']}")
    print(f"📊 Threats Detected: {report['threats_detected']}")
    print(f"📊 Threats Blocked: {report['threats_blocked']}")
    print(f"📊 System Status: {report['system_status']}")
    
    print("\n🎉 SECURITY GUARD TEST COMPLETED!")
    print("=" * 80)
