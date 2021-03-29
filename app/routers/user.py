from flask import render_template, Blueprint, request, make_response, jsonify
from app.controllers.user import signup_worker_controller, signup_admin_controller, login_controller, get_user_details_controller
from config.constants.constants import UNAUTHORIZED_USER_ERROR_MESSAGE

blueprint = Blueprint('user', __name__)


@blueprint.route('/api/signup-worker', methods=['POST'])
def signup_worker():
    email = request.form['email']
    password = request.form['password']
    user_type = 0

    response = signup_worker_controller(email, password, user_type)
    return make_response(jsonify(response)), response['response_code']


@blueprint.route('/api/signup-admin', methods=['POST'])
def signup_admin():
    email = request.form['email']
    password = request.form['password']
    user_type = 1

    response = signup_admin_controller(email, password, user_type)
    return make_response(jsonify(response)), response['response_code']


@blueprint.route('/api/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    response = login_controller(email, password)
    return make_response(jsonify(response)), response['response_code']


@blueprint.route('/api/get-user-details', methods=['GET'])
def get_user_details():
    try:
        token = request.headers['Authorization'].split(' ')[1]
        response = get_user_details_controller(token)
        return make_response(jsonify(response)), response['response_code']
    except:
        response = {
            'status': 'Failed',
            'message': UNAUTHORIZED_USER_ERROR_MESSAGE,
            'response_code': 401
        }
        return make_response(jsonify(response)), response['response_code']