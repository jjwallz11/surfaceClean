# app/Dockerfile
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install system deps first
RUN apt-get update && \
    apt-get install -y make gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 2911

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "2911"]