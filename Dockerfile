# Dockerfile
# Author: Matej Daransky <xdaranm00@stud.fit.vutbr.cz>


# -=-=-=-=-=-=-=-=-=-=-=- INTERPRET -=-=-=-=-=-=-=-=-=-=-=- #

ARG PYTHON_VERSION=3.14.3
ARG NODE_VERSION=25.2.1

FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

FROM base AS check

COPY int/requirements*.txt /tmp/

RUN pip install -r /tmp/requirements.txt -r /tmp/requirements-dev.txt

COPY --from=node:25.2.1-slim /usr/local/bin /usr/local/bin
COPY --from=node:25.2.1-slim /usr/local/lib /usr/local/lib

RUN apt-get update && apt-get install -y --no-install-recommends \
    libatomic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /src/tester
COPY tester/package.json ./
COPY tester/package-lock.json ./

RUN npm install

WORKDIR /
RUN mkdir /src/int

ENTRYPOINT ["/bin/bash"]


FROM base AS runtime

COPY int/requirements.txt /
RUN pip install -r /requirements.txt

COPY int/solint.py /int/
ADD int/interpreter/ /int/interpreter/

ENTRYPOINT ["python", "/int/solint.py"]

# -=-=-=-=-=-=-=-=-=-=-=- INTERPRET -=-=-=-=-=-=-=-=-=-=-=- #

# -=-=-=-=-=-=-=-=-=-=-=-= TESTER =-=-=-=-=-=-=-=-=-=-=-=-= #

FROM node:${NODE_VERSION}-slim AS build-test

WORKDIR /build
COPY tester/ .
RUN npm install
RUN npm run build


FROM runtime AS test

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    nodejs \
    libxml2 \
    libxslt1.1 \
    libxml2-dev \
    libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY /int/requirements.txt /int/requirements.txt
COPY /tester/sol2xml/requirements-sol2xml.txt /int/requirements-sol2xml.txt

RUN pip install -r /int/requirements.txt -r /int/requirements-sol2xml.txt

COPY --from=build-test /build/dist ./dist
COPY --from=build-test /build/node_modules ./node_modules

WORKDIR /

COPY /tester/sol2xml/sol_to_xml.py .
COPY /tester/sol2xml/parser_output_schema.xsd .

ENTRYPOINT ["node", "dist/tester.js"]

# -=-=-=-=-=-=-=-=-=-=-=-= TESTER =-=-=-=-=-=-=-=-=-=-=-=-= #
