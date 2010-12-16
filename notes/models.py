from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)

class Position(models.Model):
    title = models.CharField(max_length=50, unique=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.title

class Company(models.Model):
    name = models.CharField(max_length=50, unique=True)
    positions = models.ManyToManyField(Position)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Companies'

class Interview(models.Model):
    company = models.ForeignKey(Company)
    position = models.ForeignKey(Position)
    profile = models.ForeignKey(Profile, blank=True, null=True)
    description = models.CharField(max_length=2000)
    date = models.DateField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return '%s interview at %s' % (self.position.title, self.company.name)

class Question(models.Model):
    interview = models.ForeignKey(Interview)
    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000, blank=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True)

    def __unicode__(self):
        return 'Question for %s' % (self.interview)
