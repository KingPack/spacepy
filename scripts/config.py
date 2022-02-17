SECRET_KEY = 'batatinha'




DB_HOST = 'localhost'
DB_PORT = '49153'
DB_USER = 'root'
DB_PASS = 'root'
DB_DATA = 'postgres'

SQLALCHEMY_DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_DATA}'
