from django.db import models
from board.models import TimestampedModel

from django.contrib.auth.models import User

class Board(TimestampedModel):
    title = models.CharField(max_length=140)
    content = models.CharField(max_length=60)
    viewcount = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    tag = models.ManyToManyField('Tag', through='BoardTag', related_name='boards')

    class Meta:
        db_table = 'boards'

class Review(TimestampedModel):
    content = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='reply')
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='reviews')
    review_author = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

class Category(TimestampedModel):
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'categories'
    
class Tag(TimestampedModel):
    name = models.CharField(max_length=50, blank=True, unique=True)

    class Meta:
        db_table = 'tags'
    
    def __str__(self):
        return self.name

class BoardTag(models.Model):
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE)
    board = models.ForeignKey('Board', on_delete=models.CASCADE)

    



