import jwt
import random
import string
import time
import datetime
import math
import requests 

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password 
from spin_backend.settings import JWT_SECRET, WEB_SOCKET_BASE_DIR
from leads.models import User, BlacklistedJWT, InventoryItem, Item, MarketItem
from leads.utility import (
    rarities,
    map_degree_to_rarity, 
    map_rarity_to_value, 
    authenticate
)

# Create your views here.

def log_in(request):
    if request.method != 'POST':
        return JsonResponse({'authError': "Request error"}, status=400)

    try: 
        user = User.objects.get(username=request.POST.get('username'))
    except:
        return JsonResponse({
            'authError': "User could not be found"
        }, status=400)
    
    if not check_password(request.POST.get('password'), user.password):
        return JsonResponse({'authError': "Incorrect password"}, status=400) 
    
    expirationTime = 3600
    encoded = jwt.encode(
        {'username': user.username, 'exp': time.time() + expirationTime}, 
        JWT_SECRET, 
        algorithm='HS256'
    ).decode('utf-8')

    response = JsonResponse({
        'token': encoded,
        'user': user.username,
        'sp': user.sp, 
        'expirationTime': expirationTime
    })

    return response 

def register(request):
    if request.method != 'POST':
        return JsonResponse({'authError': "Request error"}, status=400) 
    
    if not request.POST.get('password') == request.POST.get('confirmPassword'):
        return JsonResponse({'authError': "Passwords do not match"}, status=400)
    
    for user in User.objects.all():
        if request.POST.get('username') == user.username:
            return JsonResponse({'authError': "Username is taken"}, status=400)
    
    user = User.objects.create(
        username=request.POST.get('username'),
        email=request.POST.get('email'),
        password=make_password(request.POST.get('password')),
        sp=0
    )

    expirationTime = 3600
    encoded = jwt.encode(
        {'username': user.username, 'exp': time.time() + expirationTime}, 
        JWT_SECRET, 
        algorithm='HS256'
    ).decode('utf-8')
    
    return JsonResponse({
        'token': encoded,
        'user': user.username,
        'sp': user.sp,
        'expirationTime': expirationTime
    })

def log_out(request):
    if request.method != 'POST':
        return JsonResponse({'authError': "Request error"}, status=400) 
    
    try:
        jwt.decode(
            request.headers.get('Authorization'), 
            JWT_SECRET, 
            algorithms=['HS256']
        )
    except:
        return JsonResponse({'authError': "Log out error"}, status=401)

    BlacklistedJWT.objects.create(jwt=request.headers.get('Authorization'))
    
    return JsonResponse({})

def purchase_spin(request):
    if request.method != 'POST':
        return JsonResponse({'purchaseError': "Request error"}, status=400)

    authentication = authenticate(
        request, 
        'purchaseError', 
        "Authentication error"
    )
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    # Subtract SP 
    user = User.objects.get(username=decoded['username'])
    if user.sp - 500 < 0:
        return JsonResponse({'purchaseError': "Not enough SP"}, status=400)
    user.sp -= 500
    user.save()
    
    '''
    Determine InventoryItem, add InventoryItem to inventory, and update
    InventoryItem's Item's in_circulation
    '''
    degree = random.random() * 360
    items = Item.objects.filter(rarity=map_degree_to_rarity(degree))
    index = random.randrange(items.count()) 
    obj, created = InventoryItem.objects.get_or_create(
        user=user,
        item=items[index],
        defaults={'quantity': 1}
    )

    if not created:
        obj.quantity += 1
        obj.save()
    item = Item.objects.get(name=items[index].name)
    item.in_circulation += 1
    item.save()

    body = {
        'item': obj.item,
        'rarity': obj.item.rarity,
        'unboxer': user.username
    } 
    try:
        requests.post(
            WEB_SOCKET_BASE_DIR + 'item-unboxed', 
            data=body
        )
    except:
        pass

    # Update stats
    user.total_spins += 1
    if item.rarity == '???':
        user.tq_unboxed += 1
    else: 
        user.__dict__['{}_unboxed'.format(item.rarity).lower()] += 1
    # if created:
    #     user.items_found += 1
    user.save()

    # Create response 
    response = {'degree': degree}
    response['item'] = {
        'name': "{}".format(item), 
        'rarity': item.rarity, 
        'description': item.description, 
        'circulationNum': item.in_circulation, 
        'quantity': obj.quantity
    }

    return JsonResponse(response)

