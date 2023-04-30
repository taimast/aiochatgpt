FROM ghcr.io/withlogicco/poetry:1.4.0-python-3.11-buster
WORKDIR /tmp
RUN apt update \
#    && apt install -y --no-install-recommends gcc libc6-dev \
    && apt clean -y \
    && rm -rf /var/lib/apt/* /var/log/* /var/cache/*
WORKDIR /app
COPY pyproject.toml ./
RUN poetry install --no-root
COPY aiochatgpt aiochatgpt
COPY README.md README.md
ENV PYTHONPATH=/app
# todo L1 TODO 06.04.2023 18:57 taima: Запустить poetry install до копирования файлов
