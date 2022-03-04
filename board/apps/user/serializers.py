from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'account_name', 'token']
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class LoginSerializer(serializers.ModelSerializer):

    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255, required=False, write_only = True)
    account_name = serializers.CharField(max_length=30, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'account_name', 'access_token', 'refresh_token')

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            error_msg = '이메일이 입력되지 않았습니다.'
            raise serializers.ValidationError(error_msg)
        
        if password is None:
            error_msg = '패스워드가 입력되지 않았습니다.'
            raise serializers.ValidationError(error_msg)

        user = authenticate(username=email, password=password)

        if user is None:
            error_msg = '로그인 정보가 틀립니다.'
            raise serializers.ValidationError(error_msg)
        
        if not user.is_active:
            error_msg = '비활성화 된 사용자입니다.'
            raise serializers.ValidationError(error_msg)

        return {
            'email': user.email,
            'account_name': user.account_name,
            'access_token': user.access_token.decode('utf-8'),
            'refresh_token': user.refresh_token.decode('utf-8'),
        }

class UserGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('account_name', 'email')