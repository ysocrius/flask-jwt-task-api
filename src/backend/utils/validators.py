"""
Input validation utilities.
"""
import re
from typing import Tuple

def validate_email(email: str) -> Tuple[bool, str]:
    """
    Validate email format using RFC 5322 regex.
    
    Returns:
        (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    return True, ""

def validate_password(password: str) -> Tuple[bool, str]:
    """
    Validate password strength.
    Requirements: min 8 chars, uppercase, lowercase, number
    
    Returns:
        (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    return True, ""

def validate_task_title(title: str) -> Tuple[bool, str]:
    """Validate task title"""
    if not title or not title.strip():
        return False, "Title is required"
    
    if len(title) > 200:
        return False, "Title must be 200 characters or less"
    
    return True, ""

def validate_task_status(status: str) -> Tuple[bool, str]:
    """Validate task status enum"""
    valid_statuses = ['pending', 'in_progress', 'completed']
    
    if not status:
        return False, "Status is required"
    
    if status not in valid_statuses:
        return False, f"Status must be one of: {', '.join(valid_statuses)}"
    
    return True, ""

def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS.
    Strips HTML tags and dangerous characters.
    """
    if not text:
        return ""
    
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    
    # Remove script tags and content
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL | re.IGNORECASE)
    
    return text.strip()
