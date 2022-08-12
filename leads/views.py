import jwt
import random
import time
import math
import requests 
import os
import importlib

from django.shortcuts import render
from django.http import JsonResponse
from django.core.validators import validate_email
from django.contrib.auth.hashers import make_password, check_password 
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
settings = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE'])
JWT_SECRET = settings.JWT_SECRET
SOCKET_IO_BASE_DIR = settings.SOCKET_IO_BASE_DIR
SOCKET_KEY = settings.SOCKET_KEY

from leads.models import User, BlacklistedJWT, InventoryItem, Item, MarketItem
from leads.utility import (
    SPIN_PRICE,
    JWT_EXPIRATION_TIME,
    FREE_SP_TIMEOUT,
    FREE_SP_LOW,
    FREE_SP_HIGH,
    MAX_LIST_PRICE,
    LIST_PRICE_PER_FEE,
    RARITIES,
    RARITY_TO_VALUE,
    map_degree_to_rarity, 
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
            'authError': "The user could not be found."
        }, status=400)
    
    if not check_password(request.POST.get('password'), user.password):
        return JsonResponse({'authError': "The password is incorrect."}, status=400) 
    
    encoded = jwt.encode(
        {'user': user.username, 'exp': time.time() + JWT_EXPIRATION_TIME}, 
        JWT_SECRET, 
        algorithm='HS256'
    )

    return JsonResponse({
        'token': encoded,
        'user': user.username,
        'sp': user.sp, 
        'expirationTime': JWT_EXPIRATION_TIME
    }) 

def register(request):
    if request.method != 'POST':
        return JsonResponse({'authError': "Request error"}, status=400) 
    
    # Check if username is valid
    maxNameLength = User._meta.get_field('username').max_length

    if len(request.POST.get('username')) == 0 or len(request.POST.get('username')) > maxNameLength:
        return JsonResponse(
            {'authError': """This username does not meet length requirements. 
                Username lengths should be between 1 and {} inclusive.""".format(maxNameLength)},
            status=400
        )

    for user in User.objects.all():
        if request.POST.get('username') == user.username:
            return JsonResponse({'authError': "This username is taken."}, status=400)
    
    # Check if email is valid
    try:
        validate_email(request.POST.get('email'))
    except ValidationError as err:
        return JsonResponse({'authError': [e.message for e in err.error_list]}, status=400)
    
    # Check if password is valid
    if not request.POST.get('password') == request.POST.get('confirmPassword'):
        return JsonResponse({'authError': "The passwords do not match."}, status=400)
    
    try:
        validate_password(request.POST.get('password'))
    except ValidationError as err:
        return JsonResponse({'authError': [e.message for e in err.error_list]}, status=400)
    
    user = User.objects.create(
        username=request.POST.get('username'),
        email=request.POST.get('email'),
        password=make_password(request.POST.get('password')),
        sp=0
    )

    encoded = jwt.encode(
        {'user': user.username, 'exp': time.time() + JWT_EXPIRATION_TIME}, 
        JWT_SECRET, 
        algorithm='HS256'
    )
    
    return JsonResponse({
        'token': encoded,
        'user': user.username,
        'sp': user.sp,
        'expirationTime': JWT_EXPIRATION_TIME
    })

def log_out(request):
    if request.method != 'POST':
        return JsonResponse({'logOutError': "Request error"}, status=400) 

    authentication = authenticate(request, 'logOutError', "Log out error. Try refreshing.")
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    BlacklistedJWT.objects.create(
        jwt=request.headers.get('Authorization'),
        exp_time=decoded['exp']
    )
    
    return JsonResponse({})

