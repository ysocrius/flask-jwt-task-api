from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Initialize Cache
cache = Cache()

# Initialize Limiter
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=os.getenv("REDIS_URL", "memory://")
)

def init_extensions(app):
    """Initialize extensions with app context"""
    cache_type = "RedisCache" if os.getenv("REDIS_URL") else "SimpleCache"
    
    cache.init_app(app, config={
        'CACHE_TYPE': cache_type,
        'CACHE_REDIS_URL': os.getenv("REDIS_URL"),
        'CACHE_DEFAULT_TIMEOUT': 60
    })
    
    limiter.init_app(app)
