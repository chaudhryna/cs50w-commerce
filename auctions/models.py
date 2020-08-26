from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY = [
        ('Toy', 'Toy'),
        ('Book', 'Book'),
        ('Jewelry', 'Jewelry'),
        ('Fashion', 'Fashion'),
        ('Electronics', 'Electronics'),
        ('Home', 'Home')
    ]
    STATUS = [
        ('Active', 'Active'),
        ('Closed', 'Closed')
    ]
    picture = models.ImageField(null=True, blank=True, upload_to='images')
    title = models.CharField(max_length=70)
    description = models.CharField(max_length=200)
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=15, null=True, choices=CATEGORY)
    status = models.CharField(max_length=10, null=True, choices=STATUS, default='Active')
    

    def __str__(self):
        return self.title