def buy_spin(request):
    if request.method != 'POST':
        return JsonResponse({'buySpinError': "Request error"}, status=400)

    authentication = authenticate(request, 'buySpinError', "Authentication error")
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    # Subtract SP 
    user = User.objects.get(username=decoded['user'])
    if user.sp - SPIN_PRICE < 0:
        return JsonResponse({'buySpinError': "Not enough SP"}, status=400)
    user.sp -= SPIN_PRICE
    user.save()
    
    # Determine InventoryItem, add InventoryItem to inventory, and update
    # InventoryItem's Item's in_circulation
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

    body = {
        'itemName': obj.item.name,
        'rarity': obj.item.rarity,
        'unboxer': user.username
    }
    try:
        requests.post(
            SOCKET_IO_BASE_DIR + 'item-unboxed', 
            headers={'Authorization': SOCKET_KEY},
            json=body
        )
    except Exception:
        # Posting to Socket.io is not essential
        pass

    return JsonResponse(response)

def auto_log_in(request):
    if request.method != 'POST':
        return JsonResponse({'autoLogInError': "Request error"}, status=400)

    authentication = authenticate(request, 'autoLogInError', 'Authentication error')
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    user = User.objects.get(username=decoded['user'])
    
    return JsonResponse({
        'expirationDate': int(decoded['exp'] * 1000),
        'sp': user.sp
    })

def fetch_inventory(request):
    if request.method != 'GET':
        return JsonResponse({'fetchInventoryError': "Request error"}, status=400)

    authentication = authenticate(request, 'fetchInventoryError', "Must be logged in...")
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 
    
    user = User.objects.get(username=decoded['user'])
    response = {}
    filtered = InventoryItem.objects.filter(user=user)
    for x in range(filtered.count()):
        response['{}'.format(filtered[x].item.name)] = {
            'quantity': filtered[x].quantity, 
            'rarity': filtered[x].item.rarity, 
            'inventoryID': filtered[x].id
        }
    
    return JsonResponse(response)
    
