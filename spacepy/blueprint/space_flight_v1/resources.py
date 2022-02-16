import json
from flask import Blueprint
from flask import jsonify
from flask import Response
from flask import request

from spacepy.models.article import ArticleModel, ArticleEventsModel, ArticlelaunchesModel
from spacepy.models.article import ArticleSchema, ArticleEventsSchema, ArticlelaunchesSchema

from spacepy.ext.database import SessionLocal, Base, engine

from spacepy.ext import doc_swagger
from spacepy.insert_data import get_article_database


#----------------------------------------------------------------------------#
# Resources

bp = Blueprint('space_flight_v1', __name__, url_prefix='/v1/')


def init_app(app):
    app.register_blueprint(bp)

#----------------------------------------------------------------------------#
# database

db = SessionLocal()
Base.metadata.create_all(bind=engine)

article_schema = ArticleSchema(many=True)
article_launches_schema = ArticlelaunchesSchema(many=True)
article_events_schema = ArticleEventsSchema(many=True)

#----------------------------------------------------------------------------#
# Routes bp

@bp.route('/', methods=['GET'])
def index() -> Response:
    result = '<H1> Welcome to Space Flight News API Version 1.0</H1>'
    
    return Response(result, status=200, mimetype='text/html')


@bp.route('/articles', methods=['GET'])
@doc_swagger.swag_from("docs/articles_GET.yaml")
def articles_get():

    data_json_request = request.get_json()

    if data_json_request is None:
        article_init = 0
        quantity_articles = 10

    elif data_json_request['article_init'] is None:
        article_init = 0
        quantity_articles = 10

    elif data_json_request['quantity_articles'] is None:
        quantity_articles = 10
        article_init = 0

    else:
        article_init = data_json_request['article_init']
        quantity_articles = data_json_request['quantity_articles']


    articles = db.query(ArticleModel).filter(ArticleModel.canceled == False).order_by(ArticleModel.id.desc()).limit(quantity_articles).offset(article_init).all()

    try:
        if not articles:
            raise Exception('Não existe nenhum artigo no banco de dados.')

        elif int(article_init) < 0 :
            raise Exception(f'O artigo {article_init} informado excede o valor minimo permitido = 0')

        elif int(quantity_articles) > 150:
            raise Exception('O limite de artigos permitido é de ate 150.')

        elif int(quantity_articles) < 1:
            raise Exception('o Minimo de artigos permitido é de 1.')

        else:

            artigos = []

            for article in articles:

                if article.launches == True: # if article contains launches
                    launches_query = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_article == article.id).all()
                    launches_json = article_launches_schema.dump(launches_query)

                else:
                    launches_json = []

                if article.events == True: # if article contains events
                    events_query = db.query(ArticleEventsModel).filter(ArticleEventsModel.id_article == article.id).all()
                    events_json = article_events_schema.dump(events_query)

                else:
                    events_json = []

                article_json = {
                    'id' : article.id,
                    'title' : article.title,
                    'url' : article.url,
                    'imageUrl' : article.imageUrl,
                    'newsSite' : article.newsSite,
                    'summary' : article.summary,
                    'publishedAt' : article.publishedAt,
                    'updatedAt' : article.updatedAt,
                    'featured' : article.featured,
                    'launches' : launches_json,
                    'events' : events_json
                    }

                artigos.append(article_json)

            result = json.dumps(artigos)

    except Exception as error:
        
        result = {'mensagem': str(error)}   

    db.close()

    return Response(result)


