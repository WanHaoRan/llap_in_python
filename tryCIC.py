# Implements an in-memory CIC decimator using numpy.

from math import log
from numpy import int32, int64, array

def cic_decimator(source, decimation_factor=32, order=5, ibits=1, obits=16):

    # Calculate the total number of bits used internally, and the output
    # shift and mask required.
    numbits = order * int(round(log(decimation_factor) / log(2))) + ibits
    outshift = numbits - obits
    outmask  = (1 << obits) - 1

    # If we need more than 64 bits, we can't do it...
    assert numbits <= 64

    # Create a numpy array with the source
    result = array(source, int64 if numbits > 32 else int32)

    # Do the integration stages
    for i in range(order):
        result.cumsum(out=result)

    # Decimate
    result = array(result[decimation_factor - 1 : : decimation_factor])

    # Do the comb stages.  Iterate backwards through the array,
    # because we use each value before we replace it.
    for i in range(order):
        result[len(result) - 1 : 0 : -1] -= result[len(result) - 2 : : -1]

    # Normalize the output
    result >>= outshift
    result &= outmask
    return result
