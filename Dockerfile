FROM python:3.10-slim

WORKDIR /api
RUN pip install poetry
COPY pyproject.toml poetry.lock /api/
RUN poetry config virtualenvs.create false && \
    poetry config virtualenvs.in-project true && \
    poetry install
COPY . /api
CMD python manage.py runserver 0.0.0.0:8000