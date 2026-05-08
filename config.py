import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'any-very-long-random-string')
    
    # This is the critical change!
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        "postgresql://user:password@db:5432/my_database"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False