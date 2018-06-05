from django.db import models


class Users(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return "Name: " + self.name + "  |  Id: " + str(self.id)


class Sets(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.DO_NOTHING)

    @property
    def user_name(self):
        return self.user.name

    def __str__(self):
        return self.name


class Words(models.Model):
    word = models.CharField(max_length=40, unique=True)
    meaning = models.TextField()


class Setsandword(models.Model):
    set = models.ForeignKey(Sets, on_delete=models.DO_NOTHING)
    word = models.ForeignKey(Words, on_delete=models.DO_NOTHING)