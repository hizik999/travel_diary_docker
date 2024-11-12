# Используем официальный образ Python для архитектуры amd64
FROM --platform=linux/amd64 python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем numpy и pandas отдельно перед остальными зависимостями
RUN pip install 'fastapi[all]' python-dotenv psycopg2-binary alembic

# Копируем файл с зависимостями
COPY app/requirements.txt .

# Устанавливаем остальные зависимости из requirements.txt
# RUN pip install -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Указываем команду для запуска FastAPI приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
