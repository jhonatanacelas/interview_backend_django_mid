from django.contrib import admin
from .models import Order, OrderTag

admin.site.register(Order)
admin.site.register(OrderTag)
