import petl
from api.models import Collection
from api.swapi import FIELDS, fetch_dataset
from django.conf import settings
from django.shortcuts import render
from requests.exceptions import RequestException


def collections(request):

    if request.method == "POST":

        # With actually large amount of data
        # I would definitely put it into message
        # queue and make this endpoint async
        try:
            people = fetch_dataset()
        except RequestException:
            # Would be good to show some flash message
            # at least but I didn't have enough time for that.
            pass
        else:
            Collection.objects.create(data=people)

    return render(request, "api/collections.html", {"table": Collection.objects.all()})


def collection_detail(request, pk):

    if "limit" not in request.session:
        request.session["limit"] = settings.PAGE_SIZE

    if request.method == "POST" and "load_more" in request.POST:
        request.session["limit"] += settings.PAGE_SIZE

    collection = Collection.objects.get(pk=pk)
    table = list(collection.data[: request.session["limit"]])

    return render(
        request,
        "api/collection_detail.html",
        {
            "header": table[0],
            "table": table[1:],
            "collection_id": collection.id,
            "show_load_more": True,
        },
    )


def collection_count(request, pk):

    collection = Collection.objects.get(pk=pk)
    table = collection.data

    if request.method == "GET":
        fields = []
        button_states = {}
        header, table = table[0], table[1:]
    else:
        fields = [f for f in FIELDS if f in request.POST]

        if fields:
            table = petl.cut(table, *fields)
            header, counts = list(table[0]) + ["Count"], petl.valuecounter(table, *fields)
            table = []
            for k, v in counts.items():
                if isinstance(k, str):
                    table.append([k] + [v])
                else:
                    table.append(list(k) + [v])
        else:
            header, table = table[0], table[1:]

        button_states = {f"{f}_checked": True for f in FIELDS if f in request.POST}

    return render(
        request,
        "api/collection_detail.html",
        {
            "header": header,
            "table": table,
            "collection_id": collection.id,
            "show_load_more": False,
            **button_states,
        },
    )
