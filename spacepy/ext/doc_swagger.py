from flasgger import Swagger
from flasgger.utils import swag_from



order = {
    'Article':{
        'type': 'object',
        'properties': {
            'id': {
                'type': 'integer',
            },
            'title': {
                'type': 'integer',
            },
            'url': {
                'type': 'string',
            },
            'imageUrl': {
                'type': 'string',
            },
            'newsSite': {
                'type': 'boolean',
            },
            'summary': {
                'type': 'boolean',
            },
            'publishedAt': {
                'type': 'boolean',
            },
            'featured': {
                'type': 'integer',
                'default': False,
            },
            'launches': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                            'required': True,
                        },
                    'provider': {
                        'type': 'string',
                        },
                    }
                },
            },
            'events': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {
                            'type': 'integer',
                            'required': True,
                        },
                    'provider': {
                        'type': 'string',
                        },
                    }
                }
            },
            'canceled': {
                'type': 'integer',
                'default': False,
            },
        
        },

    },

}
    




swagger_template = {
    "swagger": '2.0',
    "openapi": '3.0',
    "operationId": "getmyData",
    "info": { 
            "title": "Spaceflight News API",
            "description": "Documentação da Spacepy. Um projeto desenvoldido com base na API Spacefligh News. \n Para mais informações acesse a [API Spaceflight News](https://api.spaceflightnewsapi.net/v3/documentation).",
            "version": "1.1.0",
            'termsOfService': "https://spaceflightnewsapi.net",
            'contact':{'url': "https://github.com/KingPack"},
            'license':{'name': "License", 'url': "http://www.apache.org/licenses/LICENSE-2.0.html"},

            },
    "definitions": order,
    }


swagger_config = {

    "headers": [],
    "specs": [{
        "endpoint": "/apispec_1",
        "route": '/api',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
        }
    ],
    "basePath": "/",
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/v1/documentation/",

    # 'swagger_ui_bundle_js' : 'https://unpkg.com/swagger-ui-dist@3.48.0/swagger-ui-bundle.js',
    'swagger_ui_bundle_css' : '//unpkg.com/swagger-ui-dist@3/swagger-ui.css',
    'jquery_js': '//unpkg.com/jquery@2.2.4/dist/jquery.min.js',
    'swagger_ui_standalone_preset_js': '//unpkg.com/swagger-ui-dist@3/swagger-ui-standalone-preset.js',
    }



def init_app(app):

    app.config['SWAGGER'] = {
        'title': 'Spacepy API',
        'uiversion': 3,
        }

    swagger = Swagger(app, config=swagger_config, template=swagger_template, validation_function=True)



