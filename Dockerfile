FROM python:3.10-slim AS builder

#Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

FROM python:3.10-slim

WORKDIR  /app

# Copy the virtual environment from the builder
COPY --from=builder /app/.venv /app/.venv

COPY . .

# Place the virtual environment's bin at the front of the PATH
ENV PATH="/app/.venv/bin:$PATH"

CMD ["python", "main.py"]


