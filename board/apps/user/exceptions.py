from rest_framework import status
from rest_framework.exceptions import APIException


class TokenExpiredError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Token expired'
    default_code = 'token_expired'


class TokenValidError(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = 'Not Authenticated'
    default_code = 'not_authenticated'


class SignupDeniedError(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Denied signup'
    default_code = 'denied_signup'


class AlreadySignedEmail(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Already signed email'
    default_code = 'already_signed_email'


class InvalidPasswordError(APIException):
    status_code = status.HTTP_406_NOT_ACCEPTABLE
    default_detail = 'Invalid Password'
    default_code = 'invalid_password'