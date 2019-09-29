import parser
from parser import build_tree
import visit2_0
# data = '''
# UINT a = 100, f = 2000
# BOOLEAN g =  NOT 500
# BOOLEAN k = g
# UINT r = k
# UINT qwe = DEC 200, c = INC qwe
# BOOLEAN q = 0
# UINT al = false
# UINT t = a
# '''
# data = '''
# UINT a = 0
# BOOLEAN f = FALSE
# WHILE (a < 10) DO
# {
# a = INC a
# f = TRUE
# }
# '''
# data = '''
# UINT a = 10
# IF (a < 50)
# {
#     UINT e = 4
#     WHILE (e < 10) DO
#     {
#         e = INC e
#         IF (e > 7)
#             a = DEC a
#     }
# }
# ELSE
# {
# UINT h = 12345
# }
#
# [UINT a = 5, BOOLEAN f = FALSE]  FUNCTION name( UINT r = 5 )
# {
#     WHILE (a < 10) DO
#     {
#         a = INC a
#     }
# }
#
# BOOLEAN a = 123 FUNCTION name_1( UINT d = INC 5555)
# {
#
# }
#
# '''
# В WHILE есть небольшая ошибка, нужно исправить

# data = '''
# UINT f = 500
# [UINT r = 100, UINT h = 1, UINT c = 123] FUNCTION nameFunc(UINT a = 90, UINT g = 0)
# {
#     UINT y = 0
#     WHILE (r < f) DO
#     {
#         r = INC r
#         h = h + g
#         g = f
#         y = INC y
#     }
#     IF (c == 123 OR c == 5)
#     {
#         c = y
#     }
# }
# UINT h = 1
# UINT a, b, c
# [a, b, c] = nameFunc(123, h)
# '''


# data = '''
# UINT a = 5, b
# b = a
# b = 12345
# b = b + a
#
# '''







# data = '''
# DARRAYOFUINT_2 h = [1, 2, 3, 4, 5; 1, 2, 3, 4, 5; 2, 3, 1, 3, 4; 1, 2, 3, 1]
# DARRAYOFUINT_2 qwe = [2, 1, 3, 1; 2, 2, 1, FALSE, 3]
# h = qwe
# DARRAYOFUINT_1 y = [1, 2, 5]
# DARRAYOFUINT_2 t = [1, 2, 5; FALSE, TRUE, 1, 23]
# '''

# data = '''
# DARRAYOFBOOLEAN_1 u = [FALSE, NOT 0, 8 < 0, 8 == 8]
# DARRAYOFBOOLEAN_1 t = [TRUE]
# t = u
# '''


# для одинарных почму - то не рпботает


# data = '''
# DARRAYOFBOOLEAN_1 r = [1, 2, 3, 4, INC 9, TRUE]
# DARRAYOFBOOLEAN_1 q = [TRUE, 7 == 9, INC 6, 9]
# q = r
# DARRAYOFBOOLEAN_2 ghf = [1, 2, 3, 4, 5; 4, FALSE, 7, 12, 423]
# DARRAYOFBOOLEAN_2 ttt = [FALSE ; TRUE]
# ttt = ghf
# '''

# data = '''
# DARRAYOFUINT_2 y = [1, 2, 3;1]
# EXTEND1 y 7
# EXTEND2 y[4] 7
# '''


# data = '''
# DARRAYOFUINT_2 y = [1, 2; 1]
# EXTEND1 y 5
# EXTEND2 y[2] 2
# EXTEND1 y 3
# EXTEND2 y[5] 7
# DARRAYOFBOOLEAN_2 r
# EXTEND1 y 5
# '''


# data = '''
# [UINT i = 5, DARRAYOFUINT_1 f = [1, 2, 4], DARRAYOFBOOLEAN_2 qweb = [1, 1, 2; 1,1 , 2]] FUNCTION func(UINT a = 1, DARRAYOFUINT_1 h = [1, 2, 3, 4, 5])
# {
#     DARRAYOFUINT_1 qqq = [1, 2, 3, 1, 2]
#     f = h
#     i = a
#     DARRAYOFBOOLEAN_2 qwe = [FALSE, TRUE, 1, 2; TRUE, TRUE, FALSE]
#     qweb = qwe
# }
# UINT w = 7
# DARRAYOFUINT_1 t
# DARRAYOFUINT_1 r = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# UINT j = SIZE1 r
# DARRAYOFBOOLEAN_2 bbb
# [w, t, bbb] = func (SIZE1 r, r)
#
#
# '''
# data = '''
# DARRAYOFUINT_1 start = [1, 2]
# UINT fffff = start[1]
# UINT w = map[1, 2]
# map[1, 2] = TRUE
# start[1] = 12345
# FORW
# BACK
# FORW
# LEFT
# RIGHT
# RIGHT
# BACK
# FORW
# FORW
# BACK
# RIGHT
# RIGHT
# BACK
# RIGHT
# BACK
# FORW
# GETF
# GETB
# PUSHR
# GETL
# GETB
# RIGHT
# RIGHT
# LEFT
# FORW
# BACK
# RIGHT
# LEFT
# LEFT
# LEFT
# RIGHT
# FORW
# BACK
# FORW
# FORW
# RIGHT
# GETR
# FORW
# GETL
# LEFT
# GETL
# '''

