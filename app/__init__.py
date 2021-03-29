import logging
from flask import Flask, request as req
from app.routers import user, task
from app.models import db

def create_app(config_filename):

    app = Flask(__name__)

    app.config.from_object(config_filename)
    app.register_blueprint(user.blueprint)
    app.register_blueprint(task.blueprint)
    app.logger.setLevel(logging.NOTSET)

    db.init_app(app)
    
    with app.app_context():
        db.create_all()

    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method, req.url, req.data, resp)
        )
        return resp

    return app
