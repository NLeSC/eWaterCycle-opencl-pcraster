from pcraster import *
import ast
import sys
import compiler, inspect
from compiler.ast import Node
from pcraster import pcraster
import pcraster as pcr

class v(ast.NodeVisitor):
    def generic_visit(self, node):
        print type(node).__name__
        ast.NodeVisitor.generic_visit(self, node)

def calculateResult(originalMap):
    pass

def calculateResult(originalMap):
    """Calculate the result map by simple adding it to itself a fixed number of times"""
    
    result = originalMap
    
    for i in range(10):
        result = result - originalMap
        result  = max(-0.0004, result)
        
    return result



def accuTravelTime(self,landSurface,groundwater,currTimeStep,\
                                                      meteo=None):
        # input: self.runoff
        #        groundwater.demandFromSurfaceWater
                
        yMean = self.eta * pow (self.avgDischarge /\
                               vos.secondsPerDay(), self.nu)
        wMean = self.tau * pow (self.avgDischarge /\
                               vos.secondsPerDay(), self.phi)
        yMean = pcr.max(yMean,0.000000001)
        wMean = pcr.max(wMean,0.000000001)

        # TODO: Understand this operation
        self.characteristicDistance = \
             ( (yMean *   wMean)/ \
               (wMean + 2*yMean) )**(2./3.) * \
               (self.gradient)**pcr.spatial(pcr.scalar(0.5))/ \
                self.manningsN* vos.secondsPerDay()
        self.characteristicDistance =  \
        pcr.max(0.,self.characteristicDistance/self.dist2celllength)

        localQ = pcr.cover(pcr.max(0.,self.runoff*self.cellArea),0.)
        self.channelStorage += localQ

        # TODO: Activating reservoirs()
        deltaResStorage = pcr.spatial(pcr.scalar(0.0))
        self.resStorage = pcr.spatial(pcr.scalar(0.0))
        self.resIDMap   = pcr.spatial(pcr.nominal(0))

        self.channelStorage -= deltaResStorage
        self.channelStorage += pcr.upstream(self.lddMap,deltaResStorage)

        # surface water abstractions
        demand = pcr.cover(groundwater.demandFromSurfaceWater,0.0)
        self.riverAbstraction = pcr.min(self.channelStorage, demand)
        self.unmetDemand      = pcr.max(0., demand - self.riverAbstraction) / self.cellArea
        self.channelStorage   = pcr.max(0., self.channelStorage - self.riverAbstraction)
        
        # updating average discharge
        self.avgDischarge = self.avgDischarge
        if currTimeStep.timeStepPCR > 1:
            self.avgDischarge = (self.avgDischarge * \
                                       (currTimeStep.timeStepPCR -1) + \
                   pcr.ifthenelse(self.resIDMap != 0,\
                                 deltaResStorage, self.Q)) / \
                                        currTimeStep.timeStepPCR

        # channel discharge (m3/day)
        self.Q = pcr.accutraveltimeflux(self.lddMap,\
                                        self.channelStorage,\
                                        self.characteristicDistance)

        # updating channel storage
        self.channelStorage  = pcr.accutraveltimestate(\
                               self.lddMap,\
                               self.channelStorage,\
                               self.characteristicDistance)
        self.channelStorage += pcr.ifthenelse(self.resIDMap !=0,\
                                              self.Q, 0.0)
        
        # channel discharge (m3/s)
        self.discharge = pcr.ifthenelse(self.resIDMap != 0,\
                                        deltaResStorage,self.Q)/\
                                        vos.secondsPerDay()

"""
A pretty-printing dump function for the ast module.  The code was copied from
the ast.dump function and modified slightly to pretty-print.

Alex Leone (acleone ~AT~ gmail.com), 2010-01-30
"""
def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    """
    Return a formatted ast_dump of the tree in *node*.  This is mainly useful for
    debugging purposes.  The returned string will show the names and the values
    for fields.  This makes the code impossible to evaluate, so if evaluation is
    wanted *annotate_fields* must be set to False.  Attributes such as line
    numbers and column offsets are not dumped by default.  If this is wanted,
    *include_attributes* can be set to True.
    """
    def _format(node, level=0):
        if isinstance(node, ast.AST):
            fields = [(a, _format(b, level)) for a, b in ast.iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)
    if not isinstance(node, ast.AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)

class FuncLister(ast.NodeVisitor):
    def visit_FunctionDef(self, node):
        print "func def", node.name
        self.generic_visit(node)
        
    def visit_Call(self, node):
        print "call to ", node.func
        self.generic_visit(node)
        
    def visit_BinOp(self, node):
        print "binary operation ", node.op
        self.generic_visit(node)


def compile(function, **argumentTypes):
    for key in argumentTypes:
        print key
        print argumentTypes[key]

    functionModule = ast.parse(inspect.getsource(function))

    FuncLister().visit(functionModule)
    
    print dump(functionModule.body[0], include_attributes=True)
    
    return function


def main():
    setclone("Global_CloneMap_30min.map")

    inputMap = readmap("Global_InterceptCapacity-Grassland_0000-12-18_30min.map")
    
    kernel = compile(calculateResult)
    
    #kernel2 = compile(accuTravelTime, originalMap=int)
    
    result = kernel(inputMap)
    
    report(result, "result.map")

def printAst(ast, indent='  ', stream=sys.stdout, initlevel=0):
    "Pretty-print an AST to the given output stream."
    rec_node(ast, initlevel, indent, stream.write)
    stream.write('\n')

def rec_node(node, level, indent, write):
    "Recurse through a node, pretty-printing it."
    pfx = indent * level

    if isinstance(node, Node):
        write(pfx)
        write(node.__class__.__name__)
        write('(')

        if any(isinstance(child, Node) for child in node.getChildren()):
            for i, child in enumerate(node.getChildren()):
                if i != 0:
                    write(',')
                write('\n')
                rec_node(child, level+1, indent, write)
            write('\n')
            write(pfx)
        else:
            # None of the children as nodes, simply join their repr on a single
            # line.
            write(', '.join(repr(child) for child in node.getChildren()))

        write(')')

    else:
        write(pfx)
        write(repr(node))

if __name__ == "__main__":
    main()


