from flask import Blueprint
from flask import jsonify
from flask import Response
from flask import request

from ext import doc_swagger

#----------------------------------------------------------------------------#
# Resources

bp = Blueprint('space_flight_v1', __name__, url_prefix='/api/v1')


def init_app(app):
    app.register_blueprint(bp)

#----------------------------------------------------------------------------#


#----------------------------------------------------------------------------#
# Routes bp

@bp.route('/', methods=['GET'])
def index():
    return Response('<H1> Welcome to Space Flight News API Version 1.0</H1>', status=200, mimetype='text/html')


@bp.route('/articles', methods=['GET'])
@doc_swagger.swag_from("docs/articles_GET.yaml")
def articles_get():

    return jsonify('artigos')


@bp.route('/articles', methods=['POST'])
def articles_post():
    request_json = request.get_json()

    data_return = request_json
    
    return jsonify(data_return)


@bp.route('/articles/<int:id_article>', methods=['GET'])
def  article(id_article):
    return Response(f'artigo {id_article}', status=200, mimetype='text/html')