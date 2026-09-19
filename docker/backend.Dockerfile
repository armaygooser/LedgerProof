FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY pyproject.toml README.md ./
COPY backend ./backend
RUN pip install --no-cache-dir .
USER 65532:65532
EXPOSE 18865
CMD ["python", "-m", "uvicorn", "ledgerproof_api.app:app", "--host", "0.0.0.0", "--port", "18865"]
