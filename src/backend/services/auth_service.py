"""
Authentication service layer.
Handles user registration and login business logic.
"""
from typing import Tuple, Optional
from models import db
from models.user import User
from utils.validators import validate_email, validate_password, sanitize_input

def register_user(email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    """
    Register a new user with email and password.
    
    Args:
        email: User's email address
        password: User's password (plain text)
    
    Returns:
        (user, error_message) - user if successful, error_message if failed
    """
    # Sanitize inputs
    email = sanitize_input(email).lower()
    
    # Validate email
    is_valid, error = validate_email(email)
    if not is_valid:
        return None, error
    
    # Validate password
    is_valid, error = validate_password(password)
    if not is_valid:
        return None, error
    
    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already registered"
    
    # Create new user
    user = User(email=email, role='user')
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"

def login_user(email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
    """
    Authenticate user with email and password.
    
    Args:
        email: User's email address
        password: User's password (plain text)
    
    Returns:
        (user, error_message) - user if successful, error_message if failed
    """
    # Sanitize email
    email = sanitize_input(email).lower()
    
    # Find user by email
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return None, "Invalid email or password"
    
    # Verify password
    if not user.check_password(password):
        return None, "Invalid email or password"
    
    return user, None
