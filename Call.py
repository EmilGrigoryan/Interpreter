# coding=utf8


from parser import build_tree


# data = '''
# IF (9)
# {
# }
# ELSE
# {
#
# }
# IF (10)
# {
# }
# WHILE (100) DO
# {
# UINT a = 500
# UINT b = 500
# }
#
#
# IF (a)
# {
# }
# UINT a = 100
# BOOLEAN b = 100
# CUINT r = 500, t = 300, r = 200
# '''

# data = '''
# UINT a = 100
# WHILE (TRUE) DO
# {
#    a = INC a
#    BOOLEAN f = FALSE
# }
# '''
# data = '''
# UINT a = 100
# a = INC 100
# '''


#
# data = '''
# [UINT a = 5, BOOLEAN f = FALSE]  FUNCTION name ( UINT f = 5 )
# {
#     a = INC 5
# }
# '''

# data = '''
# UINT h =100
# UINT a = 5 FUNCTION name ( UINT f = 5 )
# {
#
# }
# '''
#
# data = '''
# a
# '''

#
#
# data = '''
# [a] = nameFunc(1, 2, 3, 5)
# UINT f = 100
# [UINT g = 100, BOOLEAN h = 100] FUNCTION name(UINT a, BOOLEAN g = FALSE)
# {
# }
# '''

# data = '''
# UINT a = 100, b
# '''
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
#     IF (c == 123)
#     {
#         c = y
#     }
# }
# UINT h = 1
# UINT a, b, c
# [a, b, c] = nameFunc(123, h)
# '''





# data = '''
# IF (c == 123)
# {
#     c = y
# }
#
# '''
# data = '''
#     IF (c == 123)
#     {
#         c = y
#     }
# '''


# data= '''
# UINT a = 123
# UINT b
# UINT c FUNCTION funcName(UINT v, UINT g, UINT j)
# {
# }
# '''

# data = '''
# UINT f = 5
# DARRAYOFUINT_1 a = [1, 2]
# DARRAYOFUINT_1 b = [1, 2]
# [UINT a = 2, UINT f = 5] FUNCTION fname(UINT q = 0, UINT t = 4)
# {
#
# }
# UINT g = 6
# [a, g] = fname(1, 5)
# '''
#
# data = '''
# DARRAYOFUINT_2 a = [1, 2, 3; 4, 5, 6, 7, 8, 9]
# DARRAYOFBOOLEAN_2 sdf = [FALSE, NOT g, 5; 1, 2, 3, 4, 5; 1, 2, 3, 4, 5; 12, 3, 234,      1 , NOT a ,3]
# '''
# data = '''
# DARRAYOFUINT_2 a = [1, 2, 3; 4, 5, 6, 7, 8, 9]
# DARRAYOFBOOLEAN_2 f = [1, 2, 3, FALSE; NOT 9, TRUE, 1]
# '''
# data = '''
# UINT a = 100
# BOOLEAN f = NOT a
# '''
#
# data = '''
# SIZE2 name[4]
# '''
#
# data = '''
# EXTEND2 a[1] 5
# '''
#
# data = '''
# DARRAYOFUINT_1 df = [1, 2, 3, 4]
# EXTEND1 df 5
# DARRAYOFUINT_2 d = [1, 2, 3, 4; 2, 1, 3, 4]
# EXTEND2 d[1] 5
# DARRAYOFBOOLEAN_2 r = [2, 1, 3, NOT 0;  9< 0, 456]
# '''


# data = '''
# [UINT a = 0] FUNCTION fib(UINT n = 0 )
# {
#     IF (n == 1 OR n==2)
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
# [a] = fib(20)
# '''


# data = '''
# DARRAYOFUINT_2 doubleAr = [1, 2, 3, 4; 1, 2, 3, 4, 5]
# UINT g = doubleAr[1, 2]
# '''

# data = '''
# DARRAYOFUINT_2 y
# EXTEND1 y 3
# EXTEND2 y[2] 2
# DARRAYOFUINT_2 try = [2, 1, 3; 1, 2, 1, 2, 3; 3, 3, 3, 3, 3]
# EXTEND2 try[1] 4
# EXTEND1 try 3
# EXTEND2 try[3] 5
# '''


# data = '''
# [UINT a = 5, DARRAYOFUINT_1 f = [1, 2, 4]] FUNCTION func(UINT a = 1, DARRAYOFBOOLEAN_2 g = [1, 2, 3; 2, 3, 1])
# {
#     DARRAYOFUINT_1 g = [1, 1, 1, 1, 1]
# }
#
# [a, b, c] = func(1, 2)
# '''
# data = '''
# DARRAYOFUINT_2 map = [1, 1, 1, 1, 1, 1, 1;1, 1, 1, 1, 1, 1, 1;1, 1, 1, 1, 1, 1, 1;1, 1, 1, 1, 1, 1, 1;1, 1, 1, 1, 1, 1, 1;1, 1, 1, 1, 1, 1, 1;1, 1, 1, 1, 1, 1, 1]
# DARRAYOFUINT_1 start = [1, 2]
# UINT w = map[1, 2]
# map[1, 2] = 2
# '''


