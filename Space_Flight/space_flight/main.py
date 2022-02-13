
from urllib import response
from flask import Flask, jsonify
from flask import Response
from models.article import DataApiModel, DataApiSchema

from config import SECRET_KEY
from insert_data import get_article_database

from ext import cors
from ext import doc_swagger
from ext import database
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



@app.route('/', methods=['GET'])
def index() -> Response:
    result = '<H1>Back-end Challenge 🏅 2021 - Space Flight News</H1>'
    
    return Response(result, status=200, mimetype='text/html')


@app.route('/<int:id>', methods=['PUT'])
def index_put(id):
    print('estive aqui')

    return jsonify(f'PUT "{id}"')


@app.route('/<int:id>', methods=['GET'])
def article_id(id) -> object:
    """
        return Response object
    """

    # result = get_article_database(id)
    result = get_article_database(id)

    return Response(result)

#----------------------------------------------------------------------------#
# Init
@app.route('/init', methods=['GET'])
@doc_swagger.swag_from("docs/init_get.yaml")
def init() -> object:
    """
        Initialize all configurations
    """
    articles_data = initialize_database()
    
    return jsonify(articles_data)




#----------------------------------------------------------------------------#
# init/data
@app.route('/init/data', methods=['GET'])
@doc_swagger.swag_from("docs/init_data_get.yaml")
def init_data() -> object:
    """
        Inicializa os dados do banco de dados  API_DATA
        
    """

    initialize_database()

    data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()
    data_api_json = DataApiSchema().dump(data_api_query)

    return jsonify(data_api_json)


#----------------------------------------------------------------------------#
# init/data/<int:id>
@app.route('/init/data/<int:id>', methods=['GET'])
@doc_swagger.swag_from("docs/init_data_update.yaml")
def init_data_id(id) -> object:
    """
        Inicializa 
    """

    print('Inicializando o Banco de dados')
    initialize_database()
    

    data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()
    data_api_json = DataApiSchema().dump(data_api_query)
    
    end_article = data_api_query.end_articles

    if id < end_article:
        print(f'Se o id {id} é menor que o end_article {end_article} inicia get_data_api({id})')

        status_code = 200
        result = get_data_api(id)

        print(result)
    
    else:
        print(f'Se o id {id} é maior que o end_article {end_article} inicia get_data_api({id})')

        status_code = 404
        result = {
            'message': f'Ultimo adicionado foi {end_article}',
            'status_code': 404
        }

    print(result)

    return jsonify(result)
#----------------------------------------------------------------------------#





#----------------------------------------------------------------------------#
# Functions off Data


###########
#   data base
db = database.SessionLocal()
database.Base.metadata.create_all(bind=database.engine)


###########

def initialize_database() -> dict:
    """
        Initialize DataApiModel
    """
    from models.article import DataApiModel, DataApiSchema
    from datetime import datetime
    import requests

    articles_data = requests.get('https://api.spaceflightnewsapi.net/v3/articles')
    total_articles_data = requests.get('https://api.spaceflightnewsapi.net/v3/articles/count')

    total_articles = total_articles_data.json()
    total_articles = int(total_articles)


    final_id_article = articles_data.json()
    final_id_article = int(final_id_article[0]['id'])

    data_api_insert = DataApiModel(
        last_update = datetime.now(),
        init_articles = 1,
        end_articles = final_id_article,
        total_articles = total_articles,
        canceled_articles = 0,

    )

    data_api_json = DataApiSchema().dump(data_api_insert)

    db.add(data_api_insert)
    db.commit()
    db.close()

    return data_api_json



