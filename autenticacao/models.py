from django.db import models
from django.contrib.auth.models import User


class Ativacao(models.Model):
    token = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ativo = models.BooleanField(default=False)


    def __str__(self):
        return self.user.username