FROM mundialis/esa-snap:ubuntu-69f07ca as snap

FROM jupyter/scipy-notebook
USER root

# Set of all dependencies needed for pyenv to work on Ubuntu systems
RUN apt-get update
RUN apt-get install -y --no-install-recommends make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget ca-certificates curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev mecab-ipadic-utf8 git

USER $NB_UID

RUN python3 -m pip install --upgrade pip
RUN pip install poetry

# Set-up necessary ENVs for pyenv
ENV PYTHON_VERSION 3.6.15
ENV HOME /home/jovyan
ENV PYENV_ROOT /home/jovyan/.pyenv
ENV PATH $PYENV_ROOT/shims:$PYENV_ROOT/bin::$PATH
# ENV PATH /opt/conda/bin/poetry:$PATH


# Install pyenv
RUN set -ex \
    && curl https://pyenv.run | bash \
    && pyenv update \
    && pyenv install $PYTHON_VERSION \
    && pyenv global $PYTHON_VERSION \
    && pyenv rehash


# RUN pip install -U pip setuptools
# RUN pip install poetry

WORKDIR $HOME/envs
RUN python3 -m venv py36
RUN . py36/bin/activate
RUN pip install --upgrade pip && pip install ipykernel
RUN python3 -m ipykernel install --user --name=SNAP9


# RUN poetry config virtualenvs.create true
# RUN poetry config virtualenvs.prefer-active-python true
# COPY pyproject.toml poetry.lock README.md ./
# RUN poetry install

COPY --from=snap /usr/local/snap /usr/local/snap
ENV PATH="/usr/local/snap/bin:${PATH}"

# Configure the SNAP python module
RUN (timeout 20s snappy-conf $HOME/.pyenv/versions/$PYTHON_VERSION/bin/python3 $HOME/.pyenv/versions/$PYTHON_VERSION/lib/python3.6/site-packages; exit 0)







