FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -e ".[dev]"

ENV KRUTI_CONFIG=configs/kruti.yaml
CMD ["kruti", "chat"]
