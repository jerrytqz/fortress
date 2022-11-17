from django.contrib import admin

import time

from django import forms
from django.contrib.admin.helpers import ActionForm
from django.contrib import admin
from spin.models import User, BlacklistedJWT, Item, InventoryItem, MarketItem

class AddSPForm(ActionForm):
    sp = forms.IntegerField(label='SP', required=False)

class UserAdmin(admin.ModelAdmin):
    def add_sp(self, request, queryset):
        sp = int(request.POST.get('sp'))
        for x in range(queryset.count()):
            queriedUser = User.objects.get(username=queryset[x].username)
            queriedUser.sp += sp
            queriedUser.net_sp += sp
            queriedUser.save()

        self.message_user(
            request, 
            F"Successfully added {sp} SP to {queryset.count()} user{'s'[:queryset.count()^1]}."
        )
    
    action_form = AddSPForm
    actions = [add_sp]
    add_sp.short_description = "Add a specified amount of SP to selected users"

class ItemAdmin(admin.ModelAdmin): 
    def update_circulation(self, request, queryset): 
        numUpdates = 0

        for x in range(queryset.count()):
            queriedItem = Item.objects.get(name=queryset[x].name)
            circulationNum = 0
            circulationInv = InventoryItem.objects.filter(item=queriedItem)
            for y in range(circulationInv.count()):
                circulationNum += circulationInv[y].quantity
            circulationNum += MarketItem.objects.filter(item=queriedItem).count()
            if (circulationNum != queriedItem.in_circulation):
                numUpdates += 1
                queriedItem.in_circulation = circulationNum
                queriedItem.save()

        self.message_user(
            request, 
            F"Successfully updated {numUpdates} item{'s'[:numUpdates^1]}."
        )

    actions = [update_circulation]
    update_circulation.short_description = "Update circulation number for selected items" 

class BlacklistedJWTAdmin(admin.ModelAdmin):
    def remove_expired(self, request, queryset): 
        list = []
        for x in range(queryset.count()):
            queriedJWT = BlacklistedJWT.objects.get(jwt=queryset[x].jwt)
            if (queriedJWT.exp_time < time.time()):
                list.append(queriedJWT)
        for y in list: 
            y.delete()
        s=""
        self.message_user(
            request, 
            F"Successfully removed {len(list)} expired JWT{'s'[:len(list)^1]}."
        )

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
