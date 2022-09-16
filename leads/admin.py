import time

from django import forms
from django.contrib.admin.helpers import ActionForm
from django.contrib import admin
from leads.models import User, BlacklistedJWT, Item, InventoryItem, MarketItem

class AddSPForm(ActionForm):
    SP = forms.IntegerField(label='SP')

class UserAdmin(admin.ModelAdmin):
    def add_sp(self, request, queryset):
        for x in range(queryset.count()):
            obj = User.objects.get(username=queryset[x].username)
            obj.sp += int(request.POST.get('SP'))
            obj.net_sp += int(request.POST.get('SP'))
            obj.save()
    
    action_form = AddSPForm
    actions = [add_sp]
    add_sp.short_description = "Add a specified amount of SP to selected users"

class ItemAdmin(admin.ModelAdmin): 
    def update_circulation(self, request, queryset): 
        for x in range(queryset.count()):
            obj = Item.objects.get(name=queryset[x].name)
            circulationNum = 0
            circulationInv = InventoryItem.objects.filter(item=obj)
            for y in range(circulationInv.count()):
                circulationNum += circulationInv[y].quantity
            circulationNum += MarketItem.objects.filter(item=obj).count()
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

admin.site.register(User, UserAdmin)
admin.site.register(BlacklistedJWT, BlacklistedJWTAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(InventoryItem, InventoryItemAdmin)
admin.site.register(MarketItem, MarketItemAdmin)
