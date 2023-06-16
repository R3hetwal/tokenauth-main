from django.contrib import admin
from django.urls import path, include
from api.viewsets.viewsets import ProjectSiteAddressViewSet, ProjectViewSet, DocumentAPIView, DepartmentAPIView, UserInfoAPIView, UserFilesView, export_shapefile
from rest_framework import routers
from api.utility.import_utility import import_layer

router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename="project")
router.register(r'projectsiteaddress', ProjectSiteAddressViewSet, basename="project_site")
# router.register(r'path', PathViewSet, basename="path")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('documents/', DocumentAPIView.as_view(), name='document-list'),
    path('documents/<int:id>', DocumentAPIView.as_view(), name='document-list'),
    path('departments/', DepartmentAPIView.as_view(), name='department-list'),
    path('departments/<int:pk>', DepartmentAPIView.as_view(), name='department-list'),

    path('userinfo/<str:user_name>/', UserInfoAPIView.as_view(), name='user-info'),

    path('filesuploaded/documents/', UserFilesView.as_view(), name='files-uploaded'),

    path('export-shapefile/', export_shapefile, name='export-shapefile'),
    path('api/v1/import-shapefile/', import_layer, name="import_shapefile"),

]

urlpatterns += router.urls
