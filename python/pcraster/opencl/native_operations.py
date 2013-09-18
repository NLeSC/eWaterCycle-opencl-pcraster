'''
Operations implemented using pcraster

Created on May 8, 2013

@author: niels
'''

import pcraster.operations as pcr_operations
from pcraster.opencl.field import Field
import types

def to_pcr(argument):
    if isinstance(argument, types.StringTypes) or isinstance(argument, types.IntType) or isinstance(argument, types.LongType) or isinstance(argument, types.FloatType):
        #filenames and primitive number types handled by pcraster
        return argument
    elif isinstance(argument, Field):
        return argument.toPcr()
    else:
        raise Exception('OpenCL PCRaster cannot handle argument: ' + str(argument))
    
def from_pcr(result):
    #print 'converting from pcr ' + str(result)

    return Field(result)


#     #normal case, result is a map
#     if result.isSpatial():
#         return Field(result)
#      
#     #corner case: result is a single number (or boolean). Return a standard python value
#      
#     value, isValid = _pcraster.cellvalue(result, 0)
#      
#     if not isValid:
#         print 'not valid'
#         return None 
#     elif result.dataType() == _pcraster.Boolean:
#         print 'boolean'
#         return bool(value)
#     elif result.dataType() == _pcraster.Scalar:
#         print 'scalar'
#         return float(value)
#     elif result.dataType() == _pcraster.Nominal:
#         print 'nominal'
#         return int(value)
#     elif result.dataType() == _pcraster.Ordinal:
#         print 'ordinal'
#         return int(value)
#     elif result.dataType() == _pcraster.Directional:
#         print 'directional'
#         return float(value)
#     else:
#         raise Exception('Unsupported data type in conversion ' + str(result.dataType()))
    
def list_to_pcr(*arguments):
    result = [len(arguments)]
    
    for count, argument in enumerate(arguments):
        print count, '=', argument
        result[count] = to_pcr(argument)
    
    return result

    
def ifthen(arg1, arg2):
    return from_pcr(pcr_operations.ifthen(to_pcr(arg1), to_pcr(arg2)))

def ifthenelse(arg1, arg2, arg3):
    return from_pcr(pcr_operations.ifthenelse(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3)))

def pcrne(arg1, arg2):
    return from_pcr(pcr_operations.pcrne(to_pcr(arg1), to_pcr(arg2)))

def pcreq(arg1, arg2):
    return from_pcr(pcr_operations.pcreq(to_pcr(arg1), to_pcr(arg2)))

def pcrgt(arg1, arg2):
    return from_pcr(pcr_operations.pcrgt(to_pcr(arg1), to_pcr(arg2)))

def pcrge(arg1, arg2):
    return from_pcr(pcr_operations.pcrge(to_pcr(arg1), to_pcr(arg2)))

def pcrlt(arg1, arg2):
    return from_pcr(pcr_operations.pcrlt(to_pcr(arg1), to_pcr(arg2)))

def pcrle(arg1, arg2):
    return from_pcr(pcr_operations.pcrle(to_pcr(arg1), to_pcr(arg2)))

def min(arg1, *arg2):
    return from_pcr(pcr_operations.min(to_pcr(arg1), *list_to_pcr(*arg2)))

def max(arg1, *arg2):
    return from_pcr(pcr_operations.max(to_pcr(arg1), *list_to_pcr(*arg2)))

def cover(arg1, *arg2):
    return from_pcr(pcr_operations.cover(to_pcr(arg1), *list_to_pcr(*arg2)))

# def timeinput(arg1):
# def timeinputsparse(arg1):
# def timeinputmodulo(arg1, arg2):
# def lookupmapstack(arg1, arg2):
# def spreadmax(arg1, arg2, arg3, arg4):
# def spreadmaxzone(arg1, arg2, arg3, arg4):

def spread(arg1, arg2, arg3):
    return from_pcr(pcr_operations.spread(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3)))

