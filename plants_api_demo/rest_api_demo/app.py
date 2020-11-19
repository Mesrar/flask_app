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
from flask_restx.apidoc import Apidoc

app = Flask(__name__, static_folder="static", template_folder="static/templates")

logging_conf_path = os.path.normpath(os.path.join(app.root_path, 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'library'

CORS(app, resources=r'/static/swagger.json')
### swagger specific ###

SWAGGER_URL = '/api/doc/v1'
apidoc = Apidoc(
    "app_doc",
    __name__,
    template_folder="static/templates",
    static_folder="static",
    static_url_path="/",

)
api = Api(apidoc)
URL_PREFIX = '/static/swagger.json'
apidoc.url_prefix = URL_PREFIX


### end swagger specific ###


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route('/api/doc/v1', methods=['GET'])
def swagger():
    return render_template("swagger-ui.html", title=api.title, specs_url="/static/swagger.json")


@app.route('/static/swagger.json', methods=['GET'])
def index():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'swagger.json')


def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['flask_env'] = get_env()
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP


def _register_apidoc(self, app: Flask) -> None:
    conf = app.extensions.setdefault('restplus', {})
    custom_apidoc = Apidoc('app_doc', __name__,
                           template_folder="static/templates", static_folder='static',
                           static_url_path="/")

    @custom_apidoc.add_app_template_global
    def swagger_static(filename: str) -> str:
        return url_for("app_doc.static", filename='static_swagger/bower/swagger-ui/dist/{0}'.format(filename))

    if not conf.get('apidoc_registered', False):
        app.register_blueprint(custom_apidoc)
    conf['apidoc_registered'] = True


def api_patches(api_blueprint):
    Api._register_apidoc = _register_apidoc

    @property
    def fix_specs_url(self):
        return url_for(self.endpoint('specs'), _external=False)

    Api.specs_url = fix_specs_url

    api_fixed = Api(
        api_blueprint,
        title="le title",
        description="le description",
        version="0.1.0", doc="/doc/v1", )

    return api_fixed


api_blueprint = Blueprint('api', __name__,
                          url_prefix="/static/swagger.json")
api = api_patches(api_blueprint)


def initialize_app(flask_app):
    api.add_namespace(plants_namespace)
    api.add_namespace(image_namespace)
    app.register_blueprint(api_blueprint, url_prefix="/api/doc/v1")
    # plants.load_excel()


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))

    app.run(host='0.0.0.0', debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
