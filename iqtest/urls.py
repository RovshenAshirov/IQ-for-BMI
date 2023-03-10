from django.urls import path
from .views import index, get_index


urlpatterns = [
    path('', get_index),
]