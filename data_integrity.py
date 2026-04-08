
import hashlib
import json
from typing import Dict, Any, Optional

class DataIntegrityManager:
    """Data integrity verification and management"""
    
    @staticmethod
    def calculate_checksum(data: Any) -> str:
        """Calculate SHA-256 checksum of data"""
        if isinstance(data, str):
            data_bytes = data.encode('utf-8')
        elif isinstance(data, dict):
            data_bytes = json.dumps(data, sort_keys=True).encode('utf-8')
        else:
            data_bytes = str(data).encode('utf-8')
        
        return hashlib.sha256(data_bytes).hexdigest()
    
    @staticmethod
    def verify_data_integrity(data: Any, expected_checksum: str) -> bool:
        """Verify data integrity against checksum"""
        actual_checksum = DataIntegrityManager.calculate_checksum(data)
        return actual_checksum == expected_checksum
    
    @staticmethod
    def validate_trading_data(df: pd.DataFrame) -> pd.DataFrame:
        """Validate trading data integrity"""
        # Check for required columns
        required_columns = ['date', 'open', 'high', 'low', 'close', 'volume']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        
        # Check data consistency
        for idx, row in df.iterrows():
            # High should be >= open, close
            if row['high'] < row['open'] or row['high'] < row['close']:
                raise ValueError(f"Invalid high price at row {idx}")
            
            # Low should be <= open, close
            if row['low'] > row['open'] or row['low'] > row['close']:
                raise ValueError(f"Invalid low price at row {idx}")
            
            # Volume should be non-negative
            if row['volume'] < 0:
                raise ValueError(f"Negative volume at row {idx}")
        
        return df
    
    @staticmethod
    def sanitize_user_input(input_data: Any) -> Any:
        """Sanitize user input to prevent injection"""
        if isinstance(input_data, str):
            # Remove dangerous characters
            dangerous_chars = ['<', '>', '"', "'", '&', 'script', 'javascript', 'eval']
            sanitized = input_data
            for char in dangerous_chars:
                sanitized = sanitized.replace(char, '')
            return sanitized
        elif isinstance(input_data, dict):
            return {k: DataIntegrityManager.sanitize_user_input(v) for k, v in input_data.items()}
        elif isinstance(input_data, list):
            return [DataIntegrityManager.sanitize_user_input(item) for item in input_data]
        else:
            return input_data
