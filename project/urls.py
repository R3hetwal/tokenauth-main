"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path, include
from django.contrib import admin
from users.urls import *
from api.urls import *
from rest_framework.authtoken import views
from users.viewsets import UserLoginAPIView
from django.conf import settings
from django.conf.urls.static import static
from api.viewsets.viewsets import DocumentAPIView, DepartmentAPIView, UserInfoAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/v1/', include('users.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path("users/v1/login/", UserLoginAPIView.as_view(), name="login"),
    path('api/v1/', include('api.urls.urls')),
    path('api/v1/documents/', DocumentAPIView.as_view(), name='document-list'),
    path('api/v1/departments/', DepartmentAPIView.as_view(), name='department-list'),
    path('api/v1/userinfo/', UserInfoAPIView.as_view(), name='user-info'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)