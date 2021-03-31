import bcrypt
from flask import render_template, Blueprint, request, make_response, jsonify
from app.models import db
from app.models.user import User
from app.middleware.auth import auth_middleware
from app.config.constants.constants import UNAUTHORIZED_USER_ERROR_MESSAGE
from app.config.development.settings import BCRYPT_SALT

def signup_worker_controller(email, password, user_type):
    user = User.query.filter_by(email=email).first()

    if not user:
        password = bcrypt.hashpw(password, BCRYPT_SALT)

        user = User(email=email, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()

        auth_token = user.encode_auth_token(user.id)
        user.token = auth_token
        db.session.commit()

        response_object = {
            'status': 'Success',
            'message': 'Worker registered!',
            'token': auth_token,
            'response_code': 201
        }
    else:
        response_object = {
            'status': 'Failed',
            'message': 'Worker already exists! Please Log in.',
            'response_code': 401
        }
    
    return response_object


def signup_admin_controller(email, password, user_type):
    user = User.query.filter_by(email=email).first()

    if not user:
        password = bcrypt.hashpw(password, BCRYPT_SALT)
        
        user = User(email=email, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        
        auth_token = user.encode_auth_token(user.id)
        user.token = auth_token
        db.session.commit()
        
        response_object = {
            'status': 'Success',
            'message': 'Admin registered!',
            'token': auth_token,
            'response_code': 201
        }
    else:
        response_object = {
            'status': 'Failed',
            'message': 'Admin already exists! Please Log in.',
            'response_code': 401
        }
    
    return response_object


def login_controller(email, password):
    user = User.query.filter_by(email=email).first()

    if user:
        if bcrypt.checkpw(password, user.password): 
            auth_token = user.encode_auth_token(user.id)
            user.token = auth_token
            db.session.commit()

            response_object = {
                'status': 'Success',
                'message': 'User logged in successfully!',
                'token': auth_token,
                'response_code': 200
            }
        else:
            response_object = {
                'status': 'Failed',
                'message': 'Email or Password is incorrect!',
                'response_code': 401
            }        
    else:
        response_object = {
            'status': 'Failed',
            'message': 'User does not exist! Please register.',
            'response_code': 404
        }

    return response_object

        
def get_user_details_controller(token):
    user = auth_middleware(token)
        
    if user:
        user = {
            'id': user.id,
            'email': user.email,
            'user_type': 'admin' if user.user_type == 1 else 'worker'
        }
        response_object = {
            'status': 'Success',
            'message': user,
            'response_code': 200
        }
    else:
        response_object = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }

    return response_object


def get_all_workers_controller(token):
    user = auth_middleware(token)

    if user is not None and user.user_type == 1:
        workers = User.query.filter_by(user_type=0).all()
        
        all_workers = []

        for worker in workers:
            all_workers.append({
                'id': worker.id,
                'email': worker.email,
                } 
            )
        
        response_object = {
            'status': 'Success',
            'message': all_workers,
            'response_code': 200
        }
    
    else:
        response_object = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }

    return response_object

