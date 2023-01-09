from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.CharField(max_length=120)
    image_url = models.CharField(max_length=2083)
    file = models.FileField(upload_to='product_files/', blank=True, null=True)
    url = models.URLField()


class offer(models.Model):
    code = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    discount = models.FloatField()

class new(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.CharField(max_length=255)
    brand = models.TextField(max_length=25)
    branch = models.TextField(max_length=20)
    image_url = models.CharField(max_length=2083)


    def _str_(self):
        return self.name

    def get_display_price(self):
        return "{ 0:.2f }".format(self.price / 100)