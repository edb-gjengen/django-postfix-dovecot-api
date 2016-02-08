from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Alias(BaseModel):
    source = models.EmailField(max_length=254)
    destination = models.EmailField(max_length=254)
    domain = models.ForeignKey('dpdapi.Domain')
    active = models.BooleanField(default=True)

    def __str__(self):
        return "{}={}".format(self.source, self.destination)

    def save(self, *args, **kwargs):
        self.source = self.source.lower()
        self.destination = self.destination.lower()

        super(Alias, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'aliases'
        unique_together = ('source', 'destination', 'domain')


@python_2_unicode_compatible
class Domain(BaseModel):
    name = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()

        super(Domain, self).save(*args, **kwargs)


@python_2_unicode_compatible
class User(BaseModel):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=109)
    domain = models.ForeignKey('dpdapi.Domain')

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)

