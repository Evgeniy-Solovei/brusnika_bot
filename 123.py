from pprint import pprint

import requests
import hashlib
import json

PUBLIC_KEY = "00e320c273dd70b276b78cd2ba5a91ae"
PRIVATE_KEY = "3c59dc048e8850243be8079a5c74d079"

# Данные запроса
data = {
    "begin_date": "2025-03-15",
    "end_date": "2025-03-17",
}


# Функция для сортировки параметров и генерации строки
def generate_data_string(params, private_key):
    sorted_keys = sorted(params.keys())
    string = "".join(f"{key}={params[key]}" for key in sorted_keys)
    return string + private_key


# Функция для создания MD5 подписи
def generate_md5(string):
    return hashlib.md5(string.encode("utf-8")).hexdigest()


# Генерируем подпись
sign = generate_md5(generate_data_string(data, PRIVATE_KEY))
data["sign"] = sign  # Добавляем в данные запроса

# Формируем URL
url = f"https://realtycalendar.ru/api/v1/bookings/{PUBLIC_KEY}/"

# Заголовки
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Отправляем запрос
response = requests.post(url, data=json.dumps(data), headers=headers)

# Выводим результат
print("Статус:", response.status_code)
print("Ответ:")
pprint(response.json())

