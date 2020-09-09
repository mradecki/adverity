import os
from unittest import mock

from api.models import Collection
from django.test import TestCase, override_settings

DATASET = """name,height,mass,hair_color,skin_color,eye_color,birth_year,gender,homeworld,edited
Luke Skywalker,172,77,blond,fair,blue,19BBY,male,Tatooine,2014-12-20
C-3PO,167,75,n/a,gold,yellow,112BBY,n/a,Tatooine,2014-12-20
R2-D2,96,32,n/a,"white, blue",red,33BBY,n/a,Naboo,2014-12-20
Darth Vader,202,136,none,white,yellow,41.9BBY,male,Tatooine,2014-12-20
Leia Organa,150,49,brown,light,brown,19BBY,female,Alderaan,2014-12-20
Owen Lars,178,120,"brown, grey",light,blue,52BBY,male,Tatooine,2014-12-20
Beru Whitesun lars,165,75,brown,light,blue,47BBY,female,Tatooine,2014-12-20
R5-D4,97,32,n/a,"white, red",red,unknown,n/a,Tatooine,2014-12-20
Biggs Darklighter,183,84,black,light,brown,24BBY,male,Tatooine,2014-12-20
Obi-Wan Kenobi,182,77,"auburn, white",fair,blue-gray,57BBY,male,Stewjon,2014-12-20
Anakin Skywalker,188,84,blond,fair,blue,41.9BBY,male,Tatooine,2014-12-20
Wilhuff Tarkin,180,unknown,"auburn, grey",fair,blue,64BBY,male,Eriadu,2014-12-20
Chewbacca,228,112,brown,unknown,blue,200BBY,male,Kashyyyk,2014-12-20
Han Solo,180,80,brown,fair,brown,29BBY,male,Corellia,2014-12-20
Greedo,173,74,n/a,green,black,44BBY,male,Rodia,2014-12-20
Jabba Desilijic Tiure,175,"1,358",n/a,"green-tan, brown",orange,600BBY,hermaphrodite,Nal Hutta,2014-12-20
Wedge Antilles,170,77,brown,fair,hazel,21BBY,male,Corellia,2014-12-20
Jek Tono Porkins,180,110,brown,fair,blue,unknown,male,Bestine IV,2014-12-20
Yoda,66,17,white,green,brown,896BBY,male,unknown,2014-12-20
Palpatine,170,75,grey,pale,yellow,82BBY,male,Naboo,2014-12-20
Boba Fett,183,78.2,black,fair,brown,31.5BBY,male,Kamino,2014-12-20
IG-88,200,140,none,metal,red,15BBY,none,unknown,2014-12-20
Bossk,190,113,none,green,red,53BBY,male,Trandosha,2014-12-20
Lando Calrissian,177,79,black,dark,brown,31BBY,male,Socorro,2014-12-20
Lobot,175,79,none,light,blue,37BBY,male,Bespin,2014-12-20
Ackbar,180,83,none,brown mottle,orange,41BBY,male,Mon Cala,2014-12-20
Mon Mothma,150,unknown,auburn,fair,blue,48BBY,female,Chandrila,2014-12-20
Arvel Crynyd,unknown,unknown,brown,fair,brown,unknown,male,unknown,2014-12-20
Wicket Systri Warrick,88,20,brown,brown,brown,8BBY,male,Endor,2014-12-20
Nien Nunb,160,68,none,grey,black,unknown,male,Sullust,2014-12-20
Qui-Gon Jinn,193,89,brown,fair,blue,92BBY,male,unknown,2014-12-20
Nute Gunray,191,90,none,mottled green,red,unknown,male,Cato Neimoidia,2014-12-20
Finis Valorum,170,unknown,blond,fair,blue,91BBY,male,Coruscant,2014-12-20
Padmé Amidala,185,45,brown,light,brown,46BBY,female,Naboo,2014-12-20
Jar Jar Binks,196,66,none,orange,orange,52BBY,male,Naboo,2014-12-20
Roos Tarpals,224,82,none,grey,orange,unknown,male,Naboo,2014-12-20
Rugor Nass,206,unknown,none,green,orange,unknown,male,Naboo,2014-12-20
Ric Olié,183,unknown,brown,fair,blue,unknown,male,Naboo,2014-12-20
Watto,137,unknown,black,"blue, grey",yellow,unknown,male,Toydaria,2014-12-20
Sebulba,112,40,none,"grey, red",orange,unknown,male,Malastare,2014-12-20
Quarsh Panaka,183,unknown,black,dark,brown,62BBY,male,Naboo,2014-12-20
Shmi Skywalker,163,unknown,black,fair,brown,72BBY,female,Tatooine,2014-12-20
Darth Maul,175,80,none,red,yellow,54BBY,male,Dathomir,2014-12-20
Bib Fortuna,180,unknown,none,pale,pink,unknown,male,Ryloth,2014-12-20
"""

