"""
Authentication middleware for protected routes.
"""
from functools import wraps
from flask import request, jsonify, current_app, g
from utils.jwt_helper import decode_access_token

def require_auth(f):
    """
    Decorator to require valid JWT token.
    Extracts token from Authorization header and validates it.
    Attaches user_id and role to Flask's g object.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Missing authorization header'}), 401
        
        # Extract token from "Bearer <token>"
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({'error': 'Invalid authorization header format. Use: Bearer <token>'}), 401
        
        token = parts[1]
        
        # Decode and validate token
        payload = decode_access_token(token, current_app.config['JWT_SECRET_KEY'])
        
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Attach user info to request context
        g.user_id = payload.get('user_id')
        g.role = payload.get('role')
        
        return f(*args, **kwargs)
    
    return decorated_function

def require_role(required_role: str):
    """
    Decorator to require specific role.
    Must be used after @require_auth.
    
    Args:
        required_role: Role required to access endpoint ('user', 'admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            user_role = getattr(g, 'role', None)
            
            if not user_role:
                return jsonify({'error': 'Authentication required'}), 401
            
            if user_role != required_role:
                return jsonify({'error': f'Insufficient permissions. {required_role} role required'}), 403
            
            return f(*args, **kwargs)
        
        return decorated_function
    return decorator
