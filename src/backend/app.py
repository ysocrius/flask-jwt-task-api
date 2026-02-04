"""
Flask application factory.
"""
from flask import Flask, jsonify
from flask_cors import CORS
from config import get_config
from models import db
from models.user import User
from models.task import Task
from routes.auth import auth_bp
from routes.tasks import tasks_bp
from routes.admin import admin_bp
from utils.extensions import cache, limiter, init_extensions
from utils.logging_config import setup_logging

def create_app(config_name=None):
    """
    Create and configure Flask application.
    
    Args:
        config_name: Configuration name ('development', 'production', 'testing')
    
    Returns:
        Configured Flask app
    """
    app = Flask(__name__)
    
    # Load configuration
    if config_name:
        from config import config
        app.config.from_object(config[config_name])
    else:
        app.config.from_object(get_config())
    
    # Initialize extensions
    db.init_app(app)
    init_extensions(app)
    setup_logging(app)
    CORS(app, origins=app.config['ALLOWED_ORIGINS'])
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Resource not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed'}), 405
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'healthy'}), 200
    
    # API info endpoint
    @app.route('/api/v1', methods=['GET'])
    def api_info():
        return jsonify({
            'name': 'PrimeTrade Backend API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/v1/auth',
                'tasks': '/api/v1/tasks',
                'admin': '/api/v1/admin'
            }
        }), 200
    
    # Create database tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists (for testing)
        admin = User.query.filter_by(email='admin@primetrade.ai').first()
        if not admin:
            admin = User(email='admin@primetrade.ai', role='admin')
            admin.set_password('Admin123!')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created: admin@primetrade.ai / Admin123!")
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
