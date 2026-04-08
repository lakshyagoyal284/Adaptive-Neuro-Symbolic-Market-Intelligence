
import logging
import traceback
from typing import Optional, Any, Callable
from functools import wraps

class ErrorHandler:
    """Comprehensive error handling"""
    
    @staticmethod
    def safe_execute(func: Callable, default_return: Any = None, log_errors: bool = True):
        """Decorator for safe function execution"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_errors:
                    logging.error(f"Error in {func.__name__}: {str(e)}")
                    logging.error(f"Traceback: {traceback.format_exc()}")
                return default_return
        return wrapper
    
    @staticmethod
    def validate_and_execute(validation_func: Callable, execution_func: Callable, error_msg: str = None):
        """Validate input then execute function"""
        try:
            # Validate input
            if validation_func():
                # Execute function
                return execution_func()
            else:
                if error_msg:
                    logging.error(f"Validation failed: {error_msg}")
                return None
        except Exception as e:
            logging.error(f"Error in validation/execution: {str(e)}")
            return None
    
    @staticmethod
    def handle_file_operation(file_path: str, operation: str, default_return: Any = None):
        """Safe file operation with error handling"""
        try:
            if operation == 'read':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif operation == 'write':
                def writer(content):
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    return True
                return writer
            elif operation == 'exists':
                return os.path.exists(file_path)
            else:
                logging.error(f"Unknown file operation: {operation}")
                return default_return
        except Exception as e:
            logging.error(f"File operation {operation} failed: {str(e)}")
            return default_return

# Usage examples
@ErrorHandler.safe_execute(default_return={}, log_errors=True)
def load_config_file():
    """Safe config loading"""
    with open('config.json', 'r') as f:
        return json.load(f)

@ErrorHandler.safe_execute(default_return=0.0, log_errors=True)
def calculate_rsi(prices: list, period: int = 14):
    """Safe RSI calculation"""
    if len(prices) < period:
        return 0.0
    
    # RSI calculation logic here
    return 50.0  # Placeholder
