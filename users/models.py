from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN='admin','Admin'
        MANAGER='manager','Manager'
        STAFF='staff','Staff'


    role=models.CharField(max_length=10,choices=Role.choices,default=Role.STAFF)

    