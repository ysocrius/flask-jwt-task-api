"""
Authentication routes.
Handles user registration and login endpoints.
"""
from flask import Blueprint, request, jsonify, current_app
from services.auth_service import register_user, login_user
from utils.jwt_helper import create_access_token

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Request body:
        {
            "email": "user@example.com",
            "password": "SecurePass123"
        }
    
    Response:
        201: {"message": "User registered successfully", "user": {...}}
        400: {"error": "..."}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user, error = register_user(email, password)
    
    if error:
        return jsonify({'error': error}), 400
    
    current_app.logger.info(f"New user registered: {email}")
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login and receive JWT token.
    
    Request body:
        {
            "email": "user@example.com",
            "password": "SecurePass123"
        }
    
    Response:
        200: {"token": "...", "user": {...}}
        401: {"error": "Invalid credentials"}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400
    
    user, error = login_user(email, password)
    
    if error:
        current_app.logger.warning(f"Failed login attempt for email: {email}")
        return jsonify({'error': error}), 401
    
    current_app.logger.info(f"User login successful: {email}")
    
    # Generate JWT token
    token = create_access_token(
        user.id,
        user.role,
        current_app.config['JWT_SECRET_KEY'],
        current_app.config['JWT_ACCESS_TOKEN_EXPIRES']
    )
    
    return jsonify({
        'token': token,
        'user': user.to_dict()
    }), 200
