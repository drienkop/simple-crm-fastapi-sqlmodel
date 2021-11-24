FROM python:3.10-buster

ENV USR nonroot
ENV HOME /home/${USR}
ENV PROJECT_DIR ${HOME}/code/

ENV PATH="${PATH}:${HOME}/.local/bin"
ENV PYTHONPATH=.

RUN useradd -m -r ${USR}

COPY --chown=nonroot:nonroot . ${PROJECT_DIR}

USER ${USR}
WORKDIR ${PROJECT_DIR}

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
