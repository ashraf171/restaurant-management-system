from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class Customer(models.Model):
    phone_regex = RegexValidator(
    regex=r'^\+?\d{9,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    first_name = models.CharField(max_length=60, db_index=True)
    last_name = models.CharField(max_length=60, db_index=True)
    email = models.EmailField(unique=True,db_index=True)
    phone=models.CharField(validators=[phone_regex],max_length=17,db_index=True,unique=True)

    address = models.TextField()
    registration_date=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-registration_date']
        verbose_name = "Customer"
        verbose_name_plural = "Customers"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name