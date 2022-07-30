import jwt

from leads.models import BlacklistedJWT
from spin_backend.settings import JWT_SECRET
from django.http import JsonResponse

rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Holy', 'Godly', '???']
rarityToValue = {
    'Common': 1,
    'Uncommon': 2,
    'Rare': 3,
    'Epic': 4,
    'Holy': 5,
    'Godly': 6,
    '???': 7
}

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
