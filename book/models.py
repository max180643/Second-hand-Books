from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

# instance comefrom model


def user_directory_path(instance, filename):
    now = datetime.today().strftime('%Y%m%d')
    return 'user_id_%s/%s/%s' % (instance.create_by.id, now, filename)


class Post(models.Model):
    create_by = models.ForeignKey(User, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    text_book = models.CharField(max_length=255)
    TYPE_choice = (
        ('1', 'sell'),
        ('2', 'buy')
    )
    type = models.CharField(max_length=1, choices=TYPE_choice)
    price = models.FloatField()
    picture = models.ImageField(upload_to=user_directory_path, null=True)
    STATUS_choice = (
        ('1', 'open'),
        ('2', 'closed')
    )
    status = models.CharField(
        max_length=1, choices=STATUS_choice, default='1')
