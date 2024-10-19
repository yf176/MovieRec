from django.db import models


class Comment(models.Model):
    username = models.CharField(max_length=30)
    movieDataId = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.username} - {self.movieDataId}'
