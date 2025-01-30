FROM python:3.12-slim

# Установка базовых зависимостей
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

# Обновление системы и установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    ca-certificates \
    curl \
    telnet \
    dnsutils \
    net-tools \
    && rm -rf /var/lib/apt/lists/* \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && update-ca-certificates

# Рабочая директория
WORKDIR /brusnika_bot

# Установка зависимостей Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY . .

# Команда запуска
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 & python bot.py"]