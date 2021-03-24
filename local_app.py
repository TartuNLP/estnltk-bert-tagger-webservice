from flask import Flask
from flask_cors import CORS

from nauron import Sauron, ServiceConf
from bert_tagger_nazgul import BertTaggerRingwraith

# Define Flask application
app = Flask(__name__)
CORS(app)

bert_conf = ServiceConf(name='bert',
                        endpoint='/api/berttagger',
                        nazguls= {'public': BertTaggerRingwraith()})

# Define API endpoints
app.add_url_rule(bert_conf.endpoint, view_func=Sauron.as_view(bert_conf.name, bert_conf))


if __name__ == '__main__':
    app.run()