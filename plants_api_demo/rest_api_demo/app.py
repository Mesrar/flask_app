import logging.config

import os
from flask import Flask, Blueprint
import settings

from api.plants.endpoints.plants import ns as plants_namespace
from api.plants.endpoints.imageapi import ns as imgapi_namespace
from api.restplus import api
from flask.helpers import get_env
from flask_cors import CORS, cross_origin
from flask_restx import Api

from flask_restx.apidoc import apidoc

URL_PREFIX = '/api'
apidoc.url_prefix = URL_PREFIX

app = Flask(__name__, static_folder="../build", static_url_path="/")

app.config['MONGOALCHEMY_DATABASE'] = 'library'

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


@app.route('/')
def index():
    print(">>>>>>>>>>>> test")
    return app.send_static_file('index.html')


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['flask_env'] = get_env()
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', 'blueprint_name', url_prefix=URL_PREFIX)
    api = Api(blueprint, doc='/doc/')
    app.register_blueprint(blueprint)

    api.add_namespace(plants_namespace)
    api.add_namespace(imgapi_namespace)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    if get_env() == 'production':
        app.run(debug=False)
    else:
        app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
