from django.contrib import admin
from django.urls import path, include
from api.viewsets.viewsets import ProjectViewSet, DocumentAPIView, DepartmentAPIView, UserInfoAPIView
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename="project")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('documents/', DocumentAPIView.as_view(), name='document-list'),
    path('departments/', DepartmentAPIView.as_view(), name='department-list'),
    path('userinfo/', UserInfoAPIView.as_view(), name='user-info'),
]

urlpatterns += router.urls
