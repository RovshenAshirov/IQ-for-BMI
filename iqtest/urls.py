from django.urls import path
from .views import index, get_index, test, get_question, post_question, end

urlpatterns = [
    path('', get_index),
    path('end/', end),
    path('get/', get_question),
    path('post/', post_question),
    path('game/', test),
]