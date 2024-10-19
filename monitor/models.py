from django.db import models


class LoginRecord(models.Model):
    username = models.CharField(max_length=30)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} - {self.login_time}"
