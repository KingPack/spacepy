import requests
import json

from spacepy.config import *

from spacepy.models.article import ArticleModel

from spacepy.models.article import DataApiModel

from spacepy.models.article import ArticleSchema
from spacepy.models.article import ArticleEventsSchema
from spacepy.models.article import ArticlelaunchesSchema
from spacepy.models.article import DataApiSchema

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

        
#----------------------------------------------------------------------------#
# Database.

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
Base.metadata.create_all(bind=engine)

#----------------------------------------------------------------------------#
# Schemas
article_schema = ArticleSchema()
article_launches_schema = ArticlelaunchesSchema(many=True)
article_events_schema = ArticleEventsSchema(many=True)
data_api_schema = DataApiSchema()

#----------------------------------------------------------------------------#
# Funçoes para validar e inserir dados no banco de dados



# inicializa o banco de dados chamando a função que adiciona na tabela data_api 
def initialize_database() -> dict:
    """ Initialize first DataApiModel """

    init_articles_ext = 1
    init_articles_new = 100000

    end_articles_data = requests.get('https://api.spaceflightnewsapi.net/v3/articles')
    end_articles_ext = end_articles_data.json()

    total_articles_data = requests.get('https://api.spaceflightnewsapi.net/v3/articles/count')
    total_articles_ext = total_articles_data.json()

    end_articles_ext = int(end_articles_ext[0]['id'])
    total_articles_ext = int(total_articles_ext)
    canceled_articles_ext = end_articles_ext - total_articles_ext

    article_end_query = db.query(ArticleModel).filter(ArticleModel.id >= init_articles_new).order_by(ArticleModel.id.desc()).first()

    if article_end_query:
        end_articles_new = article_end_query.id
    
    else:
        end_articles_new = init_articles_new

    init_articles_new = init_articles_new
    end_articles_new = end_articles_new
    total_articles_new = end_articles_new - init_articles_new
    canceled_articles_new = end_articles_new - init_articles_new

    total_articles_query = db.query(ArticleModel).all()
    total_articles_canceled_query = db.query(ArticleModel).filter(ArticleModel.canceled == True).all()
    
    canceled_articles_db = len(total_articles_canceled_query)
    total_articles_db = len(total_articles_query)


    data_api_insert = DataApiModel(
        init_articles_ext = init_articles_ext,
        end_articles_ext = end_articles_ext,
        total_articles_ext = total_articles_ext,
        canceled_articles_ext = canceled_articles_ext,
        init_articles_new = init_articles_new,
        end_articles_new = end_articles_new,
        total_articles_new = total_articles_new,
        canceled_articles_new = canceled_articles_new,
        total_articles_db = total_articles_db,
        canceled_articles_db = canceled_articles_db,
    )

    db.add(data_api_insert)
    db.commit()
    
    data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()
    data_api_json = DataApiSchema().dump(data_api_query)
    data_api_dump = json.dumps(data_api_json, indent=4)

    data_api_result = json.loads(data_api_dump)

    db.close()

    return data_api_result




# # Verifica se o artigo já existe no banco de dados se nao adiciona com base na api externa
# def get_article_database(id:int) -> dict:

#     data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()
#     data_api_json = DataApiSchema().dump(data_api_query)

#     if id <= data_api_query.total_articles_ext:
        
#         article_query = db.query(ArticleModel).filter(ArticleModel.id == id).first()
        
#         if article_query: # if article exists in database

#             if article_query.launches == True:
#                 launches = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_article == id).all()
#                 launches_json = article_launches_schema.dump(launches)

#             else:
#                 launches_json = []
    
#             if article_query.events == True:
#                 events = db.query(ArticleEventsModel).filter(ArticleEventsModel.id_article == id).all()
#                 events_json = article_events_schema.dump(events)

#             else:
#                 events_json = []

#             article_json = {
#                 'id' : article_query.id,
#                 'title' : article_query.title,
#                 'url' : article_query.url,
#                 'imageUrl' : article_query.imageUrl,
#                 'newsSite' : article_query.newsSite,
#                 'summary' : article_query.summary,
#                 'publishedAt' : article_query.publishedAt,
#                 'updatedAt' : article_query.updatedAt,
#                 'featured' : article_query.featured,
#                 'launches' : launches_json,
#                 'events' : events_json
#                 }

#             db.close()

#             result = article_json

#         else: # if article doesn't exist in database

#             article_insert = article_insert_db(id)
            
#             result = article_insert

#     else:
#         result = {'message': f'O limite de artigos externos e de ate o id : { data_api_json["total_articles_ext"]}'}

#     return dict(result)


# # Verifica requisitos e insere artigo no banco de dados
# def article_insert_db(id:int) -> dict:

