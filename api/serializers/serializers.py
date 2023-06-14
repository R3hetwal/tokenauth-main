from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User, Address
from core.models import Project, Document, Department, ProjectSite, ProjectSiteAddress, AdditionalDoc
from rest_framework.authtoken.models import Token
import re 
from rest_framework import status
from rest_framework.views import Response
from django.contrib.gis.geos import Point, LineString, GEOSGeometry

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

class AdditionalDocSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalDoc
        fields = ['file']

class DocumentSerializer(serializers.ModelSerializer):
    '''
    In the DocumentSerializer, update the additional_docs field to use AdditionalDocSerializer
    (source='additionaldoc_set', many=True, read_only=True). This setup assumes that the reverse 
    relationship from Document to AdditionalDoc is named additionaldoc_set (the default name when
    using a ForeignKey relationship).
    '''
    additional_docs = AdditionalDocSerializer(source='additionaldoc_set', many=True, read_only=True)

    class Meta:
        model = Document
        #Both method work
        # fields = '__all__'
        fields = ['id', 'document_name', 'document_owner', 'project_name', 'department_name', 'created_at', 'identifier', 'content', 'additional_docs']


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
    distance_to_home = serializers.SerializerMethodField()
    distance_in_meters = serializers.SerializerMethodField()
    class Meta:
        model = Address
        fields = ('home_address', 'location', 'distance_to_home', 'distance_in_meters',)
    
        
    def get_distance_to_home(self, obj):
        user = obj.user
        project = user.project
        user_coords = obj.location.coords
        project_loc = project.projectsites.filter(geom_type='point').first()
        project_coords = project_loc.geom.coords
        line = LineString(user_coords, project_coords)
        distance = line.length
        return distance

    def get_distance_in_meters(self, obj):
        
        # Convert PointField from SRID=4326(Globe, Flat Surface) to SRID=3857(Map, Plane Surface)
        """ transforms the coordinates of the start and end points from SRS 4326 (WGS84, a spherical 
        coordinate system) to SRS 3857 (Web Mercator, a projected coordinate system).

        'clone=True' argument is used to create a copy of the original object to avoid modifying it directly. 
        The new point object returned by the transform() method will have the same x and y coordinates as the 
        original point, but it will be in the new spatial reference system with ID 3857"""

        user = obj.user
        project = user.project
        start_point = obj.location.coords
        end_point = project.projectsites.filter(geom_type='point').first().geom.coords
        start_point_3857 = Point(start_point, srid=4326).transform(3857, clone=True)
        end_point_3857 = Point(end_point, srid=4326).transform(3857, clone=True) 
        line = LineString(start_point_3857, end_point_3857)
        distance_3857 = line.length
        return distance_3857
        

class ProjectSiteSerializer(serializers.ModelSerializer):
    project = serializers.SerializerMethodField()
    class Meta:
        model = ProjectSiteAddress
        fields = ('geom', 'project',)

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




# class PathSerializer(serializers.ModelSerializer):
#     home = AddressSerializer()
#     length = serializers.SerializerMethodField()
#     site_loc = PointSerializer()
#     converted_data = serializers.SerializerMethodField()

#     class Meta:
#         model = Path
#         fields = ('home', 'site_address', 'site_loc', 'length', 'converted_data',)
    
#     def get_length(self, obj):
#         start_point = obj.home.location
#         end_point = obj.site_loc
#         line = LineString(start_point, end_point)
#         distance = line.length
#         return distance
    
#     def get_converted_data(self, obj):
        
#         # Convert PointField from SRID=4326(Globe, Flat Surface) to SRID=3857(Map, Plane Surface)
#         """ transforms the coordinates of the start and end points from SRS 4326 (WGS84, a spherical 
#         coordinate system) to SRS 3857 (Web Mercator, a projected coordinate system).

#         'clone=True' argument is used to create a copy of the original object to avoid modifying it directly. 
#         The new point object returned by the transform() method will have the same x and y coordinates as the 
#         original point, but it will be in the new spatial reference system with ID 3857"""

#         start_point = obj.home.location
#         end_point = obj.site_loc
#         start_point_3857 = start_point.transform(3857, clone=True)
#         end_point_3857 = end_point.transform(3857, clone=True) 
#         line = LineString(start_point_3857, end_point_3857)
#         distance_3857 = line.length
#         return distance_3857

    # def get_converted_data(self, obj):

    #     # Convert PointField from SRID=4326(Globe, Flat Surface) to SRID=3857(Map, Plane Surface)
    #     """ Does not convert the coordinates, but instead computes the distance between the start and 
    #     end points directly in SRS 4326.  This is an approximation that works well for small distances, 
    #     but becomes increasingly inaccurate for larger distances and closer to the poles."""

    #     start_point = obj.home.location
    #     end_point = obj.site_location
    #     line = LineString(start_point, end_point)
    #     distance_4326 = line.length
    #     ''' conversion factor on equatorial radius of the Earth in meters '''
    #     distance_3857 = distance_4326 * 111319.49079327357  
    #     return distance_3857