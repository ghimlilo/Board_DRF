from django.urls import URLPattern, path
from .views import (BoardListCreateAPIView, BoardDetailAPIView,
                            ReviewCreateAPIView, ReviewDetailAPIView)

urlpatterns = [
    path("/board", BoardListCreateAPIView.as_view()),
    path("/board/<int:pk>", BoardDetailAPIView.as_view()),
    path("/board/<int:board_pk>/review", ReviewCreateAPIView.as_view()),
    path("/review/<int:pk>", ReviewDetailAPIView.as_view())
]