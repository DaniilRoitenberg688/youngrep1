FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir aiogram dotenv

COPY . .


CMD ["python", "run.py"]

