from django.urls import path
from .views import trophy_list

urlpatterns = [
    path("", trophy_list, name="trophy_list"),
]
