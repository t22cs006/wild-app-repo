from django.urls import path
from maps import api_post_heatmap
from maps import views_post_heatmap

urlpatterns = [
    # 投稿ヒートマップ 
    path("heatmap/", views_post_heatmap.heatmap_dashboard, name="heatmap_dashboard"),
    # API 
    path("api/heatmap/present/", api_post_heatmap.heatmap_present),
    path("api/heatmap/absent/", api_post_heatmap.heatmap_absent), 
    path("api/heatmap/total/", api_post_heatmap.heatmap_total), 
    path("api/heatmap/recommend/", api_post_heatmap.heatmap_recommend),
]
