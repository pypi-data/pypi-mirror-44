from scipy.optimize import least_squares as olsq

def dotest():

    return olsq(lambda x: x - 5.,0)['x']
