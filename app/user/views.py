from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt import views as jwt_views

from drf_spectacular.utils import extend_schema

from user.serializers import UserSerializer, JWTTokenSerializer


@extend_schema(
    tags=['User']
)
class CreateUserView(generics.CreateAPIView):
    '''user 생성'''
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


@extend_schema(
    tags=['User']
)
class UserLoginView(APIView):
    '''user login'''
    serializer_class = JWTTokenSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)
        if valid:
            return Response(status=status.HTTP_200_OK, data=serializer.data)
