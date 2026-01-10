from django.db import models
from customers.models import Customer
from menu.models import Product
from django.core.validators import MinValueValidator
from django.db.models import Sum, F
from django.core.exceptions import ValidationError

# Create your models here.
STATUS_CHOICES = [
        ('New', 'New'),
        ('Preparing', 'Preparing'),
        ('Ready', 'Ready'),
        ('Delivered', 'Delivered'),
    ]

class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.PROTECT,related_name='orders')
    order_date=models.DateTimeField(auto_now_add=True)
    total_amount=models.DecimalField(max_digits=10,decimal_places=2,default=0)
    status=models.CharField(max_length=12,choices=STATUS_CHOICES,default='New')
    notes=models.TextField(blank=True,null=True)
    class Meta:
        ordering = ['-order_date']

    
    def __str__(self):
        return f"Order #{self.id} - {self.customer.first_name} {self.customer.last_name} ({self.status})"
    
    def update_total_amount(self):
        
        total = self.items.aggregate(
            total=Sum('subtotal')
        )['total'] or 0

        self.total_amount = total
        self.save(update_fields=['total_amount'])



    def set_preparing(self):
        if self.status != 'New':
            raise ValidationError("Only new orders can be set to Preparing.")
        self.status = 'Preparing'
        self.save(update_fields=['status'])

    def set_ready(self):
        if self.status != 'Preparing':
            raise ValidationError("Only preparing orders can be set to Ready.")
        self.status = 'Ready'
        self.save(update_fields=['status'])

    def set_delivered(self):
        if self.status != 'Ready':
            raise ValidationError("Only ready orders can be set to Delivered.")
        self.status = 'Delivered'
        self.save(update_fields=['status'])


        

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.PROTECT,related_name='items')
    quantity=models.PositiveIntegerField(default=1,validators=[MinValueValidator(1)])
    price=models.DecimalField(max_digits=10,decimal_places=2)
    subtotal=models.DecimalField(max_digits=10,decimal_places=2,editable=False)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.price * self.quantity  
        super().save(*args, **kwargs)
        

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

