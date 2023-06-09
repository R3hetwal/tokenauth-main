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
from api.viewsets.viewsets import DocumentAPIView, DepartmentAPIView, UserInfoAPIView, UserFilesView, export_shapefile
from api.viewsets.userstatsviewsets import UserStatsView
from api.viewsets.projectstats import ProjectSummaryView
from api.utility.import_utility import import_layer

app_name = 'http'  # Set the app_name for the http namespace

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/v1/', include('users.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    path("users/v1/login/", UserLoginAPIView.as_view(), name="login"),
    path('api/v1/', include('api.urls.urls')),
    path('api/v1/stats/', include('api.urls.statsurls')),
    
    path('api/v1/documents/', DocumentAPIView.as_view(), name='document-list'),
    path('api/v1/departments/', DepartmentAPIView.as_view(), name='department-list'),

    #Fetch all user info
    path('api/v1/userinfo/<str:user_name>/', UserInfoAPIView.as_view(), name='user-info'),

    #Fetch filterable data
    path('api/v1/filesuploaded/documents/', UserFilesView.as_view(), name='files-uploaded'),    

    #User Stats
    path('api/v1/user-stats/<int:user_id>/', UserStatsView.as_view(), name='user-stats'),
    
    #Project Stats
    path('api/v1/project-stats/', ProjectSummaryView.as_view(), name='project_summary'),
    path('api/v1/project-stats/<int:pk>/', ProjectSummaryView.as_view(), name='project-summary-detail'),

    path('api/v1/export-shapefile/', export_shapefile, name='export-shapefile'),
    path('api/v1/import-shapefile/', import_layer, name="import_shapefile"),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

