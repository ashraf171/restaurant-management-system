from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Customer(models.Model):
    first_name = models.CharField(max_length=60, db_index=True)
    last_name = models.CharField(max_length=60, db_index=True)
    email = models.EmailField()
    phone=models.CharField(validators=[phone_regex],max_length=17,db_index=True)

    address = models.TextField()
    registration_date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"