from django.urls import path
from . import views

app_name = "dangergrid"

urlpatterns = [
    path("batch/", views.batch_danger_post, name="batch"),
    path("result/", views.batch_danger_result, name="result"),
    path("api/", views.danger_grid_api, name="api"),
]
