import petl
from django.conf import settings
from django.db import models
from django.utils import timezone


class CollectionManager(models.Manager):
    def create(self, data, *args, **kwargs):
        kwargs["filename"] = "dataset_" + timezone.now().strftime("%Y_%m_%d_%H_%M_%S")
        collection = super().create(*args, **kwargs)
        petl.io.csv.tocsv(data, collection.filepath)
        return collection


class Collection(models.Model):
    filename = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)

    objects = CollectionManager()

    @property
    def filepath(self):
        return f"{settings.STORAGE_LOCATION}/{self.filename}"

    @property
    def data(self):
        return petl.io.csv.fromcsv(source=self.filepath)
