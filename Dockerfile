# Base comum: dependencias de execucao e codigo da aplicacao
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /courseCatalog

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py create_db.py ./
COPY project/ project/

# Imagem de teste: docker build --target test -t course_catalog:test .
FROM base AS test

COPY requirements-dev.txt pytest.ini ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY tests/ tests/

CMD ["pytest", "tests/unit"]

# Imagem final, a que vai para o registry (alvo padrao do build)
FROM base AS runtime

ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}

RUN useradd --system --uid 1000 --no-create-home app
USER app

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--access-logfile", "-", "app:app"]
