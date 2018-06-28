# project/config.py


import os


class BaseConfig:
    """Base configuration"""
    TESTING = False
    DEBUG_TB_ENABLED = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    #USERS_SERVICE_URL = os.environ.get('USERS_SERVICE_URL')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    DEBUG_TB_ENABLED = True
    MONGO_DB_URL = "mongodb://sam_census:sam_houz_123@cluster0-shard-00-00-wxp3r.mongodb.net:27017,cluster0-shard-00-01-wxp3r.mongodb.net:27017,cluster0-shard-00-02-wxp3r.mongodb.net:27017/admin?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"


class TestingConfig(BaseConfig):
    """Testing configuration"""
    TESTING = True


class StagingConfig(BaseConfig):
    """Staging configuration"""
    TESTING = False


class ProductionConfig(BaseConfig):
    """Production configuration"""
    TESTING = False
