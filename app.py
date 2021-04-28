import logging
from flask import request, abort
from flask_cors import CORS

from nauron import Nauron

import settings

logger = logging.getLogger("gunicorn.error")

# Define application
app = Nauron(__name__, timeout=settings.MESSAGE_TIMEOUT, mq_parameters=settings.MQ_PARAMS)
CORS(app)

bert = app.add_service(name=settings.SERVICE_NAME, remote=settings.DISTRIBUTED)

if not settings.DISTRIBUTED:
    from bert_tagger_worker import BertTaggerWorker

    bert.add_worker(BertTaggerWorker())


@app.post('/estnltk/tagger/bert')
def tagger_bert():
    if request.content_length > settings.MAX_CONTENT_LENGTH:
        abort(413)
    response = bert.process_request(content=request.json)
    return response


@app.get('/estnltk/tagger/bert/about')
def tagger_bert_about():
    return 'Tags BERT embeddings using EstNLTK 1.6.7beta webservice.'


@app.get('/estnltk/tagger/bert/status')
def tagger_bert_status():
    return 'OK'


if __name__ == '__main__':
    app.run()
