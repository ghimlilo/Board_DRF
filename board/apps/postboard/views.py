from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import generics 
from rest_framework import permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response


from board.apps.postboard.models import Board, Review, Category, Tag
from board.apps.postboard.serializers import BoardSerializer, ReviewSerializer
from board.apps.user import serializers
#pagination


class BoardListCreateAPIView(generics.ListCreateAPIView):
    queryset = Board.objects.all().order_by("-id")
    serializer_class = BoardSerializer
    filter_backends = [filters.SearchFilter]
    search_fields  = ['category__name', 'tag__name']
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    
class BoardDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
