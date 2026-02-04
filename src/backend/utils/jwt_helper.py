"""
JWT token helper utilities.
"""
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional

def create_access_token(user_id: int, role: str, secret_key: str, expires_delta: timedelta) -> str:
    """
    Generate JWT access token with user_id and role in payload.
    
    Args:
        user_id: User's database ID
        role: User's role ('user' or 'admin')
        secret_key: JWT secret key from config
        expires_delta: Token expiration time
    
    Returns:
        Encoded JWT token string
    """
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + expires_delta,
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def decode_access_token(token: str, secret_key: str) -> Optional[Dict]:
    """
    Decode and verify JWT token.
    
    Args:
        token: JWT token string
        secret_key: JWT secret key from config
    
    Returns:
        Decoded payload dict if valid, None if invalid/expired
    """
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token expired
    except jwt.InvalidTokenError:
        return None  # Invalid token
