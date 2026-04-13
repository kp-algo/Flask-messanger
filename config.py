import os

class Config:
    SECRET_KEY = 'any-very-long-random-string'
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@db:5432/my_database"
    SQLALCHEMY_TRACK_MODIFICATIONS = False