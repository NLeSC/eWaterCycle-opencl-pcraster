'''
Value Scale types of PCRaster

Created on Oct 8, 2013

@author: Niels Drost
'''

import pcraster._pcraster as pcr_native

class ValueScale(object):
    '''Data types available in pcraster'''
    @classmethod
    def toPCR(cls):
        pass

class Scalar(ValueScale):
    '''Pcraster Scalar type'''
    @classmethod
    def toPCR(cls):
        return pcr_native.Scalar

class Directional(ValueScale):
    '''Pcraster Directional type'''
    @classmethod
    def toPCR(cls):
        return pcr_native.Directional
    
class Ordinal(ValueScale):
    '''Pcraster Ordinal type'''
    @classmethod
    def toPCR(cls):
        return pcr_native.Ordinal

class Nominal(ValueScale):
    '''Pcraster Nominal type'''
    @classmethod
    def toPCR(cls):
        return pcr_native.Nominal