def get_data_api(id) -> dict:
    print('estou inicializando get_data_api')
    print('vou entrar nos imports')
    import requests
    print('request feito')
    from models.article import DataApiModel
    print('dataapi feito')
    from models.article import ArticleModel, ArticleSchema
    print('article feito')
    from models.article import ArticleEventsModel
    from models.article import ArticlelaunchesModel
    print('passei pelos imports')

    print('entrando pela query')
    
    article_query = db.query(ArticleModel).filter(ArticleModel.id == id).first()
    print('passei pela query')

    print('entrando nos requests')
    request_article_data = requests.get(f'https://api.spaceflightnewsapi.net/v3/articles/{id}')
    print(f'status code {request_article_data.status_code}')
    request_article_json = request_article_data
    print(request_article_json.status_code)
    print(type(request_article_json.status_code))
    print('passei nos requests')

    if request_article_data.status_code == 200:
        print('cheguei ate data_api_query')

        data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()

        if data_api_query: # if data_api_query is not None
            print('Os dados da api foram carregados')

            if article_query:
                print(f'Existe um artigo com esse id {id} no banco de dados')
                article_json = ArticleSchema(many=False).dump(article_query)
                print(article_json)
                    
                print(f'Vou te mostrar o artigo {id}')
                result = article_json

            else:
                print(f'Não existe um artigo {id} com esse id no banco de dados')
                
                if request_article_data.status_code == 200:
                    print(f'Artigo {id} existente na api externa')

                    if request_article_json['launches']:
                        print(f'Artigo {id} possui launches')
                        launches = True

                        for launch in request_article_json['launches']:

                            launches_insert = ArticlelaunchesModel(
                                id = launch['id'],
                                provider = launch['provider'],
                                id_launches_article = id,
                                )
                            
                            db.add(launches_insert)
                            db.commit()
                            db.close()

                    else:
                        print(f'Artigo {id} não possui launches')
                        launches = False

                    if request_article_json['events']:
                        print(f'Artigo {id} possui events')
                        events = True

                        for event in request_article_json['events']:

                            events_insert = ArticleEventsModel(
                                id = event['id'],
                                id_events_article = id,
                                provider = event['provider'],
                                )
                            
                            db.add(events_insert)
                            db.commit()
                            db.close()

                    else:
                        print(f'Artigo {id} não possui events')
                        events = False

                        article_insert = ArticleModel(
                            id = request_article_json['id'],
                            title = request_article_json['title'],
                            url = request_article_json['url'],
                            imageUrl = request_article_json['imageUrl'],
                            newsSite = request_article_json['newsSite'],
                            summary = request_article_json['summary'],
                            publishedAt = request_article_json['publishedAt'],
                            updatedAt = request_article_json['updatedAt'],
                            featured = False,
                            launches = launches,
                            events = events,
                            )

                        print(f'criei o model {article_insert.id} para o banco')

                        db.add(article_insert)
                        db.commit()
                        db.close()

                        print(f'adicionei o artigo {id} no banco de dados \O/')

                        result = {
                            'message': f'Artigo {id} criado com sucesso',
                            'status_code': 200,
                        }
                    
                elif request_article_data.status_code == 404:
                    print(f'Artigo {id} não existe na api externa')


                    if id > data_api_query.end_articles:
                        print(f'Talvez esse artigo {id} ainda nao foi escrito.')

                        result = {
                            'message': f'Artigo {id} não foi escrito ainda.',
                            'status_code': 404,
                        }

                    else:   
                        print(f'O artigo {id} deve ta excluido na API externa')

                        print('começando a adicionar a query sql')
                        article_insert = ArticleModel(
                            id = id,
                            title = 'Excluido',
                            description = 'Excluido',
                            url = 'Excluido',
                            imageUrl = 'Excluido',
                            newsSite = 'Excluido',
                            summary = 'Excluido',
                            publishedAt = 'Excluido',
                            updatedAt = 'Excluido',
                            featured = False,
                            launches = False,
                            events = False,
                            canceled = True
                            )

                        print(f'criei o model {article_insert.id} para o banco')

                        db.add(article_insert)
                        print(f'adicionei o artigo {id} excluido no banco de dados \O/')

                        db.commit()
                        db.close()

                        print(f'Adicionei com suscesso o artigo {id} como excluido')

        else:

            print('Os dados da api ainda não foram carregados')

            result = {
                'message': 'A API não foi carregado ainda !!! ',
                'status_code': 404,
            }
        
        print('Esse e o resultado')

    else:
        print(f'Artigo {id} não existe na api externa')



        



        status_code = 404
        result = {
            'message': f'Artigo {id} não foi escrito ainda.',
            'status_code': 404,
        }

  

    return result






if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
