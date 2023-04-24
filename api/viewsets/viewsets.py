from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from api.models import Project, Document, Department
from api.serializers.serializers import ProjectSerializer, DocumentSerializer, DepartmentSerializer, UserInfoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.dispatch import Signal
from api.signals import *


# Create your views here.

update_user_info = Signal()

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
            update_user_info.send(sender=Project, user=request.user, action="create")
            return Response({'msg':'Data Created'}, status=status.HTTP_201_CREATED)
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        id = pk
        queryset = Project.objects.get(pk=id)
        serializer_class = ProjectSerializer(queryset, data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            update_user_info.send(sender=Project, user=request.user, action="update")
            return Response({'msg':'Complete Data Updated'})
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk):
        id = pk
        queryset = Project.objects.get(id=id)
        serializer_class = ProjectSerializer(queryset, data=request.data, partial=True)
        if serializer_class.is_valid():
            serializer_class.save()
            update_user_info.send(sender=Project, user=request.user, action="partial_update")
            return Response({'msg':'Partial Data Updated'})
        return Response(serializer_class.errors)
    
    def destroy(self, request, pk):
        id = pk
        queryset = Project.objects.get(pk=id)
        queryset.delete()
        update_user_info.send(sender=Project, user=request.user, action="delete")
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
            update_user_info.send(sender=Document, user=request.user, action="create")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        document = Document.objects.get(pk=pk)
        serializer = DocumentSerializer(document, data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_user_info.send(sender=Document, user=request.user, action="update")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        document = Document.objects.get(pk=pk)
        document.delete()
        update_user_info.send(sender=Document, user=request.user, action="delete")
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
            update_user_info.send(sender=Department, user=request.user, action="create")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        department = Department.objects.get(pk=pk)
        serializer = DepartmentSerializer(department, data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_user_info.send(sender=Department, user=request.user, action="update")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        department = Department.objects.get(pk=pk)
        department.delete()
        update_user_info.send(sender=Department, user=request.user, action="delete")
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserInfoAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        queryset = UserInfo.objects.all()
        serializer_class = UserInfoSerializer(queryset, many=True)
        return Response(serializer_class.data)
    
    def retrieve(self, request, pk=None):
        id = pk
        if id is not None:
            queryset = UserInfo.objects.get(pk=id)
            serializer_class = UserInfoSerializer(queryset)
            return Response(serializer_class.data)

    def get(self, request):
        queryset = UserInfo.objects.all()
        serializer = UserInfoSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_user_info.send(sender=UserInfo, user=request.user, action="create")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        userinfo = UserInfo.objects.get(pk=pk)
        serializer = UserInfoSerializer(userinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            update_user_info.send(sender=UserInfo, user=request.user, action="update")
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        userinfo = UserInfo.objects.get(pk=pk)
        userinfo.delete()
        update_user_info.send(sender=Department, user=request.user, action="delete")
        return Response(status=status.HTTP_204_NO_CONTENT)