


import os

from flask import Flask, render_template, current_app
from flask.helpers import get_env
from flask_sqlalchemy import SQLAlchemy

from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
import flask_mail
import flask_fanstatic
from dotenv import load_dotenv
import os

from werkzeug.middleware.proxy_fix import ProxyFix

import logging
from logging.config import dictConfig


toolbar = DebugToolbarExtension()
flask_bcrypt = Bcrypt()
flask_mailer = flask_mail.Mail()
fanstatic = flask_fanstatic.Fanstatic()


def create_app(test_config=None):
    # create and configure the app
    log.info("create_app: called")

    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app,
            x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    app.config.from_mapping(
        SQLALCHEMY_TRACK_MODIFICATIONS=True,
    )
    #app.config.from_object('config')
    app.config.from_pyfile('config.py')

    log.debug(f"value of config[SERVER_NAME] is '{ app.config['SERVER_NAME'] }'")


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # bind subsystems
    #db_app.init_app(app)
    flask_bcrypt.init_app(app)
    flask_mailer.init_app(app)
    fanstatic.init_app(app)

    if app.debug:
        toolbar.init_app(app)

    from . import views
    views.init_app(app)

    #from . import auth
    #auth.init_security(app, db_app.db)

    #from . import deployme
    #app.register_blueprint(deployme.bp)

    #from . import returned
    #app.register_blueprint(returned.bp)

    #from . import vc_scrape
    #vc_scrape.init_app(app)

    #from . import root
    #root.init_app(app)

    #from . import dat
    #dat.init_app(app)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        log.debug(f"hello method called.  current_app { current_app }")
        return '/hello method called'


    return app

def init_logging(app_name):
    logging_config = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'DEBUG',
                'stream': 'ext://sys.stderr'
            },
            'wsgi': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'DEBUG',
                'stream': 'ext://flask.logging.wsgi_errors_stream'
            },
        },
        'formatters': {
            'default': {
                'format': '%(asctime)s %(levelname)-5s %(name)-10s %(funcName)-.15s:%(lineno)d %(message)s',
                'datefmt': '%Y-%m-%d %H:%M:%S',
            },
        },
        'root': {
            'level': 'DEBUG',
            #'handlers': [ 'console', 'wsgi' ],
            'handlers': [ 'wsgi' ],
        },
        'loggers': {
            'urllib3': {
                'level': 'INFO',
            },
            'selenium': {
                'level': 'INFO',
            },
            'pyexcel': {
                'level': 'INFO',
            },
            'pyexcel_io': {
                'level': 'INFO',
            },
            'lml': {
                'level': 'INFO',
            },
        },
    }

    logging.config.dictConfig(logging_config)
    log = logging.getLogger(app_name)
    return log

log = init_logging(__name__)
