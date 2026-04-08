
import threading
import time
from typing import Dict, Any, Optional
from contextlib import contextmanager

class ThreadSafeManager:
    """Thread-safe operations manager"""
    
    def __init__(self):
        self._locks: Dict[str, threading.Lock] = {}
        self._global_lock = threading.Lock()
    
    def get_lock(self, lock_name: str) -> threading.Lock:
        """Get or create lock for given name"""
        with self._global_lock:
            if lock_name not in self._locks:
                self._locks[lock_name] = threading.Lock()
            return self._locks[lock_name]
    
    @contextmanager
    def atomic_operation(self, lock_name: str):
        """Context manager for atomic operations"""
        lock = self.get_lock(lock_name)
        lock.acquire()
        try:
            yield
        finally:
            lock.release()
    
    def safe_dict_update(self, dict_name: str, key: str, value: Any) -> None:
        """Thread-safe dictionary update"""
        with self.atomic_operation(dict_name):
            # This would need to be implemented with actual dict reference
            pass
    
    def safe_list_append(self, list_name: str, item: Any) -> None:
        """Thread-safe list append"""
        with self.atomic_operation(list_name):
            # This would need to be implemented with actual list reference
            pass

# Global thread-safe manager
thread_safe = ThreadSafeManager()

# Example usage in learning engine
class SafeLLMLearningEngine:
    """Thread-safe learning engine"""
    
    def __init__(self):
        self.learning_weights = {}
        self.experiences = []
        self.model_version = 1
        self._weights_lock = threading.Lock()
        self._experiences_lock = threading.Lock()
        self._version_lock = threading.Lock()
    
    def update_weights(self, updates: Dict[str, float]) -> None:
        """Thread-safe weight updates"""
        with self._weights_lock:
            for key, value in updates.items():
                if key in self.learning_weights:
                    self.learning_weights[key] += value
                else:
                    self.learning_weights[key] = value
    
    def add_experience(self, experience: Any) -> None:
        """Thread-safe experience addition"""
        with self._experiences_lock:
            self.experiences.append(experience)
    
    def increment_version(self) -> None:
        """Thread-safe version increment"""
        with self._version_lock:
            self.model_version += 1
    
    def get_weights(self) -> Dict[str, float]:
        """Thread-safe weight access"""
        with self._weights_lock:
            return self.learning_weights.copy()
    
    def get_version(self) -> int:
        """Thread-safe version access"""
        with self._version_lock:
            return self.model_version
