from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.create_post, name="create_post"),
    # path("success/", views.post_success, name="post_success"),
    path("batch_post/", views.batch_post_view, name="batch_post"),
    path("batch_post/success/", views.batch_post_success, name="batch_post_success"),
    path("result/", views.post_result, name="post_result"),
    path("bulk_absent/", views.bulk_absent, name="bulk_absent"),
    path("bulk_success/", views.bulk_success, name="bulk_success"),
]
