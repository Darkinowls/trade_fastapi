FROM python:3.11-alpine3.19

WORKDIR /app

COPY pyproject.toml .

RUN python -m venv .venv
RUN source .venv/bin/activate
ENV PATH="/app/.venv/bin:$PATH"

ENV pythonunbuffered 1

RUN pip install poetry
RUN poetry install


COPY src /app/src
COPY tests /app/tests
COPY migrations /app/migrations
COPY alembic.ini .
COPY Makefile .
