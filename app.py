import os

from flask import Flask
from route import scraper
from logging import config

log_config = {
    "version": 1,
    "root": {
        "handlers": ["console"],
        "level": "DEBUG"
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        }
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s : %(levelname)s : %(message)s",
            "datefmt": "%d-%m-%Y %I:%M:%S"
        }
    },
}

config.dictConfig(log_config)


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(scraper, url_prefix='/scraper')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
