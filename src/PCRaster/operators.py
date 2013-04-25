import operations, PCRaster, _PCRaster

def pcrAnd(self, field):
    return operations.pcrand(self, field)

def pcrRAnd(self, number):
    return operations.pcrand(number, self)

def pcrOr(self, field):
    return operations.pcror(self, field)

def pcrROr(self, number):
    return operations.pcror(number, self)

def pcrXOr(self, field):
    return operations.pcrxor(self, field)

def pcrNot(self):
    return operations.pcrnot(self)

def pcrNE(self, field):
    return operations.pcrne(self, field)

def pcrEQ(self, field):
    return operations.pcreq(self, field)

def pcrGT(self, field):
    return operations.pcrgt(self, field)

def pcrGE(self, field):
    return operations.pcrge(self, field)

def pcrLT(self, field):
    return operations.pcrlt(self, field)

def pcrLE(self, field):
    return operations.pcrle(self, field)

def pcrMul(self, field):
    return operations.pcrmul(self, field)

def pcrRMul(self, number):
    return operations.pcrmul(number, self)

def pcrDiv(self, field):
    return operations.pcrfdiv(self, field)

def pcrRDiv(self, number):
    return operations.pcrfdiv(number, self)

def pcrFloorDiv(self, field):
    return operations.pcridiv(self, field)

def pcrRFloorDiv(self, number):
    return operations.pcridiv(number, self)

def pcrPow(self, field):
    return operations.pcrpow(self, field)

def pcrRPow(self, number):
    return operations.pcrpow(number, self)

def pcrMod(self, field):
    return operations.pcrmod(self, field)

def pcrRMod(self, number):
    return operations.pcrmod(number, self)

def pcrAdd(self, field):
    return operations.pcrbadd(self, field)

def pcrRAdd(self, number):
    return operations.pcrbadd(number, self)

def pcrSub(self, field):
    return operations.pcrbmin(self, field)

def pcrRSub(self, number):
    return operations.pcrbmin(number, self)

def pcrNeg(self):
    return operations.pcrumin(self)

def pcrPos(self):
    return operations.pcruadd(self)

def _bool(self):
    if self.isSpatial():
        raise Exception(
             "The truth value for PCRaster spatial data types is ambiguous. "
             "For comparison operations use 'ifthen' or 'ifthenelse' instead.")

    result = None
    value, isValid = PCRaster.cellvalue(self, 0)

    if isValid:
        result = bool(value)

    return result

def _int(self):
    if self.isSpatial():
        raise Exception(
             "The integer value for PCRaster spatial data types is ambiguous.")

    result = None
    value, isValid = PCRaster.cellvalue(self, 0)

    if isValid:
        result = int(value)

    return result

def _float(self):
    if self.isSpatial():
        raise Exception(
             "The floating point value for PCRaster spatial data types is ambiguous.")

    result = None
    value, isValid = PCRaster.cellvalue(self, 0)

    if isValid:
        result = float(value)

    return result


# Some syntactic sugar to allow the use of operators on Field objects.
_PCRaster.Field.__and__ = pcrAnd
_PCRaster.Field.__rand__ = pcrRAnd
_PCRaster.Field.__or__ = pcrOr
_PCRaster.Field.__ror__ = pcrROr
_PCRaster.Field.__xor__ = pcrXOr
_PCRaster.Field.__invert__ = pcrNot

_PCRaster.Field.__ne__ = pcrNE
_PCRaster.Field.__eq__ = pcrEQ
_PCRaster.Field.__gt__ = pcrGT
_PCRaster.Field.__ge__ = pcrGE
_PCRaster.Field.__lt__ = pcrLT
_PCRaster.Field.__le__ = pcrLE

_PCRaster.Field.__mul__ = pcrMul
_PCRaster.Field.__rmul__ = pcrRMul
_PCRaster.Field.__div__ = pcrDiv
_PCRaster.Field.__rdiv__ = pcrRDiv
_PCRaster.Field.__floordiv__ = pcrFloorDiv
_PCRaster.Field.__rfloordiv__ = pcrRFloorDiv
_PCRaster.Field.__pow__ = pcrPow
_PCRaster.Field.__rpow__ = pcrRPow
_PCRaster.Field.__mod__ = pcrMod
_PCRaster.Field.__rmod__ = pcrRMod
_PCRaster.Field.__add__ = pcrAdd
_PCRaster.Field.__radd__ = pcrRAdd
_PCRaster.Field.__sub__ = pcrSub
_PCRaster.Field.__rsub__ = pcrRSub

_PCRaster.Field.__neg__ = pcrNeg
_PCRaster.Field.__pos__ = pcrPos
_PCRaster.Field.__nonzero__ = _bool  # pcrNonzero


_PCRaster.Field.__bool__ = _bool
_PCRaster.Field.__int__ = _int
_PCRaster.Field.__float__ = _float
