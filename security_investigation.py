"""
Security Check and Investigation
Comprehensive investigation to detect any biasing during backtesting
"""

import os
import sys
import json
import hashlib
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

class SecurityInvestigator:
    """Comprehensive security investigation system"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.investigation_results = {}
        
    def run_comprehensive_investigation(self):
        """Run comprehensive security investigation"""
        print("🔍 COMPREHENSIVE SECURITY INVESTIGATION")
        print("=" * 80)
        print("🔍 Investigating for biasing and security violations...")
        print("=" * 80)
        
        # Investigation 1: Weight Distribution Analysis
        weight_analysis = self.investigate_weight_distribution()
        
        # Investigation 2: Learning Parameter Analysis
        parameter_analysis = self.investigate_learning_parameters()
        
        # Investigation 3: Result Authenticity Check
        result_analysis = self.investigate_result_authenticity()
        
        # Investigation 4: System Integrity Check
        integrity_analysis = self.investigate_system_integrity()
        
        # Investigation 5: Timeline Analysis
        timeline_analysis = self.investigate_timeline_consistency()
        
        # Investigation 6: Bias Pattern Detection
        bias_analysis = self.detect_bias_patterns()
        
        # Compile results
        self.compile_investigation_report(
            weight_analysis, parameter_analysis, result_analysis,
            integrity_analysis, timeline_analysis, bias_analysis
        )
        
        return self.investigation_results
    
    def investigate_weight_distribution(self):
        """Investigate weight distribution for biasing"""
        print("\n🔍 INVESTIGATING WEIGHT DISTRIBUTION")
        print("-" * 50)
        
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            weights = engine.learning_weights
            
            # Analysis 1: Check for extreme concentration
            max_weight = max(weights.values())
            min_weight = min(weights.values())
            weight_ratio = max_weight / min_weight if min_weight > 0 else float('inf')
            
            # Analysis 2: Check for zero weights
            zero_weights = [k for k, v in weights.items() if v < 0.01]
            
            # Analysis 3: Check for suspicious patterns
            sorted_weights = sorted(weights.values(), reverse=True)
            top_3_sum = sum(sorted_weights[:3])
            total_weight = sum(weights.values())
            top_3_concentration = top_3_sum / total_weight if total_weight > 0 else 0
            
            # Analysis 4: Check weight distribution fairness
            expected_fair_weight = 1.0 / len(weights)  # Equal distribution
            weight_variance = sum((v - expected_fair_weight) ** 2 for v in weights.values()) / len(weights)
            
            results = {
                'max_weight': max_weight,
                'min_weight': min_weight,
                'weight_ratio': weight_ratio,
                'zero_weights': zero_weights,
                'top_3_concentration': top_3_concentration,
                'weight_variance': weight_variance,
                'bias_detected': False,
                'bias_level': 'NONE'
            }
            
            # Determine bias level
            if weight_ratio > 20:
                results['bias_detected'] = True
                results['bias_level'] = 'EXTREME'
                print(f"  🚨 EXTREME BIAS DETECTED: Weight ratio {weight_ratio:.2f}")
            elif weight_ratio > 10:
                results['bias_detected'] = True
                results['bias_level'] = 'HIGH'
                print(f"  ⚠️ HIGH BIAS DETECTED: Weight ratio {weight_ratio:.2f}")
            elif weight_ratio > 5:
                results['bias_level'] = 'MEDIUM'
                print(f"  ⚠️ MEDIUM BIAS DETECTED: Weight ratio {weight_ratio:.2f}")
            else:
                results['bias_level'] = 'LOW'
                print(f"  ✅ LOW BIAS: Weight ratio {weight_ratio:.2f}")
            
            if zero_weights:
                results['bias_detected'] = True
                print(f"  🚨 ZERO WEIGHTS DETECTED: {zero_weights}")
            
            if top_3_concentration > 0.7:
                results['bias_detected'] = True
                print(f"  🚨 EXTREME CONCENTRATION: {top_3_concentration:.2%}")
            
            print(f"  📊 Weight Distribution Analysis:")
            print(f"    Max Weight: {max_weight:.4f}")
            print(f"    Min Weight: {min_weight:.4f}")
            print(f"    Weight Ratio: {weight_ratio:.2f}")
            print(f"    Top 3 Concentration: {top_3_concentration:.2%}")
            print(f"    Weight Variance: {weight_variance:.6f}")
            
            return results
            
        except Exception as e:
            print(f"  ❌ Error investigating weight distribution: {e}")
            return {'error': str(e)}
    
    def investigate_learning_parameters(self):
        """Investigate learning parameters for tampering"""
        print("\n🔍 INVESTIGATING LEARNING PARAMETERS")
        print("-" * 50)
        
        try:
            from adaptive_module.llm_learning_engine import LLMLearningEngine
            
            engine = LLMLearningEngine()
            
            # Analysis 1: Check learning rate
            learning_rate = engine.learning_rate
            learning_rate_suspicious = learning_rate > 0.5 or learning_rate < 0.01
            
            # Analysis 2: Check reward/punishment scales
            reward_scale = engine.reward_scale
            punishment_scale = engine.punishment_scale
            reward_punishment_ratio = reward_scale / punishment_scale if punishment_scale > 0 else float('inf')
            
            # Analysis 3: Check for suspicious parameter combinations
            suspicious_combination = (
                learning_rate > 0.3 and reward_scale > 5.0 or
                punishment_scale > 10.0 or
                reward_punishment_ratio > 3.0
            )
            
            results = {
                'learning_rate': learning_rate,
                'reward_scale': reward_scale,
                'punishment_scale': punishment_scale,
                'reward_punishment_ratio': reward_punishment_ratio,
                'learning_rate_suspicious': learning_rate_suspicious,
                'suspicious_combination': suspicious_combination,
                'tampering_detected': False,
                'tampering_level': 'NONE'
            }
            
            # Determine tampering level
            if suspicious_combination:
                results['tampering_detected'] = True
                results['tampering_level'] = 'HIGH'
                print(f"  🚨 HIGH TAMPERING DETECTED: Suspicious parameter combination")
            elif learning_rate_suspicious:
                results['tampering_detected'] = True
                results['tampering_level'] = 'MEDIUM'
                print(f"  ⚠️ MEDIUM TAMPERING DETECTED: Learning rate {learning_rate}")
            else:
                results['tampering_level'] = 'LOW'
                print(f"  ✅ LOW TAMPERING: Parameters appear normal")
            
            print(f"  📊 Learning Parameter Analysis:")
            print(f"    Learning Rate: {learning_rate}")
            print(f"    Reward Scale: {reward_scale}")
            print(f"    Punishment Scale: {punishment_scale}")
            print(f"    Reward/Punishment Ratio: {reward_punishment_ratio:.2f}")
            
            return results
            
        except Exception as e:
            print(f"  ❌ Error investigating learning parameters: {e}")
            return {'error': str(e)}
    
    def investigate_result_authenticity(self):
        """Investigate result authenticity"""
        print("\n🔍 INVESTIGATING RESULT AUTHENTICITY")
        print("-" * 50)
        
        try:
            # Load backtest results
            with open('simple_backtest_report.json', 'r') as f:
                results = json.load(f)
            
            # Analysis 1: Check for unrealistic returns
            total_return = results.get('total_return', 0)
            win_rate = results.get('win_rate', 0)
            profit_factor = results.get('profit_factor', 0)
            
            unrealistic_return = abs(total_return) > 100
            unrealistic_win_rate = win_rate > 95
            unrealistic_profit_factor = profit_factor > 10
            
            # Analysis 2: Check for perfect patterns
            total_trades = results.get('total_trades', 0)
            winning_trades = results.get('winning_trades', 0)
            losing_trades = results.get('losing_trades', 0)
            
            perfect_pattern = (
                total_trades > 0 and
                (winning_trades == total_trades or losing_trades == total_trades)
            )
            
            # Analysis 3: Check for suspicious consistency
            avg_win = results.get('avg_win', 0)
            avg_loss = results.get('avg_loss', 0)
            
            suspicious_consistency = (
                avg_win > 50 and avg_loss > -1 and
                abs(avg_win) == abs(avg_loss) and
                win_rate == 50.0
            )
            
            results = {
                'total_return': total_return,
                'win_rate': win_rate,
                'profit_factor': profit_factor,
                'unrealistic_return': unrealistic_return,
                'unrealistic_win_rate': unrealistic_win_rate,
                'unrealistic_profit_factor': unrealistic_profit_factor,
                'perfect_pattern': perfect_pattern,
                'suspicious_consistency': suspicious_consistency,
                'fabrication_detected': False,
                'fabrication_level': 'NONE'
            }
            
            # Determine fabrication level
            if unrealistic_return or unrealistic_win_rate or unrealistic_profit_factor:
                results['fabrication_detected'] = True
                results['fabrication_level'] = 'HIGH'
                print(f"  🚨 HIGH FABRICATION DETECTED: Unrealistic results")
            elif perfect_pattern or suspicious_consistency:
                results['fabrication_detected'] = True
                results['fabrication_level'] = 'MEDIUM'
                print(f"  ⚠️ MEDIUM FABRICATION DETECTED: Suspicious patterns")
            else:
                results['fabrication_level'] = 'LOW'
                print(f"  ✅ LOW FABRICATION: Results appear authentic")
            
            print(f"  📊 Result Authenticity Analysis:")
            print(f"    Total Return: {total_return:.2f}%")
            print(f"    Win Rate: {win_rate:.2f}%")
            print(f"    Profit Factor: {profit_factor:.2f}")
            print(f"    Total Trades: {total_trades}")
            print(f"    Winning Trades: {winning_trades}")
            print(f"    Losing Trades: {losing_trades}")
            
            return results
            
        except Exception as e:
            print(f"  ❌ Error investigating result authenticity: {e}")
            return {'error': str(e)}
    
    def investigate_system_integrity(self):
        """Investigate system integrity"""
        print("\n🔍 INVESTIGATING SYSTEM INTEGRITY")
        print("-" * 50)
        
        try:
            # Analysis 1: Check file integrity
            files_to_check = [
                'adaptive_module/llm_learning_engine.py',
                'symbolic_engine/rules.py',
                'symbolic_engine/decision_engine.py',
                'market_data_processor.py',
                'backtesting.py'
            ]
            
            file_integrity_issues = []
            for file_path in files_to_check:
                if os.path.exists(file_path):
                    # Check file size and modification time
                    stat = os.stat(file_path)
                    file_size = stat.st_size
                    
                    # Check for unusually large files
                    if file_size > 10 * 1024 * 1024:  # > 10MB
                        file_integrity_issues.append(f"Large file: {file_path}")
                    
                    # Check for recent modifications
                    mod_time = datetime.fromtimestamp(stat.st_mtime)
                    time_diff = datetime.now() - mod_time
                    
                    if time_diff.total_seconds() < 60:  # Modified in last minute
                        file_integrity_issues.append(f"Recently modified: {file_path}")
                else:
                    file_integrity_issues.append(f"Missing file: {file_path}")
            
            # Analysis 2: Check for suspicious files
            suspicious_files = []
            for file_path in os.listdir('.'):
                if file_path.endswith('.py') and file_path not in files_to_check:
                    if os.path.isfile(file_path):
                        suspicious_files.append(file_path)
            
            results = {
                'files_checked': len(files_to_check),
                'file_integrity_issues': file_integrity_issues,
                'suspicious_files': suspicious_files,
                'integrity_breached': len(file_integrity_issues) > 0,
                'integrity_level': 'GOOD' if len(file_integrity_issues) == 0 else 'COMPROMISED'
            }
            
            if results['integrity_breached']:
                print(f"  🚨 INTEGRITY BREACH DETECTED: {len(file_integrity_issues)} issues")
            else:
                print(f"  ✅ INTEGRITY GOOD: No issues detected")
            
            print(f"  📊 System Integrity Analysis:")
            print(f"    Files Checked: {results['files_checked']}")
            print(f"    Integrity Issues: {len(file_integrity_issues)}")
            print(f"    Suspicious Files: {len(suspicious_files)}")
            
            return results
            
        except Exception as e:
            print(f"  ❌ Error investigating system integrity: {e}")
            return {'error': str(e)}
    
    def investigate_timeline_consistency(self):
        """Investigate timeline consistency"""
        print("\n🔍 INVESTIGATING TIMELINE CONSISTENCY")
        print("-" * 50)
        
        try:
            # Check log files for timeline consistency
            logs_dir = 'logs'
            timeline_issues = []
            
            if os.path.exists(logs_dir):
                log_files = [f for f in os.listdir(logs_dir) if f.endswith('.log')]
                
                for log_file in log_files:
                    log_path = os.path.join(logs_dir, log_file)
                    stat = os.stat(log_path)
                    
                    # Check for future timestamps
                    mod_time = datetime.fromtimestamp(stat.st_mtime)
                    if mod_time > datetime.now():
                        timeline_issues.append(f"Future timestamp in {log_file}")
                    
                    # Check for empty logs
                    if stat.st_size == 0:
                        timeline_issues.append(f"Empty log file: {log_file}")
            
            # Check backtest report
            report_file = 'simple_backtest_report.json'
            if os.path.exists(report_file):
                stat = os.stat(report_file)
                mod_time = datetime.fromtimestamp(stat.st_mtime)
                
                # Check if report is too old or too new
                time_diff = datetime.now() - mod_time
                if time_diff.total_seconds() > 3600:  # > 1 hour old
                    timeline_issues.append("Old backtest report")
                elif time_diff.total_seconds() < 10:  # < 10 seconds old
                    timeline_issues.append("Very recent backtest report")
            
            results = {
                'log_files_checked': len(log_files) if os.path.exists(logs_dir) else 0,
                'timeline_issues': timeline_issues,
                'timeline_consistent': len(timeline_issues) == 0,
                'timeline_level': 'CONSISTENT' if len(timeline_issues) == 0 else 'INCONSISTENT'
            }
            
            if results['timeline_consistent']:
                print(f"  ✅ TIMELINE CONSISTENT: No issues detected")
            else:
                print(f"  🚨 TIMELINE INCONSISTENT: {len(timeline_issues)} issues")
            
            print(f"  📊 Timeline Consistency Analysis:")
            print(f"    Log Files Checked: {results['log_files_checked']}")
            print(f"    Timeline Issues: {len(timeline_issues)}")
            
            return results
            
        except Exception as e:
            print(f"  ❌ Error investigating timeline consistency: {e}")
            return {'error': str(e)}
    
    def detect_bias_patterns(self):
        """Detect bias patterns in the system"""
        print("\n🔍 DETECTING BIAS PATTERNS")
        print("-" * 50)
        
        try:
            bias_patterns = []
            
            # Pattern 1: Check for systematic favoritism
            try:
                from adaptive_module.llm_learning_engine import LLMLearningEngine
                engine = LLMLearningEngine()
                weights = engine.learning_weights
                
                # Check if certain features consistently get higher weights
                feature_weights = list(weights.items())
                feature_weights.sort(key=lambda x: x[1], reverse=True)
                
                if len(feature_weights) >= 2:
                    top_weight = feature_weights[0][1]
                    second_weight = feature_weights[1][1]
                    
                    if top_weight > second_weight * 3:
                        bias_patterns.append(f"Systematic favoritism: {feature_weights[0][0]}")
                        
            except:
                pass
            
            # Pattern 2: Check for learning anomalies
            try:
                # Check if learning is too fast or too slow
                if hasattr(engine, 'experiences'):
                    experience_count = len(engine.experiences)
                    
                    if experience_count > 10000:
                        bias_patterns.append("Excessive learning rate")
                    elif experience_count < 10:
                        bias_patterns.append("Insufficient learning data")
                        
            except:
                pass
            
            # Pattern 3: Check for decision bias
            try:
                # Load backtest results
                with open('simple_backtest_report.json', 'r') as f:
                    results = json.load(f)
                
                decisions = results.get('decisions', [])
                
                # Check for biased decision patterns
                if decisions:
                    decision_types = [d.get('decision_type', '') for d in decisions]
                    type_counts = {dt: decision_types.count(dt) for dt in set(decision_types)}
                    
                    # Check if one decision type dominates
                    if type_counts:
                        max_count = max(type_counts.values())
                        total_count = sum(type_counts.values())
                        
                        if max_count > total_count * 0.8:
                            dominant_type = max(type_counts, key=type_counts.get)
                            bias_patterns.append(f"Decision bias: {dominant_type}")
                            
            except:
                pass
            
            results = {
                'bias_patterns_detected': bias_patterns,
                'bias_count': len(bias_patterns),
                'bias_present': len(bias_patterns) > 0,
                'bias_severity': 'HIGH' if len(bias_patterns) > 3 else 'MEDIUM' if len(bias_patterns) > 0 else 'LOW'
            }
            
            if results['bias_present']:
                print(f"  🚨 BIAS PATTERNS DETECTED: {len(bias_patterns)} patterns")
                for pattern in bias_patterns:
                    print(f"    - {pattern}")
            else:
                print(f"  ✅ NO BIAS PATTERNS DETECTED")
            
            print(f"  📊 Bias Pattern Analysis:")
            print(f"    Bias Patterns: {len(bias_patterns)}")
            print(f"    Bias Severity: {results['bias_severity']}")
            
            return results
            
        except Exception as e:
            print(f"  ❌ Error detecting bias patterns: {e}")
            return {'error': str(e)}
    
    def compile_investigation_report(self, weight_analysis, parameter_analysis, 
                                 result_analysis, integrity_analysis, 
                                 timeline_analysis, bias_analysis):
        """Compile comprehensive investigation report"""
        print("\n🔍 COMPILING INVESTIGATION REPORT")
        print("=" * 80)
        
        # Calculate overall security score
        security_score = 100
        security_issues = []
        
        # Weight distribution impact
        if weight_analysis.get('bias_detected', False):
            security_score -= 25
            security_issues.append("Weight distribution bias detected")
        
        # Parameter tampering impact
        if parameter_analysis.get('tampering_detected', False):
            security_score -= 20
            security_issues.append("Learning parameter tampering detected")
        
        # Result fabrication impact
        if result_analysis.get('fabrication_detected', False):
            security_score -= 30
            security_issues.append("Result fabrication detected")
        
        # System integrity impact
        if integrity_analysis.get('integrity_breached', False):
            security_score -= 15
            security_issues.append("System integrity breach detected")
        
        # Timeline consistency impact
        if not timeline_analysis.get('timeline_consistent', True):
            security_score -= 10
            security_issues.append("Timeline inconsistency detected")
        
        # Bias patterns impact
        if bias_analysis.get('bias_present', False):
            security_score -= 20
            security_issues.append("Bias patterns detected")
        
        # Determine overall security level
        if security_score >= 90:
            security_level = "EXCELLENT"
        elif security_score >= 75:
            security_level = "GOOD"
        elif security_score >= 60:
            security_level = "FAIR"
        elif security_score >= 40:
            security_level = "POOR"
        else:
            security_level = "CRITICAL"
        
        # Compile results
        self.investigation_results = {
            'investigation_timestamp': datetime.now().isoformat(),
            'security_score': security_score,
            'security_level': security_level,
            'security_issues': security_issues,
            'weight_distribution_analysis': weight_analysis,
            'learning_parameter_analysis': parameter_analysis,
            'result_authenticity_analysis': result_analysis,
            'system_integrity_analysis': integrity_analysis,
            'timeline_consistency_analysis': timeline_analysis,
            'bias_pattern_analysis': bias_analysis,
            'overall_assessment': {
                'biasing_detected': len(security_issues) > 0,
                'biasing_severity': 'HIGH' if len(security_issues) > 3 else 'MEDIUM' if len(security_issues) > 0 else 'LOW',
                'system_secure': security_score >= 75,
                'recommendations': self._generate_recommendations(security_score, security_issues)
            }
        }
        
        # Save investigation report
        with open('security_investigation_report.json', 'w') as f:
            json.dump(self.investigation_results, f, indent=2, default=str)
        
        print(f"  📊 Overall Security Score: {security_score}/100")
        print(f"  📊 Security Level: {security_level}")
        print(f"  📊 Security Issues: {len(security_issues)}")
        
        if security_issues:
            print(f"  🚨 SECURITY ISSUES FOUND:")
            for issue in security_issues:
                print(f"    - {issue}")
        else:
            print(f"  ✅ NO SECURITY ISSUES DETECTED")
        
        print(f"  ✅ Investigation report saved to 'security_investigation_report.json'")
    
    def _generate_recommendations(self, security_score, security_issues):
        """Generate security recommendations"""
        recommendations = []
        
        if security_score < 75:
            recommendations.append("IMMEDIATE ACTION REQUIRED: Address security issues")
        
        if "Weight distribution bias detected" in security_issues:
            recommendations.append("Review and normalize weight distribution")
            recommendations.append("Implement weight constraints and monitoring")
        
        if "Learning parameter tampering detected" in security_issues:
            recommendations.append("Reset learning parameters to secure defaults")
            recommendations.append("Implement parameter validation")
        
        if "Result fabrication detected" in security_issues:
            recommendations.append("Investigate potential result manipulation")
            recommendations.append("Implement result validation checks")
        
        if "System integrity breach detected" in security_issues:
            recommendations.append("Scan for unauthorized file modifications")
            recommendations.append("Implement file integrity monitoring")
        
        if "Timeline inconsistency detected" in security_issues:
            recommendations.append("Investigate timeline anomalies")
            recommendations.append("Implement proper timestamp validation")
        
        if "Bias patterns detected" in security_issues:
            recommendations.append("Review learning algorithms for bias")
            recommendations.append("Implement bias detection and prevention")
        
        if not security_issues:
            recommendations.append("System appears secure - continue monitoring")
            recommendations.append("Implement regular security audits")
        
        return recommendations

def main():
    """Main investigation function"""
    print("🔍 SECURITY CHECK AND INVESTIGATION")
    print("=" * 80)
    print("🔍 Comprehensive security investigation starting...")
    print("=" * 80)
    
    # Create investigator
    investigator = SecurityInvestigator()
    
    # Run comprehensive investigation
    results = investigator.run_comprehensive_investigation()
    
    # Display final assessment
    print("\n" + "=" * 80)
    print("🔍 SECURITY INVESTIGATION COMPLETED")
    print("=" * 80)
    
    overall = results.get('overall_assessment', {})
    
    print(f"📊 FINAL SECURITY ASSESSMENT:")
    print(f"  Security Score: {results.get('security_score', 0)}/100")
    print(f"  Security Level: {results.get('security_level', 'UNKNOWN')}")
    print(f"  Biasing Detected: {overall.get('biasing_detected', 'UNKNOWN')}")
    print(f"  Biasing Severity: {overall.get('biasing_severity', 'UNKNOWN')}")
    print(f"  System Secure: {overall.get('system_secure', 'UNKNOWN')}")
    
    recommendations = overall.get('recommendations', [])
    if recommendations:
        print(f"\n📋 RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations, 1):
            print(f"  {i}. {rec}")
    
    if overall.get('biasing_detected', False):
        print(f"\n🚨 BIASING DETECTED!")
        print("⚠️ Security issues found - immediate action required")
    else:
        print(f"\n✅ NO BIASING DETECTED!")
        print("✅ System appears secure and bias-free")
    
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    main()
