import jwt

from django.conf import settings
from django.db import transaction

from rest_framework import status, exceptions
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from board.settings import JWT_ALGORITHM

from .serializers import RegistrationSerializer, LoginSerializer, UserGetSerializer
from .authenticate import validate_password
from .models import User, get_user
from .exceptions import TokenExpiredError


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer

    @transaction.atomic
    def post(self, request):
        new_user = {
            'email' : request.data.get('email'),
            'password' : request.data.get('password'),
            'account_name' : request.data.get('account_name'),
        }

        validate_password(new_user.get('password', ''))

        serializer = self.serializer_class(data=new_user, context={'request' : request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request):
        auth_data = {
            'email' : request.data.get('email'),
            'password' : request.data.get('password'),
        }
    
        serializer = self.serializer_class(data=auth_data, context={'request' : request})
        serializer.is_valid(raise_exception=True)

        payload = jwt.decode(serializer.data['access_token'], settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        user = get_user(payload['id'])
        user.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class RefreshAccessTokenAPIView(APIView):
    permisson_classes = (AllowAny, )

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY)
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError()
        except:
            msg = '유효하지 않은 토큰입니다.'
            raise exceptions.AuthenticationFailed(msg)
        
        user = User.objects.get(pk=payload['id'])
        user.save()

        response_data = {
            'email' : user.email,
            'access_token' : user.access_token,
            'refresh_token' : user.refresh_token,
        }

        return Response(response_data)


class SelfInfoAPIView(APIView):

    def get(self, request):
        serializer = UserGetSerializer(request.user, context={'request' : request})
        return Response(serializer.data, status=status.HTTP_200_OK)

