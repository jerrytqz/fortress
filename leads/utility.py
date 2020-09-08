def map_degree_to_rarity(degree):
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

def map_rarity_to_value(rarity): 
    if (rarity == 'Common'): 
        return 1
    if (rarity == 'Uncommon'): 
        return 2
    if (rarity == 'Rare'):
        return 3
    if (rarity == 'Epic'):
        return 4
    if (rarity == 'Holy'):
        return 5
    if (rarity == 'Godly'):
        return 6
    if (rarity == '???'):
        return 7

def sec_to_time(seconds):
    a = seconds//3600
    b = (seconds%3600)//60
    c = (seconds%3600)%60

    d = ''
    e = ''
    f = ''

    if a == 0 or a > 1:
        d = 's'

    if b == 0 or b > 1:
        e = 's'

    if c == 0 or c > 1:
        f = 's'

    output = "{} hour{} {} minute{} {} second{}".format(
        str(a), d, str(b), e, str(c), f)
    return output

rarities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Holy', 'Godly', '???']
