from rest_framework import serializers
from core.models import Project
# from django.contrib.auth import get_user_model

# User = get_user_model()

class UserStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'

