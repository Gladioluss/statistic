FROM python:3.11.4-alpine

EXPOSE 8000

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock ./alembic.ini /app/

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . ./

CMD poetry run alembic upgrade head && poetry run uvicorn app.main:app --host 0.0.0.0