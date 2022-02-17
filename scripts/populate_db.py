import json
import requests

from data_base import SessionLocal, engine, Base
from article_model import ArticleEventsModel, ArticleEventsSchema, ArticleModel, ArticlelaunchesModel, ArticlelaunchesSchema, DataApiModel, ArticleSchema, DataApiSchema



#----------------------------------------------------------------------------#
# Database.
db = SessionLocal()
Base.metadata.create_all(bind=engine)

article_schema = ArticleSchema()
article_launches_schema = ArticlelaunchesSchema(many=True)
article_events_schema = ArticleEventsSchema(many=True)
data_api_schema = DataApiSchema()
#----------------------------------------------------------------------------#


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


# Verifica requisitos e insere artigo no banco de dados
def article_insert_db(id:int) -> dict:

    data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()

    end_article_ext = data_api_query.end_articles_ext
    init_article_new = data_api_query.init_articles_new

    article_request = requests.get(f'https://api.spaceflightnewsapi.net/v3/articles/{id}')

    try:

        if id > end_article_ext:
            raise Exception(f'O id {id} e maior que o ultimo artigo publicado na api externa {end_article_ext} .')

        elif id < 1:
            raise Exception(f'O id {id} e menor que o primeiro artigo publicado na api externa.')

        elif article_request.status_code == 404 and id < init_article_new:

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
            db.close()

            raise Exception(f'O artigo {id} está excluido na api externa.')

        else:

            data_article_json = article_request.json()
            
            if not data_article_json['launches']: # if article doesn't have launches
                launches = False

            else: # if article has launches
                launches = True

                for launch in data_article_json['launches']: # for each launch in article

                    article_launches_insert = ArticlelaunchesModel(
                        id=launch['id'],
                        id_article=id,
                        provider=launch['provider']
                        )

                    db.add(article_launches_insert)

            if not data_article_json['events']: # if article doesn't have events
                events = False

            else: # if article has events
                events = True

                for event in data_article_json['events']: # for each event in article

                    article_events_insert = ArticleEventsModel(
                        id = event['id'],
                        id_article = id,
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
            db.close()
                    
            result = json.dumps(data_article_json, indent=4)
        
    except Exception as error:
        status_code = 404
        result = json.dumps({'mensagem': str(error), 'status_code': status_code}, indent=4)



    db.close()

    return result


def get_article_database(id:int) -> dict:

    data_api_query = db.query(DataApiModel).order_by(DataApiModel.id.desc()).first()
    data_api_json = DataApiSchema().dump(data_api_query)

    if id <= data_api_query.end_articles_ext:
        
        article_query = db.query(ArticleModel).filter(ArticleModel.id == id).first()
        
        if article_query: # if article exists in database

            if article_query.launches == True:
                launches = db.query(ArticlelaunchesModel).filter(ArticlelaunchesModel.id_article == id).all()
                launches_json = article_launches_schema.dump(launches)

            else:
                launches_json = []
    
            if article_query.events == True:
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

            db.close()

            result = article_json

        else: # if article doesn't exist in database

            article_insert = article_insert_db(id)
            
            result = article_insert

    else:
        result = json.dumps({'message': f'O limite de artigos externos e de ate o id : { data_api_json["end_articles_ext"]}'})
        result = dict(result)

    return result



def create_data_loop() -> str:

    api_data_start = initialize_database()

    init_articles_ext = api_data_start['init_articles_ext']
    end_articles_ext = api_data_start['end_articles_ext']
    total_articles_ext = api_data_start['total_articles_ext']
    count_article = end_articles_ext


    for article in range(init_articles_ext, end_articles_ext + 1):

        data_article = get_article_database(article)

        print('--------------------------------------------------------------------------------------------')
        print(f'Faltam {count_article - article} artigos para serem adicionados')
        print(f'Artigo : {article} adicionado...')
        print(f'Artigos de {article} até {end_articles_ext} adicionados com sucesso')


    total_articles_query = db.query(ArticleModel).all()
    total_articles_canceled_query = db.query(ArticleModel).filter(ArticleModel.canceled == True).all()
    
    canceled_articles = len(total_articles_canceled_query)
    total_articles_db  = len(total_articles_query)

    print(f'--------------------------------------------------------------------------------------------')
    print(f'Total de artigos adicionados no banco de dados: {total_articles_db}')
    print(f'Total de artigos excluidos: {canceled_articles}')
    print(f'Total de artigos não excluidos: {total_articles_db - canceled_articles}')
    print(f'Total de artigos na api externa: {total_articles_ext}')
    print(f'--------------------------------------------------------------------------------------------')
    print(f'Quantidade de artigos na api interna: {total_articles_db - canceled_articles}')
    print(f'Artigos criados dentro da api interna: {init_articles_ext}')
    print(f'--------------------------------------------------------------------------------------------')
    

    api_data_end = initialize_database()

        
    result = api_data_end

    db.close()
    return result
