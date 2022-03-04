from django.urls import path
from .views import RegistrationAPIView, LoginAPIView, RefreshAccessTokenAPIView, SelfInfoAPIView

urlpatterns = [
    path('/signup', RegistrationAPIView.as_view()),
    path('/signin', LoginAPIView.as_view()),
    path('/token/refresh', RefreshAccessTokenAPIView().as_view()),
    path('/self_info', SelfInfoAPIView.as_view()),
]