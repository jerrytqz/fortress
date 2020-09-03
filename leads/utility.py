def mapDegreeToRarity(degree):
    if 0 <= degree and degree < 187.2:
        return 'Common'
    if 187.2 <= degree and degree < 259.2:
        return 'Uncommon'
    if 259.2 <= degree and degree < 313.2:
        return 'Rare'
    if 313.2 <= degree and degree < 349.2:
        return 'Epic'
    if 349.2 <= degree and degree < 358.2: 
        return 'Holy'
    if 358.2 <= degree and degree < 359.964:
        return 'Godly'
    if 359.964 <= degree and degree < 360:
        return '???'
