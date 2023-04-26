from rest_framework import serializers
from core.models import Project

class ProjectStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

