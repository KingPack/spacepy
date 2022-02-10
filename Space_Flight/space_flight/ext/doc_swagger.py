from flasgger import Swagger
from flasgger.utils import swag_from

swagger_template = {
    "swagger": '2.0',
    "operationId": "getmyData",
    "info": { 
            "title": "Spaceflight News API",
            "description": "Documentation for the Spaceflight News API. Join The Space Devs Discord server to contact me for support :) NOTE: to use filters like _contains, specify the field you want to filter. For example: title_contains=nasa. This can not be done in this Swagger interface. More info and examples.",
            "version": "0.2.1",
            }
    }


swagger_config = {

    "headers": [],
    "specs": [{
        "endpoint": "/apispec_1",
        "route": '/api',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True}
        ],
    "basePath": "localhost:8050/api/v1/",
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/api/docs/",
    }


def init_app(app):
    app.config['SWAGGER'] = {
        'title': 'Swagger UI',
        'uiversion': 3,
        'description': 'Documentation for the Spaceflight News API. Join The Space Devs Discord server to contact me for support :) NOTE: to use filters like _contains, specify the field you want to filter. For example: title_contains=nasa. This can not be done in this Swagger interface. More info and examples.'
        }

    swagger = Swagger(app, config=swagger_config, template=swagger_template, validation_function=True)
