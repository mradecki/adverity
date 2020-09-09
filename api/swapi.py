import petl
import requests
from django.conf import settings

FIELDS = [
    "name",
    "height",
    "mass",
    "hair_color",
    "skin_color",
    "eye_color",
    "birth_year",
    "gender",
    "homeworld",
    "edited",
]


def consume_swapi(url, process_chunk):

    data = []

    while True:
        r = requests.get(url)
        r_json = r.json()
        url = r_json["next"]
        process_chunk(data, r_json["results"])
        if url is None:
            break

    return data


def get_people():

    def process_chunk(data, results):

        # Getting rid of all excessive data as soon as we get it
        for r in results:
            data.append(list(r.values())[:9] + [list(r.values())[-2]])

    return consume_swapi(f"{settings.SW_API_URL}/people", process_chunk)


def get_planets():
    return consume_swapi(f"{settings.SW_API_URL}/planets", lambda d, r: d.extend(r))


def fetch_dataset():

    people = [FIELDS] + get_people()
    planets = get_planets()

    homeworlds = {p["url"]: p["name"] for p in planets}

    people = petl.convert(people, "homeworld", homeworlds)
    people = petl.convert(people, "edited", lambda x: x[:10])

    return people
