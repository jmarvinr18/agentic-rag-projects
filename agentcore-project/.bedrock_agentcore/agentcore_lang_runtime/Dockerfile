# ---- builder ----
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder
WORKDIR /app
ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1 UV_NO_PROGRESS=1

COPY pyproject.toml uv.lock* ./
RUN uv pip install --no-cache --target /app/deps . aws-opentelemetry-distro==0.12.2
COPY . .

# ---- final ----
FROM python:3.13-slim
WORKDIR /app
ENV PYTHONUNBUFFERED=1 DOCKER_CONTAINER=1 AWS_REGION=ap-southeast-1 AWS_DEFAULT_REGION=ap-southeast-1 PYTHONPATH=/app/deps

COPY --from=builder /app/deps /app/deps
COPY --from=builder /app /app

RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore

EXPOSE 8080

CMD ["python", "-m", "01_agentcore_runtime"]