# data = '''
# DARRAYOFUINT_1 start = [1, 2]
# UINT fffff = start[0]
# '''

# data = '''
# UINT fffff = start[1]
# start[10] = 12345
# FORW
# '''

# data ='''
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
# DARRAYOFUINT_1 df = [1, 2, 3, 4]
# EXTEND1 df 5
# DARRAYOFUINT_2 d = [1, 2, 3, 4; 2, 1, 3, 4]
# EXTEND2 d[1] 5
# DARRAYOFBOOLEAN_2 r = [2, 1, 3, NOT 0;  9< 0, 456]
# EXTEND1 r 10
# DARRAYOFUINT_2 a = [1, 2, 3; 4, 5, 6, 7, 8, 9]
# DARRAYOFBOOLEAN_2 f = [1, 2, 3, FALSE; NOT 9, TRUE, 1]
#
#
#
#
# UINT a = 1
# UINT f = 12345
# '''
#
# data = '''
# [UINT dir = 0, UINT size = 0] FUNCTION min(UINT first = 0, UINT second = 0)
# {
#     IF(first < second)
#     {
#         dir = 1
#         size = first
#     }
#     ELSE
#     {
#         dir = 2
#         size = second
#     }
# }
# '''
# '''[UINT dir = 0] FUNCTION new(UINT first = 0, UINT second = 0, UINT third = 0, UINT fourth = 0)
# {
#     UINT direction, min
#     [direction, min] = min(first, second)
#     [direction, min] = min(min, third)
#     [direction, min] = min(min, fourth)
#     dir = direction
# }
# '''

# data = '''
# [UINT dir = 0, UINT size = 0] FUNCTION check_walls(UINT MAX = 0)
# {
#     UINT size_1
#     PUSHF
#     size1 = GETF
#     IF (size1 == MAX)
#     {
#         UNDO
#         PUSHR
#         size1 = GETF
#         IF (size1 = MAX)
#         {
#             UNDO
#             PUSHR
#             size1 = GETF
#             IF (size1 = MAX)
#             {
#                 UNDO
#                 PUSHR
#                 size1 = GETF
#                 IF (SIZE == MAX)
#                 {
#                     UNDO
#                 }
#             }
#         }
#     }
#     size = size1
#     dir = 0
# }
# '''

# data = '''
# WHILE (NOT flag) DO
# {
#     sizeF = GETF
#     sizeB = GETB
#     sizeR = GETR
#     sizeL = GETL
#     [direction, size] = new(sizeF, sizeB, sizeR, sizeL)
#     IF (size == MAX)
#     {
#         [direction, size] = check_walls(MAX)
#     }
#     IF (size == MAX)
#     {
#         flag = TRUE
#     }
#     ELSE
#     {
#         IF (size == 1)
#         {
#             flag = TRUE
#         }
#         ELSE
#         {
#             IF (direction == 0)
#             {
#                 FORW
#             }
#             ELSE
#             {
#                 IF (direction == 1)
#                 {
#                     BACK
#                 }
#                 ELSE
#                 {
#                     IF (direction == 2)
#                     {
#                         RIGHT
#                     }
#                     ELSE
#                     {
#                         LEFT
#                     }
#                 }
#             }
#         }
#     }
# }
# '''


# data ='''
# IF ()
# {
#
# }
# '''

# data = '''
#
#
#
#
#
#
# WHILE (a)
# {
# }
# '''

# data = '''
# [UINT a = 0] FUNCTION (UINT w = 12)
# {
#
#
# }
# '''
# data ='''
# INC
# '''
# data = '''
# IF(NOT NOT a)
# {
# }
#
# INC
#
# [UINT a = 0] FUNCTION (UINT w = 12)
# {
#
#
# }
#
# WHILE (a)
# {
# }
#
# IF ()
# {
#
# }
# '''

# data = '''
# UINT f = 12345 FUNCTION name1 (UINT f = 12, UINT g = 9)
# {
#
# }
#
# [d, a, d, , ] = name1(a, , , h, d, e, q, e)
#
# UINT f = 8, w = 1, j
# '''
#

data = '''
[UINT a = 1, UINT f = 6] FUNCTION sum (UINT q = 1, UINT t = 7)
{
    a = 0
}
'''


# Такое правило не работает
data = '''
a = func(1, 2, 3, 4)
'''


data = '''
d = fff(5)
'''
# # А так уже работает
# data = '''
# [a] = func(1, 2, 3, 4)
# '''


# С объявлением все работает, нужно сделать с вызовом функций
# data = '''
# UINT a FUNCTION name (UINT g)
# {
# }
# '''



# Этот фрагмент сворачивается, как присваивание, нужно исправить
# data = '''f = fname'''
# f = open('testD16.txt', 'r')
# data = f.read()
#
# print(data)
# data = '''
# [] = fname(,,)
# d = f(5)
#
# '''

data = '''
UINT a = 6
a = INC a
a = a + 2
'''

data = '''
IF(NOT NOT a)
{
}



[UINT a = 0] FUNCTION (UINT w = 12)
{


}

WHILE (a)
{
}

IF ()
{

}

IF (8)
{
} ELSE
{
}
'''



# нужно сделать так, чтобы это не работало
result = build_tree(data)
# print(result)