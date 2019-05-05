from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    def __str__(self):
        return f"Name: {self.username} | ID: {self.id}"


class Set(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name


class Word(models.Model):
    word = models.CharField(max_length=40, unique=True)
    meaning = models.TextField()
    sets = models.ManyToManyField(to=Set, related_name='words')

    def __str__(self):
        return self.word
