FROM python:3.12-slim

ARG VERSION=1.2.1

WORKDIR /app

RUN echo "VERSION=${VERSION}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

LABEL org.opencontainers.image.version="${VERSION}"
EXPOSE 8000

ENV ROOT_PATH=""

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers --forwarded-allow-ips='*' ${ROOT_PATH:+--root-path $ROOT_PATH}"]
