import logging.config

import os
from flask import Flask, Blueprint
import settings

from api.plants.endpoints.plants import ns as plants_namespace
from api.plants.endpoints.imageapi import ns as imgapi_namespace
from api.restplus import api
from flask.helpers import get_env
from flask_restx import Api

from flask_restx.apidoc import apidoc

URL_PREFIX = '/api'
apidoc.url_prefix = URL_PREFIX

app = Flask(__name__, static_folder="../build", static_url_path="/")


app.config['MONGOALCHEMY_DATABASE'] = 'library'

logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


try:
    from flask_cors import CORS  # The typical way to import flask-cors
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)
from flask_cors import CORS

public_routes = Blueprint('public', __name__)


@public_routes.route("/api/*")
def helloWorld():
    '''
        Since the path '/' does not match the regular expression r'/api/*',
        this route does not have CORS headers set.
    '''
    return '''<h1>Hello CORS!</h1> Read about my spec at the
<a href="http://www.w3.org/TR/cors/">W3</a> Or, checkout my documentation
on <a href="https://github.com/corydolphin/flask-cors">Github</a>'''


api_v1 = Blueprint('API_v1', __name__)

logging.basicConfig(level=logging.INFO)
app = Flask('FlaskCorsBlueprintBasedExample')
app.register_blueprint(api_v1)
app.register_blueprint(public_routes)


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,OPTIONS,POST,PUT"
    response.headers["Access-Control-Allow-Headers"] = \
        "Access-Control-Allow-Headers,  Access-Control-Allow-Origin, Origin,Accept, " + \
        "X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers"
    return response


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

    api.add_namespace(plants_namespace)
    api.add_namespace(imgapi_namespace)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(app.config['SERVER_NAME']))
    if get_env() == 'production':
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        app.run(debug=settings.FLASK_DEBUG)


if __name__ == "__main__":
    main()
