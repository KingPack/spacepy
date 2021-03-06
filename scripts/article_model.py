from data_base import Base
from data_base import engine

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer

from marshmallow import Schema
from marshmallow import fields

from datetime import datetime

from sqlalchemy.sql.sqltypes import Text
from sqlalchemy.sql.sqltypes import String
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.sql.sqltypes import DateTime

# Criando as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

# models e schemas para o banco de dados
class ArticleModel(Base):

    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    imageUrl = Column(String)
    newsSite = Column(String)
    summary = Column(Text)
    publishedAt = Column(String)
    updatedAt = Column(String)
    featured = Column(Boolean)
    launches = Column(Boolean)
    events = Column(Boolean)
    canceled = Column(Boolean(False), default=False)

class ArticleSchema(Schema):

    id = fields.Integer()
    title = fields.String()
    url = fields.String()
    imageUrl = fields.String()
    newsSite = fields.String()
    summary = fields.String()
    publishedAt = fields.String()
    updatedAt = fields.String()
    featured = fields.Boolean()
    launches = fields.Boolean()
    events = fields.Boolean()

#----------------------------------------------------------------------------#
# Model and schema Article Lauchens.

class ArticlelaunchesModel(Base):

    __tablename__ = 'article_launches'

    id_launches = Column(Integer, primary_key=True)
    id_article = Column(Integer)

    id = Column(String)
    provider = Column(String)

class ArticlelaunchesSchema(Schema):

    id = fields.String()
    provider = fields.String()

#----------------------------------------------------------------------------#
# Model and schema Article Events.

class ArticleEventsModel(Base):
    
    __tablename__ = 'article_events'

    id_events = Column(Integer, primary_key=True)
    id_article = Column(Integer)

    id = Column(Integer)
    provider = Column(String)

class ArticleEventsSchema(Schema):

    id = fields.String()
    provider = fields.String()

#----------------------------------------------------------------------------#

class DataApiModel(Base):

    __tablename__ = 'data_api'

    id = Column(Integer, primary_key=True)
    last_update = Column(DateTime, default=datetime.now())
    init_articles_ext = Column(Integer)
    end_articles_ext = Column(Integer)
    total_articles_ext = Column(Integer)
    canceled_articles_ext = Column(Integer)
    init_articles_new = Column(Integer)
    end_articles_new = Column(Integer)
    total_articles_new = Column(Integer)
    canceled_articles_new = Column(Integer)
    total_articles_db = Column(Integer)
    canceled_articles_db = Column(Integer)
    
class DataApiSchema(Schema):

    id = fields.Integer()
    last_update = fields.String()
    init_articles_ext = fields.Integer()
    end_articles_ext = fields.Integer()
    total_articles_ext = fields.Integer()
    canceled_articles_ext = fields.Integer()
    init_articles_new = fields.Integer()
    end_articles_new = fields.Integer()
    total_articles_new = fields.Integer()
    canceled_articles_new = fields.Integer()
    total_articles_db = fields.Integer()
    canceled_articles_db = fields.Integer()