from api.views import collection_count, collection_detail, collections
from django.urls import path

urlpatterns = [
    path('collections', collections, name='collections'),
    path('collections/<int:pk>/', collection_detail, name='collection_detail'),
    path('collections/<int:pk>/count', collection_count, name='collection_count'),
]
