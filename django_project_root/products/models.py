from django.db import models
from django.db.models import Count

from django.contrib import messages

# Create your models here.

class Categories(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=300, blank=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.category_name

class Product(models.Model):
    BOOL_CHOICES = ((True, 'Display'), (False, 'Keep Hidden'))
    
    product_category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, related_name='categories', blank=True)
    title = models.CharField(max_length=100)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    description = models.TextField(max_length=250)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    display_product = models.BooleanField(null=True, default=False, choices=BOOL_CHOICES)
    id_hidden = models.IntegerField(default=0, null=True, blank=True)
    
    @property
    def stock_amount(self):
        if self.stock <= 0:
            return "This item is out of stock!"
        elif self.stock <= 10:
            return f'Hurry this item is almost out of stock! Only {self.stock} left.'
        else:
            return f"{self.stock} in stock"       
    
    @property 
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
    class Meta:
        verbose_name_plural = 'Products'
        unique_together = ['title', 'product_category']
    
    def __str__(self):
        return str(self.product_category) + '-' + self.title