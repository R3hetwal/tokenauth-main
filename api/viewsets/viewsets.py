from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from api.models import Project, Document, Department
from api.serializers.serializers import ProjectSerializer, DocumentSerializer, DepartmentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

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
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        id = pk
        queryset = Project.objects.get(pk=id)
        serializer_class = ProjectSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        id = pk
        queryset = Project.objects.get(id=id)
        serializer_class = ProjectSerializer(queryset, data=request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer_class.errors)
    
    def destroy(self, request, pk):
        id = pk
        queryset = Project.objects.get(pk=id)
        queryset.delete()
        return Response({'msg':'Data Deleted'})

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]