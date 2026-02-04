"""
Task service layer.
Handles task CRUD operations business logic.
"""
from typing import List, Tuple, Optional, Dict
from models import db
from models.task import Task
from utils.validators import validate_task_title, validate_task_status, sanitize_input

def create_task(user_id: int, title: str, description: str = None, status: str = 'pending') -> Tuple[Optional[Task], Optional[str]]:
    """
    Create a new task for a user.
    
    Returns:
        (task, error_message)
    """
    # Sanitize inputs
    title = sanitize_input(title)
    description = sanitize_input(description) if description else None
    
    # Validate
    is_valid, error = validate_task_title(title)
    if not is_valid:
        return None, error
    
    is_valid, error = validate_task_status(status)
    if not is_valid:
        return None, error
    
    # Create task
    task = Task(
        title=title,
        description=description,
        status=status,
        user_id=user_id
    )
    
    try:
        db.session.add(task)
        db.session.commit()
        return task, None
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"

def get_user_tasks(user_id: int, page: int = 1, limit: int = 10) -> Dict:
    """
    Get paginated tasks for a user.
    
    Returns:
        {
            'tasks': [...],
            'total': int,
            'page': int,
            'limit': int,
            'total_pages': int
        }
    """
    query = Task.query.filter_by(user_id=user_id).order_by(Task.created_at.desc())
    
    # Pagination
    total = query.count()
    tasks = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        'tasks': [task.to_dict() for task in tasks],
        'total': total,
        'page': page,
        'limit': limit,
        'total_pages': (total + limit - 1) // limit  # Ceiling division
    }

def get_task_by_id(task_id: int, user_id: int) -> Tuple[Optional[Task], Optional[str]]:
    """
    Get a specific task by ID (ownership validated).
    
    Returns:
        (task, error_message)
    """
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return None, "Task not found or access denied"
    
    return task, None

def update_task(task_id: int, user_id: int, data: Dict) -> Tuple[Optional[Task], Optional[str]]:
    """
    Update a task (ownership validated).
    
    Args:
        task_id: Task ID
        user_id: User ID (for ownership check)
        data: Dict with 'title', 'description', 'status' (all optional)
    
    Returns:
        (task, error_message)
    """
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return None, "Task not found or access denied"
    
    # Update fields if provided
    if 'title' in data:
        title = sanitize_input(data['title'])
        is_valid, error = validate_task_title(title)
        if not is_valid:
            return None, error
        task.title = title
    
    if 'description' in data:
        task.description = sanitize_input(data['description']) if data['description'] else None
    
    if 'status' in data:
        is_valid, error = validate_task_status(data['status'])
        if not is_valid:
            return None, error
        task.status = data['status']
    
    try:
        db.session.commit()
        return task, None
    except Exception as e:
        db.session.rollback()
        return None, f"Database error: {str(e)}"

def delete_task(task_id: int, user_id: int) -> Tuple[bool, Optional[str]]:
    """
    Delete a task (ownership validated).
    
    Returns:
        (success, error_message)
    """
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()
    
    if not task:
        return False, "Task not found or access denied"
    
    try:
        db.session.delete(task)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"

def get_all_tasks(page: int = 1, limit: int = 10) -> Dict:
    """
    Get all tasks (admin only).
    
    Returns:
        Paginated task data
    """
    query = Task.query.order_by(Task.created_at.desc())
    
    total = query.count()
    tasks = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        'tasks': [task.to_dict() for task in tasks],
        'total': total,
        'page': page,
        'limit': limit,
        'total_pages': (total + limit - 1) // limit
    }

def delete_any_task(task_id: int) -> Tuple[bool, Optional[str]]:
    """
    Delete any task (admin only, no ownership check).
    
    Returns:
        (success, error_message)
    """
    task = Task.query.get(task_id)
    
    if not task:
        return False, "Task not found"
    
    try:
        db.session.delete(task)
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"
