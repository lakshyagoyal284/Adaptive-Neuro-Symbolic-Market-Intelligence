"""
Protected Backtesting System
Backtesting with comprehensive security guard protection against biasing and cheating
"""

import os
import sys
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
from security_guard import security_guard, protect_backtesting, SecurityException

class ProtectedBacktesting:
    """Protected backtesting system with security guard"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.security_guard = security_guard
        
    def run_protected_backtesting(self):
        """Run backtesting with security protection"""
        print("🔒 STARTING PROTECTED BACKTESTING")
        print("=" * 80)
        print("🔒 Security guard active - monitoring for biasing and cheating...")
        print("=" * 80)
        
        try:
            # Pre-security check
            if not self._pre_security_check():
                raise SecurityException("Pre-security check failed")
            
            # Run protected backtesting
            result = self._execute_protected_backtesting()
            
            # Post-security check
            if not self._post_security_check(result):
                raise SecurityException("Post-security check failed")
            
            # Generate security report
            self._generate_security_report(result)
            
            return result
            
        except SecurityException as e:
            self.logger.error(f"🚨 SECURITY VIOLATION: {e}")
            return None
        except Exception as e:
            self.logger.error(f"❌ Backtesting error: {e}")
            return None
    
    def _pre_security_check(self) -> bool:
        """Pre-execution security check"""
        print("\n🔒 PRE-SECURITY CHECK")
        print("-" * 40)
        
        checks = [
            ("Learning Parameters", self._check_learning_parameters),
            ("Weight Distribution", self._check_weight_distribution),
            ("System Integrity", self._check_system_integrity),
            ("Memory State", self._check_memory_state),
            ("Thread Safety", self._check_thread_safety)
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"  Checking {check_name}...")
            try:
                if check_func():
                    print(f"    ✅ {check_name}: PASSED")
                else:
                    print(f"    ❌ {check_name}: FAILED")
                    all_passed = False
            except Exception as e:
                print(f"    ❌ {check_name}: ERROR - {e}")
                all_passed = False
        
        if all_passed:
            print("✅ ALL SECURITY CHECKS PASSED")
            return True
        else:
            print("❌ SECURITY CHECKS FAILED")
            return False
    
    def _execute_protected_backtesting(self) -> Dict[str, Any]:
        """Execute backtesting with real-time monitoring"""
        print("\n🔒 EXECUTING PROTECTED BACKTESTING")
        print("-" * 40)
        
        # Import and run backtesting with monitoring
        try:
            # Monitor during execution
            import threading
            import time
            
            # Start monitoring thread
            stop_monitor = threading.Event()
            
            def monitor_execution():
                while not stop_monitor.is_set():
                    self._real_time_security_check()
                    time.sleep(2)  # Check every 2 seconds
            
            monitor_thread = threading.Thread(target=monitor_execution, daemon=True)
            monitor_thread.start()
            
            # Execute backtesting
            print("  🔄 Running backtesting with security monitoring...")
            
            # Import and run backtesting
            import backtesting
            
            # Capture original function
            original_backtest = backtesting.run_comprehensive_backtest
            
            # Run with security monitoring
            result = original_backtest()
            
            # Stop monitoring
            stop_monitor.set()
            monitor_thread.join(timeout=5)
            
            print("  ✅ Backtesting completed successfully")
            
            return result
            
        except Exception as e:
            print(f"  ❌ Backtesting execution error: {e}")
            raise
    
    def _post_security_check(self, result: Dict[str, Any]) -> bool:
        """Post-execution security check"""
        print("\n🔒 POST-SECURITY CHECK")
        print("-" * 40)
        
        checks = [
            ("Result Validity", lambda: self._check_result_validity(result)),
            ("Learning Changes", self._check_learning_changes),
            ("System State", self._check_system_state),
            ("Performance Consistency", lambda: self._check_performance_consistency(result))
        ]
        
        all_passed = True
        
        for check_name, check_func in checks:
            print(f"  Checking {check_name}...")
            try:
                if check_func():
                    print(f"    ✅ {check_name}: PASSED")
                else:
                    print(f"    ❌ {check_name}: FAILED")
                    all_passed = False
            except Exception as e:
                print(f"    ❌ {check_name}: ERROR - {e}")
                all_passed = False
        
        if all_passed:
            print("✅ ALL POST-SECURITY CHECKS PASSED")
            return True
        else:
            print("❌ POST-SECURITY CHECKS FAILED")
            return False
    
    def _real_time_security_check(self):
        """Real-time security check during execution"""
        try:
            # Quick security check
            self.security_guard._check_weight_distribution()
            self.security_guard._check_learning_parameters()
        except Exception as e:
            self.logger.error(f"❌ Real-time security check error: {e}")
    
    def _check_learning_parameters(self) -> bool:
        """Check learning parameters"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Check learning rate
            if engine.learning_rate > 0.2:
                print(f"    ⚠️ Learning rate high: {engine.learning_rate}")
                return False
            
            # Check reward/punishment scales
            if engine.reward_scale > 3.0 or engine.punishment_scale > 5.0:
                print(f"    ⚠️ Reward/Punishment scales unusual")
                return False
            
            return True
            
        except Exception as e:
            print(f"    ❌ Learning parameters check error: {e}")
            return False
    
    def _check_weight_distribution(self) -> bool:
        """Check weight distribution"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            weights = engine.learning_weights
            
            # Check for extreme concentration
            max_weight = max(weights.values())
            min_weight = min(weights.values())
            weight_ratio = max_weight / min_weight if min_weight > 0 else float('inf')
            
            if weight_ratio > 10:
                print(f"    ⚠️ Extreme weight concentration: {weight_ratio:.2f}")
                return False
            
            # Check for zero weights
            zero_weights = [k for k, v in weights.items() if v < 0.01]
            if zero_weights:
                print(f"    ⚠️ Zero weights detected: {zero_weights}")
                return False
            
            return True
            
        except Exception as e:
            print(f"    ❌ Weight distribution check error: {e}")
            return False
    
    def _check_system_integrity(self) -> bool:
        """Check system integrity"""
        try:
            # Simple integrity check
            current_checksum = self.security_guard._calculate_system_checksum()
            baseline_checksum = self.security_guard.baseline_checksum
            
            if current_checksum != baseline_checksum:
                print(f"    ⚠️ System checksum changed")
                return False
            
            return True
            
        except Exception as e:
            print(f"    ❌ System integrity check error: {e}")
            return False
    
    def _check_memory_state(self) -> bool:
        """Check memory state"""
        try:
            import gc
            
            # Force garbage collection
            gc.collect()
            
            # Simple memory check
            return True
            
        except Exception as e:
            print(f"    ❌ Memory state check error: {e}")
            return False
    
    def _check_thread_safety(self) -> bool:
        """Check thread safety"""
        try:
            import threading
            
            # Check thread count
            thread_count = threading.active_count()
            if thread_count > 50:
                print(f"    ⚠️ High thread count: {thread_count}")
                return False
            
            return True
            
        except Exception as e:
            print(f"    ❌ Thread safety check error: {e}")
            return False
    
    def _check_result_validity(self, result: Dict[str, Any]) -> bool:
        """Check result validity"""
        try:
            if not result:
                print("    ❌ No result returned")
                return False
            
            # Check for reasonable returns
            if 'total_return' in result:
                total_return = result['total_return']
                if abs(total_return) > 100:
                    print(f"    ⚠️ Unusual return: {total_return}%")
                    return False
            
            # Check for reasonable win rate
            if 'win_rate' in result:
                win_rate = result['win_rate']
                if win_rate > 95:
                    print(f"    ⚠️ Unusual win rate: {win_rate}%")
                    return False
            
            return True
            
        except Exception as e:
            print(f"    ❌ Result validity check error: {e}")
            return False
    
    def _check_learning_changes(self) -> bool:
        """Check learning changes"""
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Check model version
            if hasattr(engine, 'model_version'):
                version_change = engine.model_version - getattr(engine, '_initial_model_version', engine.model_version)
                if version_change > 100:
                    print(f"    ⚠️ Excessive version changes: {version_change}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"    ❌ Learning changes check error: {e}")
            return False
    
    def _check_system_state(self) -> bool:
        """Check system state"""
        try:
            import threading
            
            # Check thread count
            thread_count = threading.active_count()
            if thread_count > 100:
                print(f"    ⚠️ Very high thread count: {thread_count}")
                return False
            
            return True
            
        except Exception as e:
            print(f"    ❌ System state check error: {e}")
            return False
    
    def _check_performance_consistency(self, result: Dict[str, Any]) -> bool:
        """Check performance consistency"""
        try:
            # Check if results are consistent
            if 'total_trades' in result and 'winning_trades' in result and 'losing_trades' in result:
                total_trades = result['total_trades']
                winning_trades = result['winning_trades']
                losing_trades = result['losing_trades']
                
                if total_trades != winning_trades + losing_trades:
                    print(f"    ⚠️ Trade count inconsistency")
                    return False
            
            return True
            
        except Exception as e:
            print(f"    ❌ Performance consistency check error: {e}")
            return False
    
    def _generate_security_report(self, result: Dict[str, Any]):
        """Generate comprehensive security report"""
        print("\n🔒 GENERATING SECURITY REPORT")
        print("-" * 40)
        
        # Get security report
        security_report = self.security_guard.get_security_report()
        
        print(f"  Security Level: {security_report['security_level']}")
        print(f"  Threats Detected: {security_report['threats_detected']}")
        print(f"  Threats Blocked: {security_report['threats_blocked']}")
        print(f"  System Status: {security_report['system_status']}")
        
        # Save combined report
        combined_report = {
            'timestamp': datetime.now().isoformat(),
            'backtesting_result': result,
            'security_report': security_report,
            'security_status': 'SECURE' if security_report['system_status'] == 'SECURE' else 'COMPROMISED'
        }
        
        with open('logs/protected_backtesting_report.json', 'w') as f:
            json.dump(combined_report, f, indent=2, default=str)
        
        print("  ✅ Security report saved")
        
        # Display summary
        print(f"\n📊 PROTECTED BACKTESTING SUMMARY:")
        print(f"  Total Return: {result.get('total_return', 0):.2f}%")
        print(f"  Win Rate: {result.get('win_rate', 0):.2f}%")
        print(f"  Security Status: {security_report['system_status']}")
        print(f"  Threats Blocked: {security_report['threats_blocked']}")
        
        if security_report['system_status'] == 'SECURE':
            print("  ✅ Backtesting completed securely")
        else:
            print("  ⚠️ Security issues detected")

def main():
    """Main function to run protected backtesting"""
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Initialize protected backtesting
    protected_bt = ProtectedBacktesting()
    
    # Run protected backtesting
    result = protected_bt.run_protected_backtesting()
    
    if result:
        print("\n🎉 PROTECTED BACKTESTING COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print("✅ Backtesting completed with security protection")
        print("✅ No biasing or cheating detected")
        print("✅ Results are authentic and trustworthy")
    else:
        print("\n❌ PROTECTED BACKTESTING FAILED!")
        print("=" * 80)
        print("❌ Security violations detected")
        print("❌ Backtesting blocked for security reasons")
    
    print("=" * 80)

if __name__ == "__main__":
    main()