def fetch_profile(request):
    if request.method != 'POST':
        return JsonResponse({'fetchProfileError': "Request error"}, status=400)

    username = request.POST.get('username')
    if len(User.objects.filter(username=username)) != 1: 
        return JsonResponse({'fetchProfileError': "No such user..."}, status=400)

    # Find stats 
    user = User.objects.get(username=username)
    # totalSpinItems = Item.objects.all().count()

    # Find top 3 items according to rarity,
    # then lowest in_circulation, then quantity, then lowest id (oldest)
    showcaseItems = []
    inventoryItems = InventoryItem.objects.filter(user=user)
    for x in range(inventoryItems.count()):
        showcaseItems.append(inventoryItems[x])
    showcaseItems = sorted(showcaseItems, key=lambda el: (
        -RARITY_TO_VALUE[el.item.rarity], 
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
    for rarity in RARITIES[:-1]:
        response['stats']['rarityStats'][rarity.lower()] \
            = user.__dict__['{}_unboxed'.format(rarity.lower())]
    response['stats']['rarityStats']['???'] = user.tq_unboxed

    return JsonResponse(response)

def get_free_sp(request):
    if request.method != 'GET':
        return JsonResponse({'getFreeSPError': "Request error"}, status=400)

    authentication = authenticate(
        request, 
        'getFreeSPError', 
        "Authentication error"
    )
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 
    
    user = User.objects.get(username=decoded['user'])
    if time.time() - user.last_free_sp_time >= FREE_SP_TIMEOUT: 
        freeSPAmount = random.randint(FREE_SP_LOW, FREE_SP_HIGH)
        user.sp = user.sp + freeSPAmount
        user.net_sp = user.net_sp + freeSPAmount 
        user.last_free_sp_time = time.time()
        user.save()
        return JsonResponse({'freeSP': freeSPAmount})

    timeLeft = int((FREE_SP_TIMEOUT - (time.time() - user.last_free_sp_time)) * 1000)

    return JsonResponse({'getFreeSPError': timeLeft}, status=400)

def list_item(request):
    if request.method != 'POST':
        return JsonResponse({'listItemError': "Request error"}, status=400)
    
    authentication = authenticate(request, 'listItemError', "Authentication error")
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    try: 
        numPrice = int(request.POST.get('price'))
    except: 
        return JsonResponse({'listItemError': "Invalid price"}, status=400)
    
    if numPrice <= 0 or numPrice > MAX_LIST_PRICE: 
        return JsonResponse({'listItemError': "Invalid price"}, status=400)
    
    user = User.objects.get(username=decoded['user'])

    if user.sp - math.floor(int(request.POST.get('price'))/LIST_PRICE_PER_FEE) < 0:
        return JsonResponse({'listItemError': "Not enough SP"}, status=400)
    
    try: 
        inventoryItem = InventoryItem.objects.get(
            id=request.POST.get('inventoryID'),
            user=user
        )
    except: 
        return JsonResponse({'listItemError': "You don't have that item"}, 
            status=400)

    if inventoryItem.quantity > 1: 
        inventoryItem.quantity -= 1
        inventoryItem.save()
    else:
        inventoryItem.delete()

    user.sp -= math.floor(int(request.POST.get('price'))/LIST_PRICE_PER_FEE)
    user.save()

    marketItem = MarketItem.objects.create(
        user=user, 
        item=inventoryItem.item, 
        price=int(request.POST.get('price')), 
        listTime=time.time()
    ) 

    body = {
        marketItem.id: {
            'itemName': marketItem.item.name,
            'seller': marketItem.user.username, 
            'rarity': marketItem.item.rarity, 
            'price': marketItem.price,
            'listTime': int(marketItem.listTime * 1000)
        }
    }
    try:
        requests.post(
            SOCKET_IO_BASE_DIR + 'item-listed', 
            headers={'Authorization': SOCKET_KEY},
            json=body
        ) 
    except Exception:
        # Posting to Socket.io is not essential
        pass
    
    return JsonResponse({})

def fetch_market(request):
    if request.method != 'GET':
        return JsonResponse({'fetchMarketError': "Request error"}, status=400)

    response = {}
    marketItems = MarketItem.objects.all()
    for x in range(marketItems.count()):
        response[marketItems[x].id] = {
            'itemName': marketItems[x].item.name,
            'seller': marketItems[x].user.username, 
            'rarity': marketItems[x].item.rarity, 
            'price': marketItems[x].price,
            'listTime': int(marketItems[x].listTime * 1000)
        }

    return JsonResponse(response)

def buy_item(request):
    if request.method != 'POST':
        return JsonResponse({'buyItemError': "Request error"}, status=400)
    
    authentication = authenticate(request, 'buyItemError', "Authentication error")
    if not authentication[0]: 
        return authentication[1]
    decoded = authentication[1] 

    buyer = User.objects.get(username=decoded['user'])

    try: 
        marketItem = MarketItem.objects.get(id=request.POST.get('marketID'))
    except: 
        return JsonResponse({'buyItemError': "Item already bought"}, status=400)
    
    if buyer.sp < marketItem.price:
        return JsonResponse({'buyItemError': "Not enough SP"}, status=400)
    
    if buyer == marketItem.user: 
        return JsonResponse({'buyItemError': "Cannot buy own item"}, status=400)
    
    marketItem.delete()

    buyer.sp -= marketItem.price 
    buyer.save()
    
    inventoryItem, created = InventoryItem.objects.get_or_create(
        user=buyer,
        item=marketItem.item,
        defaults={'quantity': 1}
    )
    if not created:
        inventoryItem.quantity += 1
        inventoryItem.save()

    seller = marketItem.user
    seller.sp += marketItem.price
    seller.net_sp += marketItem.price 
    seller.save()

    body = {
        'marketID': request.POST.get('marketID'), 
        'seller': marketItem.user.username, 
        'price': marketItem.price
    }
    try:
        requests.post(
            SOCKET_IO_BASE_DIR + 'item-bought', 
            headers={'Authorization': SOCKET_KEY},
            data=body
        )
    except Exception:
        # Posting to Socket.io is not essential
        pass

    return JsonResponse({})
