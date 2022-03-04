import jwt
from datetime import date, datetime, timedelta
from rest_framework.exceptions import NotFound
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)

from board.models import TimestampedModel
from board.settings import SECRET_KEY


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **user_data):
        user = self.model(email=self.normalize_email(email), **user_data)
        user.set_password(password)
        user.save(self._db)
        return user
    
    def create_superuser(self, email, password):
        if password is None:
            raise ValueError('Superusers must have a password.')
        
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(self._db)

        return user

        
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(db_index=True, verbose_name='email', max_length=255, unique=True)
    account_name = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    @property
    def access_token(self):
        return self._generate_access_token()

    @property
    def refresh_token(self):
        return self._generate_refresh_token()

    def __str__(self):
        return self.account_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def _generate_jwt_token(self, secure_algorithm, expired):
        token = jwt.encode({
            'id' : self.pk,
            'exp': int(expired.strftime('%s'))
        }, settings.SECRET_KEY, algorithm=secure_algorithm)
        return token
    
    def _generate_access_token(self):
        access_expired = datetime.now() + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRED)
        return self._generate_jwt_token('HS256', access_expired)

    def _generate_refresh_token(self):
        refresh_expired = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRED)
        return self._generate_jwt_token('HS256', refresh_expired)
    
    class Meta:
        db_table = 'user'
        ordering = ['-created_at']

def get_user(pk):
    try:
        return User.objects.get(pk=pk)
    except User.DoesNotExist:
        raise NotFound(f'User(id={pk}) is Not Found')



