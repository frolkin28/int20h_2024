FROM python:3.12.0-slim as base

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# ========= install and configure pdm
ENV PIP_VERSION=23.3.1
ENV PDM_VERSION=2.10
ENV PDM_USE_VENV=no
ENV PYTHONPATH=/work/__pypackages__/3.12/lib

RUN pip install --upgrade pip==${PIP_VERSION} && \
    pip install pdm==${PDM_VERSION} && \
    pdm config cache_dir /pdm_cache && \
    pdm config check_update false

WORKDIR /app

COPY pyproject.toml .
COPY pdm.lock .
RUN pdm install --no-lock --no-editable --prod

ENTRYPOINT ["pdm", "run"]

# ==== dev backend build (don`t need to copy source code, because of mounting)
FROM base AS dev

ENV BACKEND_CONFIG_PATH "config/app/dev.yaml"

CMD [ "python", "-m", "backend" ]
# ==== production stage ====
FROM base AS prd

ENV BACKEND_CONFIG_PATH "config/app/prd.yaml"
COPY config /app/config
COPY backend /app/backend
COPY pyproject.toml /app/pyproject.toml
COPY pdm.lock /app/pdm.lock
COPY migrations /app/migrations

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:8080", "--log-level=info", "backend.wsgi:app"]