def spreadzone(arg1, arg2, arg3):
    return from_pcr(pcr_operations.spreadzone(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3)))

# def spreadldd(arg1, arg2, arg3, arg4):
# def spreadlddzone(arg1, arg2, arg3, arg4):
# def dynamicwaveq(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16):
# def dynamicwaveh(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12, arg13, arg14, arg15, arg16):
# def order(arg1):
# def areaorder(arg1, arg2):
# def argorder(*arg1):
# def argorderwithid(arg1, arg2):
# def argorderarealimited(arg1, arg2):
# def argorderwithidarealimited(arg1, arg2, arg3):
# def argorderaddarealimited(arg1, arg2, arg3):
# def argorderwithidaddarealimited(arg1, arg2, arg3, arg4):
# def windowminimum(arg1, arg2):
# def brenner(arg1, arg2, arg3, arg4, arg5, arg6):
# def windowmaximum(arg1, arg2):
# def windowdiversity(arg1, arg2):
# def areadiversity(arg1, arg2):
# def areamajority(arg1, arg2):
# def windowmajority(arg1, arg2):

def pcrmul(arg1, arg2):
    return from_pcr(pcr_operations.pcrmul(to_pcr(arg1), to_pcr(arg2)))

def pcrfdiv(arg1, arg2):
    return from_pcr(pcr_operations.pcrfdiv(to_pcr(arg1), to_pcr(arg2)))

def pcrpow(arg1, arg2):
    return from_pcr(pcr_operations.pcrpow(to_pcr(arg1), to_pcr(arg2)))

def pcrmod(arg1, arg2):
    return from_pcr(pcr_operations.pcrmod(to_pcr(arg1), to_pcr(arg2)))

def pcridiv(arg1, arg2):
    return from_pcr(pcr_operations.pcridiv(to_pcr(arg1), to_pcr(arg2)))

def pcruadd(arg1):
    return from_pcr(pcr_operations.pcruadd(to_pcr(arg1)))

def pcrumin(arg1):
    return from_pcr(pcr_operations.pcrumin(to_pcr(arg1)))

def pcrbadd(arg1, arg2):
    return from_pcr(pcr_operations.pcrbadd(to_pcr(arg1), to_pcr(arg2)))

def pcrbmin(arg1, arg2):
    return from_pcr(pcr_operations.pcrbmin(to_pcr(arg1), to_pcr(arg2)))

def timeinputscalar(arg1, arg2):
    return from_pcr(pcr_operations.timeinputscalar(to_pcr(arg1), to_pcr(arg2)))

# def timeinputdirectional(arg1, arg2):
# def timeinputboolean(arg1, arg2):
# def timeinputldd(arg1, arg2):
# def timeinputnominal(arg1, arg2):
# def timeinputordinal(arg1, arg2):
# def lookupnominal(arg1, *arg2):
# def lookupboolean(arg1, *arg2):
# def lookupordinal(arg1, *arg2):

def lookupscalar(arg1, *arg2):
    return from_pcr(pcr_operations.lookupscalar(to_pcr(arg1), *list_to_pcr(*arg2)))

# def lookuplinear(arg1, arg2):
# def lookupdirectional(arg1, *arg2):
# def lookupldd(arg1, *arg2):
# def indexnominal(arg1):
# def indexboolean(arg1):
# def indexordinal(arg1):
# def indexscalar(arg1):
# def indexdirectional(arg1):
# def indexldd(arg1):
# def indextable(arg1):
# def index(arg1):

def ldd(arg1):
    return from_pcr(pcr_operations.ldd(to_pcr(arg1)))

def directional(arg1):
    return from_pcr(pcr_operations.directional(to_pcr(arg1)))

def scalar(arg1):
     return from_pcr(pcr_operations.scalar(to_pcr(arg1)))
    
def boolean(arg1):
    return from_pcr(pcr_operations.boolean(to_pcr(arg1)))


