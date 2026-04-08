
import hashlib
import secrets
import json
import time
from typing import Dict, Optional, List
from dataclasses import dataclass
from enum import Enum

class UserRole(Enum):
    """User roles for authorization"""
    ADMIN = "admin"
    TRADER = "trader"
    VIEWER = "viewer"

@dataclass
class User:
    """User account"""
    username: str
    password_hash: str
    role: UserRole
    created_at: float
    last_login: Optional[float] = None
    is_active: bool = True
    api_key: Optional[str] = None

class AuthenticationSystem:
    """Simple authentication and authorization system"""
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.sessions: Dict[str, Dict] = {}
        self.session_timeout = 3600  # 1 hour
        self._load_users()
    
    def _load_users(self):
        """Load users from storage"""
        try:
            if os.path.exists('users.json'):
                with open('users.json', 'r') as f:
                    users_data = json.load(f)
                    for username, user_data in users_data.items():
                        self.users[username] = User(
                            username=username,
                            password_hash=user_data['password_hash'],
                            role=UserRole(user_data['role']),
                            created_at=user_data['created_at'],
                            last_login=user_data.get('last_login'),
                            is_active=user_data.get('is_active', True),
                            api_key=user_data.get('api_key')
                        )
        except Exception as e:
            self.logger.error(f"Failed to load users: {e}")
            # Create default admin user
            self._create_default_admin()
    
    def _create_default_admin(self):
        """Create default admin user"""
        default_password = "admin123"  # Change this in production
        password_hash = self._hash_password(default_password)
        
        admin_user = User(
            username="admin",
            password_hash=password_hash,
            role=UserRole.ADMIN,
            created_at=time.time(),
            api_key=self._generate_api_key()
        )
        
        self.users["admin"] = admin_user
        self._save_users()
        self.logger.warning("Default admin user created - please change password!")
    
    def _hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}${password_hash.hex()}"
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            salt, hash_value = password_hash.split('$')
            computed_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return computed_hash.hex() == hash_value
        except:
            return False
    
    def _generate_api_key(self) -> str:
        """Generate secure API key"""
        return secrets.token_urlsafe(32)
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return session token"""
        user = self.users.get(username)
        if not user or not user.is_active:
            return None
        
        if not self._verify_password(password, user.password_hash):
            return None
        
        # Create session
        session_token = secrets.token_urlsafe(32)
        self.sessions[session_token] = {
            'username': username,
            'role': user.role.value,
            'created_at': time.time(),
            'last_activity': time.time()
        }
        
        # Update last login
        user.last_login = time.time()
        self._save_users()
        
        return session_token
    
    def authorize(self, session_token: str, required_role: UserRole) -> bool:
        """Authorize user based on role"""
        session = self.sessions.get(session_token)
        if not session:
            return False
        
        # Check session timeout
        if time.time() - session['last_activity'] > self.session_timeout:
            del self.sessions[session_token]
            return False
        
        # Update last activity
        session['last_activity'] = time.time()
        
        # Check role authorization
        user_role = UserRole(session['role'])
        return self._check_role_permission(user_role, required_role)
    
    def _check_role_permission(self, user_role: UserRole, required_role: UserRole) -> bool:
        """Check if user role has required permissions"""
        role_hierarchy = {
            UserRole.VIEWER: 1,
            UserRole.TRADER: 2,
            UserRole.ADMIN: 3
        }
        
        return role_hierarchy.get(user_role, 0) >= role_hierarchy.get(required_role, 0)
    
    def _save_users(self):
        """Save users to storage"""
        try:
            users_data = {}
            for username, user in self.users.items():
                users_data[username] = {
                    'password_hash': user.password_hash,
                    'role': user.role.value,
                    'created_at': user.created_at,
                    'last_login': user.last_login,
                    'is_active': user.is_active,
                    'api_key': user.api_key
                }
            
            with open('users.json', 'w') as f:
                json.dump(users_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save users: {e}")

# Global authentication instance
auth_system = AuthenticationSystem()
