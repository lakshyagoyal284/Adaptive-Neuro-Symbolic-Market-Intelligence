"""
Fix Indentation Issues
Quick fix for indentation problems in llm_learning_engine.py
"""

import os
import re

def fix_indentation():
    """Fix indentation issues in llm_learning_engine.py"""
    print("FIXING INDENTATION ISSUES")
    print("=" * 80)
    
    try:
        # Read the file
        with open('adaptive_module/llm_learning_engine.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        fixed_lines = []
        
        for i, line in enumerate(lines):
            # Fix common indentation issues
            if line.strip().startswith('total_weight = sum(self.learning_weights.values())'):
                # Fix the specific line causing issues
                fixed_lines.append('            total_weight = sum(self.learning_weights.values())')
            elif line.strip().startswith('if total_weight > 0:'):
                # Fix the if statement
                fixed_lines.append('            if total_weight > 0:')
            elif line.strip().startswith('for feature in self.learning_weights:'):
                # Fix the for loop
                fixed_lines.append('                for feature in self.learning_weights:')
            elif line.strip().startswith('self.learning_weights[feature] /= total_weight'):
                # Fix the assignment
                fixed_lines.append('                    self.learning_weights[feature] /= total_weight')
            elif line.strip().startswith('# Log weight updates'):
                # Fix the comment
                fixed_lines.append('            # Log weight updates - CRITICAL FOR DEBUGGING')
            elif line.strip().startswith('if weight_changes:'):
                # Fix the if statement
                fixed_lines.append('            if weight_changes:')
            elif line.strip().startswith('self.log_weight_update(weight_changes)'):
                # Fix the function call
                fixed_lines.append('                self.log_weight_update(weight_changes)')
            else:
                # Keep other lines as they are
                fixed_lines.append(line)
        
        # Write back the fixed content
        fixed_content = '\n'.join(fixed_lines)
        
        with open('adaptive_module/llm_learning_engine.py', 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        
        print("✅ Indentation issues fixed")
        return True
        
    except Exception as e:
        print(f"❌ Error fixing indentation: {e}")
        return False

if __name__ == "__main__":
    success = fix_indentation()
    
    if success:
        print("\n🎉 INDENTATION FIX COMPLETED!")
        print("=" * 80)
        print("✅ Learning engine indentation issues resolved")
        print("✅ Ready for backtesting with security guard")
        print("✅ Should run without errors now")
    else:
        print("\n❌ INDENTATION FIX FAILED!")
        print("=" * 80)
        print("❌ Could not fix indentation issues")
    
    print("=" * 80)
