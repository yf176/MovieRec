from django.db import models


class score(models.Model):
    username = models.CharField(max_length=30)
    movieDataId = models.CharField(max_length=255)
    score = models.FloatField()
