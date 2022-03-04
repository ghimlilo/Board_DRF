import jwt
import six
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import authentication, exceptions
from .models import User


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None
        
        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header or len(auth_header) == 1 or len(auth_header) > 2:
            return None
        
        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None
        
        return self._authenticate_credentials(request, token)
    
    def _authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
        except Exception:
            return None
        
        not_valid_msg = '유효하지 않은 사용자입니다.'
        try:
            user = User.objects.get(pk=payload['id'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(not_valid_msg)

        if not user.is_active:
            raise exceptions.AuthenticationFailed(not_valid_msg)
        
        return user, token
    
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (six.text_type(user.pk) + six.text_type(timestamp)) + six.text_type(user.is_active)


account_activation_token = AccountActivationTokenGenerator()


def validate_password(password):
    if len(password) < 8:
        not_valid_msg = '유효하지 않은 비밀번호 입니다.'
        raise exceptions.AuthenticationFailed(not_valid_msg)
    return True