SECRET_KEY = 'batatinha'


DB = 'dev'

if 'dev' in DB:

    DB_HOST = 'localhost'
    DB_PORT = '49153'
    DB_USER = 'root'
    DB_PASS = 'root'
    DB_DATA = 'postgres'

    SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATA}'


elif 'prod' in DB:
    
    DB_HOST = 'ec2-52-73-149-159.compute-1.amazonaws.com'
    DB_PORT = '5432'
    DB_USER = 'oayqwltvouhlxu'
    DB_PASS = '637c5b2342aa7cd7fc261ed57b6bd9a0fc819ce48057e1f863e7a68a461c28b1'
    DB_DATA = 'dcjh5c3mc7uptu'

    SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATA}'