MOCK_PEOPLE_RESPONSE_1 = {
    "count": 82,
    "next": "swapi/people/?page=2",
    "previous": None,
    "results": [
        {
            "name": "Luke Skywalker",
            "height": "172",
            "mass": "77",
            "hair_color": "blond",
            "skin_color": "fair",
            "eye_color": "blue",
            "birth_year": "19BBY",
            "gender": "male",
            "homeworld": "swapi/planets/1/",
            "films": [
                "swapi/films/1/",
                "swapi/films/2/",
                "swapi/films/3/",
                "swapi/films/6/",
            ],
            "species": [],
            "vehicles": ["swapi/vehicles/14/", "swapi/vehicles/30/"],
            "starships": ["swapi/starships/12/", "swapi/starships/22/"],
            "created": "2014-12-09T13:50:51.644000Z",
            "edited": "2014-12-20T21:17:56.891000Z",
            "url": "swapi/people/1/",
        },
        {
            "name": "C-3PO",
            "height": "167",
            "mass": "75",
            "hair_color": "n/a",
            "skin_color": "gold",
            "eye_color": "yellow",
            "birth_year": "112BBY",
            "gender": "n/a",
            "homeworld": "swapi/planets/1/",
            "films": [
                "swapi/films/1/",
                "swapi/films/2/",
                "swapi/films/3/",
                "swapi/films/4/",
                "swapi/films/5/",
                "swapi/films/6/",
            ],
            "species": ["swapi/species/2/"],
            "vehicles": [],
            "starships": [],
            "created": "2014-12-10T15:10:51.357000Z",
            "edited": "2014-12-20T21:17:50.309000Z",
            "url": "swapi/people/2/",
        },
    ],
}
MOCK_PEOPLE_RESPONSE_2 = {
    "count": 82,
    "next": None,
    "previous": None,
    "results": [
        {
            "name": "R2-D2",
            "height": "96",
            "mass": "32",
            "hair_color": "n/a",
            "skin_color": "white, blue",
            "eye_color": "red",
            "birth_year": "33BBY",
            "gender": "n/a",
            "homeworld": "swapi/planets/8/",
            "films": [
                "swapi/films/1/",
                "swapi/films/2/",
                "swapi/films/3/",
                "swapi/films/4/",
                "swapi/films/5/",
                "swapi/films/6/",
            ],
            "species": ["swapi/species/2/"],
            "vehicles": [],
            "starships": [],
            "created": "2014-12-10T15:11:50.376000Z",
            "edited": "2014-12-20T21:17:50.311000Z",
            "url": "swapi/people/3/",
        },
        {
            "name": "Darth Vader",
            "height": "202",
            "mass": "136",
            "hair_color": "none",
            "skin_color": "white",
            "eye_color": "yellow",
            "birth_year": "41.9BBY",
            "gender": "male",
            "homeworld": "swapi/planets/1/",
            "films": [
                "swapi/films/1/",
                "swapi/films/2/",
                "swapi/films/3/",
                "swapi/films/6/",
            ],
            "species": [],
            "vehicles": [],
            "starships": ["swapi/starships/13/"],
            "created": "2014-12-10T15:18:20.704000Z",
            "edited": "2014-12-20T21:17:50.313000Z",
            "url": "swapi/people/4/",
        },
    ],
}


