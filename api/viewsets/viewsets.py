import ast
from glob import glob
import tempfile
from urllib import request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from api.utility.export_utility import layer_exporter
from api.utility.utility import extract_shapefile
from core.models import Project, Document, Department, ProjectSiteAddress
from api.serializers.serializers import ProjectSerializer, DocumentSerializer, DepartmentSerializer, UserInfoSerializer, ProjectSiteSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from users.models import Address, User
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
import os
import geopandas as gpd
import psycopg2
import shapefile
import zipfile
from django.contrib.gis.geos import GEOSGeometry
from django.conf import settings
from rest_framework import status
from django.http import HttpResponse
import shutil
from rest_framework.decorators import api_view

# Create your views here.
class ProjectViewSet(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        queryset = Project.objects.all()
        serializer_class = ProjectSerializer(queryset, many=True)
        return Response(serializer_class.data)
    
    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            queryset = Project.objects.get(pk=id)
            serializer_class = ProjectSerializer(queryset)
            return Response(serializer_class.data)
        
    def create(self, request):
        serializer_class = ProjectSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            # update_user_info.send(sender=Project, user=request.user, action="create")
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        id = pk
        queryset = Project.objects.get(pk=id)
        serializer_class = ProjectSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            # update_user_info.send(sender=Project, user=request.user, action="update")
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        id = pk
        queryset = Project.objects.get(id=id)
        serializer_class = ProjectSerializer(queryset, data=request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            # update_user_info.send(sender=Project, user=request.user, action="partial_update")
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer_class.errors)
    
    def destroy(self, request, pk):
        id = pk
        queryset = Project.objects.get(pk=id)
        queryset.delete()
        # update_user_info.send(sender=Project, user=request.user, action="delete")
        return Response({'msg':'Data Deleted'})
    
class DocumentAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Document.objects.all()
        serializer = DocumentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        id = pk
        document = Document.objects.get(id=id)
        serializer = DocumentSerializer(document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        id = pk
        document = Document.objects.get(id=id)
        document.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class DepartmentAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Department.objects.all()
        serializer = DepartmentSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        department = Department.objects.get(pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = Department.objects.get(pk=pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#API to fetch UserInfo
class UserInfoAPIView(APIView):
    serializer_class = UserInfoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['user_name']
    filterset_fields = ['user_name']
    lookup_field = 'user_name'

    def get_queryset(self):
        user_name = self.kwargs.get('user_name')
        return User.objects.filter(user_name=user_name)

    def get(self, request, *args, **kwargs):
        user = self.get_queryset().first()
        if user:
            projects = Project.objects.filter(owner=user)
            departments = Department.objects.filter(members=user)
            documents = Document.objects.filter(document_owner=user)
            serializer = {
                'user': self.serializer_class(user).data,
                'projects': ProjectSerializer(projects, many=True).data,
                'departments': DepartmentSerializer(departments, many=True).data,
                'documents': DocumentSerializer(documents, many=True).data
            }
            return Response(serializer)
        else:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

#API to fetch uploaded documents
class UserFilesView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = DocumentSerializer

    def get(self, request, *args, **kwargs):
        documents = Document.objects.all()

        # filter by document_owner
        document_owner = request.query_params.get('document_owner', None)
        if document_owner is not None:
            documents = documents.filter(document_owner__id=document_owner)

        # filter by department_name
        department_name = request.query_params.get('department_name', None)
        if department_name is not None:
            documents = documents.filter(department_name__id=department_name)

        # filter by project_name
        project_name = request.query_params.get('project_name', None)
        if project_name is not None:
            documents = documents.filter(project_name__id=project_name)

        # filter by created_at date
        created_at = request.query_params.get('created_at', None)    
        if created_at is not None:
            created_at = datetime.strptime(created_at, '%Y-%m-%d').date()
            documents = documents.filter(created_at__date=created_at)

        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
    
''' Note:
The double underscore __ is used to perform a lookup across a relation. 
Specifically, the department_name__id part of the lookup refers to the id attribute of the 
department_name ForeignKey relationship. '''


# class PathViewSet(viewsets.ModelViewSet):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = (IsAuthenticated,)
#     serializer_class = PathSerializer
#     queryset = Path.objects.all()

class ProjectSiteAddressViewSet(viewsets.ModelViewSet):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSiteSerializer
    queryset = ProjectSiteAddress.objects.all()

    def create(self, request, *args, **kwargs):
        from django.contrib.gis import geos
        
        try:
            geom = geos.GEOSGeometry(request.data.get('geom'))
        except geos.GEOSException as e:
            return Response({'error': str(e)}, status=400)  
         
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            geom_type = instance.geom.geom_type.lower()
            dummy_geom = instance.geom
            area = 0.0
            if geom_type in "multipolygon" or "polygon":
                # dummy_geom.transform(srid=3857)
                area = dummy_geom.area
            instance.area = area
            if geom_type in ["multipoint", "point"]:
                instance.geom_type = "point"
            elif geom_type in ['polygon', 'multipolygon']:
                instance.geom_type = "polygon"
            else:
                return Response("Error: GEOM type not supported.")
            
            project_id = serializer.validated_data.get('project').id
            project = Project.objects.get(id=project_id)
            site = project.projectsites.filter(geom_type=geom_type).first()
            if site:
                site.delete()
            instance.save()
            return Response({**serializer.data, "geom_type": geom_type, "area": area}, status=201)
        return Response(serializer.error, status=400)
    

'''EXPORT SHAPEFILE'''

@api_view(["GET"])
def export_shapefile(request):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    
    layer_id = request.query_params.get("layer_id")
    if not layer_id:
        return Response("layer_id is required", status=400)

    export_dir = os.path.join(settings.BASE_DIR, "layer_exports", "uploads")
    file_url, status, status_msg = layer_exporter(layer_id, "shapefile", export_dir)

    if status == 404:
        return Response(status_msg, status=status)

    vector_file = open(file_url, "rb")
    response = HttpResponse(vector_file, content_type="application/force-download")
    response["Content-Disposition"] = 'attachment; filename="%s"' % os.path.basename(file_url)
    return response

# @api_view(["GET",])
# def export_shapefile(request):
#     layer_id = request.data.get("projectsiteaddress_id", None)

#     if not layer_id:
#         return Response("layer_id and output_format are required", status=400)


#     layer_instances = ProjectSiteAddress.objects.filter(id=layer_id)

#     if not layer_instances.exists():
#         return Response(f"Sorry, those layer(s) don't exist", status=404)
    
#     layer_instance = layer_instances.first()
#     # Getting the actual project the layer(s) belongs to

#     """
#     Exporting starts from here
#     """
#     root_dir = "layer_exports/"
#     export_dir = os.path.join(root_dir, "uploads")

#     # Check if directory exists from previous call, remove if it exists then create it again
#     root_dir = os.path.dirname(root_dir)
#     if os.path.exists(root_dir):
#         shutil.rmtree(root_dir)
#     os.makedirs(export_dir)

#     response_file_name = ""
#     # file_url, status, status_msg = layer_exporter(
#     #         instance, output_format, export_dir
#     #     )
    
#     response_file_name = "layers-export.zip"
#     payload_path = os.path.join(root_dir, os.path.splitext(response_file_name)[0])
#     shutil.make_archive(base_name=payload_path, format="zip", root_dir=export_dir)
#     vector_file = open(f"{payload_path}.zip", "rb")

#     response = HttpResponse(vector_file, content_type="application/force-download")
#     response["Content-Disposition"] = 'attachment; filename="%s"' % response_file_name
#     return response