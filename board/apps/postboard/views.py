import datetime

from django_filters.rest_framework import DjangoFilterBackend
from django.core.cache import cache
from django.db import transaction
from pytz import timezone
from rest_framework import filters
from rest_framework import generics 
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response


from board.apps.postboard.models import Board, Review
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
    # permission_classes = (AllowAny,)

    def retrieve(self, request, pk):
        instance = get_object_or_404(self.get_queryset(), pk=pk)
        
        tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
        expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        if request.COOKIES.get('hit') is not None:
            cookies = request.COOKIES.get('hit')
            cookies_list = cookies.split('|')
            if str(pk) not in cookies_list:
                response.set_cookie('hit', cookies+f'|{pk}', expires=expires)
                with transaction.atomic():
                    instance.viewcount += 1
                    instance.save()
                    return response
        
        else:
            response.set_cookie('hit', pk, expires=expires)
            instance.viewcount += 1
            instance.save()
            return response
        
        serializer = self.get_serializer(instance)
        response = Response(serializer.data, status=status.HTTP_200_OK)

        return response


class ReviewCreateAPIView(generics.CreateAPIView):
    queryset = Review.objects.all().order_by("-id")
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        board_pk = self.kwargs.get("board_pk")
        board = get_object_or_404(Board, pk=board_pk)
    
        review_author = self.request.user

        # review_queryset = Review.objects.filter(board=board, review_author=review_author)

        # if review_queryset.exists:
        #     raise ValidationError("You have already reviewed this content.")

        serializer.save(board=board, review_author=review_author)
        

class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all().order_by("-id")
    serializer_class = ReviewSerializer
    