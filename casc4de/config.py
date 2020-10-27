import os

class Config(object):
    TESTING = False
    SECRET_KEY = "X8slQiQWkvC0Zytlrntx9NQB009oOOg5r5kiah68NkckksDyuguwkz0KCV9lK3P5"
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:2361/{db_name}".format(
    #     username = os.environ["MYSQL_USER"],
    #     password = os.environ["MYSQL_PASSWORD"],
    #     host = os.environ["MYSQL_HOST"],
    #     db_name = os.environ["MYSQL_DATABASE"]
    # )
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{username}:{password}@{host}:2361/{db_name}".format(
        username='mddo',
        password='dung123',
        host='192.168.1.16',
        db_name='casc4de_test'
    )
    SQL_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = "cookies"
    basedir = os.path.abspath(os.path.dirname(__file__))

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    # print ("base dir is ", Config.basedir)
    TESTING = True
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(Config.basedir, "site.db")
