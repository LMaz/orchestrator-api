FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

# https://github.com/pypa/pipenv/issues/4220
RUN pip install pipenv==2018.11.26
COPY ./app /app
COPY Pipfile.lock Pipfile.lock
COPY Pipfile Pipfile
RUN pipenv install --deploy --system
