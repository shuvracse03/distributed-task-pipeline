from django.db import models


# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=500)
    parent_url = models.TextField()
    description = models.TextField()
    upc = models.CharField(max_length=30)
    product_type = models.CharField(max_length=30)
    price_exclude_tax= models.FloatField()
    price_include_tax = models.FloatField()
    currency = models.CharField(max_length=3)
    tax = models.FloatField()
    stock = models.IntegerField()
    no_reviews = models.IntegerField()
    
    def __str__(self):
        return f"{self.title}"
