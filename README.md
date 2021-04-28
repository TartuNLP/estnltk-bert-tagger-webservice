### Configuration

The Docker image can be built with 3 configurations that can be defined by a build argument `NAURON_MODE`. By default,
 the image contains a Gunicorn + Flask API running the Bert tagger. The `GATEWAY` configuration creates an image
 that only contains the API which posts requests to a RabbitMQ message queue server. The `WORKER` configuration
 creates a worker that picks up requests from the message queue and processes them.

The RabbitMQ server configuration can be defined with environment variables `MQ_HOST`, `MQ_PORT`, `MQ_USERNAME` and
 `MQ_PASSWORD`. The web server can be configured with the default Gunicorn parameters by using the `GUNICORN_` prefix.

Docker compose configuration to run separate a gateway and worker containers with RabbitMQ:
```
version: '3'
services:
  rabbitmq:
    image: 'rabbitmq:3.8'
    container_name: rabbitmq
    environment:
      - RABBITMQ_DEFAULT_USER=${RABBITMQ_USER}
      - RABBITMQ_DEFAULT_PASS=${RABBITMQ_PASS}
    restart: unless-stopped
  bert_tagger_gateway:
    container_name: bert_tagger_gateway
    image: bert_tagger:gateway
    build:
      context: berttaggernazgul
      args:
        - NAURON_MODE=GATEWAY
    environment:
      - MQ_HOST=rabbitmq
      - MQ_PORT=5672
      - MQ_USERNAME=${RABBITMQ_USER}
      - MQ_PASSWORD=${RABBITMQ_PASS}
      - GUNICORN_TIMEOUT=120
    ports:
      - 5000:5000
    depends_on:
      - rabbitmq
    restart: unless-stopped
  bert_tagger_worker:
    container_name: bert_tagger_worker
    image: bert_tagger:worker
    build:
      context: berttaggernazgul
      args:
        - NAURON_MODE=WORKER
    environment:
      - MQ_HOST=rabbitmq
      - MQ_PORT=5672
      - MQ_USERNAME=${RABBITMQ_USER}
      - MQ_PASSWORD=${RABBITMQ_PASS}
    volumes:
      - ./berttaggernazgul/bert_model:/bert_tagger/bert_model
    depends_on:
      - rabbitmq
    restart: unless-stopped
```