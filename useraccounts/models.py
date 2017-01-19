from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

class UserProfle(models.Model):
	user = models.OneToOneField(User, unique=True)
	address = models.CharField(max_length=255,blank=True,default="")