MOCK_PLANETS_RESPONSE_1 = {
    "count": 60,
    "next": "swapi/planets/?page=2",
    "previous": None,
    "results": [
        {
            "name": "Tatooine",
            "rotation_period": "23",
            "orbital_period": "304",
            "diameter": "10465",
            "climate": "arid",
            "gravity": "1 standard",
            "terrain": "desert",
            "surface_water": "1",
            "population": "200000",
            "residents": [
                "swapi/people/1/",
                "swapi/people/2/",
                "swapi/people/4/",
                "swapi/people/6/",
                "swapi/people/7/",
                "swapi/people/8/",
                "swapi/people/9/",
                "swapi/people/11/",
                "swapi/people/43/",
                "swapi/people/62/",
            ],
            "films": [
                "swapi/films/1/",
                "swapi/films/3/",
                "swapi/films/4/",
                "swapi/films/5/",
                "swapi/films/6/",
            ],
            "created": "2014-12-09T13:50:49.641000Z",
            "edited": "2014-12-20T20:58:18.411000Z",
            "url": "swapi/planets/1/",
        }
    ],
}
MOCK_PLANETS_RESPONSE_2 = {
    "count": 60,
    "next": None,
    "previous": None,
    "results": [
        {
            "name": "Naboo",
            "rotation_period": "26",
            "orbital_period": "312",
            "diameter": "12120",
            "climate": "temperate",
            "gravity": "1 standard",
            "terrain": "grassy hills, swamps, forests, mountains",
            "surface_water": "12",
            "population": "4500000000",
            "residents": [
                "swapi/people/3/",
                "swapi/people/21/",
                "swapi/people/35/",
                "swapi/people/36/",
                "swapi/people/37/",
                "swapi/people/38/",
                "swapi/people/39/",
                "swapi/people/42/",
                "swapi/people/60/",
                "swapi/people/61/",
                "swapi/people/66/",
            ],
            "films": [
                "swapi/films/3/",
                "swapi/films/4/",
                "swapi/films/5/",
                "swapi/films/6/",
            ],
            "created": "2014-12-10T11:52:31.066000Z",
            "edited": "2014-12-20T20:58:18.430000Z",
            "url": "swapi/planets/8/",
        }
    ],
}


@override_settings(STORAGE_LOCATION="/tmp")
class APITest(TestCase):
    @classmethod
    def setUpTestData(cls):

        data = [line.split(',') for line in DATASET.splitlines()]

        for id in range(10):
            Collection.objects.create(data=data)

            with open(f"/tmp/file_{id}", "w") as f:
                f.write(DATASET)

    def test_collection_list_view(self):
        response = self.client.get("/collections")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/collections.html")
        self.assertEqual(len(response.context["table"]), 10)

    @mock.patch("api.views.generate_filename")
    @mock.patch("api.swapi.requests")
    def test_collection_list_view_fetch(self, requests, generate_filename):

        response1 = mock.Mock()
        response1.json.return_value = MOCK_PEOPLE_RESPONSE_1
        response2 = mock.Mock()
        response2.json.return_value = MOCK_PEOPLE_RESPONSE_2
        response3 = mock.Mock()
        response3.json.return_value = MOCK_PLANETS_RESPONSE_1
        response4 = mock.Mock()
        response4.json.return_value = MOCK_PLANETS_RESPONSE_2

        requests.get.side_effect = [
            response1,
            response2,
            response3,
            response4,
        ]

        generate_filename.return_value = "file_11"

        response = self.client.post("/collections")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(os.path.exists("/tmp/file_11"))
        self.assertTrue(Collection.objects.filter(filename="file_11").exists())
        self.assertEqual(len(response.context["table"]), 11)

    def test_collection_detail_view(self):
        response = self.client.get("/collections/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/collection_detail.html")
        self.assertEqual(self.client.session["limit"], 10)
        self.assertEqual(len(response.context["table"]), 9)

    def test_collection_detail_view_load_more(self):
        self.client.get("/collections/1/")
        response = self.client.post("/collections/1/", data={"load_more": "Load More"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["table"]), 19)

    def test_collection_deatil_count_feature(self):
        response = self.client.post(
            "/collections/1/count",
            data={"birth_year": "on", "homeworld": "on", "Count": "Count"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "api/collection_detail.html")
        self.assertEqual(len(response.context["table"]), 41)
        self.assertEqual(len(response.context["table"][0]), 3)
