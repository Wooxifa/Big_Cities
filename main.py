import sys
from io import BytesIO  # Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

# python search.py Москва, ул. Ак. Королева, 12
toponym_to_find = " ".join("Москва, ул. Ак. Королева, 12")

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "901c2d74-0eb9-4ba0-b49d-6ba02a4aead5",
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


apikey = "901c2d74-0eb9-4ba0-b49d-6ba02a4aead5"
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