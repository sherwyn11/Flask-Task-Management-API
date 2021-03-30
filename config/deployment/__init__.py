import os
import bcrypt

DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')
JWT_SECRET = os.environ.get('JWT_SECRET')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/task_manager'
BCRYPT_SALT = bcrypt.gensalt()