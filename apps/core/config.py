"""
Configuration for the flask app
THIS IS FOR DEVELOPMENT PURPOSES ONLY
DO NOT USE IN PRODUCTION
"""
class Config():
    DEBUG = False
    TESTING = False
    ENV = 'development'
    SECRET_KEY = 'thisisasecretkey'

    MONGODB_SETTINGS = {
        'host': 'localhost',
        'db': 'dscweb'
    }
class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    
    MONGODB_SETTINGS = {
        'host': 'localhost',
        'db': 'dscwebtest'
    }

config = {
    'default': DevelopmentConfig,
    'dev': DevelopmentConfig,
    'testing': TestingConfig
}    
    

