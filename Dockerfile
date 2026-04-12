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

COPY int/requirements*.txt /int/

RUN pip install -r /int/requirements.txt -r /int/requirements-dev.txt

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

COPY int/requirements.txt /
RUN pip install -r /requirements.txt

COPY int/solint.py /int/
ADD int/interpreter/ /int/interpreter/

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


COPY /int/requirements.txt /int/requirements.txt
COPY /int/requirements-sol2xml.txt /int/requirements-sol2xml.txt

RUN pip install -r /int/requirements.txt -r /int/requirements-sol2xml.txt

# -=-=-=-=-=-=-=-=-=-=-=-= TESTER =-=-=-=-=-=-=-=-=-=-=-=-= #
