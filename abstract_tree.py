import sys


def _repr(obj):
    if isinstance(obj, list):
        return '[' + (',\n '.join((_repr(e).replace('\n', '\n ') for e in obj))) + '\n]'
    else:
        return repr(obj)




class Unit:
    __slots__ = ()

    def __repr__(self):
        result = self.__class__.__name__ + '('

        indent = ''
        separator = ''
        for name in self.__slots__[:-2]:
            result += separator
            result += indent
            result += name + '=' + (
                _repr(getattr(self, name)).replace('\n', '\n  ' + (' ' * (len(name) + len(self.__class__.__name__)))))

            separator = ','
            indent = '\n ' + (' ' * len(self.__class__.__name__))

        result += indent + ')'

        return result



class Root(Unit):
    __slots__ = ('ext', 'coord', '__weakref__')
    def __init__(self, ext, coord=None):
        self.ext = ext
        self.coord = coord



class While(Unit):
    __slots__ = ('cond', 'stmt', 'coord', '__weakref__')
    def __init__(self, cond, stmt, coord=None):
        self.cond = cond
        self.stmt = stmt
        self.coord = coord





class If(Unit):
    __slots__ = ('cond', 'iftrue', 'iffalse', 'coord', '__weakref__')
    def __init__(self, cond, iftrue, iffalse, coord=None):
        self.cond = cond
        self.iftrue = iftrue
        self.iffalse = iffalse
        self.coord = coord




class Suite(Unit):
    __slots__ = ('block_items', 'coord', '__weakref__')
    def __init__(self, block_items, coord=None):
        self.block_items = block_items
        self.coord = coord


class EmptyStatement(Unit):
    __slots__ = ('coord', '__weakref__')
    def __init__(self, coord=None):
        self.coord = coord



# [('exprs[0]', 12), ('exprs[1]', 12), ('exprs[2]', 13), ('exprs[3]', 14), ('exprs[4]', 15)]
class ExprList(Unit):
    __slots__ = ('exprs', 'coord', '__weakref__')
    def __init__(self, exprs, coord=None):
        self.exprs = exprs
        self.coord = coord



class BinaryOp(Unit):
    __slots__ = ('op', 'left', 'right', 'coord', '__weakref__')
    def __init__(self, op, left, right, coord=None):
        self.op = op
        self.left = left
        self.right = right
        self.coord = coord



class UnaryOp(Unit):
    __slots__ = ('op', 'expr', 'coord', '__weakref__')
    def __init__(self, op, expr, coord=None):
        self.op = op
        self.expr = expr
        self.coord = coord


class Digit(Unit):
    __slots__ = ('type', 'value', 'coord', '__weakref__')
    def __init__(self, type, value, coord=None):
        self.type = type
        self.value = value
        self.coord = coord




class ID(Unit):
    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord





class Declaration(Unit):
    __slots__ = ('type', 'name', 'init', 'pos', '__weakref__')
    def __init__(self, type, name, init):
        self.type = type
        self.name = name
        self.init = init



class Decl(Unit):
   __slots__ = ('declArray', 'pos', '__weakref__')
   def __init__(self, Array):
       self.declArray= Array




class TypeDecl(Unit):
    __slots__ = ('declname', 'type', 'coord', '__weakref__')
    def __init__(self, declname, type, coord=None):
        self.declname = declname
        self.type = type
        self.coord = coord



class IdentifierType(Unit):
    __slots__ = ('names', 'coord', '__weakref__')
    def __init__(self, names, coord=None):
        self.names = names
        self.coord = coord




class BOOL_TOF(Unit):
    __slots__ = ("true_or_false", 'coord', '__weakref__')
    def __init__(self, name, coord=None):
        self.true_or_false = name



# обрабатывает a = INC a
class Assignment(Unit):
    __slots__ = ('op', 'lvalue', 'rvalue', 'coord', '__weakref__')
    def __init__(self, op, lvalue, rvalue, coord=None):
        self.op = op
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.coord = coord




class FunctionDecl(Unit):
    __slots__ = ('ret_values','name', 'args', 'suite', 'coord', '__weakref__')
    def __init__(self, ret_values, name, args, suite, coord=None):
        self.ret_values = ret_values
        self.name = name
        self.args = args
        self.suite = suite
        self.coord = coord





#  в построении дерева не участвует, нужен для обработки вызова функции
class FunctionCall(Unit):
    __slots__ = ('name', 'suite', 'coord', '__weakref__')
    def __init__(self,  name,  suite, coord=None):
        self.name = name
        self.suite = suite
        self.coord = coord



class CallFunction(Unit):
    __slots__ = ('ret_values','name', 'args', 'coord', '__weakref__')
    def __init__(self, ret_values, name, args,  coord=None):
        self.ret_values = ret_values
        self.name = name
        self.args = args






class ParamList(Unit):
    __slots__ = ('params', 'coord', '__weakref__')
    def __init__(self, params, coord=None):
        self.params = params
        self.coord = coord







class Vector(Unit):
    __slots__ = ('type', 'name', 'array', 'coord', '__weakref__')

    def __init__(self, type, name, array, coord=None):
        self.type = type
        self.name = name
        self.array = array
        self.coord = coord


class DoubleVector(Unit):
    __slots__ = ('type', 'name', 'list', 'coord', '__weakref__')

    def __init__(self, type, name, list, coord=None):
        self.type = type
        self.name = name
        self.list = list
        self.coord = coord



class TypeVector(Unit):
    __slots__ = ('names', 'coord', '__weakref__')
    def __init__(self, names, coord=None):
        self.names = names
        self.coord = coord



class SizeArray1(Unit):
    __slots__ = ('name', 'coord', '__weakref__')
    def __init__(self, name, coord=None):
        self.name = name
        self.coord = coord




class SizeArray2(Unit):
    __slots__ = ('name','index','coord', '__weakref__')

    def __init__(self, name, index, coord=None):
        self.name = name
        self.index = index
        self.coord = coord


class ArrayExtend1(Unit):
    __slots__ = ('name', 'size', 'coord', '__weakref__')
    def __init__(self, name, size, coord=None):
        self.name = name
        self.size = size
        self.coord = coord

class ArrayExtend2(Unit):
    __slots__ = ('name', 'index', 'size', 'coord', '__weakref__')
    def __init__(self, name, index, size, coord=None):
        self.name = name
        self.index = index
        self.size = size
        self.coord = coord


class CallArrayElement(Unit):
    __slots__ = ('name', 'index', 'coord', '__weakref__')
    def __init__(self, name, index, coord=None):
        self.name = name
        self.index = index
        self.coord = coord


class CallDoubleArrayElement(Unit):
    __slots__ = ('name', 'index_1', 'index_2', 'coord', '__weakref__')
    def __init__(self, name, index_1, index_2, coord=None):
        self.name = name
        self.index_1 = index_1
        self.index_2 = index_2
        self.coord = coord




class RobotOperator(Unit):
    __slots__ = ('operator', 'coord', '__weakref__')
    def __init__(self, operator, coord=None):
        self.operator = operator
        self.coord = coord



# последние две решил не использовать

class DoubleVectorList(Unit):
    __slots__ = ('list1', 'list2', 'coord', '__weakref__')

    def __init__(self, list1, list2, coord=None):
        self.list1 = list1
        self.list2 = list2
        self.coord = coord

class VectorList(Unit):
    __slots__ = ('list1', 'list2', 'coord', '__weakref__')

    def __init__(self, list1, coord=None):
        self.list1 = list1
        self.coord = coord
