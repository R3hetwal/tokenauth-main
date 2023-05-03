from api.serializers.userstatsserializers import UserStatsSerializer
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Project
from users.models import User

class UserStatsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserStatsSerializer

    def get(self, request, user_id):
        month = request.GET.get('month')
        year = request.GET.get('year')
        
        try:
            projects = Project.objects.filter(owner_id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=400)
        
        if month and year:
            try:
                start_date = datetime.strptime(f'{year}-{month}-01', '%Y-%m-%d').date()
                end_date = start_date + relativedelta(months=1) - timedelta(days=1)
            except ValueError:
                return JsonResponse({'error': 'Invalid month or year'}, status=400)
            
            projects = projects.filter(start_date__range=[start_date, end_date])
            project_count = projects.count()
    
            summary_data = [{'month': month, 'year': year, 'project_count': project_count}]
            
        elif year:
            try:
                start_date = datetime.strptime(f'{year}-01-01', '%Y-%m-%d').date()
                end_date = datetime.strptime(f'{year}-12-31', '%Y-%m-%d').date()
            except ValueError:
                return JsonResponse({'error': 'Invalid year'}, status=400)
            
            summary_data = []
            for i in range(1, 13):
                month_start_date = datetime.strptime(f'{year}-{i:02d}-01', '%Y-%m-%d').date()
                month_end_date = month_start_date + relativedelta(months=1) - timedelta(days=1)
                month_projects = projects.filter(start_date__range=[month_start_date, month_end_date])
                month_project_count = month_projects.count()
                summary_data.append({'month': str(i).zfill(2), 'year': year, 'project_count': month_project_count})
                
            year_project_count = projects.count()
            summary_data.append({'year': year, 'project_count': year_project_count})
        
        else:
            summary_data = []
            current_year = datetime.now().year
            for i in range(current_year-2, current_year+1):
                year_projects = projects.filter(start_date__year=i)
                year_project_count = year_projects.count()
                summary_data.append({'year': str(i).zfill(2), 'year': year, 'project_count': year_project_count})
                
                ''' 
                    'year': str(i).zfill(2)
                 -> This sets the value of the 'year' key to a zero-padded string representing the current year,
                   which is stored in the i variable.
                '''

        response_data = {'user_id': user_id, 'summary_data': summary_data}
        return JsonResponse(response_data)


