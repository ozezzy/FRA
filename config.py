import os
basedir = os.path.abspath(os.path.dirname(__file__))

# default config
class BaseConfig(object):
    DEBUG = False
    # shortened for readability
    SECRET_KEY = '\xbf\xb0\x11\xb1\xcd\xf9\xba\x8bp\x0c...'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + \
    os.path.join(basedir, "feature_requests.db")


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + \
    os.path.join(basedir, "test.db")


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False