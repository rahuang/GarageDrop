from django.db import models


class TestObject(models.Model):
    intField = models.IntegerField(default=2)
    charField = models.CharField(max_length=1, default='a')
    textField = models.TextField()
    
    