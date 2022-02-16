
from flask import Flask
from flask import jsonify
from flask import Response

# from ext import cors
# from ext import doc_swagger

# from config import SECRET_KEY

from .insert_data import get_article_database

from .blueprint.space_flight_v1 import resources

def create_app():

#----------------------------------------------------------------------------#
# Initialize app and set config

    app = Flask(__name__)

    # app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # cors.init_app(app)
    resources.init_app(app)
    # doc_swagger.init_app(app)


    #----------------------------------------------------------------------------#
    # Routes Main


    @app.route('/', methods=['GET'])
    def index() -> Response:
        result = '<H1>Back-end Challenge 🏅 2021 - Space Flight News</H1>'
        
        return Response(result, status=200, mimetype='text/html')


    @app.route('/<int:id>', methods=['GET'])
    def article_id(id:int) -> Response:

        result = get_article_database(id)

        return jsonify(result)




    if __name__ == '__main__':
        app.run(debug=True)


    return app