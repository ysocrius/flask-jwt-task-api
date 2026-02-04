"""
Admin routes.
Handles admin-only endpoints.
"""
from flask import Blueprint, request, jsonify
from middleware.auth import require_auth, require_role
from services.task_service import get_all_tasks, delete_any_task

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

@admin_bp.route('/tasks', methods=['GET'])
@require_auth
@require_role('admin')
def list_all_tasks():
    """
    List all tasks from all users (admin only).
    
    Query params:
        page: Page number (default: 1)
        limit: Items per page (default: 10)
    
    Response:
        200: {"tasks": [...], "total": int, "page": int, "limit": int, "total_pages": int}
        403: {"error": "Insufficient permissions"}
    """
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    
    if page < 1:
        page = 1
    if limit < 1 or limit > 100:
        limit = 10
    
    result = get_all_tasks(page, limit)
    
    return jsonify(result), 200

@admin_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@require_auth
@require_role('admin')
def delete_task(task_id):
    """
    Delete any task (admin only, no ownership check).
    
    Response:
        200: {"message": "Task deleted"}
        404: {"error": "Task not found"}
        403: {"error": "Insufficient permissions"}
    """
    success, error = delete_any_task(task_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify({'message': 'Task deleted successfully'}), 200
