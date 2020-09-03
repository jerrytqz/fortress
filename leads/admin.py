from django.contrib import admin
from leads.models import User, BlacklistedJWT, Item, InventoryItem

# Register your models here.
admin.site.register(User)
admin.site.register(BlacklistedJWT)
admin.site.register(Item)
admin.site.register(InventoryItem)
