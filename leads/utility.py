import jwt

from leads.models import User, BlacklistedJWT
from spin_backend.settings import JWT_SECRET
from django.http import JsonResponse

rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Holy', 'Godly', '???']

def map_degree_to_rarity(degree):
    if 0 <= degree and degree < 187.2:
        return rarities[0]
    if 187.2 <= degree and degree < 259.2:
        return rarities[1]
    if 259.2 <= degree and degree < 313.2:
        return rarities[2]
    if 313.2 <= degree and degree < 349.2:
        return rarities[3]
    if 349.2 <= degree and degree < 358.2: 
        return rarities[4]
    if 358.2 <= degree and degree < 359.964:
        return rarities[5]
    if 359.964 <= degree and degree < 360:
        return rarities[6]

def map_rarity_to_value(rarity): 
    if (rarity == rarities[0]): 
        return 1
    if (rarity == rarities[1]): 
        return 2
    if (rarity == rarities[2]):
        return 3
    if (rarity == rarities[3]):
        return 4
    if (rarity == rarities[4]):
        return 5
    if (rarity == rarities[5]):
        return 6
    if (rarity == rarities[6]):
        return 7

def authenticate(request, errorName, errorMessage): 
    for token in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == token.jwt: 
            return False, JsonResponse({errorName: errorMessage}, status=401)
    try:
        decoded = jwt.decode(
            request.headers.get('Authorization'), 
            JWT_SECRET, 
            algorithms=['HS256']
        )
    except:
        return False, JsonResponse({errorName: errorMessage}, status=401)
    return True, decoded 
