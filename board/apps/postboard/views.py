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


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        board_pk = self.kwargs.get("board_pk")
        board = get_object_or_404(Board, pk=board_pk)

        #parent id 저장

        review_author = self.request.user

        review_queryset = Review.objects.filter(board=board, review_author=review_author)
        
        if review_queryset.exists:
            raise ValidationError("You have already reviewed this content.")

        serializer.save(board=board, review_author=review_author)
        

#reviewdetail