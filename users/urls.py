from django.contrib import admin
from django.urls import path, include
from users.viewsets import UserRegistrationViewSet
from rest_framework import routers
from users.viewsets import UserLoginAPIView


router = routers.DefaultRouter()
router.register(r"sign-up", UserRegistrationViewSet, basename="registration")


urlpatterns = [
    path('', include(router.urls)),
    path("login/", UserLoginAPIView.as_view(), name="login"),
    path('api-auth/', include('rest_framework.urls', namespace='signup'))
]
