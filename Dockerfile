
FROM python:3.12.6-slim-bookworm

WORKDIR /app

COPY pyproject.toml poetry.lock .

RUN poetry install 

COPY . .

EXPOSE 8002

CMD ["poetry", "run", "fastapi", "dev", "app/main.py"]