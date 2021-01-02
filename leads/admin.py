import time

from django.contrib import admin
from leads.models import User, BlacklistedJWT, Item, InventoryItem, MarketItem

def update_circulation(modeladmin, request, queryset): 
    for x in range(queryset.count()):
        obj = Item.objects.get(name=queryset[x].name)
        circulationNum = 0
        circulation = InventoryItem.objects.filter(item=obj)
        for y in range(circulation.count()):
            circulationNum += circulation[y].quantity
        obj.in_circulation = circulationNum
        obj.save()
    update_circulation.short_description = "Update circulation number" 

def remove_expired(modeladmin, request, queryset): 
    list = []
    for x in range(queryset.count()):
        obj = BlacklistedJWT.objects.get(jwt=queryset[x].jwt)
        if (obj.exp_time < time.time()):
            list.append(obj)
    for y in list: 
        y.delete()
    remove_expired.short_description = "Remove expired JWTs" 

class ItemAdmin(admin.ModelAdmin): 
    actions = [update_circulation]

class BlacklistedJWTAdmin(admin.ModelAdmin):
    actions = [remove_expired]

class InventoryItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class MarketItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(User)
admin.site.register(BlacklistedJWT, BlacklistedJWTAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(MarketItem, MarketItemAdmin)
