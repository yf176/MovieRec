from django.db import models
from user.models import MyUser
from django.db import models


class portrait(models.Model):
    username = models.CharField(max_length=30)
    movieDataId = models.CharField(max_length=255)
    favourite_director = models.CharField(max_length=255)
    favourite_writer = models.CharField(max_length=255)
    favourite_actor = models.CharField(max_length=255)
    favourite_tag = models.CharField(max_length=255)
    favourite_period = models.CharField(max_length=255)
