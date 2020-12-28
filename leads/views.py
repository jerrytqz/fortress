from django.shortcuts import render
from django.http import JsonResponse
from leads.models import User, BlacklistedJWT, InventoryItem, Item
from django.contrib.auth.hashers import make_password, check_password 
from spin_backend.settings import JWT_SECRET
from leads.utility import (
    map_degree_to_rarity, 
    map_rarity_to_value, 
    sec_to_time, 
    rarities
)

import jwt
import random
import string
import time
import datetime

# Create your views here.

def login(request):
    if request.method != 'POST':
        return JsonResponse({
            'authError': "Request error"
        }, status=400)
    try: 
        user = User.objects.get(username=request.POST.get('username'))
    except:
        return JsonResponse({
            'authError': "User could not be found"
        }, status=400)
    if not check_password(request.POST.get('password'), user.password):
        return JsonResponse({
            'authError': "Incorrect password"
        }, status=400) 
    expirationTime = 3600
    encoded = jwt.encode(
        {'username': user.username, 'exp': time.time() + expirationTime}, 
        JWT_SECRET, 
        algorithm='HS256').decode('utf-8')
    response = JsonResponse({
        'token': encoded,
        'user': user.username,
        'expirationTime': expirationTime
    })
    return response 

def register(request):
    if request.method != 'POST':
        return JsonResponse({
            'authError': "Request error"
        }, status=400) 
    if not request.POST.get('password') == request.POST.get('confirmPassword'):
        return JsonResponse({
            'authError': "Passwords do not match"
        }, status=400)
    for user in User.objects.all():
        if request.POST.get('username') == user.username:
            return JsonResponse({
                'authError': "Username is taken"
            }, status=400)
    user = User.objects.create(
        username=request.POST.get('username'),
        email=request.POST.get('email'),
        password=make_password(request.POST.get('password')),
        sp=0)
    expirationTime = 3600
    encoded = jwt.encode(
        {'username': user.username, 'exp': time.time() + expirationTime}, 
        JWT_SECRET, 
        algorithm='HS256').decode('utf-8')
    return JsonResponse({
        'token': encoded,
        'user': user.username,
        'expirationTime': expirationTime
    })

def logout(request):
    if request.method != 'POST':
        return JsonResponse({
            'authError': "Request error"
        }, status=400) 
    try:
        jwt.decode(request.headers.get('Authorization'), 
            JWT_SECRET, 
            algorithms=['HS256'])
    except:
        return JsonResponse({
            'authError': "Log out error" 
        }, status=401)

    BlacklistedJWT.objects.create(jwt=request.headers.get('Authorization'))
    return JsonResponse({})

def fetch_sp(request):
    if request.method != 'GET':
        return JsonResponse({'fetchError': "REQUEST ERROR"}, status=400)
    for BJwt in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == BJwt.jwt:
            return JsonResponse({'fetchError': "LOG IN TO SPIN"}, status=401)
    try:
        decoded = jwt.decode(request.headers.get('Authorization'), 
            JWT_SECRET, 
            algorithms=['HS256'])
    except:
        return JsonResponse({'fetchError': "LOG IN TO SPIN"}, status=401)
    
    user = User.objects.get(username=decoded['username'])
    return JsonResponse({'SP': user.sp})

def purchase_spin(request):
    if request.method != 'POST':
        return JsonResponse({'purchaseError': "Request error"}, status=400)
    for BJwt in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == BJwt.jwt:
            return JsonResponse({
                'purchaseError': "Authentication error"
            }, status=401)
    try:
        decoded = jwt.decode(request.headers.get('Authorization'), 
            JWT_SECRET, 
            algorithms=['HS256'])
    except:
        return JsonResponse({
            'purchaseError': "Authentication error"
        }, status=401)

    # Subtract SP 
    user = User.objects.get(username=decoded['username'])
    if user.sp - 500 < 0:
        return JsonResponse({'purchaseError': "Not enough SP"}, status=400)
    user.sp = user.sp - 500
    user.save()
    
    # Determine InventoryItem, add InventoryItem to inventory, and update
    # InventoryItem's Item's in_circulation 
    degree = random.random()*360
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
    if created:
        user.items_found += 1
    user.save()

    # Create response 
    response = {'SP': user.sp, 'degree': degree}
    response['item'] = {'name': "{}".format(item), 'rarity': 
        item.rarity, 'description': item.description, 
        'circulationNum': item.in_circulation, 'quantity': obj.quantity}
    return JsonResponse(response)

