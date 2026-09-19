ARG CYBERGUARD_EXECUTOR_BASE=ghcr.io/elsechord/cyberguard-executor:sha-3b34e4c
FROM ${CYBERGUARD_EXECUTOR_BASE}

COPY --chown=10002:10002 adapter/finance_adapter.py /app/finance_adapter.py

CMD ["python", "-m", "uvicorn", "finance_adapter:app", "--host", "0.0.0.0", "--port", "8080"]
