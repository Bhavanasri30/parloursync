import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'parloursync_secret_key_123_abc')
    # Use SQLite inside the instance/ folder or root of parloursync
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///parloursync.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Enable iframe cookie support
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SAMESITE = 'None'
    REMEMBER_COOKIE_SECURE = True

