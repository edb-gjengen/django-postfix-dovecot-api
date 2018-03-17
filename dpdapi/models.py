from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Alias(BaseModel):
    source = models.EmailField(max_length=254)
    destination = models.EmailField(max_length=254)
    domain = models.ForeignKey('dpdapi.Domain', models.CASCADE)
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


class Domain(BaseModel):
    name = models.CharField(max_length=254, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()

        super(Domain, self).save(*args, **kwargs)


class User(BaseModel):
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=109)
    domain = models.ForeignKey('dpdapi.Domain', models.CASCADE)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.email = self.email.lower()

        super(User, self).save(*args, **kwargs)

