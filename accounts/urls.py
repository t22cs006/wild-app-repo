from django.urls import path
from .views import check_trophies_api

urlpatterns = [
    path('api/check_trophies/', check_trophies_api, name='check_trophies_api'),
]
