import logging.config

import os
from flask import Flask, Blueprint, make_response, jsonify, send_from_directory, request, url_for, render_template
import settings

from flask.helpers import get_env

from flask_restx import Api
from flask_restx.apidoc import Apidoc

from api.endpoints.plants import ns as ns1
from api.endpoints.imageapi import ns as ns2
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__, static_folder="static", template_folder="static/templates")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
logging_conf_path = os.path.normpath(os.path.join(app.root_path, 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

api_blueprint = Blueprint('api', __name__,
                          url_prefix="/static/swagger.json")


@app.route('/favicon.ico', methods=['GET'])
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


def swagger_static(filename):
    return url_for("static", filename='static_swagger/bower/swagger-ui/dist/{0}'.format(filename))


@app.route('/api/doc/v1/', methods=['GET'])
def swagger():
    return render_template("swagger-ui.html", swagger_static=swagger_static, title="custom_apidoc.title",
                           specs_url="/static/swagger.json")


@app.route('/static/swagger.json', methods=['GET'])
def sawggerui():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'swagger.json')



def configure_app(flask_app):
    flask_app.config['flask_env'] = get_env()
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['MONGOALCHEMY_DATABASE'] = 'library'
    flask_app.config["CACHE_TYPE"] = "null"
    flask_app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] \
                + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']


def initialize_app(flask_app):
    api.add_namespace(ns1)
    api.add_namespace(ns2)
    configure_app(flask_app)
    flask_app.register_blueprint(api_blueprint, url_prefix="/api/doc/v1/")

    # plants.load_excel()


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



api = api_patches(api_blueprint)

initialize_app(app)
log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))


