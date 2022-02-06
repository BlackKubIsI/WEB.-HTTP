import math
import requests

GEOCODER_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"


def lonlat_distance(a, b):
    degree_to_meters_factor = 111 * 1000
    a_lon, a_lat = a
    b_lon, b_lat = b
    radians_lattitude = math.radians((a_lat + b_lat) / 2.)
    lat_lon_factor = math.cos(radians_lattitude)
    dx = abs(a_lon - b_lon) * degree_to_meters_factor * lat_lon_factor
    dy = abs(a_lat - b_lat) * degree_to_meters_factor
    distance = math.sqrt(dx * dx + dy * dy)
    return dx, dy, distance


def get_spn_object(name):
    response = requests.get(GEOCODER_API_SERVER, params={
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"
    }).json()
    coords = list(map(lambda x: list(map(float, x.split())),
                  response["response"]["GeoObjectCollection"]["featureMember"][
                      0]["GeoObject"]["boundedBy"]["Envelope"].values()))
    spn = abs(coords[0][0] - coords[1][0]), abs(coords[0][1] - coords[1][1])
    return spn
    