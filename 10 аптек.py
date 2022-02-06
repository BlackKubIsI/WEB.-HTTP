import requests
import sys
from PIL import Image
from help_module import lonlat_distance
from io import BytesIO

GEOCODE_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
ORGANIZATION_SEARCH_API_SERVER = "https://search-maps.yandex.ru/v1/"
MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"

name = " ".join(sys.argv[1:])
response_place = requests.get(GEOCODE_API_SERVER, params={
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": name,
    "format": "json"
}).json()
coords_of_place = ",".join(response_place["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]["Point"]["pos"].split())

response_pharmacy = requests.get(ORGANIZATION_SEARCH_API_SERVER, params={
    "apikey": "12ecf2f5-4503-40ec-bd7d-fd704013dd32",
    "text": "аптека",
    "lang": "ru_RU",
    "type": "biz",
    "ll": coords_of_place,
    "results": 10}).json()["features"]

pt = []
d = {"круглосуточно": "gn", "некруглосуточно": "db", "n": "gr"}
for i in range(len(response_pharmacy)):
    color = ""
    try:
        working_hours_of_pharmacy = response_pharmacy[i][
            "properties"]["CompanyMetaData"]["Hours"]["text"]
        if "круглосуточно" in working_hours_of_pharmacy:
            color = d["круглосуточно"]
        else:
            color = d["некруглосуточно"]
    except Exception:
        color = d["n"]
    coords = ",".join(
        list(map(str, response_pharmacy[i]["geometry"]["coordinates"])))
    pt.append(f"{coords},pm{color}m{i + 1}")

response_map = requests.get(MAP_API_SERVER, params={
    "l": "map",
    "pt": "~".join(pt)})

Image.open(BytesIO(
    response_map.content)).show()
