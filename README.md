# Webservice for EstNLTK's BERT tagger webservice

The service is based on FastAPI and uses the [tartuNLP/EstBERT](https://huggingface.co/tartuNLP/EstBERT) to return text embeddings. The model is downloaded automatically upon startup.

The API uses the following endpoints:

- `POST /estnltk/tagger/bert` - the main endpoint for obtaining BERT embeddings
- `GET /estnltk/tagger/bert/about` - returns information about the webservice
- `GET /estnltk/tagger/bert/status` - returns the status of the webservice

## Configuration

The service should be run as a Docker container using the included `Dockerfile`. The API is exposed on port `8000`. The following environment variables can be used to change webservice behavior:

- `BERT_MODEL` - the BERT model used, the value should be a valid HuggingFace model ID (`tartuNLP/EstBERT` by default).
- `MAX_CONTENT_LENGHT` - maximum lenght of the POST request body size in characters.

The container uses uvicorn as the ASGI server. The entrypoint of the container is `["uvicorn", "app:app", "--host", "0.0.0.0", "--proxy-headers"]`. Any additional  [uvicorn parameters](https://uvicorn.dev/deployment/) can be passed to the container at runtime as CMD arguments.
