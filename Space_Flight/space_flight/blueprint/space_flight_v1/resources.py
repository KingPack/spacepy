import json
from flask import Blueprint
from flask import jsonify
from flask import Response
from flask import request

from models.article import ArticleModel, ArticleEventsModel, ArticlelaunchesModel
from models.article import ArticleSchema, ArticleEventsSchema, ArticlelaunchesSchema

from ext.database import SessionLocal, Base, engine

from ext import doc_swagger


#----------------------------------------------------------------------------#
# Resources

bp = Blueprint('space_flight_v1', __name__, url_prefix='/v1/')


def init_app(app):
    app.register_blueprint(bp)

#----------------------------------------------------------------------------#
# database

db = SessionLocal()
Base.metadata.create_all(bind=engine)

article_schema = ArticleSchema()
article_launches_schema = ArticlelaunchesSchema(many=True)
article_events_schema = ArticleEventsSchema(many=True)

#----------------------------------------------------------------------------#
# Routes bp

@bp.route('/', methods=['GET'])
def index():
    result = '<H1> Welcome to Space Flight News API Version 1.0</H1>'
    
    return Response(result, status=200, mimetype='text/html')


@bp.route('/articles', methods=['GET'])
@doc_swagger.swag_from("docs/articles_GET.yaml")
def articles_get():
    print('Estive aqui /articles [GET]')
    data_json_request = request.get_json()
    print(data_json_request)

    articles = db.query(ArticleModel).all()
    articles_json = article_schema.dump(articles)

    if not articles_json:

        status_code = 404
        result = {
            'message': 'Nenhum artigo criado ainda',
            'status_code': 'Not found'
            }

    else:
        status_code = 200
        result = articles_json


    return jsonify(result, status_code)


@bp.route('/articles', methods=['POST'])
@doc_swagger.swag_from("docs/articles_POST.yaml")
def articles_post() -> Response:
    print('Estive aqui [POST]')
    data_request_json = request.get_json()

    article_query = db.query(ArticleModel).filter(ArticleModel.id == data_request_json['id']).first()

    if article_query: # if article exists in database

        status_code = 404

        article_data = {
            'message': 'Argito ja existe no banco de dados',
            'status_code': status_code 

        }

        result = json.dumps(article_data)

    else: # if article not exists in database

        status_code = 200

        if not data_request_json['launches']: # if article doesn't have launches
            launches = False

        else: # if article has launches
            launches = True

            for launch in data_request_json['launches']: # for each launch in article

                article_launches_insert = ArticlelaunchesModel(
                    id=launch['id'],
                    id_launches_article=data_request_json['id'],
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
                    id_events = event['id'],
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
        
        result = json.dumps(article_data)


    
    return Response(result, status=status_code, mimetype='application/json')


@bp.route('/articles/<int:id>', methods=['GET'])
@doc_swagger.swag_from("docs/article_id_GET.yaml")
def article_get(id: int) -> Response:
    article_query = db.query(ArticleModel).filter(ArticleModel.id == id).first()

    if article_query: # if article exists

        if article_query.canceled == False: # if article is not canceled
                

            if article_query.launches == True: # if article contains launches
                launches = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_launches == id).all()
                launches_json = article_launches_schema.dump(launches)

            else:
                launches_json = []

            if article_query.events == True: # if article contains events
                events = db.query(ArticleEventsModel).filter(ArticleEventsModel.id_events == id).all()
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
        


    return result



@bp.route('/articles/<int:id>', methods=['DELETE'])
@doc_swagger.swag_from("docs/article_DELETE.yaml")
def article_delete(id: int) -> Response:
    print('Estive aqui [DELETE]')
    article_query = db.query(ArticleModel).filter(ArticleModel.id == id).first()
    
    if not article_query: # if not exist

        result = {
            "message": f"Artigo {id} não esta cadastrado no banco de dados",
            "status_code": 404,
            }

        status_code = 404

    else: # if exist

        if article_query.canceled == False: # if not canceled

            article_query.canceled = True
            
            result = {
                'message': f'O artigo {id} foi deletado com sucesso',
                'status_code': 200,
                'data': article_schema.dump(article_query),
            }
        
        else: # if canceled

            result = {
                'message': f'Artigo {id} ja esta deletado',
                'status_code': 200, 
            }

    db.commit()
    db.close()

    return jsonify(result)



@bp.route('/articles/<int:id>', methods=['PUT'])
@doc_swagger.swag_from("docs/article_id_PUT.yaml")
def article_put(id: int) -> Response:

    data_request_json = request.get_json()

    article_query = db.query(ArticleModel).filter(ArticleModel.id == id, ArticleModel.canceled == False).first()
        
    if article_query.canceled == False: # if article is not canceled

        article_events_query = db.query(ArticleEventsModel).filter(ArticleEventsModel.id_events == id).all()
        article_launches_query = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_launches == id).all()

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
                    id_launches_article = id,
                    provider = launche['provider'],
                    )

                db.add(article_launches_insert)

        if data_request_json['events']: # if events is not empty

            article_query.events = True

            for event in data_request_json['events']:

                article_events_insert = ArticleEventsModel(

                    id = event['id'],
                    id_events = id,
                    name = event['name'],
                    url = event['url'],
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