def auto_log_in(request):
    if request.method != 'POST':
        return JsonResponse({'error': "Request error"}, status=400)

    authentication = authenticate(request, '', '')
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    user = User.objects.get(username=decoded['username'])
    
    return JsonResponse({
        'expirationDate': int(decoded['exp'] * 1000),
        'sp': user.sp
    })

def fetch_inventory(request):
    if request.method != 'GET':
        return JsonResponse({'fetchError': "Request error"}, status=400)

    authentication = authenticate(request, 'fetchError', "Must be logged in...")
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 
    
    user = User.objects.get(username=decoded['username'])
    response = {}
    filtered = InventoryItem.objects.filter(user=user)
    for x in range(filtered.count()):
        response['{}'.format(filtered[x].item)] = {
            'quantity': filtered[x].quantity, 
            'rarity': filtered[x].item.rarity, 
            'inventoryID': filtered[x].id, 
            'itemID': filtered[x].item.id
        }
    
    return JsonResponse(response)
    
def fetch_profile(request):
    if request.method != 'POST':
        return JsonResponse({'fetchError': "Request error"}, status=400)

    username = request.POST.get('username')
    if len(User.objects.filter(username=username)) != 1: 
        return JsonResponse({'fetchError': "No such user..."}, status=400)

    # Find stats 
    user = User.objects.get(username=username)
    # totalSpinItems = Item.objects.all().count()

    '''
    Find top 3 items according to rarity,
    then lowest in_circulation, then quantity, then lowest id (oldest)
    '''
    showcaseItems = []
    inventoryItems = InventoryItem.objects.filter(user=user)
    for x in range(inventoryItems.count()):
        showcaseItems.append(inventoryItems[x])
    showcaseItems = sorted(showcaseItems, key=lambda el: (
        -map_rarity_to_value(el.item.rarity), 
        el.item.in_circulation,
        -el.quantity, el.id
        )
    )[:3]
    showcaseItems = list(map(lambda el: {
        'name': el.item.name, 
        'rarity': el.item.rarity, 
        'quantity': el.quantity}, showcaseItems
        )
    )
    while len(showcaseItems) < 3:
        showcaseItems.append("nothing")

    # Create response 
    response = {
        'username': username, 
        'stats': {
            'sp': user.sp,
            'netSP': user.net_sp, 
            'totalSpins': user.total_spins, 
            # 'itemsFound': user.items_found, 
            # 'totalSpinItems': totalSpinItems, 
            'rarityStats': {}
        }, 
        'showcaseItems': {
            'one': showcaseItems[0], 
            'two': showcaseItems[1], 
            'three': showcaseItems[2]
        }
    }
    for rarity in rarities[:-1]:
        response['stats']['rarityStats'][rarity.lower()] \
            = user.__dict__['{}_unboxed'.format(rarity.lower())]
    response['stats']['rarityStats']['???'] = user.tq_unboxed

    return JsonResponse(response)

def free_sp(request):
    if request.method != 'GET':
        return JsonResponse({'freeSPError': "Request error"}, status=400)

    authentication = authenticate(
        request, 
        'freeSPError', 
        "Authentication error"
    )
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 
    
    user = User.objects.get(username=decoded['username'])
    if time.time() - user.last_free_sp_time >= 7200: 
        freeSPAmount = random.randint(1500, 3000)
        user.sp = user.sp + freeSPAmount
        user.net_sp = user.net_sp + freeSPAmount 
        user.last_free_sp_time = time.time()
        user.save()
        return JsonResponse({'freeSP': freeSPAmount})

    timeLeft = int((7200 - (time.time() - user.last_free_sp_time)) * 1000)

    return JsonResponse({'freeSPError': timeLeft}, status=400)

