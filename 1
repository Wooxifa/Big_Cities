import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# python search.py Москва, ул. Ак. Королева, 12
toponym_to_find = " ".join("Москва, ул. Ак. Королева, 12")

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"}


def get_map_parameters():
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    if not toponym:
        return (None, None)
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_lattitude])
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.
    span = f"{dx},{dy}"
    return ll, span


def create_flag(ll):
    return f"{ll},pm2bl"


apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
ll, spn = get_map_parameters()
map_params = {
    "ll": ll,
    "spn": spn,
    "l": "map",
    "pt": create_flag(ll),
    "apikey": apikey,

}
map_api_server = "https://static-maps.yandex.ru/v1"
response = requests.get(map_api_server, params=map_params)
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.show()
