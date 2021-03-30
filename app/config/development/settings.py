import os
import bcrypt

DEBUG = True
SECRET_KEY = 'my precious'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@localhost:5432/task_manager'
HOST = '127.0.0.1'
PORT = int(os.environ.get('PORT', 5000))
BCRYPT_SALT = bcrypt.gensalt()
JWT_SECRET = 'test'