from django.shortcuts import render
from django.http import JsonResponse
from leads.models import User, BlacklistedJWT, InventoryItem, Item
from django.contrib.auth.hashers import make_password, check_password 
from spin_backend.settings import JWT_SECRET
from leads.utility import mapDegreeToRarity

import jwt
import random
import string
import time

# Create your views here.

def login(request):
    if request.method != 'POST':
        return JsonResponse({
            'authError': "Request type error"
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
    encoded = jwt.encode(
            {'username': user.username, 'exp': time.time()+3600}, 
            JWT_SECRET, 
            algorithm='HS256').decode('utf-8')
    response = JsonResponse({
        'token': encoded 
    })
    return response 

def register(request):
    if request.method != 'POST':
        return JsonResponse({
            'authError': "Request type error"
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
            SP=0)
    encoded = jwt.encode(
            {'username': user.username, 'exp': time.time()+3600}, 
            JWT_SECRET, 
            algorithm='HS256').decode('utf-8')
    return JsonResponse({
        'token': encoded
    })

def logout(request):
    if request.method != 'POST':
        return JsonResponse({
            'authError': "Request type error"
        }, status=400) 
    try:
        jwt.decode(request.headers.get('Authorization'), 
                JWT_SECRET, 
                algorithms=['HS256'])
    except:
        return JsonResponse({
            'authError': """Log out error 
                    (you are probably already logged out), try refreshing"""
        }, status=401)
    BlacklistedJWT.objects.create(jwt=request.headers.get('Authorization'))
    return JsonResponse({})

def fetch_sp(request):
    if request.method != 'GET':
        return JsonResponse({'fetchError': "REQUEST TYPE ERROR"}, status=400)
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
    return JsonResponse({'SP': user.SP})

def purchase_spin(request):
    if request.method != 'POST':
        return JsonResponse({'purchaseError': "Request type error"}, status=400)
    for BJwt in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == BJwt.jwt:
            return JsonResponse({
                'purchaseError': """Log in error 
                        (your session has probably expired), 
                        try refreshing the page and logging back in"""
            }, status=401)
    try:
        decoded = jwt.decode(request.headers.get('Authorization'), 
                JWT_SECRET, 
                algorithms=['HS256'])
    except:
        return JsonResponse({
            'purchaseError': """Log in error 
                    (your session has probably expired), 
                    try refreshing the page and logging back in"""
        }, status=401)

    # Subtract SP 
    user = User.objects.get(username=decoded['username'])
    if user.SP - 500 < 0:
        return JsonResponse({'purchaseError': "Not enough SP"}, status=400)
    user.SP = user.SP - 500
    user.save()
    
    # Determine item
    degree = random.random()*360
    item = Item.objects.filter(rarity=mapDegreeToRarity(degree))
    index = random.randrange(item.count()) 
    obj, created = InventoryItem.objects.get_or_create(
        user=user,
        item=item[index],
        defaults={'quantity': 1}
    )
    if not created:
        obj.quantity += 1
        obj.save()

    # Create response 
    response = {'SP': user.SP, 'degree': degree}
    response['item'] = {'name': '{}'.format(obj.item), 'rarity': 
        "{}".format(obj.item.rarity)}
    return JsonResponse(response)

def auto_log_in(request):
    if request.method != 'POST':
        return JsonResponse({'error': "Request type error"}, status=400)
    for BJwt in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == BJwt.jwt:
            return JsonResponse({}, status=401)
    try:
        jwt.decode(request.headers.get('Authorization'), 
                JWT_SECRET, 
                algorithms=['HS256'])
    except:
        return JsonResponse({}, status=401)
    return JsonResponse({})

def fetch_inventory(request):
    if request.method != 'GET':
        return JsonResponse({'fetchError': "Request type error"}, status=400)
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
        "{}".format(filtered[x].quantity), 'rarity': 
        "{}".format(filtered[x].item.rarity), 'id': 
        "{}".format(filtered[x].id)}
    return JsonResponse(response)
    