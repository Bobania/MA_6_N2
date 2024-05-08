FROM ubuntu:latest

# Используйте официальный образ Python как базовый
FROM python:3.8-slim

# Установите рабочую директорию в контейнере
WORKDIR /app

# Копируйте файлы проекта в контейнер
COPY . /app

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt
CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8001"]


ENTRYPOINT ["top", "-b"]