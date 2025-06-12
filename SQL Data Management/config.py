import os

basedir = os.path.abspath(os.path.dirname(__file__))

def _env(key: str, default=None):
    return os.environ.get(key, default)

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = _env('SECRET_KEY', 'super-secret-key')
    JWT_SECRET_KEY = _env('JWT_SECRET_KEY', 'jwt-secret-key')
    CORS_ORIGINS = _env('CORS_ORIGINS', '*')

class InstanceConfig(Config):
    """Load configuration from environment variables."""
    SQLALCHEMY_DATABASE_URI = _env('DATABASE_URI', Config.SQLALCHEMY_DATABASE_URI)
    SECRET_KEY = _env('SECRET_KEY', Config.SECRET_KEY)
    JWT_SECRET_KEY = _env('JWT_SECRET_KEY', Config.JWT_SECRET_KEY)
    CORS_ORIGINS = _env('CORS_ORIGINS', Config.CORS_ORIGINS)