@bp.route('/articles', methods=['POST'])
@doc_swagger.swag_from("docs/articles_POST.yaml")
def articles_post() -> Response:
    data_request_json = request.get_json()

    try:

        if data_request_json['id'] is None:
            raise Exception('O campo id é obrigatório.')
        
        elif data_request_json['title'] is None:
            raise Exception('O campo title é obrigatório.')
        
        elif data_request_json['url'] is None:
            raise Exception('O campo url é obrigatório.')
        
        elif data_request_json['imageUrl'] is None:
            raise Exception('O campo imageUrl é obrigatório.')
        
        elif data_request_json['newsSite'] is None:
            raise Exception('O campo newsSite é obrigatório.')
        
        elif data_request_json['summary'] is None:
            raise Exception('O campo summary é obrigatório.')
        
        elif data_request_json['publishedAt'] is None:
            raise Exception('O campo publishedAt é obrigatório.')

        elif data_request_json['updatedAt'] is None:
            raise Exception('O campo updatedAt é obrigatório.')

        elif data_request_json['featured'] is None:
            raise Exception('O campo featured é obrigatório.')

        else:
            status_code = 200
            launches = data_request_json['launches']
            events = data_request_json['events']

            get_article_database(data_request_json['id'])

            article_query = db.query(ArticleModel).filter(ArticleModel.id == data_request_json['id']).first()


            if article_query.launches == True: # if article contains launches
                launches_query = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_article == id).all()
                launches_json = article_launches_schema.dump(launches_query)

            else:
                launches_json = []

            if article_query.events == True: # if article contains events
                events_query = db.query(ArticleEventsModel).filter(ArticleEventsModel.id_article == id).all()
                events_json = article_events_schema.dump(events_query)

            else:
                events_json = []

            article_json = {
                'id' : article_query.id,
                'title' : article_query.title,
                'url' : article_query.url,
                'imageUrl' : article_query.imageUrl,
                'newsSite' : article_query.newsSite,
                'summary' : article_query.summary,
                'publishedAt' : article_query.publishedAt,
                'updatedAt' : article_query.updatedAt,
                'featured' : article_query.featured,
                'launches' : launches_json,
                'events' : events_json
                }

            result = json.dumps(article_json)

            pass

    except Exception as error:
        status_code = 404
        result = {'mensagem': error}


    try:
        if article_query:
            raise Exception('O artigo já existe no banco de dados')

        else:
        
            if not data_request_json['launches']: # if article doesn't have launches

                launches = False

            else: # if article has launches

                launches = True

                for launch in data_request_json['launches']: # for each launch in article

                    article_launches_insert = ArticlelaunchesModel(
                        id=launch['id'],
                        id_article=id,
                        provider=launch['provider']
                        )

                    db.add(article_launches_insert)

            if not data_request_json['events']: # if article doesn't have events

                events = False

            else: # if article has events

                events = True

                for event in data_request_json['events']: # for each event in article

                    article_events_insert = ArticleEventsModel(
                        id = data_request_json['id'],
                        id_arcile = id,
                        provider = event['provider']
                        )

                    db.add(article_events_insert)

            article_insert = ArticleModel(
                id = data_request_json['id'],
                title = data_request_json['title'],
                url = data_request_json['url'],
                imageUrl = data_request_json['imageUrl'],
                newsSite = data_request_json['newsSite'],
                summary = data_request_json['summary'],
                publishedAt = data_request_json['publishedAt'],
                updatedAt = data_request_json['updatedAt'],
                featured = data_request_json['featured'],
                launches = launches,
                events = events,
            )

            article_data = {
                'id' : data_request_json['id'],
                'title' : data_request_json['title'],
                'url' : data_request_json['url'],
                'imageUrl' : data_request_json['imageUrl'],
                'newsSite' : data_request_json['newsSite'],
                'summary' : data_request_json['summary'],
                'publishedAt' : data_request_json['publishedAt'],
                'updatedAt' : data_request_json['updatedAt'],
                'featured' : data_request_json['featured'],
                'launches' : data_request_json['launches'],
                'events' : data_request_json['events'],
                }


            db.add(article_insert)
            db.commit()
            
            result = article_data

    except Exception as error:

        status_code = 404
        result = {'mensagem': str(error)}


    db.close()
    return jsonify(result), status_code