#     data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()
#     final_id_article = data_api_query.total_articles_ext
#     article_request = requests.get(f'https://api.spaceflightnewsapi.net/v3/articles/{id}')

#     try:

#         if id > final_id_article:
#             raise Exception('id e maior que o ultimo artigo publicado na api externa.')

#         elif id < 1:
#             raise Exception('id e menor que o primeiro artigo publicado na api externa.')

#         elif article_request.status_code == 404 and id < final_id_article:

#             article_insert = ArticleModel(
#                 id = id,
#                 title = 'Excluido',
#                 url = "not found",
#                 imageUrl = 'not found',
#                 newsSite = 'not found',
#                 summary = 'not found',
#                 publishedAt = 'not found',
#                 updatedAt = 'not found',
#                 featured =  False,
#                 launches = False,
#                 events = False,
#                 canceled = True,
#                 )

#             db.add(article_insert)
#             db.commit()
#             db.close()

#             raise Exception('O artigo está excluido na api externa.')

#         else:

#             data_article_json = article_request.json()
            
#             if not data_article_json['launches']: # if article doesn't have launches
#                 launches = False

#             else: # if article has launches
#                 launches = True

#                 for launch in data_article_json['launches']: # for each launch in article

#                     article_launches_insert = ArticlelaunchesModel(
#                         id=launch['id'],
#                         id_article=id,
#                         provider=launch['provider']
#                         )

#                     db.add(article_launches_insert)

#             if not data_article_json['events']: # if article doesn't have events
#                 events = False

#             else: # if article has events
#                 events = True


#                 for event in data_article_json['events']: # for each event in article

#                     article_events_insert = ArticleEventsModel(
#                         id = event['id'],
#                         id_article = id,
#                         provider = event['provider']
#                         )

#                     db.add(article_events_insert)
#                     db.commit()

#             article_insert = ArticleModel(
#                 id = data_article_json['id'],
#                 title = data_article_json['title'],
#                 url = data_article_json['url'],
#                 imageUrl = data_article_json['imageUrl'],
#                 newsSite = data_article_json['newsSite'],
#                 summary = data_article_json['summary'],
#                 publishedAt = data_article_json['publishedAt'],
#                 updatedAt = data_article_json['updatedAt'],
#                 featured = data_article_json['featured'],
#                 launches = launches,
#                 events = events,
#             )

#             db.add(article_insert)
#             db.commit()
#             db.close()
                    
#             result = data_article_json

        
#     except Exception as error:
        
#         result = {'mensagem': str(error)}


#     return dict(result)


# # Loop para adicionar artigos da api externa ao banco de dados
# def create_data_loop() -> str:

#     api_data = initialize_database()

#     init_articles_ext = api_data['init_articles_ext']
#     end_articles_edb = api_data['end_articles_db']
#     total_articles_ext = api_data['total_articles_ext']
#     final_id_contador = total_articles_ext

#     if init_articles_ext > total_articles_ext:

#         result = {'message': f'O limite de artigos e ate {total_articles_ext}'}

#     else:

#         for article in range(init_articles_ext, total_articles_ext + 1):

#             insert_article = get_article_database(article)

#             print('--------------------------------------------------------------------------------------------')
#             print(f'Faltam {final_id_contador - article} artigos para serem adicionados')
#             print(f'Artigo : {article} adicionado...')
#             print(f'Artigos de {article} até {total_articles_ext} adicionados com sucesso')


#         total_articles_query = db.query(ArticleModel).all()
#         total_articles_canceled_query = db.query(ArticleModel).filter(ArticleModel.canceled == True).all()
        
#         canceled_articles = len(total_articles_canceled_query)
#         total_articles_db  = len(total_articles_query)

#         print(f'--------------------------------------------------------------------------------------------')
#         print(f'Total de artigos adicionados no banco de dados: {total_articles_db}')
#         print(f'Total de artigos excluidos: {canceled_articles}')
#         print(f'Total de artigos não excluidos: {total_articles_db - canceled_articles}')
#         print(f'Total de artigos na api externa: {total_articles_ext}')
#         print(f'--------------------------------------------------------------------------------------------')
#         print(f'Quantidade de artigos na api interna: {total_articles_db - canceled_articles}')
#         print(f'Artigos criados dentro da api interna: {init_articles_ext}')
#         print(f'--------------------------------------------------------------------------------------------')
        
#         data_api_insert = DataApiModel(
            
#             init_articles_ext = init_articles_ext,
#             end_articles_db = end_articles_db,
#             total_articles_ext = total_articles_ext,
#             total_articles_db = total_articles_db,
#             canceled_articles = canceled_articles,
#             )
        

#         db.add(data_api_insert)
#         db.commit()
#         db.close()

#         data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()
#         data_api_json = DataApiSchema().dump(data_api_query)
        
#         result = data_api_json


#     return result

