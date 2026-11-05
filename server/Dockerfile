FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS build

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini ./

FROM build AS test

RUN uv sync --frozen --group dev
COPY tests ./tests
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    APP_ENV=test
ENTRYPOINT []
CMD ["pytest", "-q"]

FROM python:3.12-slim-bookworm AS runtime

RUN useradd --create-home --uid 10001 --shell /usr/sbin/nologin app
WORKDIR /app
COPY --from=build --chown=app:app /app /app
COPY --chown=app:app docker-entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh
USER app
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    APP_ENV=dev
EXPOSE 8000
HEALTHCHECK --interval=5s --timeout=3s --start-period=20s --retries=20 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/api/health')"]
ENTRYPOINT ["/entrypoint.sh"]
