import requests
import scale
import sys
from io import BytesIO
from PIL import Image

API_KEY = {"static": "40d1649f-0493-4b70-98ba-98533de7710b",
           "geosearch": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"}

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:

toponym_to_find = " ".join(sys.argv[1:])
#toponym_to_find = input()

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": API_KEY["static"],
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coodrinates = toponym["Point"]["pos"]
# Долгота и широта:
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

delta = ','.join(str(x) for x in scale.get_scale(toponym))
print(delta)
# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": delta,
    "l": "map",
    'pt': f'{", ".join(toponym_coodrinates.split())}, pmwtm'.replace(' ', '')
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

#Если не работает код показа картинки
# with open('res.jpg', 'wb') as f:
#     # f.write(BytesIO(response.content))
#     f.write(response.content)

# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы

Image.open(BytesIO(
    response.content)).show()