# нельзя добалять только при инициализации в массивы

# data = '''
# DARRAYOFBOOLEAN_1 t
# DARRAYOFUINT_2 y
# EXTEND1 y 6
# EXTEND2 y[0] 4
# EXTEND2 y[1] 5
# '''



# data = '''
# UINT a
# BOOLEAN f
# UINT r = 5
#
# a = r
# f = f
# f = a
# f = r
# f = 0
# [UINT a = 12, BOOLEAN f = 6] FUNCTION fname (UINT g = 2, BOOLEAN fh = 0)
# {
#
#     a = g
#     fh = 0
#     IF (fh)
#     {
#         f = fh
#     }
#     ELSE
#     {
#         f = TRUE
#     }
#
#
#
# }
#
# [a, f] = fname(123, 0)
#
# '''


# data = '''
# UINT g = 7, h = 123456789
# BOOLEAN sdf = 145
# DARRAYOFUINT_1 b = [1, g, h]
# DARRAYOFBOOLEAN_1 qr = [FALSE, TRUE, 123, sdf, NOT 0, 9 < 7]
# UINT y = SIZE1 b
# g = b[2]
# '''

# data = '''
# DARRAYOFUINT_2 a = [1, 2, 3; 4, 5, 6, 7, 8, 9]
# DARRAYOFBOOLEAN_2 f = [1, 2, 3, FALSE; NOT 9, TRUE, 1]
# '''

# data = '''
# DARRAYOFBOOLEAN_1 a = [1, 2, 3, 4, NOT 0, 7 < 0, 9 == 0, 9 == 9]
# '''
#
# data = '''
# DARRAYOFBOOLEAN_2 a = [1, 2, 3, 4; 9 < 0; FALSE, 9 == 0, 9==1, NOT 0, NOT 1 == 0]
# DARRAYOFUINT_1 df = [1, 2, 3, 4]
# EXTEND1 df 1
# '''


# data = '''
# DARRAYOFUINT_2 f = [1, 2, 3, 4, 5; 1, 2, 3, 4, 5, 6; 4, 3, 1, 2, 3]
# UINT r = SIZE2 f[1]
# UINT a
# a = SIZE2 f[1]
# UINT t = SIZE1 f
# '''

# data = '''
# DARRAYOFUINT_1 df = [1, 2, 3, 4]
# EXTEND1 df 5
# DARRAYOFUINT_2 d = [1, 2, 3, 4; 2, 1, 3, 4]
# EXTEND2 d[1] 5
# DARRAYOFBOOLEAN_2 r = [2, 1, 3, NOT 0;  9< 0, 456]
# '''


# data = '''
# UINT a
# UINT b = a
#
# '''


# data = '''
# UINT k
# UINT g = 100
# k = g
# '''

# data = '''
# UINT a = 0
# a = INC a
# '''



# data = '''
# UINT a = 100, b
# UINT g = a
# '''


# data = '''
# UINT a = 5
#
# IF (a == 5 OR a == 6)
# {
#     a = INC a
# }
# '''

# data = '''
# UINT a = 5
# a = 6
#
# '''





# data = '''
# [UINT a = 0] FUNCTION fib(UINT n = 0 )
# {
#     IF (n == 1 OR n == 2)
#     {
#         a = 1
#     }
#     ELSE
#     {
#         UINT f, g
#         [g] = fib(n - 1)
#         [f] = fib(n - 2)
#         a = g + f
#     }
# }
# UINT a
# [a] = fib(10)
# '''


# data = '''
# DARRAYOFUINT_1 array = [2, 1, 5, 4, 3, 1, 5]
# UINT N = SIZE1 array
# UINT i = 0
# UINT j = 0
# UINT buf = 0
# WHILE (i < N - 1) DO
# {
#     WHILE (j < N - i - 1) DO
#     {
#         IF (array[j] > array[j + 1])
#         {
#             buf = array[j + 1]
#             array[j + 1] = array[j]
#             array[j] = buf
#         }
#         j = INC j
#     }
# i = INC i
# j = 0
# }
# '''

