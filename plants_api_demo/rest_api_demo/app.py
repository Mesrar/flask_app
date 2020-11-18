import logging.config

import os
from flask import Flask, Blueprint, make_response, jsonify, send_from_directory, request, url_for, render_template
import settings

from flask.helpers import get_env

from flask_restx.apidoc import Apidoc, ui_for
from flask_restx import Api
from api.endpoints.imageapi import ns as image_namespace
from api.endpoints.plants import ns as plants_namespace

import api.endpoints.plants as plants
import api.endpoints.imageapi as imageapi
from flask_cors import CORS, cross_origin
from flask_swagger_ui import get_swaggerui_blueprint

app = Flask(__name__)

logging_conf_path = os.path.normpath(os.path.join(app.root_path, 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'library'

CORS(app, resources=r'/swagger/*')

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python-Flask-REST"
    }
)

### end swagger specific ###


apidoc = Apidoc(
    "restx_doc.static",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/swaggerui",
)


@app.before_request
def log_request():
    return None


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/static/swagger.json', methods=['GET'])
def swagger():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'swagger.json')


@app.route('/swagger', methods=['GET'])
def swaggerview():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'swagger.json')


@app.route('/', methods=['GET'])
def index():
    api = Api(apidoc)

    return render_template("swagger-ui.html", title=api.title, specs_url=api.specs_url)


def configure_app(flask_app):
    # xflask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['flask_env'] = get_env()
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def initialize_app(flask_app):
    configure_app(flask_app)
    api = Api(SWAGGERUI_BLUEPRINT)
    app.register_blueprint(SWAGGERUI_BLUEPRINT)
    api.add_namespace(plants_namespace)
    api.add_namespace(image_namespace)
    app.register_blueprint(plants.get_blueprint())
    app.register_blueprint(imageapi.get_blueprint())
    # plants.load_excel()


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))

    app.run(host='0.0.0.0', debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
