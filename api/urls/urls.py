from django.contrib import admin
from django.urls import path, include
from api.viewsets.viewsets import ProjectViewSet, DocumentAPIView, DepartmentAPIView, UserInfoAPIView, UserFilesView, ProjectSiteViewSet, PathViewSet, ExportShapeFile
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename="project")
router.register(r'projectsite', ProjectSiteViewSet, basename="project_site")
router.register(r'path', PathViewSet, basename="path")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('documents/', DocumentAPIView.as_view(), name='document-list'),
    path('departments/', DepartmentAPIView.as_view(), name='department-list'),

    path('userinfo/<str:user_name>/', UserInfoAPIView.as_view(), name='user-info'),

    path('filesuploaded/documents/', UserFilesView.as_view(), name='files-uploaded'),

   path('export-shapefile/', ExportShapeFile.as_view(), name='export-shapefile')

]

urlpatterns += router.urls
