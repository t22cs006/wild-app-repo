"""
URL configuration for wildlife project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from accounts.views import MyLoginView, dashboard
from django.contrib.auth.views import LogoutView
from django.conf import settings 
from django.conf.urls.static import static

# class LogoutAllowGetView(auth_views.LogoutView):
#      http_method_names = ['get', 'post']

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # ログイン・ログアウト
    path('login/', MyLoginView.as_view(template_name='login.html'), name='login'),
    
    # Django 5.0以降、LogoutViewはPOSTリクエストのみを受け付け、
    # 完了後にリダイレクトする必要があります（テンプレートを直接レンダリングしません）。
    # そのため、ログアウト完了ページを表示するためのビュー("logout_done")を定義し、
    # LogoutViewの next_page に指定します。
    path("logout/", LogoutView.as_view(next_page="logout_done"), name="logout"),
    path("logout/done/", TemplateView.as_view(template_name="logout.html"), name="logout_done"),

    # ログイン後のローディング画面
    path('loading/', TemplateView.as_view(template_name='loading.html'), name='loading'),

    # 仮のダッシュボード（ログイン必須）
    path('', dashboard, name='dashboard'),

    # Accounts API
    path('accounts/', include('accounts.urls')),

    path('posts/', include('posts.urls')),

    path('maps/', include('maps.urls')),
    path('collectionmap/', include('collectionmap.urls')),
    path('dangergrid/', include('dangergrid.urls')),
    path("trophy/", include("trophy.urls")),
    path('tutorial/',TemplateView.as_view(template_name='tutorial.html'),name='tutorial')

]

# 開発時のみ static ファイルを serve
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
