from django.db import models

class Store(models.Model):
    store_name = models.CharField(max_length=200)

    def __str__(self):
        return self.store_name

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    is_available = models.IntegerField(default=0)

    def __str__(self):
        return self.product_name
