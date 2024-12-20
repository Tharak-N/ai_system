
FROM python:3.12.6-slim-bookworm

WORKDIR /app

RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install poetry

# RUN curl -sSL https://install.python.poetry.org | python3 -

# ENV PATH="/root/.local/bin:${PATH}"

# RUN echo $PATH && poetry --version

RUN poetry --version

COPY pyproject.toml poetry.lock .

RUN poetry install 

COPY . .

EXPOSE 8000

CMD ["poetry", "run", "fastapi", "dev", "app/main.py", "--host", "0.0.0.0"]