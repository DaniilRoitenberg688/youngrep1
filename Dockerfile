# Используем базовый образ Python 3.12
FROM python:3.12-slim

# Копируем все файлы приложения в контейнер
COPY . .

# Устанавливаем зависимости из файла requirements.txt
RUN pip install gspread
RUN pip install flask

# Задаем системную переменную
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Открываем порт 5000
EXPOSE 5000

# Запускаем приложение Flask
CMD ["python3", "main.py"]