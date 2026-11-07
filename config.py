import os
from dotenv import load_dotenv

# Load environment variables from a .env file
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    # Secret key for session management and CSRF protection
    SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key')
    
    #Database configuration
database_url = os.getenv('DATABASE_URL') or "sqlite:///kedatrack.db"

if database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://", "postgresql+psycopg://", 1
    )
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )

SQLALCHEMY_DATABASE_URI = database_url
SQLALCHEMY_TRACK_MODIFICATIONS = False Database configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or "sqlite:///kedatrack.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable unnecessary overhead
    
    # Additional configurations (for future enhancements)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
    PERMANENT_SESSION_LIFETIME = 3600  # Session lifetime in seconds
