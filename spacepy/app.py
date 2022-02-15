
from flask import Flask, jsonify
from flask import Response
from models.article import DataApiModel, DataApiSchema

from config import SECRET_KEY
from insert_data import get_article_database, create_data_loop, initialize_database

from ext import cors
from ext import doc_swagger
from ext import database
from blueprint.space_flight_v1 import resources

#----------------------------------------------------------------------------#
# Initialize application and set config

application = Flask(__name__)

application.config['SECRET_KEY'] = SECRET_KEY
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

cors.init_app(application)
resources.init_app(application)
doc_swagger.init_app(application)


# Data Base

db = database.SessionLocal()
database.Base.metadata.create_all(bind=database.engine)

#----------------------------------------------------------------------------#



#----------------------------------------------------------------------------#
# Routes Main


@application.route('/', methods=['GET'])
def index() -> Response:
    result = '<H1>Back-end Challenge 🏅 2021 - Space Flight News</H1>'
    
    return Response(result, status=200, mimetype='text/html')


@application.route('/<int:id>', methods=['GET'])
def article_id(id) -> Response:

    result = get_article_database(id)

    return jsonify(result)


@application.route('/init', methods=['GET'])
@doc_swagger.swag_from("docs/init_get.yaml")
def init() -> Response:

    articles_data = initialize_database()
    #sadsa
    return jsonify(articles_data)

@application.route('/init/loop', methods=['GET'])
def loop_db():


    result = create_data_loop()

    return jsonify(result)


@application.route('/init/data', methods=['GET'])
@doc_swagger.swag_from("docs/init_data_get.yaml")
def init_data() -> object:
    """
        Inicializa os dados do banco de dados  API_DATA
        
    """

    data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()
    data_api_json = DataApiSchema().dump(data_api_query)


    result = data_api_json

    return jsonify(result)










if __name__ == '__main__':
    application.run()
