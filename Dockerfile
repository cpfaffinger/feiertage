FROM python:3.12-slim

ARG VERSION=1.3.0

WORKDIR /app

RUN echo "VERSION=${VERSION}"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

LABEL org.opencontainers.image.version="${VERSION}"
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers", "--forwarded-allow-ips", "*"]
