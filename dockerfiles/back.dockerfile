FROM python:3.12-alpine as base

RUN apk update && apk add curl
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="$POETRY_HOME/bin:$PATH"

WORKDIR /app
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi --no-root

COPY . .
RUN mv .container.env .env && mv alembic.container.ini alembic.ini

FROM base as back

EXPOSE 8000

CMD ["gunicorn", "servidor.config:app", "--workers=1", "--worker-class=uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000", "--access-logfile=-"]

FROM base as celery-worker

CMD ["celery", "-A", "servidor.celery_config.tasks:celery_app", "worker", "--loglevel=INFO"]

FROM base as celery-beat

CMD ["celery", "-A", "servidor.celery_config.tasks:celery_app", "beat", "--loglevel=INFO"]
