FROM python:3.12-slim

ARG GIT_SHA=local
ARG BUILD_TIME=unknown
ARG APP_VERSION=1.0.0

ENV GIT_SHA=$GIT_SHA \
    BUILD_TIME=$BUILD_TIME \
    APP_VERSION=$APP_VERSION \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd -m appuser
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]