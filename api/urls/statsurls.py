from django.urls import path
from api.viewsets.userstatsviewsets import UserStatsView
from api.viewsets.projectstats import ProjectSummaryView

urlpatterns = [
    path('user-stats/<int:user_id>/', UserStatsView.as_view(), name='user-stats'),

    path('project-stats/', ProjectSummaryView.as_view(), name='project_summary'),
    path('project-stats/<int:pk>/', ProjectSummaryView.as_view(), name='project-summary-detail'),

]