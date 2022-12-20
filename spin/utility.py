import jwt
import os
import importlib

from spin.models import BlacklistedJWT
from django.http import JsonResponse
settings = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE'])
SPIN_JWT_SECRET = settings.SPIN_JWT_SECRET

# Constants
SPIN_PRICE = 500
JWT_EXPIRATION_TIME = 3600 # Seconds
FREE_SP_TIMEOUT = 7200 # Seconds
FREE_SP_LOW = 1500 
FREE_SP_HIGH = 3000 
MAX_LIST_PRICE = 10000000
LIST_PRICE_PER_FEE = 20 

RARITIES = ['Common', 'Uncommon', 'Rare', 'Epic', 'Holy', 'Godly', '???']
RARITY_TO_VALUE = {
    RARITIES[0]: 1,
    RARITIES[1]: 2,
    RARITIES[2]: 3,
    RARITIES[3]: 4,
    RARITIES[4]: 5,
    RARITIES[5]: 6,
    RARITIES[6]: 7
}

# Functions
def map_degree_to_rarity(degree):
    if 0 <= degree and degree < 187.2:
        return RARITIES[0]
    if 187.2 <= degree and degree < 259.2:
        return RARITIES[1]
    if 259.2 <= degree and degree < 313.2:
        return RARITIES[2]
    if 313.2 <= degree and degree < 349.2:
        return RARITIES[3]
    if 349.2 <= degree and degree < 358.2: 
        return RARITIES[4]
    if 358.2 <= degree and degree < 359.964:
        return RARITIES[5]
    if 359.964 <= degree and degree < 360:
        return RARITIES[6]
        
def authenticate(request, errorName, errorMessage): 
    for token in BlacklistedJWT.objects.all():
        if request.headers.get('Authorization') == token.jwt: 
            return False, JsonResponse({errorName: errorMessage}, status=401)
    try:
        decoded = jwt.decode(
            request.headers.get('Authorization'), 
            SPIN_JWT_SECRET, 
            algorithms=['HS256']
        )
    except:
        return False, JsonResponse({errorName: errorMessage}, status=401)
    return True, decoded 
