from django.db import models
from board.models import TimestampedModel

from django.contrib.auth.models import User

class Board(TimestampedModel):
    title = models.CharField(max_length=140)
    content = models.CharField(max_length=60)
    viewcount = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    tag = models.ManyToManyField('tag', related_name='boards')

    class Meta:
        db_table = 'boards'

class Review(TimestampedModel):
    content = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    board = models.ForeignKey('board', on_delete=models.CASCADE)
    review_author = models.ForeignKey('user.User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'

class Category(TimestampedModel):
    name = models.CharField(max_length=100, blank=True)

    class Meta:
        db_table = 'categories'
    
class Tag(TimestampedModel):
    name = models.CharField(max_length=50, blank=True)

    class Meta:
        db_table = 'tags'
    



