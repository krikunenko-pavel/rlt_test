FROM python:3.11-bookworm

WORKDIR /app

RUN pip install poetry

COPY poetry.lock /app

COPY pyproject.toml /app

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . /app

CMD python3 main.py