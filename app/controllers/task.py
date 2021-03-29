from flask import render_template, Blueprint, request, make_response, jsonify

from app.models import db
from app.models.user import User
from app.models.task import Task
from app.middleware.auth import auth_middleware
from config.constants.constants import UNAUTHORIZED_USER_ERROR_MESSAGE

blueprint = Blueprint('task', __name__)


def create_task_controller(token, worker_id, title):
    user = auth_middleware(token)    
    worker = User.query.filter_by(id=worker_id).first()

    if user is not None and user.user_type == 1 and worker.user_type == 0:
        admin_id = user.id

        task = Task(worker_id=worker_id, admin_id=admin_id, title=title)
        db.session.add(task)
        db.session.commit()

        response_object = {
            'status': 'Success',
            'message': 'Task: {} is created successfully!'.format(title),
            'response_code': 201
        }    
    else:
        response_object = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }
    
    return response_object


def view_assigned_tasks_controller(token):
    user = auth_middleware(token)

    if user is not None and user.user_type == 0:
        tasks = Task.query.filter_by(worker_id=user.id).all()
        assigned_tasks = []

        for task in tasks:
            assigned_tasks.append({
                'id': task.id,
                'title': task.title,
                'admin_id': task.admin_id,
                'completed': task.completed
            })

        response_object = {
            'status': 'Success',
            'message': assigned_tasks,
            'response_code': 200
        }
    
    else:
        response_object = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }

    return response_object


def view_created_tasks_controller(token):
    user = auth_middleware(token)

    if user is not None and user.user_type == 1:

        tasks = Task.query.filter_by(admin_id=user.id).all()
        created_tasks = []

        for task in tasks:
            created_tasks.append({
                'id': task.id,
                'title': task.title,
                'worker_id': task.worker_id,
                'completed': task.completed
            })

        response_object = {
            'status': 'Success',
            'message': created_tasks,
            'response_code': 200
        }
    else:
        response_object = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }
    
    return response_object


def update_task_controller(token):
    user = auth_middleware(token)
    
    if user is not None and user.user_type == 0:
        task = Task.query.filter_by(id=request.args['tid']).first()
        task.completed = not task.completed
        db.session.commit()

        message = 'completed' if task.completed else 'not completed'

        response_object = {
            'status': 'Success',
            'message': 'Task is marked as {}'.format(message),
            'response_code': 201
        }    
    else:
        response_object = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }

    return response_object