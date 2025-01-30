FROM python:3.12

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1
ENV TZ=Europe/Moscow

# Установка зависимостей и настройка времени
RUN apt-get update && apt-get install -y \
    telnet \
    iputils-ping \
    dnsutils \
    && rm -rf /var/lib/apt/lists/* \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# Рабочая директория и копирование файлов
WORKDIR /brusnika_bot
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# Порт и команда запуска
EXPOSE 8000
CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 & python bot.py"