import logging
from typing import Dict, Any

from nauron import Response, Nazgul, MQConsumer
from marshmallow import Schema, fields, ValidationError
import pika

from estnltk import Text
from estnltk.converters import layer_to_json
from estnltk.converters import layer_to_dict
from estnltk.converters import json_to_layers

from bert_tagger import BertTagger

import settings

logger = logging.getLogger( settings.MQ_EXCHANGE )


class BertTaggerRequestSchema(Schema):
    text         = fields.Str(required=True)
    meta         = fields.Raw(required=True)
    layers       = fields.Str(required=True)
    output_layer = fields.Str(required=False)
    parameters   = fields.Raw(required=False, allow_none=True)


class BertTaggerRingwraith(Nazgul):
    def __init__(self, bert_location: str = "bert_model/"):
        self.schema = BertTaggerRequestSchema
        self.tagger = BertTagger( bert_location = bert_location )

    def process_request(self, body: Dict[str, Any], _: str = None) -> Response:
        try:
            body = self.schema().load( body )
            text = Text( body["text"] )
            text.meta = body["meta"]
            layers = json_to_layers( text, json_str=body['layers'] )
            for layer in Text.topological_sort( layers ):
                text.add_layer(layer)
            layer = self.tagger.make_layer(text, layers)
            if 'output_layer' in body.keys():
                layer.name = body['output_layer']
            # No need to do layer_to_json: Response obj will handle the conversion
            return Response( layer_to_dict(layer), mimetype="application/json" )
        except ValidationError as error:
            return Response(content=error.messages, http_status_code=400)
        except ValueError as err:
            # If tagger.make_layer throws a ValueError, report about a missing layer
            return Response(content='Error at input processing: {}'.format( str(err) ), http_status_code=400)
        except Exception as error:
            return Response(content='Internal error at input processing', http_status_code=400)


if __name__ == "__main__":
    mq_parameters = pika.ConnectionParameters(host=settings.MQ_HOST,
                                              port=settings.MQ_PORT,
                                              credentials=pika.credentials.PlainCredentials(
                                                  username=settings.MQ_USERNAME,
                                                  password=settings.MQ_PASSWORD))

    service = MQConsumer(nazgul=BertTaggerRingwraith(),
                         connection_parameters=mq_parameters,
                         exchange_name=settings.MQ_EXCHANGE,
                         queue_name=settings.MQ_QUEUE_NAME)
    service.start()
