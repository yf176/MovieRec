import numpy as np
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import csv


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, label=''):
        if not username:
            raise ValueError('Users must have a valid username.')

        if not email:
            raise ValueError('Users must have a valid email address.')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            label=label
        )

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class MyUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True)
    label = models.CharField(max_length=255, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'

    def set_label(self, label):
        self.label = label
        return self

    def __str__(self):
        return self.username


def similarity(u, v):
    """
    计算余弦相似度
    :param u: 用户u的评分向量
    :param v: 用户v的评分向量
    :return: 用户u和用户v的余弦相似度
    """
    return np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
