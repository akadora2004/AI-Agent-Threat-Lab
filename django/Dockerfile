FROM python:3.12-slim AS builder

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY --from=builder /install /usr/local

RUN useradd -m django-user && chown -R django-user:django-user /code
USER django-user

CMD ["uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]