from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from core.models import Project, Document, Department, ProjectSite, Path
from api.serializers.serializers import ProjectSerializer, DocumentSerializer, DepartmentSerializer, UserInfoSerializer, ProjectSiteSerializer, PathSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.gis.geos import Point
from datetime import datetime
from users.models import User
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

import os
import psycopg2
import shapefile
import zipfile
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse

# Create your views here.

# update_user_info = Signal()

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
            # update_user_info.send(sender=Document, user=request.user, action="create")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        id = pk
        document = Document.objects.get(id=id)
        serializer = DocumentSerializer(document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # update_user_info.send(sender=Document, user=request.user, action="update")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        id = pk
        document = Document.objects.get(id=id)
        document.delete()
        # update_user_info.send(sender=Document, user=request.user, action="delete")
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
            # update_user_info.send(sender=Department, user=request.user, action="create")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        department = Department.objects.get(pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            # update_user_info.send(sender=Department, user=request.user, action="update")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = Department.objects.get(pk=pk)
        department.delete()
        # update_user_info.send(sender=Department, user=request.user, action="delete")
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


class PathViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = PathSerializer
    queryset = Path.objects.all()

class ExportShapeFile(APIView):
    def get_project_sites(self):
        # Connect to the database
        conn = psycopg2.connect(
            database=settings.DATABASES['default']['NAME'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
        )
        # Create a cursor object
        cur = conn.cursor()
        # Query the database
        query = 'SELECT  project_id, site_location_id, site_area, way_id FROM core_projectsite'
        cur.execute(query)
        # Fetch all the results
        results = cur.fetchall()
        # Close the cursor and database connection
        cur.close()
        conn.close()
        # Write the results to a shapefile using pyshp
        shp_path = os.path.join(settings.BASE_DIR, 'project_sites.shp')
        w = shapefile.Writer(shp_path, shapeType=shapefile.POINT)
        w.autoBalance = 1
        w.field('project_id', 'N') 
        w.field('site_location_id', 'N')
        w.field('site_area', 'F', decimal=2)
        w.field('way_id', 'N')

        '''In this code block, the results variable contains the results of the database query. 
        The for loop iterates over each row in the results and extracts the relevant fields for 
        creating the shapefile. The try-except block tries to write a point to the shapefile and a 
        record to the attribute table for each row, using the point() and record() methods of the 
        Writer object w. If a ValueError is raised, it means that one of the fields has an invalid data 
        type, so the row is skipped. Finally, the close() method is called on the Writer object to 
        close the shapefile and return the path to the shapefile.'''

        for row in results:
            try:
                w.point(float(row[3]), float(row[2]))
                w.record(int(row[0]), int(row[1]), float(row[2]), int(row[3]))
            except ValueError:
                # skip rows with invalid data types
                pass
        w.close()
        return shp_path

    def export_project_sites(self):
        # Get the path to the shapefile
        shp_path = self.get_project_sites()
        # Compress the shapefile to a zip file
        zip_path = os.path.join(settings.BASE_DIR, 'project_sites.zip')
        with zipfile.ZipFile(zip_path, 'w') as myzip:
            myzip.write(shp_path)
            myzip.write(shp_path.replace('.shp', '.dbf'))
            myzip.write(shp_path.replace('.shp', '.shx'))
        # Remove the shapefile to avoid leaving any unnecessary files in the server file system, 
        # which could potentially take up storage space and create clutter.
        os.remove(shp_path)
        os.remove(shp_path.replace('.shp', '.dbf'))
        os.remove(shp_path.replace('.shp', '.shx'))
        # Open the zip file and read its contents
        with open(zip_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename=project_sites.zip'
            return response

    def get(self, request):
        if request.method == 'GET':
            response = self.export_project_sites()
            return response
        else:
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ProjectSiteViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    serializer_class = ProjectSiteSerializer
    queryset = ProjectSite.objects.all()

