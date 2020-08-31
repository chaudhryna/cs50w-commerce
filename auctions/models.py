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
    listed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listed_by')
    created = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.CharField(max_length=15, null=True, choices=CATEGORY)
    status = models.CharField(max_length=10, null=True, choices=STATUS, default='Active')
    watchlisted = models.ManyToManyField(User, default=None, blank=True, related_name='watchlisted')
    bids = models.ManyToManyField(User, default=None, blank=True, related_name='bids')
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True,related_name='winner')

    def __str__(self):
        return self.title

WATCHLIST_CHOICES= [
    ('Add', 'Add'),
    ('Remove', 'Remove')
]

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    value = models.CharField(choices=WATCHLIST_CHOICES, default='Add', max_length=10)

    def __str__(self):
        return str(self.listing)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment, self.user)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_price = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return str(self.listing)

    @property
    def num_bids(self):
        return self.all().count()