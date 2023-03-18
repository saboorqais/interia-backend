from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='category_images')

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='product_images')
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name
    

