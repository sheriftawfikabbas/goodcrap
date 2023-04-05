import numpy as np

def get_crap(crap_label):
    if crap_label == 'goodcrap_salary':
        pass
    elif crap_label == 'goodcrap_creditlimit':
        pass
    elif crap_label == 'goodcrap_networth':
        pass
    elif crap_label == 'goodcrap_valuation':
        pass
    elif crap_label == 'goodcrap_shareprice':
        pass
    elif crap_label == 'goodcrap_salary':
        pass
    elif crap_label == 'goodcrap_salary':
        pass

def crapper_unique(props: dict):
    pass

def crapper(props: dict):
    decimals = 2
    multiplier = 1
    if props['type'] == 'random_int':
        if 'multiplier' in props.keys():
            multiplier = props['multiplier']
        return int(np.random.random()*(props['max'] - props['min'] + 1) + props['min'])*multiplier
    elif props['type'] == 'random_float':
        if 'multiplier' in props.keys():
            multiplier = props['multiplier']
        if 'decimals' in props.keys():
            decimals = props['decimals']
        return (int(np.power(10, decimals)*np.random.random()*(props['max'] - props['min'] + 1) + props['min']))/np.power(10, decimals)*multiplier
    elif props['type'] == 'random_percent':
        if 'decimals' in props.keys():
            decimals = props['decimals']
        return (int(np.power(10, decimals)*np.random.random()*(101)))/np.power(10, decimals)
    
