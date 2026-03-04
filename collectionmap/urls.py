# collectionmap/urls.py

from django.urls import path
from . import api_views, views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("api/my/", api_views.my_collection_api, name="my_collection_api"),
    path("", views.collectionmap_view, name="collectionmap"),
    path("mycollection/", views.mycollection_view, name="mycollection"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
