import hashlib
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

class SessionManager:
    def __init__(self):
        self.active_sessions: Dict[str, Dict[str, Any]] = {}
        self.session_timeout = 3600  # 1 hour in seconds
    
    def create_session(self, user_id: int, user_data: Dict[str, Any]) -> str:
        """Create a new session for a user"""
        # Generate session token
        session_data = f"{user_id}_{time.time()}_{user_data.get('phone', '')}"
        session_token = hashlib.sha256(session_data.encode()).hexdigest()
        
        # Store session data
        self.active_sessions[session_token] = {
            'user_id': user_id,
            'user_data': user_data,
            'created_at': datetime.now(),
            'last_activity': datetime.now()
        }
        
        return session_token
    
    def validate_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """Validate session token and return user data if valid"""
        if session_token not in self.active_sessions:
            return None
        
        session = self.active_sessions[session_token]
        
        # Check if session has expired
        if datetime.now() - session['last_activity'] > timedelta(seconds=self.session_timeout):
            self.remove_session(session_token)
            return None
        
        # Update last activity
        session['last_activity'] = datetime.now()
        return session['user_data']
    
    def remove_session(self, session_token: str) -> bool:
        """Remove a session"""
        if session_token in self.active_sessions:
            del self.active_sessions[session_token]
            return True
        return False
    
    def get_user_id(self, session_token: str) -> Optional[int]:
        """Get user ID from session token"""
        if session_token in self.active_sessions:
            return self.active_sessions[session_token]['user_id']
        return None
    
    def cleanup_expired_sessions(self):
        """Remove all expired sessions"""
        current_time = datetime.now()
        expired_tokens = []
        
        for token, session in self.active_sessions.items():
            if current_time - session['last_activity'] > timedelta(seconds=self.session_timeout):
                expired_tokens.append(token)
        
        for token in expired_tokens:
            del self.active_sessions[token]
    
    def get_active_sessions_count(self) -> int:
        """Get number of active sessions"""
        return len(self.active_sessions)

# Global session manager instance
session_manager = SessionManager()

def hash_password(password: str) -> str:
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify password against hashed password"""
    return hash_password(password) == hashed_password 