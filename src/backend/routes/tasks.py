"""
Task routes.
Handles task CRUD endpoints.
"""
from flask import Blueprint, request, jsonify, g
from middleware.auth import require_auth
from utils.extensions import cache, limiter
from services.task_service import (
    create_task, get_user_tasks, get_task_by_id,
    update_task, delete_task
)

tasks_bp = Blueprint('tasks', __name__, url_prefix='/api/v1/tasks')

@tasks_bp.route('', methods=['POST'])
@require_auth
def create():
    """
    Create a new task (protected).
    
    Request body:
        {
            "title": "Task title",
            "description": "Optional description",
            "status": "pending"  // optional, defaults to 'pending'
        }
    
    Response:
        201: {"message": "Task created", "task": {...}}
        400: {"error": "..."}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    title = data.get('title')
    description = data.get('description')
    status = data.get('status', 'pending')
    
    task, error = create_task(g.user_id, title, description, status)
    
    if error:
        return jsonify({'error': error}), 400
    
    # Invalidate cache for task list
    cache.delete_memoized(list_tasks)
    
    current_app.logger.info(f"Task created: ID {task.id} by User {g.user_id}")
    
    return jsonify({
        'message': 'Task created successfully',
        'task': task.to_dict()
    }), 201

@tasks_bp.route('', methods=['GET'])
@require_auth
@cache.memoize(timeout=60)
def list_tasks():
    """
    List all tasks for authenticated user with pagination.
    
    Query params:
        page: Page number (default: 1)
        limit: Items per page (default: 10)
    
    Response:
        200: {"tasks": [...], "total": int, "page": int, "limit": int, "total_pages": int}
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    # Validate pagination params
    if page < 1:
        page = 1
    if limit < 1 or limit > 100:
        limit = 10
    
    result = get_user_tasks(g.user_id, page, limit)
    
    return jsonify(result), 200

@tasks_bp.route('/<int:task_id>', methods=['GET'])
@require_auth
def get_task(task_id):
    """
    Get a specific task by ID (ownership validated).
    
    Response:
        200: {"task": {...}}
        404: {"error": "Task not found or access denied"}
    """
    task, error = get_task_by_id(task_id, g.user_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify({'task': task.to_dict()}), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@require_auth
def update(task_id):
    """
    Update a task (ownership validated).
    
    Request body (all fields optional):
        {
            "title": "Updated title",
            "description": "Updated description",
            "status": "completed"
        }
    
    Response:
        200: {"message": "Task updated", "task": {...}}
        400/404: {"error": "..."}
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    task, error = update_task(task_id, g.user_id, data)
    
    if error:
        if "not found" in error:
            return jsonify({'error': error}), 404
        return jsonify({'error': error}), 400
    
    # Invalidate cache for task list
    cache.delete_memoized(list_tasks)
    
    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_dict()
    }), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@require_auth
def delete(task_id):
    """
    Delete a task (ownership validated).
    
    Response:
        200: {"message": "Task deleted"}
        404: {"error": "Task not found or access denied"}
    """
    success, error = delete_task(task_id, g.user_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    # Invalidate cache for task list
    cache.delete_memoized(list_tasks)
    
    current_app.logger.info(f"Task deleted: ID {task_id} by User {g.user_id}")
    
    return jsonify({'message': 'Task deleted successfully'}), 200
