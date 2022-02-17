
from flask import Flask, jsonify
from flask import Response

from .ext import cors
from .ext import doc_swagger

from .blueprint.space_flight_v1 import resources
from .insert_data import initialize_database

def create_app():

#----------------------------------------------------------------------------#
# Initialize app and set config

    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    cors.init_app(app)
    resources.init_app(app)
    doc_swagger.init_app(app)


    #----------------------------------------------------------------------------#
    # Routes Main


    @app.route('/', methods=['GET'])
    def index():
        result = '<H1>Back-end Challenge 🏅 2021 - Space Flight News</H1>'
        
        return Response(result, status=200, mimetype='text/html')


    @app.route('/init', methods=['GET'])
    def init():

        result = initialize_database()

        return jsonify(result)


    if __name__ == '__main__':
        app.run(debug=True)


    return app