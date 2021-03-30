from flask import render_template, Blueprint, request, make_response, jsonify
from app.controllers.task import create_task_controller, view_assigned_tasks_controller, view_created_tasks_controller, update_task_controller
from app.config.constants.constants import UNAUTHORIZED_USER_ERROR_MESSAGE

blueprint = Blueprint('task', __name__)


@blueprint.route('/api/create-task', methods=['POST'])
def create_task():
    try:
        token = request.headers['Authorization'].split(' ')[1]
        worker_id = request.form['worker_id']
        title = request.form['title']

        response = create_task_controller(token, worker_id, title)
        return make_response(jsonify(response)), response['response_code']
    except:
        response = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }
        return make_response(jsonify(response)), response['response_code']


@blueprint.route('/api/view-assigned-tasks', methods=['GET'])
def view_assigned_tasks():
    try:
        token = request.headers['Authorization'].split(' ')[1]
        response = view_assigned_tasks_controller(token)
        return make_response(jsonify(response)), response['response_code']
    except:
        response = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }
        return make_response(jsonify(response)), response['response_code']


@blueprint.route('/api/view-created-tasks', methods=['GET'])
def view_created_tasks():
    try:
        token = request.headers['Authorization'].split(' ')[1]
        response = view_created_tasks_controller(token)
        return make_response(jsonify(response)), response['response_code']
    except:
        response = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }
        return make_response(jsonify(response)), response['response_code']


@blueprint.route('/api/update-task', methods=['PATCH'])
def update_task():
    try:
        token = request.headers['Authorization'].split(' ')[1]
        response = update_task_controller(token)
        return make_response(jsonify(response)), response['response_code']
    except:
        response = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }
        return make_response(jsonify(response)), response['response_code']