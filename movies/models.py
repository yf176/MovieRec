import numpy as np
from django.db import models
from user.models import MyUser


class Movie(models.Model):
    title = models.CharField(max_length=255)
    english_title = models.CharField(max_length=255)
    director = models.CharField(max_length=255)
    writer = models.CharField(max_length=255)
    actors = models.CharField(max_length=50)
    rating = models.FloatField()
    tag1 = models.CharField(max_length=50)
    tag2 = models.CharField(max_length=50)
    tag3 = models.CharField(max_length=50)
    country = models.CharField(max_length=255)
    language = models.CharField(max_length=255)
    date = models.DateField()
    introduction = models.TextField()
    dataId = models.CharField(max_length=255,unique=True)
    url = models.CharField(max_length=255)
    pic = models.ImageField(upload_to='movie_images/', null=True, blank=True)


class UserHistory(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class UserLike(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


def similarity(u, v):
    """
    计算余弦相似度
    :param u: 用户u的评分向量
    :param v: 用户v的评分向量
    :return: 用户u和用户v的余弦相似度
    """
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))

