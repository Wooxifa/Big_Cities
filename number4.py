import sys
import requests
from io import BytesIO
from PIL import Image
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

toponym_to_find = "Москва, ул. Ак. Королева, 12"
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "8013b162-6b42-4997-9691-77b7074026e0",
    "geocode": toponym_to_find,
    "format": "json"
}


def get_map_parameters():
    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    if not toponym:
        return (None, None)
    toponym_coordinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_latitude = toponym_coordinates.split(" ")
    ll = ",".join([toponym_longitude, toponym_latitude])
    envelope = toponym["boundedBy"]["Envelope"]
    l, b = envelope["lowerCorner"].split(" ")
    r, t = envelope["upperCorner"].split(" ")
    dx = abs(float(l) - float(r)) / 2.0
    dy = abs(float(t) - float(b)) / 2.0
    span = f"{dx},{dy}"
    return ll, span


def create_flag(ll):
    return f"{ll},pm2bl"


# Get map parameters
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
app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Map")
layout = QVBoxLayout()
im = BytesIO(response.content)
opened_image = Image.open(im)
opened_image.save("map.png")
qimage = QPixmap("map.png")
label = QLabel()
label.setPixmap(qimage)
label.setAlignment(Qt.AlignmentFlag.AlignCenter)
theme_button = QPushButton("Свет")
theme_button.setFixedSize(150, 50)
theme_button.move(0, 0)


def toggle_theme():
    if theme_button.text() == "Свет":
        window.setStyleSheet("background-color: #2E2E2E; color: white;")
        theme_button.setText("Тень")
    else:
        window.setStyleSheet("background-color: white; color: black;")
        theme_button.setText("Свет")


theme_button.clicked.connect(toggle_theme)
layout.addWidget(theme_button)
layout.addWidget(label)
window.setLayout(layout)
window.resize(qimage.width() + 100, qimage.height() + 100)
window.show()
sys.exit(app.exec())
