from urllib import request
from rest_framework import serializers

import board
from .models   import Board, Review, Tag, BoardTag


class ReviewSerializer(serializers.ModelSerializer):

    review_author = serializers.StringRelatedField(read_only=True)
    reply = serializers.SerializerMethodField()
    
    def get_reply(self, instance):
        serializer = self.__class__(instance.reply, many=True)
        serializer.bind('', self)
        return serializer.data

    class Meta:
        model = Review
        fields = ('id', 'review_author', 'parent', 'content', 'reply')
        # exclude = ("board",)
        read_only_fields = ['review_author']
    


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        feilds = ["name"]  


class CreatableSlugRelatedField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        try:
            obj, created = self.get_queryset().get_or_create(**{self.slug_field: data})
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')


class BoardSerializer(serializers.ModelSerializer):
    #viewcount
    
    user = serializers.StringRelatedField(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True) 
    #related_name이 없으면 안 들어감?
    tag = CreatableSlugRelatedField(
                                        many=True,
                                        queryset=Tag.objects.all(), 
                                        slug_field="name"
                                    )
    class Meta:
        model = Board
        fields = "__all__"
    
    def create(self, validated_data):
    
        tags = validated_data.pop('tag')
        board = self.Meta.model.objects.create(**validated_data)
        
        for tag in tags:
            obj, created = Tag.objects.get_or_create(
                name=tag,
                defaults={'name':tag}
            )
            BoardTag.objects.get_or_create(tag=obj, board=board)
        
        board.save()
        return board


