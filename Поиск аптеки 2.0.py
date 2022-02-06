import requests
import sys
from PIL import Image
from help_module import lonlat_distance
from io import BytesIO

GEOCODE_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
ORGANIZATION_SEARCH_API_SERVER = "https://search-maps.yandex.ru/v1/"
"""{
        "apikey": "12ecf2f5-4503-40ec-bd7d-fd704013dd32",
        "text": object_adress(name),
        "lang": "ru_RU",
        "type": "biz",
        "spn": "5,5",
        "ll": name}).json()"""
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
    "ll": coords_of_place}).json()
coords_of_pharmacy = ",".join(
    list(map(str, response_pharmacy["features"][0]["geometry"]["coordinates"])))

response_map = requests.get(MAP_API_SERVER, params={
    "l": "map",
    "pt": f"{coords_of_place},pmywm1~{coords_of_pharmacy},pmywm2"})

distance_to_the_point = lonlat_distance(list(map(float, coords_of_pharmacy.split(","))),
                                        list(map(float, coords_of_place.split(","))))[-1]
neme_of_pharmacy = response_pharmacy["features"][0]["properties"]["CompanyMetaData"]["name"]
adress_of_pharmacy = response_pharmacy["features"][0]["properties"]["CompanyMetaData"]["address"]
working_hours_of_pharmacy = response_pharmacy["features"][
    0]["properties"]["CompanyMetaData"]["Hours"]["text"]
print(f"""
neme_of_pharmacy: {neme_of_pharmacy}
adress_of_pharmacy: {adress_of_pharmacy}
working_hours_of_pharmacy: {working_hours_of_pharmacy}
distance_to_the_point: {distance_to_the_point} meters
""")
Image.open(BytesIO(
    response_map.content)).show()
