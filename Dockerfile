# Dockerfile
# Author: Matej Daransky <xdaranm00@stud.fit.vutbr.cz>


# -=-=-=-=-=-=-=-=-=-=-=- INTERPRET -=-=-=-=-=-=-=-=-=-=-=- #

# ---- Runtime -------------------------------------------- #

ARG PYTHON_VERSION=3.14.3
FROM python:${PYTHON_VERSION}-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS runtime

COPY src/int/requirements.txt .
RUN pip install -r requirements.txt
COPY src/int/src/ ./src/int/src/

# ---- Dev ------------------------------------------------ #

FROM runtime AS dev

COPY src/int/requirements-dev.txt .
COPY src/int/pyproject.toml ./src/int/
RUN pip install -r requirements-dev.txt

# -=-=-=-=-=-=-=-=-=-=-=- INTERPRET -=-=-=-=-=-=-=-=-=-=-=- #
