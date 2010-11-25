from django.db import models

class Profile(models.Model):
    email = models.EmailField(max_length=100)

class Position(models.Model):
    title = models.CharField(max_length=100)

class Company(models.Model):
    name = models.CharField(max_length=100)
    positions = models.ManyToManyField(Position)
    class Meta:
        verbose_name_plural = 'Companies'

class Interview(models.Model):
    profile = models.ForeignKey(Profile)
    company = models.ForeignKey(Company)
    position = models.ForeignKey(Position)
    description = models.CharField(max_length=2000)
    date = models.DateField()

class Question(models.Model):
    interview = models.ForeignKey(Interview)
    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000)
