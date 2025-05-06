FROM python:3.13-slim


ENV PATH="/root/.rye/shims:/root/.rye/bin:$PATH"

WORKDIR /test0008

COPY pyproject.toml ./
COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY ./app ./app
COPY ./alembic.ini .
COPY ./alembic ./alembic
COPY ./app/celery_worker.py ./app
COPY .env .
COPY wait-for-it.sh .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]