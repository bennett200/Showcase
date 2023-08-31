from django.contrib import admin

from .models import *

# Register your models here.
# admin.site.register(OrderItemTracker)

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('date_added',)
admin.site.register(OrderItem, OrderAdmin)
admin.site.register(Order)