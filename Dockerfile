FROM python:3.12-slim AS builder

WORKDIR /usr/src/app

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 - && \
    apt-get remove -y curl && \
    apt-get clean

ENV PATH="/root/.local/bin:$PATH"

FROM python:3.12-slim

WORKDIR /usr/src/app

COPY --from=builder /root/.local /root/.local

ENV PATH="/root/.local/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY . .

CMD ["sh", "-c", "while true; do sleep 60; done"]
