from fractions import gcd
from random import randint

def description():
    return 'Find the Greated Common Divisor'

def question():
    a = randint(1, 999)
    b = randint(0, 999)
    d = gcd(a, b)
    return ('(%d,%d)' % (a, b), str(d))
