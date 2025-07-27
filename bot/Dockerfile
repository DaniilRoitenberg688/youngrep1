FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r aiogram dotenv

COPY . .


CMD ["python", "run.py"]

