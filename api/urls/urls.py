from django.contrib import admin
from django.urls import path, include
from api.viewsets.viewsets import ProjectViewSet, DepartmentViewSet, DocumentViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename="project")
router.register(r'documents', DocumentViewSet)
router.register(r'departments', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
