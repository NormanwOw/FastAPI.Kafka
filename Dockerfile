FROM ghcr.io/astral-sh/uv:python3.13-bookworm

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv venv && uv sync --frozen --no-cache

COPY . .

COPY init-topic.sh /docker-entrypoint-init.d/init-topic.sh
RUN chmod +x /docker-entrypoint-init.d/init-topic.sh

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/usr/local/lib/python3.13"