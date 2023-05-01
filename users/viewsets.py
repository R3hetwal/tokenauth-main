from rest_framework import viewsets
from users.models import User
from api.serializers.serializers import UserSerializer, UserLoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView, Response

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserRegistrationViewSet(viewsets.ViewSet):
    serializer_class = UserSerializer

    def create(self, request):
        """
        Create a new User instance with the provided data.
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({'status': 200, 'payload': serializer.data, 'token': token.key, 'msg': 'Your data is saved!'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data, status=status.HTTP_200_OK)