def nominal(arg1):
    return from_pcr(pcr_operations.nominal(to_pcr(arg1)))

def ordinal(arg1):
    return from_pcr(pcr_operations.ordinal(to_pcr(arg1)))

def pcrand(arg1, arg2):
    return from_pcr(pcr_operations.pcrand(to_pcr(arg1), to_pcr(arg2)))

def pcror(arg1, arg2):
    return from_pcr(pcr_operations.pcror(to_pcr(arg1), to_pcr(arg2)))

def pcrxor(arg1, arg2):
    return from_pcr(pcr_operations.pcrxor(to_pcr(arg1), to_pcr(arg2)))

def pcrnot(arg1):
    return from_pcr(pcr_operations.pcrnot(to_pcr(arg1)))

def sin(arg1):
    return from_pcr(pcr_operations.sin(to_pcr(arg1)))

def cos(arg1):
    return from_pcr(pcr_operations.cos(to_pcr(arg1)))

def tan(arg1):
    return from_pcr(pcr_operations.tan(to_pcr(arg1)))

def asin(arg1):
    return from_pcr(pcr_operations.asin(to_pcr(arg1)))

def acos(arg1):
    return from_pcr(pcr_operations.acos(to_pcr(arg1)))

def atan(arg1):
    return from_pcr(pcr_operations.atan(to_pcr(arg1)))

def abs(arg1):
    return from_pcr(pcr_operations.abs(to_pcr(arg1)))

def exp(arg1):
    return from_pcr(pcr_operations.exp(to_pcr(arg1)))

# def fac(arg1):
# def rounddown(arg1):
# def ln(arg1):
# def log10(arg1):
# def roundup(arg1):
# def roundoff(arg1):

def sqrt(arg1):
    return from_pcr(pcr_operations.sqrt(to_pcr(arg1)))

# def sqr(arg1):
def normal(arg1):
    return from_pcr(pcr_operations.normal(to_pcr(arg1)))

# def uniform(arg1):

def xcoordinate(arg1):
    return from_pcr(pcr_operations.xcoordinate(to_pcr(arg1)))
    

def ycoordinate(arg1):
    return from_pcr(pcr_operations.ycoordinate(to_pcr(arg1)))
        
        
# def uniqueid(arg1):
# def move(arg1, arg2, arg3):
# def shift(arg1, arg2, arg3):
# def shift0(arg1, arg2, arg3):
# def celllength():
# def cellarea():
# def time():
# def timeslice():

def mapnormal():
    print 'calling map normal'
    return from_pcr(pcr_operations.mapnormal())
    
# def mapuniform():
# def succ(arg1):
# def pred(arg1):
# def pit(arg1):
# def nodirection(arg1):

def mapminimum(arg1):
    return from_pcr(pcr_operations.mapminimum(to_pcr(arg1)))
    
def mapmaximum(arg1):
    return from_pcr(pcr_operations.mapmaximum(to_pcr(arg1)))

def defined(arg1):
    return from_pcr(pcr_operations.defined(to_pcr(arg1)))

# def maparea(arg1):

def spatial(arg1):
    return from_pcr(pcr_operations.spatial(to_pcr(arg1)))

# def accustate(arg1, arg2):
# def accuflux(arg1, arg2):
# def muskingum(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9):
# def dynwavestate(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11):
# def dynwaveflux(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11):
# def lookupstate(arg1, arg2, arg3, arg4, arg5):
# def lookuppotential(arg1, arg2, arg3, arg4, arg5):
# def accucapacitystate(arg1, arg2, arg3):
# def accucapacityflux(arg1, arg2, arg3):

def accuthresholdstate(arg1, arg2, arg3):
    return from_pcr(pcr_operations.accuthresholdstate(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3)))

def accuthresholdflux(arg1, arg2, arg3):
    return from_pcr(pcr_operations.accuthresholdflux(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3)))
 
