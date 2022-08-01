import time

from django.contrib import admin
from leads.models import User, BlacklistedJWT, Item, InventoryItem, MarketItem

class UserAdmin(admin.ModelAdmin):
    def add_100k_sp(self, request, queryset):
        for x in range(queryset.count()):
            obj = User.objects.get(username=queryset[x].username)
            obj.sp += 100000
            obj.net_sp += 100000
            obj.save()
    
    actions = [add_100k_sp]
    add_100k_sp.short_description = "Add 100,000 SP to selected users"

class ItemAdmin(admin.ModelAdmin): 
    def update_circulation(self, request, queryset): 
        for x in range(queryset.count()):
            obj = Item.objects.get(name=queryset[x].name)
            circulationNum = 0
            circulation = InventoryItem.objects.filter(item=obj)
            for y in range(circulation.count()):
                circulationNum += circulation[y].quantity
            obj.in_circulation = circulationNum
            obj.save()

    actions = [update_circulation]
    update_circulation.short_description = "Update circulation number for selected items" 

class BlacklistedJWTAdmin(admin.ModelAdmin):
    def remove_expired(self, request, queryset): 
        list = []
        for x in range(queryset.count()):
            obj = BlacklistedJWT.objects.get(jwt=queryset[x].jwt)
            if (obj.exp_time < time.time()):
                list.append(obj)
        for y in list: 
            y.delete()

    actions = [remove_expired]
    remove_expired.short_description = "Remove expired JWTs from selected JWTs" 

class InventoryItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

class MarketItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(BlacklistedJWT, BlacklistedJWTAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(MarketItem, MarketItemAdmin)
