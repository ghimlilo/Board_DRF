from urllib import request
from rest_framework import serializers
from .models   import Board, Review, Tag, BoardTag


class ReviewSerializer(serializers.ModelSerializer):

    review_author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"


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


