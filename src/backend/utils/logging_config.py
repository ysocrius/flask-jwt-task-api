import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging(app):
    """Configure structured file logging for the application"""
    # Create logs directory if it doesn't exist
    if not os.path.exists('logs'):
        os.makedirs('logs')

    # Define log file path
    log_file = 'logs/app_execution.log'
    
    # Configure rotating file handler (10MB max per file, 10 backups)
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10485760, 
        backupCount=10
    )
    
    # Define log format
    formatter = logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Add handler to app logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    
    app.logger.info('=' * 40)
    app.logger.info('🚀 PrimeTrade Task Manager Started')
    app.logger.info('=' * 40)
