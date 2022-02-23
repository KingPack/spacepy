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