import datetime

from django.utils.decorators import method_decorator    
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

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

import board
from .pagination  import SmallSetPagination


from board.apps.postboard.models import Board, Review
from board.apps.postboard.serializers import BoardSerializer, ReviewSerializer
from board.apps.user import serializers



class BoardListCreateAPIView(generics.ListCreateAPIView):
    queryset = Board.objects.all().order_by("-id")
    serializer_class = BoardSerializer
    filter_backends = [filters.SearchFilter]
    search_fields  = ['category__name', 'tag__name']
    permission_classes = (AllowAny,) #test
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    # def get(self, request, *args, **kwargs):
    #     board = cache.get_or_set('board', self.get_queryset(), 60*10)
    #     serializer = BoardSerializer(board, many=True)
    #     return Response(serializer.data)

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(60*60))
    def dispatch(self, request, *args, **kwargs):
        res = cache.get('board')
        if res:
            return res
        res = super().dispatch(request, *args, **kwargs)
        res.render()
        cache.set('board', res, 60)
        return res
    
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


class ReviewCreateAPIView(generics.ListCreateAPIView):
    queryset = Review.objects.all().order_by("-id")
    serializer_class = ReviewSerializer
    pagination_class = SmallSetPagination

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
    pagination_class = SmallSetPagination
    