from django.urls import path
from .views import hello, predict
from .views import predict, hello, get_localities

urlpatterns = [
    path("hello/", hello, name="hello"),
    path("predict/", predict, name="predict"),
    path('localities/', get_localities),
]