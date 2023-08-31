from django.db import models

from datetime import datetime
from products.models import Product
from accounts.models import User

# Create your models here.





class Order(models.Model):
    BOOL_CHOICES = ((True, 'Complete'), (False, 'Incomplete'))

    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    address = models.CharField(max_length=200, null=True)
    notes = models.TextField(max_length=300, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, null=True)
    complete = models.BooleanField(default=False, null=True, blank=True, choices=BOOL_CHOICES)
 
    def __str__(self):
        return f"{self.id}"
    
    @property
    def order_item_count(self):
        return OrderItem.objects.filter(order=self.id).count()
    
    
class OrderItem(models.Model):

    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True, related_name='order_items')
    date_added = models.DateTimeField(auto_now_add=True)
    useless = models.IntegerField(blank=True, null=True, default=0)
    id = models.AutoField(primary_key=True)
    added_to_order = models.BooleanField(default=False, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    filter_item = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
        return str(self.id)
    
    @property
    def order_item_price(self):
        var = self.quantity * self.product.price
        return var 





# class OrderItemTracker(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False, null=True, blank=True)
#     order_item = models.ForeignKey(OrderItem, on_delete=models.CASCADE, null=True, blank=True)
#     quantity = models.IntegerField(default=0, null=True, blank=True)
#     filter_item = models.IntegerField(default=0, null=True, blank=True)
#     id = models.AutoField(primary_key=True)
#     order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)

    
    
#     def __str__(self):
#         return str(self.id)

    
#     @property
#     def order_item_price(self):
#         var = self.quantity * self.order_item.product.price
#         return var 
#     @property
#     def cart_total(self):
        
#         var1 = OrderItemTracker.objects.all()[0].order_item_price
#         return f"{var1}"
    
    

        