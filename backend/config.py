# config.py
class Config:
    SQLALCHEMY_DATABASE_URI_USERS = 'sqlite:///users.db'
    SQLALCHEMY_DATABASE_URI_ADMIN = 'sqlite:///admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'Pi5neer123!@#'
