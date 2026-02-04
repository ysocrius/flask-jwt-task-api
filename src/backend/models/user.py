"""
User model for authentication and authorization.
"""
from datetime import datetime
import bcrypt
from . import db

class User(db.Model):
    """User model with authentication fields"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'user' or 'admin'
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationship to tasks
    tasks = db.relationship('Task', backref='owner', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password: str):
        """Hash password using bcrypt with cost factor 12"""
        salt = bcrypt.gensalt(rounds=12)
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password: str) -> bool:
        """Verify password against hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary (exclude password)"""
        return {
            'id': self.id,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<User {self.email}>'