def auto_log_in(request):
    if request.method != 'POST':
        return JsonResponse({'error': "Request error"}, status=400)
    for BJwt in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == BJwt.jwt:
            return JsonResponse({}, status=401)
    try:
        decoded = jwt.decode(request.headers.get('Authorization'), 
            JWT_SECRET, 
            algorithms=['HS256'])
    except:
        return JsonResponse({}, status=401)
    return JsonResponse({'expirationDate': int(decoded['exp'] * 1000)})

def fetch_inventory(request):
    if request.method != 'GET':
        return JsonResponse({'fetchError': "Request error"}, status=400)
    for BJwt in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == BJwt.jwt:
            return JsonResponse({'fetchError': "Must be logged in..."}, 
                status=401)
    try:
        decoded = jwt.decode(request.headers.get('Authorization'), 
            JWT_SECRET, 
            algorithms=['HS256'])
    except:
        return JsonResponse({'fetchError': "Must be logged in..."}, status=401)
    
    user = User.objects.get(username=decoded['username'])
    response = {}
    filtered = InventoryItem.objects.filter(user=user)
    for x in range(filtered.count()):
        response['{}'.format(filtered[x].item)] = {'quantity': 
        filtered[x].quantity, 'rarity': filtered[x].item.rarity, 'id': 
        filtered[x].id}
    return JsonResponse(response)
    
def fetch_profile(request):
    if request.method != 'POST':
        return JsonResponse({'fetchError': "Request error"}, status=400)

    username = request.POST.get('username')
    if len(User.objects.filter(username=username)) != 1: 
        return JsonResponse({'fetchError': "No such user..."}, status=400)

    # Find stats 
    user = User.objects.get(username=username)
    totalSpinItems = Item.objects.all().count()

    # Find top 3 items according to rarity,
    # then lowest in_circulation, then quantity, then lowest id (oldest)
    showcaseItems = []
    inventoryItems = InventoryItem.objects.filter(user=user)
    for x in range(inventoryItems.count()):
        showcaseItems.append(inventoryItems[x])
    showcaseItems = sorted(showcaseItems, key=lambda el: 
        (-map_rarity_to_value(el.item.rarity), el.item.in_circulation,
        -el.quantity, el.id))[:3]
    showcaseItems = list(map((lambda el: {'name': el.item.name, 
        'rarity': el.item.rarity, 'quantity': el.quantity}), showcaseItems))
    while len(showcaseItems) < 3:
        showcaseItems.append("nothing")

    # Create response 
    response = {'username': username, 'stats': {'SP': user.sp,
        'netSP': user.net_sp, 'totalSpins': user.total_spins, 
        'itemsFound': user.items_found, 'totalSpinItems': totalSpinItems, 
        'rarityStats': {}}, 'showcaseItems': {'one': showcaseItems[0], 
        'two': showcaseItems[1], 'three': showcaseItems[2]}}
    for rarity in rarities[:-1]:
        response['stats']['rarityStats'][rarity.lower()] = user.__dict__[
            '{}_unboxed'.format(rarity.lower())]
    response['stats']['rarityStats']['???'] = user.tq_unboxed

    return JsonResponse(response)

def free_sp(request):
    if request.method != 'GET':
        return JsonResponse({'freeSPError': "Request error"}, status=400)
    for BJwt in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == BJwt.jwt:
            return JsonResponse({
                'freeSPError': "Authentication error"
            }, status=401)
    try:
        decoded = jwt.decode(request.headers.get('Authorization'), 
            JWT_SECRET, 
            algorithms=['HS256'])
    except:
        return JsonResponse({
            'freeSPError': "Authentication error"
        }, status=401)
    
    user = User.objects.get(username=decoded['username'])
    if time.time() - user.last_free_sp_time >= 7200: 
        freeSPAmount = random.randint(1500, 3000)
        user.sp = user.sp + freeSPAmount
        user.net_sp = user.net_sp + freeSPAmount 
        user.last_free_sp_time = time.time()
        user.save()
        return JsonResponse({'SP': user.sp})

    timeLeft = str(sec_to_time(int(7200 
        - (time.time() - user.last_free_sp_time))))
    return JsonResponse({'freeSPError': "Next free SP in " + timeLeft}, 
        status=400)
    