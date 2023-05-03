from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User, Address
from core.models import Project, Document, Department, ProjectSite
from rest_framework.authtoken.models import Token
import re 
from rest_framework import status
from rest_framework.views import Response
from django.contrib.gis.geos import Point

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'user_name', 'first_name', 'last_name', 'contact', 'address', 'password', 'confirm_password')
        extra_kwargs = {"password": {"write_only": True}, 'confirm_password': {'write_only': True}}
    
    def validate_user_name(self, value):
        """
        Check that the username is not already in use.
        """
        if User.objects.filter(user_name=value).exists():
            raise serializers.ValidationError('Username is already in use.')
        return value
    
    def validate_email(self, email):
        domain = email.split('@')[-1]
        allowed_domains = ['gmail.com', 'hotmail.com', 'yahoo.com']

        if domain not in allowed_domains:
            raise serializers.ValidationError(f'Email domain {domain} is not allowed. Please use an email from one of these domains: {", ".join(allowed_domains)}')
        return email
    
    def validate_password(self, password):
        min_length = 8
        
        if len(password) < min_length:
            raise serializers.ValidationError(
                ("This password must contain at least 8 characters."),
                    code='password_too_short'
            )
        
        elif not re.search("[a-z]", password):
            raise serializers.ValidationError('Password should contain lowercase characters')
        
        elif not re.search("[A-Z]", password):
            raise serializers.ValidationError('Password should contain uppercase characters')

        elif not re.search("[@!#$%&^*]", password):
            raise serializers.ValidationError('Password should contain special characters')
        
        elif not re.search("[0-9]", password):
            raise serializers.ValidationError('Password should contain numeric value')
        
        else:
            print('Password Validated!')
        
        return password

    def create(self, validated_data):
        password = validated_data.pop('password')
        confirm_password = validated_data.pop('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
        
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('email', 'password', 'token')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def get_token(self, user):
        token = Token.objects.get(user=user)
        # token, created = Token.objects.get_or_create(user=user)
        return token.key

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                'Please provide both email and password.')

        data = User.objects.filter(email=email, is_active=True).first()
        if not data:
            raise serializers.ValidationError('Your account is not active. Contact the admin for activation.')
        
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'Invalid login credentials. Please try again.')

        return {'token': self.get_token(user), 'msg': 'Login Success'}
    
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


#GIS Data
class PointSerializer(serializers.Field):
    def to_representation(self, value):
        if isinstance(value, Point):
            return {'latitude': value.y, 'longitude': value.x}
        return None
    
class AddressSerializer(serializers.ModelSerializer):
    location = PointSerializer()

    class Meta:
        model = Address
        fields = ('home_address', 'location')

class ProjectSiteSerializer(serializers.ModelSerializer):
    length = serializers.SerializerMethodField()
    area = serializers.SerializerMethodField()
    site_location = AddressSerializer()
    project = serializers.SerializerMethodField()

    class Meta:
        model = ProjectSite
        fields = ('site_name', 'project', 'length', 'area', 'site_location',)

    def get_length(self, obj):
        if hasattr(obj, 'way') and obj.way:
            return obj.way.length
        return 0.0

    def get_area(self, obj):
        if obj.way:
            return obj.site_area.area
        return 0.0
    
    def get_project(self, obj):
        if obj.project:
            return obj.project.project_name
        return None

#UserInfo including GIS address
class UserInfoSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    
    class Meta:
        model = User
        fields = '__all__'