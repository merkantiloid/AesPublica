import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://aes:aes@localhost/aes?charset=utf8'
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'migrations')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
SQLALCHEMY_AUTOCOMMIT = True

WTF_CSRF_ENABLED = True
SECRET_KEY = os.getenv('SECRET_KEY', 'replace with env variable')

ESI_DATASOURCE = 'tranquility'
ESI_SWAGGER_JSON = 'https://esi.evetech.net/latest/swagger.json'
# ESI_SWAGGER_JSON = 'https://esi.evetech.net/latest/swagger.json?datasource=%s' % ESI_DATASOURCE
