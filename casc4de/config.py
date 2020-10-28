import os

class Config(object):
    TESTING = False
    SECRET_KEY = "X8slQiQWkvC0Zytlrntx9NQB009oOOg5r5kiah68NkckksDyuguwkz0KCV9lK3P5"
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}".format(
    #     username = os.environ["MYSQL_USER"],
    #     password = os.environ["MYSQL_PASSWORD"],
    #     host = os.environ["MYSQL_HOST"],
    #     port = os.environ["MYSQL_PORT"],
    #     db_name = os.environ["MYSQL_DATABASE"]
    # )
    
    SQL_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = "cookies"
    basedir = os.path.abspath(os.path.dirname(__file__))

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    SECRET_KEY = "X8slQiQWkvC0Zytlrntx9NQB009oOOg5r5kiah68NkckksDyuguwkz0KCV9lK3P5"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:2361/{db_name}".format(
        username='mddo',
        password='dung123',
        host='192.168.1.16',
        db_name='casc4de_test'
    )
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.basedir, "site.db")