# def accufractionstate(arg1, arg2, arg3):
# def accufractionflux(arg1, arg2, arg3):
# def accutriggerstate(arg1, arg2, arg3):
# def accutriggerflux(arg1, arg2, arg3):

def accutraveltimestate(arg1, arg2, arg3):
    return from_pcr(pcr_operations.accutraveltimestate(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3)))

def accutraveltimeflux(arg1, arg2, arg3):
    return from_pcr(pcr_operations.accutraveltimeflux(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3)))
 
# def accutraveltimefractionremoved(arg1, arg2, arg3, arg4):
# def accutraveltimefractionstate(arg1, arg2, arg3, arg4):
# def accutraveltimefractionflux(arg1, arg2, arg3, arg4):
# def diffusestate(arg1, arg2, arg3):
# def diffuseflux(arg1, arg2, arg3):
# def kinwavestate(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8):
# def kinwaveflux(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8):
# def kinematic(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8):
# def timeoutput(arg1, arg2):

def maptotal(arg1):
    return from_pcr(pcr_operations.maptotal(to_pcr(arg1)))

# def mapand(arg1):
# def mapor(arg1):
# def areaarea(arg1):
# def clump(arg1):
# def drain(arg1, arg2):
# def path(arg1, arg2):
# def aspect(arg1):
# def slope(arg1):
# def window4total(arg1):
# def profcurv(arg1):
# def plancurv(arg1):
# def view(arg1, arg2):
# def extentofview(arg1, arg2):
# def inversedistance(arg1, arg2, arg3, arg4, arg5):
# def catchment(arg1, arg2):
# def subcatchment(arg1, arg2):
# def windowaverage(arg1, arg2):
# def markwhilesumle(arg1, arg2, arg3):
# def markwhilesumge(arg1, arg2, arg3):
# def ellipseaverage(arg1, arg2, arg3, arg4):
# def influencesimplegauss(arg1, arg2, arg3):
# def distributesimplegauss(arg1, arg2, arg3):
# def ibngauss(arg1, arg2, arg3):
# def horizontan(arg1, arg2):
# def catchmenttotal(arg1, arg2):
# def areamaximum(arg1, arg2):
# def areaminimum(arg1, arg2):
# def areaaverage(arg1, arg2):
# def areatotal(arg1, arg2):
# def areauniform(arg1):
# def areanormal(arg1):
# def windowtotal(arg1, arg2):
# def windowhighpass(arg1, arg2):

def ldddist(arg1, arg2, arg3):
    return from_pcr(pcr_operations.ldddist(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3)))

def upstream(arg1, arg2):
    return from_pcr(pcr_operations.upstream(to_pcr(arg1), to_pcr(arg2)))

# def streamorder(arg1):
# def transient(arg1, arg2, arg3, arg4, arg5, arg6, arg7):
# def downstream(arg1, arg2):
# def downstreamdist(arg1):
# def lddmask(arg1, arg2):

def lddrepair(arg1):
    return from_pcr(pcr_operations.lddrepair(to_pcr(arg1)))

# def slopelength(arg1, arg2):
def lddcreate(arg1, arg2, arg3, arg4, arg5):
    return from_pcr(pcr_operations.lddcreate(to_pcr(arg1), to_pcr(arg2), to_pcr(arg3), to_pcr(arg4), to_pcr(arg5)))
    
# def lddcreatedem(arg1, arg2, arg3, arg4, arg5):
# def lddcreatend(arg1, arg2, arg3, arg4, arg5):
# def lddcreatenddem(arg1, arg2, arg3, arg4, arg5):
# def riksfraction(arg1, arg2, arg3):
# def squarefraction(arg1, arg2, arg3):
# def gradx(arg1):
# def grady(arg1):
# def divergence(arg1, arg2):
# def diver(arg1, arg2, arg3, arg4):
# def lax(arg1, arg2):
# def laplacian(arg1):


