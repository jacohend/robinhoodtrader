from datetime import timedelta

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://{}:{}@{}/{}'
    APP_NAME = 'pycore'
    SECRET_KEY = '{}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CONSUL = 'consul'
    REDIS = 'redis'
    IP_SERVICE = "wyre_ip"


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SUPPRESS_SEND = False


class TestingConfig(Config):
    TESTING = True
