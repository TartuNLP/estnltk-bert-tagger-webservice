FROM continuumio/miniconda3

ARG NAURON_MODE=""
ENV NAURON_MODE=$NAURON_MODE

COPY environment* ./
RUN if [ "$NAURON_MODE" = "API" ]; then \
        conda env create -f environment_api.yml -n nauron; \
    elif [ "$NAURON_MODE" = "WORKER" ]; then \
        conda env create -f environment_worker.yml -n nauron; \
    else \
        conda env create -f environment.yml -n nauron; \
    fi; \
    rm environment*

# Create conda environment and configure the shell to use it
# Info: https://pythonspeed.com/articles/activate-conda-dockerfile/
SHELL ["conda", "run", "-n", "nauron", "/bin/bash", "-c"]
# TODO remove cloning
RUN git clone https://github.com/TartuNLP/nauron.git && pip install -e nauron/
# Restore original shell
SHELL ["/bin/bash", "-c"]

WORKDIR /bert_tagger
VOLUME /bert_tagger/bert_model

RUN if [ "$NAURON_MODE" = "WORKER" ]; then \
        echo "python bert_tagger_service.py" > run.sh; \
    else \
        echo "gunicorn --config config/gunicorn.ini.py --log-config config/logging.ini app:app" > run.sh; \
    fi

COPY . .

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "nauron", "bash", "run.sh"]