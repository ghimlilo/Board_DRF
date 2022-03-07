from urllib import request
from rest_framework import serializers
from .models   import Board, Review


class ReviewSerializer(serializers.ModelSerializer):

    review_author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"
    
class BoardSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    #tag = serializers.SlugRelatedField(many=True, read_only=True, slug_field= "name")
    #view count
    
   

    class Meta:
        model = Board
        fields = "__all__"