def list_item(request):
    if request.method != 'POST':
        return JsonResponse({'listError': "Request error"}, status=400)
    
    authentication = authenticate(request, 'listError', "Authentication error")
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    try: 
        numPrice = int(request.POST.get('price'))
    except: 
        return JsonResponse({'listError': "Invalid price"}, status=400)
    
    if numPrice < 1 or numPrice > 10000000: 
        return JsonResponse({'listError': "Invalid price"}, status=400)
    
    user = User.objects.get(username=decoded['username'])

    if user.sp - math.floor(int(request.POST.get('price'))/20) < 0:
        return JsonResponse({'listError': "Not enough SP"}, status=400)
    
    try: 
        inventoryItem = InventoryItem.objects.get(
            user=user.id,
            item=request.POST.get('itemID')
        )
    except: 
        return JsonResponse({'listError': "You don't have that item"}, 
            status=400)

    user.sp -= math.floor(int(request.POST.get('price'))/20)
    user.save()
    
    if inventoryItem.quantity > 1: 
        inventoryItem.quantity -= 1
        inventoryItem.save()
    else:
        inventoryItem.delete()

    marketItem = MarketItem.objects.create(
        user=user, 
        item=inventoryItem.item, 
        price=int(request.POST.get('price')), 
        listTime=time.time()
    ) 

    body = {
        marketItem.id: {
            'item': marketItem.item.name,
            'seller': marketItem.user.username, 
            'rarity': marketItem.item.rarity, 
            'price': marketItem.price,
            'listTime': int(marketItem.listTime * 1000)
        }
    } 
    try:
        requests.post(
            WEB_SOCKET_BASE_DIR + 'item-listed', 
            json=body
        )
    except:
        pass
    
    return JsonResponse({})

def fetch_market(request):
    if request.method != 'GET':
        return JsonResponse({'fetchError': "Request error"}, status=400)

    response = {}
    marketItems = MarketItem.objects.all()
    for x in range(marketItems.count()):
        response[marketItems[x].id] = {
            'item': marketItems[x].item.name,
            'seller': marketItems[x].user.username, 
            'rarity': marketItems[x].item.rarity, 
            'price': marketItems[x].price,
            'listTime': int(marketItems[x].listTime * 1000)
        }

    return JsonResponse(response)

def buy_item(request):
    if request.method != 'POST':
        return JsonResponse({'buyError': "Request error"}, status=400)
    
    authentication = authenticate(request, 'buyError', "Authentication error")
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    buyer = User.objects.get(username=decoded['username'])

    try: 
        marketItem = MarketItem.objects.get(id=request.POST.get('marketID'))
    except: 
        return JsonResponse({'buyError': "Item already bought"}, status=400)
    
    if buyer.sp < marketItem.price:
        return JsonResponse({'buyError': "Not enough SP"}, status=400)
    
    if buyer == marketItem.user: 
        return JsonResponse({'buyError': "Cannot buy own item"}, status=400)
    
    clone = marketItem 
    marketItem.delete()

    body = {
        'marketID': request.POST.get('marketID'), 
        'seller': clone.user.username, 
        'price': clone.price
    }
    try:
        requests.post(
            WEB_SOCKET_BASE_DIR + 'item-bought', 
            data=body
        )
    except:
        pass

    buyer.sp -= clone.price 
    buyer.save()
    
    inventoryItem, created = InventoryItem.objects.get_or_create(
        user=buyer,
        item=clone.item,
        defaults={'quantity': 1}
    )
    if not created:
        inventoryItem.quantity += 1
        inventoryItem.save()

    seller = clone.user
    seller.sp += clone.price
    seller.net_sp += clone.price 
    seller.save()

    return JsonResponse({})
