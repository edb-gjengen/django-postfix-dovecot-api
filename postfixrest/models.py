from django.db import models


#TODO: Domain, User

class Alias(models.Model):
	active = models.BooleanField(default=True)
	src = models.EmailField()
	# TODO: dst EmailListField