import os
from dotenv import load_dotenv

load_dotenv() # Load variables from .env

class Config:
    WEATHER_API_KEY = os.environ.get('WEATHER_API_KEY')
    CURRENCY_EXCHANGE_API_KEY = os.environ.get('CURRENCY_EXCHANGE_API_KEY')
    LOG_FILE = 'logs/app.log'

class ProductionConfig(Config):
    DEBUG = True
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True
    LOG_FILE = 'logs/dev_app.log'