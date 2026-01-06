from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class phonedetails(models.Model):
    CATEGORY_CHOICE=[
        # ('database value','form value')
        ('iphone','iphone'),
        ('samsung','samsung'),
        ('pixel','pixel')
]
    category=models.CharField(max_length=10,choices=CATEGORY_CHOICE)
    name=models.TextField()
    description=models.TextField()
    phone_price=models.IntegerField()
    phone_image=models.ImageField(upload_to='phone_image/')
    
    

class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    product = models.ForeignKey(
        phonedetails,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('user', 'product')
