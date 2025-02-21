import sys
import requests
from io import BytesIO
from PIL import Image
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QComboBox
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


def update_map(map_type):
    global ll, spn, apikey
    map_params = {
        "ll": ll,
        "spn": spn,
        "l": map_type,
        "pt": create_flag(ll),
        "apikey": apikey,
    }
    try:
        response = requests.get(map_api_server, params=map_params)
        response.raise_for_status()
        im = BytesIO(response.content)
        opened_image = Image.open(im)
        opened_image.save("map.png")
        label.setPixmap(QPixmap())
        qimage = QPixmap("map.png")
        label.setPixmap(qimage)
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except IOError as e:
        print(f"Image processing error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


apikey = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
ll, spn = get_map_parameters()
map_api_server = "https://static-maps.yandex.ru/v1"

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Map")
layout = QVBoxLayout()
label = QLabel()
label.setAlignment(Qt.AlignmentFlag.AlignCenter)
theme_button = QPushButton("Свет")
theme_button.setFixedSize(150, 50)
map_type_combo = QComboBox()
map_type_combo.addItems(["map", "sat", "sat,skl", "trf"])


def toggle_theme():
    if theme_button.text() == "Свет":
        window.setStyleSheet("background-color: #2E2E2E; color: white;")
        theme_button.setText("Тень")
    else:
        window.setStyleSheet("background-color: white; color: black;")
        theme_button.setText("Свет")


def on_map_type_changed(index):
    map_type = map_type_combo.currentText()
    update_map(map_type)


theme_button.clicked.connect(toggle_theme)
map_type_combo.currentIndexChanged.connect(on_map_type_changed)

update_map("map")

layout.addWidget(theme_button)
layout.addWidget(map_type_combo)
layout.addWidget(label)
window.setLayout(layout)
window.resize(800, 600)
window.show()
sys.exit(app.exec())
