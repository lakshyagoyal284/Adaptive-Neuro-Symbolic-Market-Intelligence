
import os
import re
from pathlib import Path

class InputValidator:
    """Comprehensive input validation"""
    
    @staticmethod
    def validate_file_path(file_path: str, allowed_dirs: List[str] = None) -> str:
        """Validate file path against directory traversal"""
        if allowed_dirs is None:
            allowed_dirs = ['data', 'models', 'logs']
        
        # Get absolute path
        abs_path = os.path.abspath(file_path)
        
        # Check for directory traversal
        for allowed_dir in allowed_dirs:
            allowed_path = os.path.abspath(allowed_dir)
            if abs_path.startswith(allowed_path):
                return abs_path
        
        raise SecurityError(f"Path traversal detected: {file_path}")
    
    @staticmethod
    def validate_numeric_input(value: Any, min_val: float = None, max_val: float = None) -> float:
        """Validate numeric input"""
        try:
            num_val = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"Invalid numeric input: {value}")
        
        if min_val is not None and num_val < min_val:
            raise ValueError(f"Value {num_val} below minimum {min_val}")
        
        if max_val is not None and num_val > max_val:
            raise ValueError(f"Value {num_val} above maximum {max_val}")
        
        return num_val
    
    @staticmethod
    def validate_string_input(value: Any, max_length: int = 1000, allowed_chars: str = None) -> str:
        """Validate string input"""
        if not isinstance(value, str):
            value = str(value)
        
        if len(value) > max_length:
            raise ValueError(f"String too long: {len(value)} > {max_length}")
        
        if allowed_chars and not re.match(f'^[{re.escape(allowed_chars)}]*$', value):
            raise ValueError(f"String contains invalid characters")
        
        return value
    
    @staticmethod
    def validate_dataframe(df: pd.DataFrame, required_columns: List[str] = None) -> pd.DataFrame:
        """Validate DataFrame structure"""
        if df is None or df.empty:
            raise ValueError("DataFrame is empty or None")
        
        if required_columns:
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check for NaN values in critical columns
        critical_cols = ['close', 'volume'] if required_columns is None else required_columns
        for col in critical_cols:
            if col in df.columns and df[col].isna().any():
                raise ValueError(f"NaN values found in column: {col}")
        
        return df

class SecurityError(Exception):
    """Security exception for validation failures"""
    pass
