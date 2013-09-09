'''
Created on Sep 6, 2013

@author: niels
'''

import operations

class OpenCLMap(object):

    def __init__(self, pcrmap):
        self.pcrmap = pcrmap 
        
    def toPcrMap(self):
        return self.pcrmap
    
    # Some syntactic sugar to allow the use of operators on Maps.
    # See http://docs.python.org/2/reference/datamodel.html#emulating-numeric-types
    # Note the reverse of the arguments in all reflected(swapped) operands when calling the operation
    #
    # TODO: also add in-place operators such as "+="
        
    def __and__(self, other):
        return operations.pcrand(self, other)
     
    def __rand__(self, other):
        return operations.pcrand(other, self)
     
    def __or__(self, other):
        return operations.pcror(self, other)
     
    def __ror__(self, other):
        return operations.pcror(other, self)
     
    def __xor__(self, other):
        return operations.pcrxor(self, other)
     
    def __invert__(self):
        return operations.pcrnot(self)
     
    def __ne__(self, other):
        return operations.pcrne(self, other)
     
    def __eq__(self, other):
        return operations.pcreq(self, other)
     
    def __gt__(self, other):
        return operations.pcrgt(self, other)
     
    def __ge__(self, other):
        return operations.pcrge(self, other)
     
    def __lt__(self, other):
        return operations.pcrlt(self, other)
     
    def __le__(self, other):
        return operations.pcrle(self, other)
     
    def __mul__(self, other):
        return operations.pcrmul(self, other)
     
    def __rmul__(self, other):
        return operations.pcrmul(other, self)
     
    def __div__(self, other):
        return operations.pcrfdiv(self, other)
     
    def __rdiv__(self, other):
        return operations.pcrfdiv(other, self)
     
    def __floordiv__(self, other):
        return operations.pcridiv(self, other)
     
    def __rfloordiv__(self, other):
        return operations.pcridiv(other, self)
     
    def __pow__(self, other):
        return operations.pcrpow(self, other)
     
    def __rpow__(self, other):
        return operations.pcrpow(other, self)
     
    def __mod__(self, other):
        return operations.pcrmod(self, other)
     
    def __rmod__(self, other):
        return operations.pcrmod(other, self)
     
    def __add__(self, other):
        return operations.pcrbadd(self, other)
     
    def __radd__(self, other):
        print 'radd'
        return operations.pcrbadd(other, self)
     
    def __sub__(self, other):
        return operations.pcrbmin(self, other)
     
    def __rsub__(self, other):
        return operations.pcrbmin(other, self)
     
    def __neg__(self):
        return operations.pcrumin(self)
     
    def __pos__(self):
        return operations.pcruadd(self)
     
     
    #FIXME: we do not support non-spacial fields in OpenCL Python
    #def _bool(self):
    #def _int(self):
    #def _float(self):
    #def__nonzero__(self):
     