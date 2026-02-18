FROM python:3.14-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей в рабочую директорию
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь исходный код проекта в рабочую директорию
COPY . .

# Открываем порт, который будет слушать Django (по умолчанию 8000)
EXPOSE 8000

# Команда, которая выполнится при запуске контейнера
# Запускаем Django dev server. Для продакшена используйте gunicorn/uwsgi и т.д.
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]