import numpy as np
from scipy import sparse
import sys

x = float(sys.argv[1])

def power(x):
    return x ** 2

result = power(x)

print "the power of", x, "is", result 
