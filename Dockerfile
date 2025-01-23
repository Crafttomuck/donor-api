FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt-get update
RUN apt-get -y install curl ca-certificates apt-transport-https gcc
RUN curl -LsSO https://r.mariadb.com/downloads/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup

RUN rm mariadb_repo_setup
RUN apt-get -y install libmariadb3 libmariadb-dev

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1

ENV UV_LINK_MODE=copy

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []

CMD ["gunicorn", "--workers=4", "--log-level=info", "--bind=0.0.0.0", "main:app"]