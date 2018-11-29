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


class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgres://lvxargangazpdj:07a21479e345a468d8f2f21884bd3853a366b42f05618485097c6c09eedc744b@ec2-54-235-73-241.compute-1.amazonaws.com:5432/d2t06euusmki4k'
