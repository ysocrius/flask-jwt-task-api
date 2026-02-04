"""
Run script for the Flask application.
"""
import sys
import os

# Add src/backend to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src', 'backend'))

from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("=" * 60)
    print("🚀 PrimeTrade Backend API Server")
    print("=" * 60)
    print(f"✅ Server running at: http://localhost:5000")
    print(f"✅ API endpoints: http://localhost:5000/api/v1")
    print(f"✅ Health check: http://localhost:5000/health")
    print(f"✅ Default admin: admin@primetrade.ai / Admin123!")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
