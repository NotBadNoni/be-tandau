FROM python:3.11

WORKDIR app/

COPY pyproject.toml poetry.lock ./

RUN apt-get update  \
    && apt update  \
    && apt upgrade -y  \
    && pip install poetry


RUN pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root


COPY . .

EXPOSE 8000


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
