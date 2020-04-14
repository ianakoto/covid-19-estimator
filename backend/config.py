import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'password'
    SQLALCHEMY_DATABASE_URI = "postgres://dpiwjukxirskcf:391dae50ebad903e6e16e6d303c44e5181785cd7ac9bc23e8caa5587f9e46dc1@ec2-54-210-128-153.compute-1.amazonaws.com:5432/d19mg8ans3m4qk"


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
