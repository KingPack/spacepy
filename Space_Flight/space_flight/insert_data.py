import json
import requests

from config import *

from models.article import ArticleModel, ArticleEventsModel, ArticlelaunchesModel, DataApiModel
from models.article import ArticleSchema, ArticleEventsSchema, ArticlelaunchesSchema, DataApiSchema

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#----------------------------------------------------------------------------#
# Run test

Base = declarative_base()
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()
Base.metadata.create_all(bind=engine)

#----------------------------------------------------------------------------#

article_schema = ArticleSchema()
article_launches_schema = ArticlelaunchesSchema(many=True)
article_events_schema = ArticleEventsSchema(many=True)
data_api_schema = DataApiSchema()

#----------------------------------------------------------------------------#
# functions to insert data in database

def get_article_database(id:int) -> dict:

    article_query = db.query(ArticleModel).filter(ArticleModel.id == id).first()

    if article_query: # if article exists in database


        if article_query.launches == True:
            launches = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_launches == id).all()
            launches_json = article_launches_schema.dump(launches)

        else:
            launches_json = []
 
        if article_query.events == True:
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

        result = article_json

    else: # if article doesn't exist in database
        article_insert = article_insert_db(id)
        result = article_insert


    db.close()

    return json.dumps(result)

#----------------------------------------------------------------------------#
# test function

def validade_events_launches(id_launches:int, launches:bool, events:bool):
    
    if launches == True:
        launches = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_launches == id).all()
        launches_json = article_launches_schema.dump(launches)

    else:
        launches_json = []

    if events == True:
        events = db.query(ArticleEventsModel).filter(ArticleEventsModel.id_events == id).all()
        events_json = article_events_schema.dump(events)

    else:
        events_json = []
    
    return launches_json, events_json

# print(validade_events_launches(True, True))
#----------------------------------------------------------------------------#



def article_insert_db(id:int) -> dict:

    data_api = requests.get(f'https://api.spaceflightnewsapi.net/v3/articles/{id}')

    if data_api.status_code == 404: # if article doesn't exist in api
            
        article_insert = ArticleModel(
            id = id,
            title = 'Excluido',
            url = "not found",
            imageUrl = 'not found',
            newsSite = 'not found',
            summary = 'not found',
            publishedAt = 'not found',
            updatedAt = 'not found',
            featured =  False,
            launches = False,
            events = False,
            canceled = True,
        )

        db.add(article_insert)
        db.commit()


        result = {
            "message": f"Artigo {id} não existe",
            "status_code": 404,
            }
    
    elif data_api.status_code == 200: # if article exists in api

        data_article_json = data_api.json()
        

        if not data_article_json['launches']: # if article doesn't have launches
            launches = False

        else: # if article has launches
            launches = True

            for launch in data_article_json['launches']: # for each launch in article

                article_launches_insert = ArticlelaunchesModel(
                    id=launch['id'],
                    id_launches_article=id,
                    provider=launch['provider']
                    )

                db.add(article_launches_insert)

        if not data_article_json['events']: # if article doesn't have events
            events = False

        else: # if article has events
            events = True


            for event in data_article_json['events']: # for each event in article

                article_events_insert = ArticleEventsModel(
                    id = data_article_json['id'],
                    id_events = event['id'],
                    provider = event['provider']
                    )

                db.add(article_events_insert)
                db.commit()
    
        article_insert = ArticleModel(
            id = data_article_json['id'],
            title = data_article_json['title'],
            url = data_article_json['url'],
            imageUrl = data_article_json['imageUrl'],
            newsSite = data_article_json['newsSite'],
            summary = data_article_json['summary'],
            publishedAt = data_article_json['publishedAt'],
            updatedAt = data_article_json['updatedAt'],
            featured = data_article_json['featured'],
            launches = launches,
            events = events,
        )

        db.add(article_insert)
        db.commit()
             
        result = {
            'id' : data_article_json['id'],
            'title' : data_article_json['title'],
            'url' : data_article_json['url'],
            'imageUrl' : data_article_json['imageUrl'],
            'newsSite' : data_article_json['newsSite'],
            'summary' : data_article_json['summary'],
            'publishedAt' : data_article_json['publishedAt'],
            'updatedAt' : data_article_json['updatedAt'],
            'featured' : data_article_json['featured'],
            'launches' : data_article_json['launches'],
            'events' : data_article_json['events'],
            }


    db.close()

    return result



def create_data_loop():

    data_api_final = requests.get('https://api.spaceflightnewsapi.net/v3/articles')

    final_id_article = data_api_final.json()
    final_id_article = int(final_id_article[0]['id'])
    final_id_article = final_id_article

    init_id_articles = 13920

    for article in range(init_id_articles, final_id_article):
        print(article)
        get_article_database(article)
        

    total_articles_query = db.query(ArticleModel).all()
    total_articles_canceled_query = db.query(ArticleModel).filter(ArticleModel.canceled == True).all()
    
    total_canceled = len(total_articles_canceled_query)
    total_articles  = len(total_articles_query)

    data_api_insert = DataApiModel(
        
        # date_push = None,
        init_articles = init_id_articles,
        end_articles = final_id_article,
        total_articles = total_articles,
        canceled_articles = total_canceled,
        )
    
    db.add(data_api_insert)
    db.commit()
    db.close()


    return 'finalizou'

