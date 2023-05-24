from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    question = models.CharField(max_length=255)
    answer1 = models.CharField(max_length=255)
    answer2 = models.CharField(max_length=255)
    answer3 = models.CharField(max_length=255)
    answer4 = models.CharField(max_length=255)
    answer5 = models.CharField(max_length=255)
    correct = models.CharField(max_length=255)

    def __str__(self):
        return self.question


class Ability(models.Model):
    iq = models.IntegerField()
    ability = models.TextField()


class Result(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    result = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def percent(self) -> int:
        correct = (self.result - 68) / 2;
        return int(correct / 30 * 100)
