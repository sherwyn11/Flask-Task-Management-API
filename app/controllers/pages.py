from flask import render_template, Blueprint, request, make_response, jsonify

from app.models import db
from app.models.user import User
from app.models.task import Task

from app.middleware.auth import auth_middleware


blueprint = Blueprint('pages', __name__)

@blueprint.route('/')
def home():
    return 'Testing'


@blueprint.route('/api/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email, password=password).first()

    if user:
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'Success',
            'message': 'User logged in successfully!',
            'token': auth_token
        }
        return make_response(jsonify(response_object)), 200
    
    else:
        response_object = {
            'status': 'Failed',
            'message': 'User does not exist! Please register.',
        }
        return make_response(jsonify(response_object)), 404


@blueprint.route('/api/signup-worker', methods=['POST'])
def signup_worker():
    email = request.form['email']
    password = request.form['password']
    user_type = 0
    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(email=email, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'Success',
            'message': 'Worker registered!',
            'token': auth_token
        }
        return make_response(jsonify(response_object)), 201

    else:
        response_object = {
            'status': 'Failed',
            'message': 'Worker already exists! Please Log in.',
        }
        return make_response(jsonify(response_object)), 202


@blueprint.route('/api/signup-admin', methods=['POST'])
def signup_admin():
    email = request.form['email']
    password = request.form['password']
    user_type = 1

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(email=email, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        response_object = {
            'status': 'Success',
            'message': 'Admin registered!',
            'token': auth_token
        }
        return make_response(jsonify(response_object)), 201

    else:
        response_object = {
            'status': 'Failed',
            'message': 'Admin already exists! Please Log in.',
        }
        return make_response(jsonify(response_object)), 202

@blueprint.route('/api/create-task', methods=['POST'])
def create_task():

    token = request.headers['Authorization'].split(' ')[1]
    user = auth_middleware(token)

    if user is not None and user.user_type == 1:
        worker_id = request.form['worker_id']
        title = request.form['title']
        admin_id = user.id

        task = Task(worker_id=worker_id, admin_id=admin_id, title=title)
        db.session.add(task)
        db.session.commit()

        response_object = {
            'status': 'Success',
            'message': 'Task: {} is created successfully!'.format(title),
        }
        return make_response(jsonify(response_object)), 201
    
    else:
        response_object = {
            'status': 'Failed',
            'message': 'User is unauthorized!',
        }
        return make_response(jsonify(response_object)), 401
