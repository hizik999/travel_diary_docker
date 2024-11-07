# Используем официальный образ Python
FROM python:3.11

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем numpy и pandas отдельно перед остальными зависимостями
RUN pip install --no-cache-dir numpy pandas

# Копируем файл с зависимостями
COPY app/requirements.txt .

# Устанавливаем остальные зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Указываем команду для запуска FastAPI приложения
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
