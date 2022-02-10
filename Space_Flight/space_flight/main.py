from flask import Flask
from config import SECRET_KEY

from ext import cors
from ext import doc_swagger
# from ext import database

from blueprint.space_flight_v1 import resources

#----------------------------------------------------------------------------#
# Initialize app and set config

app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


cors.init_app(app)
resources.init_app(app)
doc_swagger.init_app(app)


#----------------------------------------------------------------------------#
# Routes Main

@app.route('/')
def index():
    return '<H1> Back-end Challenge 2021 🏅 - Space Flight News </H1>'







#----------------------------------------------------------------------------#



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)