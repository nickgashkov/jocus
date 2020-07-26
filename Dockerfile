FROM python:3.8-slim

ENV PATH="${PATH}:/root/.poetry/bin" \
    POETRY_VERSION="1.1.0b2" \
    POETRY_PREVIEW="1" \
    POETRY_VIRTUALENVS_CREATE="false"

WORKDIR /app/

RUN apt-get update \
 && apt-get install -y curl \
 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python \
 && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-interaction --no-ansi --no-root

COPY . /app/
RUN poetry install --no-interaction --no-ansi

ENTRYPOINT ["/app/docker-entrypoint.sh"]
