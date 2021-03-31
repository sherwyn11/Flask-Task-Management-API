import logging
from flask import Flask, request as req
from app.routers import user, task
from app.commands import create_tables
from app.models import db
import os
import bcrypt

def create_app(config_filename='config/production/settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_filename)

    app.register_blueprint(user.blueprint)
    app.register_blueprint(task.blueprint)
    app.logger.setLevel(logging.NOTSET)

    db.init_app(app)
    app.cli.add_command(create_tables)

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app
