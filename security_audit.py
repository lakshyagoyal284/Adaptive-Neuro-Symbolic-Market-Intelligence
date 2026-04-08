"""
Comprehensive Security Audit and Bug Detection System
Identifies bugs, vulnerabilities, and loopholes in the trading system
"""

import os
import sys
import re
import ast
import json
import pickle
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np

class SecurityAudit:
    """Comprehensive security and bug detection system"""
    
    def __init__(self):
        self.issues_found = []
        self.security_vulnerabilities = []
        self.bugs_detected = []
        self.performance_issues = []
        self.logic_flaws = []
        self.data_integrity_issues = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/security_audit.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def run_comprehensive_audit(self):
        """Run complete security and bug audit"""
        print("🔒 COMPREHENSIVE SECURITY AUDIT")
        print("=" * 80)
        print("🔍 Scanning for bugs, vulnerabilities, and loopholes...")
        print("=" * 80)
        
        # Security vulnerability checks
        self.check_code_injection_risks()
        self.check_file_system_vulnerabilities()
        self.check_data_validation_issues()
        self.check_authentication_gaps()
        self.check_privilege_escalation_risks()
        
        # Bug detection
        self.check_null_pointer_exceptions()
        self.check_resource_leaks()
        self.check_race_conditions()
        self.check_infinite_loops()
        self.check_memory_corruption()
        
        # Performance issues
        self.check_infinite_recursion()
        self.check_database_leaks()
        self.check_inefficient_algorithms()
        
        # Logic flaws
        self.check_business_logic_errors()
        self.check_trading_logic_flaws()
        self.check_learning_system_flaws()
        self.check_risk_management_gaps()
        
        # Data integrity
        self.check_data_corruption_risks()
        self.check_model_tampering_risks()
        self.check_data_consistency_issues()
        
        # Generate comprehensive report
        self.generate_security_report()
        
    def check_code_injection_risks(self):
        """Check for code injection vulnerabilities"""
        print("\n🔍 CHECKING CODE INJECTION RISKS...")
        
        # Check eval() usage
        files_to_check = [
            'symbolic_engine/rules.py',
            'adaptive_module/llm_learning_engine.py',
            'backtesting.py',
            'aggressive_profit_backtester.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for dangerous eval usage
                if 'eval(' in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if 'eval(' in line:
                            # Check if eval is used safely
                            if '__builtins__' not in line and 'safe' not in line.lower():
                                self.security_vulnerabilities.append({
                                    'type': 'CODE_INJECTION',
                                    'severity': 'HIGH',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': 'Unsafe eval() usage - potential code injection',
                                    'recommendation': 'Use safe evaluation with restricted globals'
                                })
                            else:
                                self.logger.info(f"Safe eval usage found in {file_path}:{i}")
                
                # Check for exec usage
                if 'exec(' in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if 'exec(' in line:
                            self.security_vulnerabilities.append({
                                'type': 'CODE_INJECTION',
                                'severity': 'CRITICAL',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': 'exec() usage - extremely dangerous code injection risk',
                                'recommendation': 'Replace exec() with safer alternatives'
                            })
                
                # Check for pickle usage
                if 'pickle' in content or 'pickle.' in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        if 'pickle.load(' in line or 'pickle.loads(' in line:
                            self.security_vulnerabilities.append({
                                'type': 'DESERIALIZATION',
                                'severity': 'HIGH',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': 'Unsafe pickle deserialization - arbitrary code execution risk',
                                'recommendation': 'Use safe serialization formats like JSON'
                            })
    
    def check_file_system_vulnerabilities(self):
        """Check for file system vulnerabilities"""
        print("\n🔍 CHECKING FILE SYSTEM VULNERABILITIES...")
        
        # Check for path traversal
        files_to_check = [
            'market_data_processor.py',
            'backtesting.py',
            'adaptive_module/llm_learning_engine.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for unsafe file operations
                dangerous_patterns = [
                    (r'open\(.*\.\.', 'Path traversal vulnerability'),
                    (r'open\(.*\/.*\/', 'Path traversal vulnerability'),
                    (r'os\.system\(', 'Command injection vulnerability'),
                    (r'subprocess\.call\(', 'Command injection vulnerability'),
                    (r'shutil\.rmtree\(', 'File deletion vulnerability'),
                    (r'os\.remove\(', 'File deletion vulnerability')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in dangerous_patterns:
                        if re.search(pattern, line):
                            self.security_vulnerabilities.append({
                                'type': 'FILE_SYSTEM',
                                'severity': 'MEDIUM',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': description,
                                'recommendation': 'Validate and sanitize file paths'
                            })
    
    def check_data_validation_issues(self):
        """Check for data validation issues"""
        print("\n🔍 CHECKING DATA VALIDATION ISSUES...")
        
        # Check trading system for validation
        trading_files = [
            'aggressive_profit_backtester.py',
            'backtesting.py'
        ]
        
        for file_path in trading_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for missing validation
                validation_patterns = [
                    (r'pd\.read_csv\(', 'CSV file validation'),
                    (r'float\(', 'Numeric conversion validation'),
                    (r'int\(', 'Integer conversion validation'),
                    (r'df\[.*\]', 'DataFrame access validation')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, validation_type in validation_patterns:
                        if re.search(pattern, line) and 'try:' not in line:
                            self.data_integrity_issues.append({
                                'type': 'DATA_VALIDATION',
                                'severity': 'MEDIUM',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': f'Missing {validation_type}',
                                'recommendation': 'Add proper data validation and error handling'
                            })
    
    def check_authentication_gaps(self):
        """Check for authentication and authorization gaps"""
        print("\n🔍 CHECKING AUTHENTICATION GAPS...")
        
        # Check if any authentication mechanisms exist
        auth_files = [
            'auth.py',
            'security.py',
            'login.py',
            'user_management.py'
        ]
        
        auth_found = False
        for file_path in auth_files:
            if os.path.exists(file_path):
                auth_found = True
                break
        
        if not auth_found:
            self.security_vulnerabilities.append({
                'type': 'AUTHENTICATION',
                'severity': 'HIGH',
                'file': 'SYSTEM',
                'line': 0,
                'code': 'No authentication system found',
                'description': 'No authentication or authorization mechanisms implemented',
                'recommendation': 'Implement proper authentication and authorization'
            })
    
    def check_privilege_escalation_risks(self):
        """Check for privilege escalation risks"""
        print("\n🔍 CHECKING PRIVILEGE ESCALATION RISKS...")
        
        # Check for admin/superuser functionality
        files_to_check = [
            'backtesting.py',
            'aggressive_profit_backtester.py',
            'adaptive_module/llm_learning_engine.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for dangerous operations
                dangerous_ops = [
                    (r'os\.chmod', 'File permission modification'),
                    (r'os\.chown', 'File ownership modification'),
                    (r'sudo', 'Privilege escalation'),
                    (r'admin', 'Admin functionality'),
                    (r'superuser', 'Superuser functionality')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in dangerous_ops:
                        if re.search(pattern, line, re.IGNORECASE):
                            self.security_vulnerabilities.append({
                                'type': 'PRIVILEGE_ESCALATION',
                                'severity': 'HIGH',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': description,
                                'recommendation': 'Implement proper access controls'
                            })
    
    def check_null_pointer_exceptions(self):
        """Check for potential null pointer exceptions"""
        print("\n🔍 CHECKING NULL POINTER EXCEPTIONS...")
        
        files_to_check = [
            'adaptive_module/llm_learning_engine.py',
            'symbolic_engine/rules.py',
            'backtesting.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for potential null references
                null_patterns = [
                    (r'\.get\([^,)]+\)', 'Dictionary access without default'),
                    (r'\[.*\]', 'List/dict access without bounds check'),
                    (r'if.*:', 'Conditional without null check')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in null_patterns:
                        if re.search(pattern, line):
                            # Check if there's proper null checking
                            if 'if' not in line and 'try:' not in line:
                                self.bugs_detected.append({
                                    'type': 'NULL_POINTER',
                                    'severity': 'MEDIUM',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': description,
                                    'recommendation': 'Add null checks before accessing data'
                                })
    
    def check_resource_leaks(self):
        """Check for resource leaks"""
        print("\n🔍 CHECKING RESOURCE LEAKS...")
        
        files_to_check = [
            'market_data_processor.py',
            'backtesting.py',
            'aggressive_profit_backtester.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for resource leaks
                leak_patterns = [
                    (r'open\(', 'File handle leak'),
                    (r'pd\.read_csv\(', 'Memory leak'),
                    (r'while True:', 'Infinite loop risk'),
                    (r'for.*in.*range\(.*\):', 'Large loop risk')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in leak_patterns:
                        if re.search(pattern, line):
                            # Check if resources are properly managed
                            if 'with' not in line and 'close()' not in line:
                                self.bugs_detected.append({
                                    'type': 'RESOURCE_LEAK',
                                    'severity': 'MEDIUM',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': description,
                                    'recommendation': 'Use context managers or explicit resource cleanup'
                                })
    
    def check_race_conditions(self):
        """Check for race conditions"""
        print("\n🔍 CHECKING RACE CONDITIONS...")
        
        files_to_check = [
            'adaptive_module/llm_learning_engine.py',
            'backtesting.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for race condition patterns
                race_patterns = [
                    (r'self\.', 'Shared state access'),
                    (r'global ', 'Global variable access'),
                    (r'threading\.', 'Threading without locks'),
                    (r'multiprocessing\.', 'Multiprocessing without locks')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in race_patterns:
                        if re.search(pattern, line):
                            # Check if there's proper synchronization
                            if 'lock' not in line.lower() and 'threading' not in line.lower():
                                self.bugs_detected.append({
                                    'type': 'RACE_CONDITION',
                                    'severity': 'HIGH',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': description,
                                    'recommendation': 'Implement proper synchronization mechanisms'
                                })
    
    def check_infinite_loops(self):
        """Check for infinite loops"""
        print("\n🔍 CHECKING INFINITE LOOPS...")
        
        files_to_check = [
            'backtesting.py',
            'aggressive_profit_backtester.py',
            'adaptive_module/llm_learning_engine.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for infinite loop patterns
                loop_patterns = [
                    (r'while True:', 'Infinite while loop'),
                    (r'for.*in.*range\(.*\):', 'Potentially large for loop'),
                    (r'while.*:', 'Conditional while loop')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in loop_patterns:
                        if re.search(pattern, line):
                            # Check if there's a break condition
                            if 'break' not in line and 'return' not in line:
                                # Look ahead for break in next few lines
                                next_lines = lines[i:i+10]
                                has_break = any('break' in next_line or 'return' in next_line for next_line in next_lines)
                                if not has_break:
                                    self.bugs_detected.append({
                                        'type': 'INFINITE_LOOP',
                                        'severity': 'HIGH',
                                        'file': file_path,
                                        'line': i,
                                        'code': line.strip(),
                                        'description': description,
                                        'recommendation': 'Add proper break conditions'
                                    })
    
    def check_memory_corruption(self):
        """Check for memory corruption risks"""
        print("\n🔍 CHECKING MEMORY CORRUPTION...")
        
        files_to_check = [
            'adaptive_module/llm_learning_engine.py',
            'market_data_processor.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for memory corruption patterns
                corruption_patterns = [
                    (r'ctypes', 'Direct memory access'),
                    (r'buffer', 'Buffer operations'),
                    (r'array\(', 'Array operations'),
                    (r'memoryview', 'Memory view operations')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in corruption_patterns:
                        if re.search(pattern, line):
                            self.bugs_detected.append({
                                'type': 'MEMORY_CORRUPTION',
                                'severity': 'HIGH',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': description,
                                'recommendation': 'Use safe memory management'
                            })
    
    def check_infinite_recursion(self):
        """Check for infinite recursion"""
        print("\n🔍 CHECKING INFINITE RECURSION...")
        
        files_to_check = [
            'adaptive_module/llm_learning_engine.py',
            'symbolic_engine/rules.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for recursion patterns
                recursion_patterns = [
                    (r'def.*\(.*\):', 'Function definition'),
                    (r'return.*\(', 'Return statement')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    if re.search(recursion_patterns[0][0], line):
                        # Look for recursive calls
                        func_name = re.search(r'def\s+(\w+)', line)
                        if func_name:
                            func_name = func_name.group(1)
                            # Check if function calls itself
                            for j in range(i, min(i+50, len(lines))):
                                if f'{func_name}(' in lines[j]:
                                    # Check if there's a base case
                                    if 'if' not in lines[j:j+5]:
                                        self.performance_issues.append({
                                            'type': 'INFINITE_RECURSION',
                                            'severity': 'HIGH',
                                            'file': file_path,
                                            'line': i,
                                            'code': line.strip(),
                                            'description': f'Recursive function {func_name} without base case',
                                            'recommendation': 'Add proper base case for recursion'
                                        })
    
    def check_database_leaks(self):
        """Check for database connection leaks"""
        print("\n🔍 CHECKING DATABASE LEAKS...")
        
        files_to_check = [
            'market_data_processor.py',
            'backtesting.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for database operations
                db_patterns = [
                    (r'sqlite3', 'SQLite database'),
                    (r'pymongo', 'MongoDB database'),
                    (r'psycopg2', 'PostgreSQL database'),
                    (r'mysql', 'MySQL database')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in db_patterns:
                        if re.search(pattern, line):
                            # Check if connections are properly managed
                            if 'with' not in line and 'close()' not in line:
                                self.performance_issues.append({
                                    'type': 'DATABASE_LEAK',
                                    'severity': 'MEDIUM',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': description,
                                    'recommendation': 'Use connection pooling or proper cleanup'
                                })
    
    def check_inefficient_algorithms(self):
        """Check for inefficient algorithms"""
        print("\n🔍 CHECKING INEFFICIENT ALGORITHMS...")
        
        files_to_check = [
            'adaptive_module/llm_learning_engine.py',
            'backtesting.py',
            'aggressive_profit_backtester.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for inefficient patterns
                inefficient_patterns = [
                    (r'for.*in.*range\(.*\):.*for.*in.*range\(', 'Nested loops'),
                    (r'list\(.*\.keys\(\)', 'Inefficient key access'),
                    (r'while.*in.*:', 'Inefficient membership test'),
                    (r'sorted\(.*\)', 'Inefficient sorting')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in inefficient_patterns:
                        if re.search(pattern, line):
                            self.performance_issues.append({
                                'type': 'INEFFICIENT_ALGORITHM',
                                'severity': 'MEDIUM',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': description,
                                'recommendation': 'Optimize algorithm complexity'
                            })
    
    def check_business_logic_errors(self):
        """Check for business logic errors"""
        print("\n🔍 CHECKING BUSINESS LOGIC ERRORS...")
        
        # Check trading logic
        trading_files = [
            'aggressive_profit_backtester.py',
            'backtesting.py'
        ]
        
        for file_path in trading_files:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for logic errors
                logic_patterns = [
                    (r'if.*>.*:', 'Potential logic error'),
                    (r'if.*<.*:', 'Potential logic error'),
                    (r'if.*==.*:', 'Potential logic error'),
                    (r'if.*!=.*:', 'Potential logic error')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in logic_patterns:
                        if re.search(pattern, line):
                            # Check for common logic mistakes
                            if '=' in line and '==' not in line:
                                self.logic_flaws.append({
                                    'type': 'BUSINESS_LOGIC',
                                    'severity': 'MEDIUM',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': 'Assignment in conditional',
                                    'recommendation': 'Use == for comparison'
                                })
    
    def check_trading_logic_flaws(self):
        """Check for trading logic flaws"""
        print("\n🔍 CHECKING TRADING LOGIC FLAWS...")
        
        files_to_check = [
            'aggressive_profit_backtester.py',
            'backtesting.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for trading-specific flaws
                trading_flaws = [
                    (r'buy.*sell', 'Simultaneous buy/sell'),
                    (r'position.*position', 'Double position'),
                    (r'balance.*balance', 'Double balance update'),
                    (r'trade.*trade', 'Double trade execution')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in trading_flaws:
                        if re.search(pattern, line, re.IGNORECASE):
                            self.logic_flaws.append({
                                'type': 'TRADING_LOGIC',
                                'severity': 'HIGH',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': description,
                                'recommendation': 'Review trading logic for double execution'
                            })
    
    def check_learning_system_flaws(self):
        """Check for learning system flaws"""
        print("\n🔍 CHECKING LEARNING SYSTEM FLAWS...")
        
        files_to_check = [
            'adaptive_module/llm_learning_engine.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for learning-specific flaws
                learning_flaws = [
                    (r'learning_rate.*>', 'Learning rate too high'),
                    (r'learning_rate.*<', 'Learning rate too low'),
                    (r'weight.*weight', 'Weight update conflict'),
                    (r'model.*model', 'Model version conflict')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in learning_flaws:
                        if re.search(pattern, line):
                            self.logic_flaws.append({
                                'type': 'LEARNING_SYSTEM',
                                'severity': 'MEDIUM',
                                'file': file_path,
                                'line': i,
                                'code': line.strip(),
                                'description': description,
                                'recommendation': 'Review learning parameters'
                            })
    
    def check_risk_management_gaps(self):
        """Check for risk management gaps"""
        print("\n🔍 CHECKING RISK MANAGEMENT GAPS...")
        
        files_to_check = [
            'aggressive_profit_backtester.py',
            'backtesting.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for risk management gaps
                risk_patterns = [
                    (r'position.*size', 'Position sizing'),
                    (r'stop.*loss', 'Stop loss'),
                    (r'take.*profit', 'Take profit'),
                    (r'max.*drawdown', 'Maximum drawdown')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in risk_patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            # Check if risk limits are enforced
                            if 'max' not in line.lower() and 'limit' not in line.lower():
                                self.logic_flaws.append({
                                    'type': 'RISK_MANAGEMENT',
                                    'severity': 'HIGH',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': f'{description} without limits',
                                    'recommendation': 'Implement proper risk limits'
                                })
    
    def check_data_corruption_risks(self):
        """Check for data corruption risks"""
        print("\n🔍 CHECKING DATA CORRUPTION RISKS...")
        
        files_to_check = [
            'market_data_processor.py',
            'adaptive_module/llm_learning_engine.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for data corruption risks
                corruption_patterns = [
                    (r'pd\.read_csv\(', 'CSV file corruption'),
                    (r'pickle\.load\(', 'Pickle corruption'),
                    (r'json\.load\(', 'JSON corruption'),
                    (r'df\.loc\(', 'DataFrame corruption')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in corruption_patterns:
                        if re.search(pattern, line):
                            # Check if there's error handling
                            if 'try:' not in line and 'except' not in line:
                                self.data_integrity_issues.append({
                                    'type': 'DATA_CORRUPTION',
                                    'severity': 'HIGH',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': description,
                                    'recommendation': 'Add proper error handling for data operations'
                                })
    
    def check_model_tampering_risks(self):
        """Check for model tampering risks"""
        print("\n🔍 CHECKING MODEL TAMPERING RISKS...")
        
        files_to_check = [
            'adaptive_module/llm_learning_engine.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for model tampering risks
                tampering_patterns = [
                    (r'save.*model', 'Model saving'),
                    (r'load.*model', 'Model loading'),
                    (r'pickle\.dump\(', 'Model serialization'),
                    (r'pickle\.load\(', 'Model deserialization')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in tampering_patterns:
                        if re.search(pattern, line):
                            # Check if there's integrity checking
                            if 'hash' not in line.lower() and 'checksum' not in line.lower():
                                self.data_integrity_issues.append({
                                    'type': 'MODEL_TAMPERING',
                                    'severity': 'HIGH',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': description,
                                    'recommendation': 'Add model integrity verification'
                                })
    
    def check_data_consistency_issues(self):
        """Check for data consistency issues"""
        print("\n🔍 CHECKING DATA CONSISTENCY ISSUES...")
        
        files_to_check = [
            'market_data_processor.py',
            'backtesting.py'
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for consistency issues
                consistency_patterns = [
                    (r'df\.', 'DataFrame operations'),
                    (r'pd\.DataFrame', 'DataFrame creation'),
                    (r'dropna\(', 'Data cleaning'),
                    (r'fillna\(', 'Data filling')
                ]
                
                lines = content.split('\n')
                for i, line in enumerate(lines, 1):
                    for pattern, description in consistency_patterns:
                        if re.search(pattern, line):
                            # Check if data is validated
                            if 'validate' not in line.lower() and 'check' not in line.lower():
                                self.data_integrity_issues.append({
                                    'type': 'DATA_CONSISTENCY',
                                    'severity': 'MEDIUM',
                                    'file': file_path,
                                    'line': i,
                                    'code': line.strip(),
                                    'description': description,
                                    'recommendation': 'Add data consistency checks'
                                })
    
    def generate_security_report(self):
        """Generate comprehensive security report"""
        print("\n" + "=" * 80)
        print("🔒 COMPREHENSIVE SECURITY AUDIT REPORT")
        print("=" * 80)
        
        # Count issues by severity
        critical_issues = len([i for i in self.security_vulnerabilities if i['severity'] == 'CRITICAL'])
        high_issues = len([i for i in self.security_vulnerabilities if i['severity'] == 'HIGH'])
        medium_issues = len([i for i in self.security_vulnerabilities if i['severity'] == 'MEDIUM'])
        
        print(f"\n📊 SECURITY VULNERABILITIES SUMMARY:")
        print(f"  Critical: {critical_issues}")
        print(f"  High: {high_issues}")
        print(f"  Medium: {medium_issues}")
        print(f"  Total: {len(self.security_vulnerabilities)}")
        
        # Count bugs by type
        bug_types = {}
        for bug in self.bugs_detected:
            bug_type = bug['type']
            bug_types[bug_type] = bug_types.get(bug_type, 0) + 1
        
        print(f"\n🐛 BUGS DETECTED SUMMARY:")
        for bug_type, count in bug_types.items():
            print(f"  {bug_type}: {count}")
        print(f"  Total: {len(self.bugs_detected)}")
        
        # Count performance issues
        perf_types = {}
        for issue in self.performance_issues:
            issue_type = issue['type']
            perf_types[issue_type] = perf_types.get(issue_type, 0) + 1
        
        print(f"\n⚡ PERFORMANCE ISSUES SUMMARY:")
        for issue_type, count in perf_types.items():
            print(f"  {issue_type}: {count}")
        print(f"  Total: {len(self.performance_issues)}")
        
        # Count logic flaws
        logic_types = {}
        for flaw in self.logic_flaws:
            flaw_type = flaw['type']
            logic_types[flaw_type] = logic_types.get(flaw_type, 0) + 1
        
        print(f"\n🧠 LOGIC FLAWS SUMMARY:")
        for flaw_type, count in logic_types.items():
            print(f"  {flaw_type}: {count}")
        print(f"  Total: {len(self.logic_flaws)}")
        
        # Count data integrity issues
        data_types = {}
        for issue in self.data_integrity_issues:
            issue_type = issue['type']
            data_types[issue_type] = data_types.get(issue_type, 0) + 1
        
        print(f"\n📊 DATA INTEGRITY ISSUES SUMMARY:")
        for issue_type, count in data_types.items():
            print(f"  {issue_type}: {count}")
        print(f"  Total: {len(self.data_integrity_issues)}")
        
        # Show critical issues first
        all_issues = (
            self.security_vulnerabilities + 
            self.bugs_detected + 
            self.performance_issues + 
            self.logic_flaws + 
            self.data_integrity_issues
        )
        
        # Sort by severity
        severity_order = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}
        all_issues.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        print(f"\n🚨 CRITICAL ISSUES (Top 10):")
        for i, issue in enumerate(all_issues[:10]):
            print(f"  {i+1}. {issue['type']} - {issue['severity']}")
            print(f"     File: {issue['file']}:{issue['line']}")
            print(f"     Code: {issue['code']}")
            print(f"     Description: {issue['description']}")
            print(f"     Recommendation: {issue['recommendation']}")
            print()
        
        # Save detailed report
        report = {
            'security_vulnerabilities': self.security_vulnerabilities,
            'bugs_detected': self.bugs_detected,
            'performance_issues': self.performance_issues,
            'logic_flaws': self.logic_flaws,
            'data_integrity_issues': self.data_integrity_issues,
            'summary': {
                'total_issues': len(all_issues),
                'critical_issues': critical_issues,
                'high_issues': high_issues,
                'medium_issues': medium_issues,
                'security_score': max(0, 100 - (critical_issues * 20) - (high_issues * 10) - (medium_issues * 5))
            },
            'audit_timestamp': pd.Timestamp.now().isoformat()
        }
        
        with open('logs/security_audit_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"📄 Detailed report saved to: logs/security_audit_report.json")
        
        # Overall assessment
        total_issues = len(all_issues)
        if total_issues == 0:
            print(f"\n🎉 EXCELLENT: No security issues or bugs found!")
        elif total_issues <= 5:
            print(f"\n✅ GOOD: Only {total_issues} minor issues found")
        elif total_issues <= 15:
            print(f"\n⚠️ FAIR: {total_issues} issues found - some attention needed")
        elif total_issues <= 30:
            print(f"\n🔶 POOR: {total_issues} issues found - significant attention needed")
        else:
            print(f"\n❌ CRITICAL: {total_issues} issues found - immediate attention required")
        
        print("=" * 80)

if __name__ == "__main__":
    # Create logs directory
    os.makedirs("logs", exist_ok=True)
    
    # Run security audit
    auditor = SecurityAudit()
    auditor.run_comprehensive_audit()
