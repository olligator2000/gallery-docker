# Указываем базовый образ — легкая версия Python 3.10 на Linux
FROM python:3.10-slim

# Устанавливаем рабочую директорию внутри контейнера
# Все команды будут выполняться из папки /app
WORKDIR /app

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Копируем файл requirements.txt с хоста в контейнер
# (сначала копируем только зависимости, чтобы использовать кэширование Docker)
COPY requirements.txt .

# Устанавливаем все Python-пакеты из requirements.txt
# --no-cache-dir — не сохранять кэш, чтобы уменьшить размер образа
RUN pip install --no-cache-dir -r requirements.txt

# Копируем ВСЁ остальное (код проекта) с хоста в контейнер
# . — текущая папка на хосте (gallery-docker)
# /app — папка в контейнере, куда копируем
COPY . .

# Загружаем начальные данные (фикстуры)
RUN python manage.py loaddata fixtures/initial_data.json || true

# Загружаем миграции
RUN python manage.py migrate

# Команда, которая выполняется при запуске контейнера
# Запускаем встроенный Django-сервер на всех интерфейсах (0.0.0.0)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# ============================================================
# Добавляем Healthcheck для Django
# ============================================================
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8000/ || exit 1