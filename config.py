import os

class Config:
    SECRET_KEY = 'any-very-long-random-string'
    SQLALCHEMY_DATABASE_URI = "sqlite:///example.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False