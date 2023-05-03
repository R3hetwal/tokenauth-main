# from users.models import User
from api.serializers.projectstatserializers import ProjectStatsSerializer
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Project
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


class ProjectSummaryView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectStatsSerializer

    def get(self, request, *args, **kwargs):
        id = self.kwargs.get('pk')  # get project id from URL parameter
        
        if id:  # retrieve single project
            '''Allows access only if user is owner of particular project'''
            project = get_object_or_404(Project, pk=id, owner=request.user)

            '''Allows details access to any user for any particular project'''
            # project = get_object_or_404(Project, pk=id)
            summary = {
                'name': project.project_name,
                'members': [member.user_name for member in project.project_members.all()],
                'complete': project.complete,
                'days_since_start': project.days_since_start,
            }
        else:  # retrieve all projects
            projects = Project.objects.filter(owner=request.user)
            
            '''Allow any user to access entire stat'''
            # projects = Project.objects.all()
        
            department = request.GET.get('department')
            if department:
                projects = projects.filter(project_members__profile__department=department)
            
            deadline = request.GET.get('deadline')
            if deadline:
                projects = projects.filter(deadline=deadline)
            
            member = request.GET.get('project_members')
            if member:
                projects = projects.filter(project_members=member)
            
            summary = {
                'total_projects': projects.count(),
                'completed_projects': projects.filter(complete=True).count(),
                'incomplete_projects': projects.filter(complete=False).count(),
                'days_since_start': sum(project.days_since_start for project in projects if project.days_since_start is not None),
                'projects': [{'name': project.project_name, 'members': [member.user_name for member in project.project_members.all()]} for project in projects]
            }
        
        return JsonResponse(summary)

