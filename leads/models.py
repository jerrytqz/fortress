from django.db import models
# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=16)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    SP = models.IntegerField(default=0)

    def __str__(self):
        return self.username 

class BlacklistedJWT(models.Model):
    jwt = models.CharField(max_length=512)

    def __str__(self):
        return self.jwt

class Item(models.Model): 
    name = models.CharField(max_length=64)
    rarity = models.CharField(max_length=16)

    def __str__(self):
        return self.name

class InventoryItem(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return self.user.username
    