@bp.route('/articles/<int:id>', methods=['GET'])
@doc_swagger.swag_from("docs/article_id_GET.yaml")
def article_get(id: int) -> Response:
    
    article_query = db.query(ArticleModel).filter(ArticleModel.id == id).first()

    if article_query: # if article exists

        if article_query.canceled == False: # if article is not canceled
                

            if article_query.launches == True: # if article contains launches
                launches = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_article == id).all()
                launches_json = article_launches_schema.dump(launches)

            else:
                launches_json = []

            if article_query.events == True: # if article contains events
                events = db.query(ArticleEventsModel).filter(ArticleEventsModel.id_article == id).all()
                events_json = article_events_schema.dump(events)

            else:
                events_json = []

            article_json = {
                'id' : article_query.id,
                'title' : article_query.title,
                'url' : article_query.url,
                'imageUrl' : article_query.imageUrl,
                'newsSite' : article_query.newsSite,
                'summary' : article_query.summary,
                'publishedAt' : article_query.publishedAt,
                'updatedAt' : article_query.updatedAt,
                'featured' : article_query.featured,
                'launches' : launches_json,
                'events' : events_json
                }

            result = json.dumps(article_json)

        else: # if article is canceled
            result = {
                "message": f"Artigo {id} esta excluido",
                "status_code": 404,
                }
    else:
        result = {
            "message": f"Artigo {id} não esta cadastrado no banco de dados",
            "status_code": 404,
            }
        

    db.close()
    return result


@bp.route('/articles/<int:id>', methods=['DELETE'])
@doc_swagger.swag_from("docs/article_DELETE.yaml")
def article_delete(id: int) -> Response:

    article_query = db.query(ArticleModel).filter(ArticleModel.id == id).first()

    try:
        if not article_query:
            raise Exception(f'Não existe o artigo {id} no banco de dados.')

        elif article_query.canceled == True:
            raise Exception(f'O artigo {id} ja está excluido.')

        else:

            article_query.canceled = True

            db.commit()
            db.close()
            status_code = 200
            result = {
                'message': f'O artigo {id} foi deletado com sucesso',
                'status_code': 200,
            }

    except Exception as error:
        
        status_code = 404
        result = {'mensagem': str(error)}

    db.close()

    return jsonify(result), status_code


@bp.route('/articles/<int:id>', methods=['PUT'])
@doc_swagger.swag_from("docs/article_id_PUT.yaml")
def article_put(id: int) -> Response:

    data_request_json = request.get_json()

    article_query = db.query(ArticleModel).filter(ArticleModel.id == id, ArticleModel.canceled == False).first()
        
    if article_query.canceled == False: # if article is not canceled

        article_events_query = db.query(ArticleEventsModel).filter(ArticleEventsModel.id_article == id).all()
        article_launches_query = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_article == id).all()

        article_query.title = data_request_json['title']
        article_query.url = data_request_json['url']
        article_query.imageUrl = data_request_json['imageUrl']
        article_query.newsSite = data_request_json['newsSite']
        article_query.summary = data_request_json['summary']
        article_query.publishedAt = data_request_json['publishedAt']
        article_query.updatedAt = data_request_json['updatedAt']
        article_query.featured = data_request_json['featured']
        
        if data_request_json['launches']: # if launches is not empty

            article_query.launches = True

            for launche in data_request_json['launches']:

                article_launches_insert = ArticlelaunchesModel(

                    id = launche['id'],
                    idarticle = id,
                    provider = launche['provider'],
                    )

                db.add(article_launches_insert)

        if data_request_json['events']: # if events is not empty

            article_query.events = True

            for event in data_request_json['events']:

                article_events_insert = ArticleEventsModel(

                    id_article = id,
                    id = event['id'],
                    provider = event['provider'],
                    )

                db.add(article_events_insert)

        if article_query.launches == True: # if launches is true
            launches_json = article_launches_schema.dump(article_launches_query)

        else:
            launches_json = []

        if article_query.events == True: # if events is true
            events_json = article_events_schema.dump(article_events_query)

        else:
            events_json = []

        article_json = {
            'id' : article_query.id,
            'title' : article_query.title,
            'url' : article_query.url,
            'imageUrl' : article_query.imageUrl,
            'newsSite' : article_query.newsSite,
            'summary' : article_query.summary,
            'publishedAt' : article_query.publishedAt,
            'updatedAt' : article_query.updatedAt,
            'featured' : article_query.featured,
            'launches' : launches_json,
            'events' : events_json
            }
        
        status_code = 200
        result = json.dumps(article_json)

        db.commit()
        db.close()
    
    else: # if article is canceled

        status_code = 404
        result = {
            "message": f"Artigo {id} esta excluido",
            "status_code": 404,
            }



    return Response(result, status=status_code, mimetype='text/html')

