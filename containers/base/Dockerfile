# Shared base for all Python APME services.
# Installs core dependencies once; service images inherit via FROM apme-base.
FROM python:3.12-slim

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir uv ".[gateway,proxy]"
