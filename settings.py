import logging.config
from os import environ

from dotenv import load_dotenv
import pika

logging.config.fileConfig('config/logging.ini')

load_dotenv('config/.env')
load_dotenv('config/sample.env')

DISTRIBUTED = environ.get('NAURON_MODE') == 'API'

MQ_PARAMS = pika.ConnectionParameters \
    (host=environ.get('MQ_HOST'), port=environ.get('MQ_PORT'),
     credentials=pika.credentials.PlainCredentials(username=environ.get('MQ_USERNAME'),
                                                   password=environ.get('MQ_PASSWORD')))
MQ_EXCHANGE = environ.get('MQ_EXCHANGE', 'estnltk-bert')
MQ_QUEUE_NAME = environ.get('MQ_QUEUE_NAME', 'default')

MESSAGE_TIMEOUT = int(environ.get('GUNICORN_TIMEOUT', '120')) * 1000
MAX_CONTENT_LENGTH = 0.1 * 1024 * 1024
