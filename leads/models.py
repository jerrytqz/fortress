from django.db import models
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    last_free_sp_time = models.FloatField(default=0)

    sp = models.IntegerField(default=0)
    net_sp = models.IntegerField(default=0)
    total_spins = models.IntegerField(default=0)
    items_found = models.IntegerField(default=0)
    common_unboxed = models.IntegerField(default=0)
    uncommon_unboxed = models.IntegerField(default=0)
    rare_unboxed = models.IntegerField(default=0)
    epic_unboxed = models.IntegerField(default=0)
    holy_unboxed = models.IntegerField(default=0)
    godly_unboxed = models.IntegerField(default=0)
    tq_unboxed = models.IntegerField(default=0) 

    def __str__(self):
        return self.username 

class BlacklistedJWT(models.Model):
    jwt = models.CharField(max_length=512)

    def __str__(self):
        return self.jwt

class Item(models.Model): 
    name = models.CharField(max_length=32, unique=True)
    rarity = models.CharField(max_length=16)
    description = models.CharField(max_length=128, default="")
    in_circulation = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta: 
        ordering = ['name']

class InventoryItem(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username + ' | ' + self.item.name

    class Meta: 
        ordering = ['user', 'item']
    
class MarketItem(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username + ' | ' + self.item.name + ' | ' + str(
            self.price)

    class Meta: 
        ordering = ['user', 'item', 'price']
    