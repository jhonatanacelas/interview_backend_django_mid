from django.contrib import admin
from .models import Inventory, InventoryTag, InventoryType, InventoryLanguage

admin.site.register(Inventory)
admin.site.register(InventoryTag)
admin.site.register(InventoryType)
admin.site.register(InventoryLanguage)
