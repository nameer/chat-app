# Reference: https://fastapi.tiangolo.com/deployment/docker/#docker-image-with-poetry

ARG PORT 8000

FROM python:3.12 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes


FROM python:3.12

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./alembic.ini /code/
COPY ./app /code/app

ENV SQLALCHEMY_WARN_20 true

EXPOSE $PORT