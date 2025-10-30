# Используем легковесный Python-образ
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта
COPY custom_exporter.py ./
COPY .env ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir prometheus_client requests python-dotenv

# Для надежности — не кэшируем слои при пересборке
ARG CACHEBUST=1

# Запуск приложения
CMD ["python", "custom_exporter.py"]