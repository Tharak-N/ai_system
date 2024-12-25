
FROM python:3.12.6-slim-bookworm

WORKDIR /app

RUN python3 -m pip install --upgrade pip \
  && python3 -m pip install poetry

# RUN apt-get update && apt-get install -y curl
# RUN curl -sSL https://install.python.poetry.org | python3 - && \
#   export PATH="/root/.local/bin:${PATH}" && \
#   poetry --version
# ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml poetry.lock .

RUN poetry install 

COPY . .

EXPOSE 8000 6006

COPY start.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/start.sh
CMD ["/usr/local/bin/start.sh"]
