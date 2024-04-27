FROM python:3.11-alpine
LABEL org.opencontainers.image.source="https://github.com/myles/arc-to-sqlite"
LABEL org.opencontainers.image.description="Save data from Arc App's daily (or monthly) export to a SQLite database."

RUN pip install poetry==1.8.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

COPY arc_to_sqlite ./arc_to_sqlite

RUN poetry install --without dev

ENTRYPOINT ["poetry", "run", "arc-to-sqlite"]