# data = '''
# UINT x = 1
# INC x
# '''
# data = '''
# UINT MAX = 2147483647
# DARRAYOFUINT_1 start = [1, 2]
# DARRAYOFUINT_2 two =  [1, 2, 3;2, 2, 2]
# UINT fffff = start[1]
# UINT w = map[1, 2]
# map[1, 2] = TRUE
# start[1] = 12345
# start[1] = GETR
# two[1, 1] = GETF
# UINT e = two[1, 1]
# FORW
# BACK
# FORW
# PUSHF
# RIGHT
# RIGHT
# RIGHT
# UNDO
# '''

# Робот с самого начала смотрит вперед

# напишу еще функцию, которая ищет минимальный из 4 (Она будет основной)


# что буду делать?

#  сначала нужно сделать с продвижением, потом без него
# WHILE(NOT
# flag) DO
# {
#     size1 = GETF
# size2 = GETB
# IF(size1 > size2)
# {
#
# }
#
# size3 = GETR
# size4 = GETL
#
# }
# data = '''
# [UINT a = 1, UINT f = 6] FUNCTION sum (UINT q = 100, UINT t = 7)
# {
# a = q + t
# }
# UINT y = 10
# UINT h = 8
# [h, ] = sum(, 89)
# PUSHL
# FORW
# UINT f = v
#
# '''
# data = '''
#
# UINT f =  r
# '''
# data = '''
# PUSHL
# FORW
# '''
# fd = open("fib.txt", 'r')
# print(fd.read())


# data = '''
# UINT a  = 1
# UINT b = 5
# a = INC b
# '''

data = '''

[UINT dir = 0, UINT size = 0] FUNCTION min(UINT first = 0, UINT num1 = 0, UINT second = 0, UINT num2 = 0)
{
    IF(first < second)
    {
        dir = num1
        size = first
    }
    ELSE
    {
        dir = num2
        size = second
    }
}
[UINT dir = 0, UINT size = 0] FUNCTION new(UINT first = 0, UINT second = 0, UINT third = 0, UINT fourth = 0)
{
    UINT direction, min
    [direction, min] = min(first, 0, second, 1)
    [direction, min] = min(min, direction, third, 2)
    [direction, min] = min(min, direction, fourth, 3)
    dir = direction
    size = min

}

[UINT dir = 0, UINT size = 0] FUNCTION check_walls(UINT MAX = 0)
{
    PUSHF
    UINT size1
    size1 = GETF
    IF (size1 == MAX)
    {
        UNDO
        PUSHR
        size1 = GETF
        IF (size1 == MAX)
        {
            UNDO
            PUSHR
            size1 = GETF
            IF (size1 == MAX)
            {
                UNDO
                PUSHR
                size1 = GETF
                IF (size1 == MAX)
                {
                    UNDO
                }
            }
        }
    }
    size = size1
    dir = 0
}


BOOLEAN flag = FALSE
UINT sizeF, sizeB, sizeR, sizeL, direction, size
WHILE (NOT flag) DO
{
    sizeF = GETF
    sizeB = GETB
    sizeR = GETR
    sizeL = GETL
    [direction, size] = new(sizeF, sizeB, sizeR, sizeL)
    IF (size == MAX)
    {
        [direction, size] = check_walls(MAX)
    }
    IF (size == MAX)
    {
        flag = TRUE
    }
    ELSE
    {
        IF (size == 1)
        {
            flag = TRUE
        }
        ELSE
        {
            IF (direction == 0)
            {
                FORW
            }
            ELSE
            {
                IF (direction == 1)
                {
                    BACK
                }
                ELSE
                {
                    IF (direction == 2)
                    {
                        RIGHT
                    }
                    ELSE
                    {
                        LEFT
                    }
                }
            }
        }
    }
}
'''








#
# data = '''
# DARRAYOFUINT_1 array = [2, 1,0,  5, 4, 3, 1, 5, 100, 4,  123,  1000, 2, 34, 21]
# UINT N = SIZE1 array
# UINT i = 0
# UINT j = 0
# UINT buf = 0
# WHILE (i < N - 1) DO
# {
#     WHILE (j < N - i - 1) DO
#     {
#         IF (array[j] > array[j + 1])
#         {
#             buf = array[j + 1]
#             array[j + 1] = array[j]
#             array[j] = buf
#         }
#         j = INC j
#     }
# i = INC i
# j = 0
# }
# '''






# data = '''
# [UINT a = 0] FUNCTION fib(UINT n = 0 )
# {
#     IF (n == 1 OR n == 2)
#     {
#         a = 1
#     }
#     ELSE
#     {
#         UINT f, g
#         [g] = fib(n - 1)
#         [f] = fib(n - 2)
#         a = g + f
#     }
# }
# UINT a
# [a] = fib(10)
# '''



data = data + '\n'


result = build_tree(data)
# print(result)
exec = visit2_0.bypass_ast()
exec.Read()
exec.visit(result)
exec.Print()
print(exec.decl_buf)