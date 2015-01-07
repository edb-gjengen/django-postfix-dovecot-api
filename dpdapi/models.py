from __future__ import unicode_literals
from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Alias(BaseModel):
    source = models.EmailField()
    destination = models.EmailField()
    domain = models.ForeignKey('dpdapi.Domain')
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "{}={}".format(self.source, self.destination)

    class Meta:
        verbose_name_plural = 'aliases'


class Domain(BaseModel):
    name = models.CharField(max_length=1000, unique=True)

    def __unicode__(self):
        return self.name


class User(BaseModel):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=109)
    domain = models.ForeignKey('dpdapi.Domain')

    def __unicode__(self):
        return self.email

