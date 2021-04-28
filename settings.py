import logging.config
from os import environ

from dotenv import load_dotenv

logging.config.fileConfig('config/logging.ini')

load_dotenv('config/.env')
load_dotenv('config/sample.env')

DISTRIBUTED = environ.get('NAURON_MODE') in ['GATEWAY', 'WORKER']

MQ_PARAMS = None
if DISTRIBUTED:
    import pika
    MQ_PARAMS = pika.ConnectionParameters \
        (host=environ.get('MQ_HOST'), port=environ.get('MQ_PORT'),
         credentials=pika.credentials.PlainCredentials(username=environ.get('MQ_USERNAME'),
                                                       password=environ.get('MQ_PASSWORD')))

SERVICE_NAME = environ.get('NAURON_SERVICE', 'estnltk-bert-tagger')
ROUTING_KEY = environ.get('NAURON_ROUTE', 'default')

MESSAGE_TIMEOUT = int(environ.get('GUNICORN_TIMEOUT', '30')) * 1000
MAX_CONTENT_LENGTH = 0.1 * 1024 * 1024
