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
CMD ["flask", "--app", "backend", "run", "--debug", "--host", "0.0.0.0", "--port", "8080"]

# ==== production stage ====
FROM base AS prd

ENV BACKEND_CONFIG_PATH "config/prd.yaml"
COPY config /app/config
COPY backend /app/backend

CMD ["flask", "--app", "backend", "run", "--host", "0.0.0.0", "--port", "8080"]

