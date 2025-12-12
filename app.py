import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from estnltk_core.common import load_text_class
from estnltk_core.converters import layer_to_dict, json_to_layers

from settings import settings
from bert_tagger import BertTagger

logger = logging.getLogger(__name__)

app = FastAPI(redoc_url=None)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)

Text = load_text_class()
tagger = BertTagger(bert_model=settings.bert_model)

class Request(BaseModel):
    text: str = Field(...)
    meta: dict = Field(...)
    layers: str = Field(...)
    output_layer: str = Field(None)
    parameters: dict = Field(None)


@app.post('/estnltk/tagger/bert')
def tagger_bert(body: Request):
    if len(str(body)) > settings.max_content_length:
        raise HTTPException(status_code=413, detail="Request body too large")
    try:
        logger.debug(body)
        text = Text(body.text)
        text.meta = body.meta
        layers = json_to_layers(text, json_str=body.layers)
        for layer in Text.topological_sort(layers):
            text.add_layer(layer)
        layer = tagger.make_layer(text, layers)
        if body.output_layer is not None:
            layer.name = body.output_layer
        return layer_to_dict(layer)
    
    except ValueError as e:
        # If tagger.make_layer throws a ValueError, report about a missing layer
        raise HTTPException(status_code=400, detail='Error at input processing: {}'.format(str(e)))
    except Exception:
        logger.exception('Internal error at input processing')
        raise HTTPException(status_code=500, detail='Internal error at input processing')

@app.get('/estnltk/tagger/bert/about')
def tagger_bert_about():
    return 'Tags BERT embeddings using EstNLTK 1.6.7beta webservice.'


@app.get('/estnltk/tagger/bert/status')
def tagger_bert_status():
    return 'OK'
