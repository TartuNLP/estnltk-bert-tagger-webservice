#
#  Based on: https://github.com/TartuNLP/bertnernazgul
#

FROM continuumio/miniconda3

# Create conda environment and configure the shell to use it
# Info: https://pythonspeed.com/articles/activate-conda-dockerfile/
COPY environment.yml .
RUN conda env create -f environment.yml -n nazgul && rm environment.yml

SHELL ["conda", "run", "-n", "nazgul", "/bin/bash", "-c"]
# TODO remove cloning
RUN git clone https://github.com/TartuNLP/nauron.git && pip install -e nauron/

RUN pip install estnltk-light

# Restore original shell and define entrypoint
SHELL ["/bin/bash", "-c"]

WORKDIR /var/log/nazgul
WORKDIR /nazgul
VOLUME /nazgul/bert_model

COPY . .

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "nazgul", \
            "python", "bert_tagger_nazgul.py"]