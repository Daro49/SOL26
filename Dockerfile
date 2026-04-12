# Dockerfile
# Author: Matej Daransky <xdaranm00@stud.fit.vutbr.cz>


# -=-=-=-=-=-=-=-=-=-=-=- INTERPRET -=-=-=-=-=-=-=-=-=-=-=- #

# ---- Runtime -------------------------------------------- #

ARG PYTHON_VERSION=3.14.3
ARG NODE_VERSION=25.2.1

FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base AS check

ADD config /config

RUN pip install -r /config/requirements.txt -r /config/requirements-dev.txt

COPY --from=node:25.2.1-slim /usr/local/bin /usr/local/bin
COPY --from=node:25.2.1-slim /usr/local/lib /usr/local/lib

RUN apt-get update && apt-get install -y --no-install-recommends \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /tester
COPY tester/package.json ./
COPY tester/package-lock.json ./
RUN npm install

WORKDIR /

ENTRYPOINT ["/bin/bash"]


FROM base AS runtime

COPY config/requirements.txt /config
RUN pip install -r /config/requirements.txt

COPY int/solint.py /int
ADD int/interpreter /int

ENTRYPOINT ["python", "/int/solint.py"]

# -=-=-=-=-=-=-=-=-=-=-=- INTERPRET -=-=-=-=-=-=-=-=-=-=-=- #

# -=-=-=-=-=-=-=-=-=-=-=-= TESTER =-=-=-=-=-=-=-=-=-=-=-=-= #

# TODO build-test

FROM base AS test

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*


COPY /config/requirements.txt /config/requirements.txt
COPY /config/requirements-sol2xml.txt /config/requirements-sol2xml.txt

RUN pip install -r /config/requirements.txt -r /config/requirements-sol2xml.txt

# -=-=-=-=-=-=-=-=-=-=-=-= TESTER =-=-=-=-=-=-=-=-=-=-=-=-= #
