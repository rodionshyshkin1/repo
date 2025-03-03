FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN pip install --no-cache-dir -r requirements.txt && \
    apt-get update && apt-get install -y netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 5000

ENTRYPOINT ["/entrypoint.sh"]
