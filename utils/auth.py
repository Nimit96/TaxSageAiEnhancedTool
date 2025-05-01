"""
Authentication and Authorization Module
Contains functions for handling user authentication and authorization
"""

import hashlib
import jwt
import time
from typing import Dict, Optional, Tuple
from datetime import datetime, timedelta
import logging
from pathlib import Path

class TaxAuth:
    def __init__(
        self,
        secret_key: str,
        token_expiry: int = 3600,  # 1 hour
        refresh_token_expiry: int = 604800  # 7 days
    ):
        """Initialize authentication with secret key and token expiry"""
        self.secret_key = secret_key
        self.token_expiry = token_expiry
        self.refresh_token_expiry = refresh_token_expiry
        self.logger = logging.getLogger(__name__)
        self._load_blacklist()

    def _load_blacklist(self) -> None:
        """Load token blacklist"""
        self.blacklist_file = Path('blacklist.json')
        if self.blacklist_file.exists():
            with open(self.blacklist_file, 'r') as f:
                self.blacklist = json.load(f)
        else:
            self.blacklist = {}

    def _save_blacklist(self) -> None:
        """Save token blacklist"""
        with open(self.blacklist_file, 'w') as f:
            json.dump(self.blacklist, f)

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify password against hash"""
        return self.hash_password(password) == hashed_password

    def generate_tokens(self, user_id: str, role: str = 'user') -> Tuple[str, str]:
        """Generate access and refresh tokens"""
        # Generate access token
        access_token = jwt.encode(
            {
                'user_id': user_id,
                'role': role,
                'exp': datetime.utcnow() + timedelta(seconds=self.token_expiry)
            },
            self.secret_key,
            algorithm='HS256'
        )
        
        # Generate refresh token
        refresh_token = jwt.encode(
            {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=self.refresh_token_expiry)
            },
            self.secret_key,
            algorithm='HS256'
        )
        
        return access_token, refresh_token

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode token"""
        try:
            # Check if token is blacklisted
            if token in self.blacklist:
                return None
                
            # Verify and decode token
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token has expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token")
            return None

    def refresh_token(self, refresh_token: str) -> Optional[Tuple[str, str]]:
        """Generate new tokens using refresh token"""
        try:
            # Verify refresh token
            payload = self.verify_token(refresh_token)
            if not payload:
                return None
                
            # Generate new tokens
            return self.generate_tokens(payload['user_id'])
        except Exception as e:
            self.logger.error(f"Failed to refresh token: {str(e)}")
            return None

    def blacklist_token(self, token: str) -> bool:
        """Add token to blacklist"""
        try:
            # Verify token before blacklisting
            payload = self.verify_token(token)
            if not payload:
                return False
                
            # Add to blacklist with expiry
            self.blacklist[token] = payload['exp']
            self._save_blacklist()
            return True
        except Exception as e:
            self.logger.error(f"Failed to blacklist token: {str(e)}")
            return False

    def cleanup_blacklist(self) -> None:
        """Remove expired tokens from blacklist"""
        current_time = time.time()
        self.blacklist = {
            token: expiry
            for token, expiry in self.blacklist.items()
            if expiry > current_time
        }
        self._save_blacklist()

    def check_permission(self, token: str, required_role: str) -> bool:
        """Check if user has required role"""
        try:
            payload = self.verify_token(token)
            if not payload:
                return False
                
            # Check role
            return payload.get('role') == required_role
        except Exception as e:
            self.logger.error(f"Failed to check permission: {str(e)}")
            return False

    def get_user_id(self, token: str) -> Optional[str]:
        """Get user ID from token"""
        try:
            payload = self.verify_token(token)
            if not payload:
                return None
                
            return payload.get('user_id')
        except Exception as e:
            self.logger.error(f"Failed to get user ID: {str(e)}")
            return None

    def validate_password_strength(self, password: str) -> Tuple[bool, str]:
        """Validate password strength"""
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
            
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
            
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
            
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
            
        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            return False, "Password must contain at least one special character"
            
        return True, "Password meets strength requirements"

    def generate_password_reset_token(self, user_id: str) -> str:
        """Generate password reset token"""
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(hours=1),
                'purpose': 'password_reset'
            },
            self.secret_key,
            algorithm='HS256'
        )

    def verify_password_reset_token(self, token: str) -> Optional[str]:
        """Verify password reset token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            if payload.get('purpose') != 'password_reset':
                return None
            return payload.get('user_id')
        except jwt.ExpiredSignatureError:
            self.logger.warning("Password reset token has expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid password reset token")
            return None

    def generate_email_verification_token(self, user_id: str) -> str:
        """Generate email verification token"""
        return jwt.encode(
            {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(days=7),
                'purpose': 'email_verification'
            },
            self.secret_key,
            algorithm='HS256'
        )

    def verify_email_verification_token(self, token: str) -> Optional[str]:
        """Verify email verification token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            if payload.get('purpose') != 'email_verification':
                return None
            return payload.get('user_id')
        except jwt.ExpiredSignatureError:
            self.logger.warning("Email verification token has expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid email verification token")
            return None 