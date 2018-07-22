"""
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from app.controllers.home import home as ctrl_home

app = Flask(__name__)
app.config.from_pyfile('config/config.py')
app.wsgi_app = ProxyFix(app.wsgi_app)


def register_logging(app):
    """
    Connects the logging to the app.

    :param app: Current Flask application
    :type app: <Flask 'app'> obj
    """
    log_dir = os.path.join(app.config['APP_DATA_PATH'], 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    app_log_file = os.path.join(log_dir, 'middle-where.log')
    handler = TimedRotatingFileHandler(app_log_file, when='midnight', interval=1)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


def register_blueprints(app):
    """
    Connect the blueprints to the router.
    @note: If ctrl_home is not last, routing gets wonky!

    :param app: Current Flask application
    :type app: <Flask 'app'> obj
    """
    app.register_blueprint(ctrl_home)


register_logging(app)
register_blueprints(app)
app.logger.info('Started App')
