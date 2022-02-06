import requests

GEOCODE_API_SERVER = "http://geocode-maps.yandex.ru/1.x/"
ORGANIZATION_SEARCH_API_SERVER = "https://search-maps.yandex.ru/v1/"
MAP_API_SERVER = "http://static-maps.yandex.ru/1.x/"

name = input()
response_place = requests.get(GEOCODE_API_SERVER, params={
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": name,
    "format": "json"
}).json()
coords_of_place = ",".join(response_place["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]["Point"]["pos"].split())

response_district = requests.get(GEOCODE_API_SERVER, params={
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": coords_of_place,
    "format": "json",
    "kind": "district"
}).json()
for i in response_district["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"]:
    if i["kind"] == "district":
        print(i["name"])
