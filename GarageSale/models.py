from django.db import models
from django.utils import timezone


class Item(models.Model):

    name = models.CharField(max_length=200)
    description = models.TextField()
    created = models.DateTimeField(default=datetime.datetime.now())
    price = models.DecimalField(max_digits=7, decimal_places=2)
    sold = models.BooleanField(default=False)
    address = models.CharField(max_length=200)
