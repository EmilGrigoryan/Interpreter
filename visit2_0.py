import copy

import numpy as np

import sys

import abstract_tree as ast

from parser import function_dict

class bypass_ast:


    def __init__(self, error_flag=False):

        self.decl_buf = {'global' : {}}

        self._error_flag = error_flag


        self.array_type = ('DARRAYOFUINT_1', 'DARRAYOFBOOLEAN_1')
        self.double_array_type = ('DARRAYOFUINT_2', 'DARRAYOFBOOLEAN_2')


        self.robot_coord = [4, 5]
        self.out_coord = [8, 1] # number 3

        self.fd = open('result.txt', 'w')

        # at first i should to check a direction of robot

        self.direction = np.array([1, 0, 0, 0])

        # at first i see on the direction then to choose nonzero element in dictionary

        self.move_operators = ['FORW', 'BACK', 'RIGHT', 'LEFT']
        self.size_operators = ['GETF','GETB','GETR','GETL']
        self.push_operators = ['PUSHF', 'PUSHB', 'PUSHR', 'PUSHL']

        self.robot_turn = {
            'FORW' : lambda : self.goForw(),
            'BACK' : lambda : self.goBack(),
            'RIGHT': lambda : self.goRight(),
            'LEFT' : lambda : self.goLeft(),
            'GETF' : lambda : self.goForw(),
            'GETB' : lambda : self.goBack(),
            'GETR' : lambda : self.goRight(),
            'GETL' : lambda : self.goLeft(),
            'PUSHF': lambda : self.goForw(),
            'PUSHB': lambda : self.goBack(),
            'PUSHR': lambda : self.goRight(),
            'PUSHL': lambda : self.goLeft()
        }

        self.robot_undo = [False, [0, 0], [0, 0]]

        self.robot_move = {
             0 : lambda: self.update_map(self.robot_coord[0] - 1, self.robot_coord[1]), # forward
             1 : lambda: self.update_map(self.robot_coord[0] + 1, self.robot_coord[1]),  # back
             2 : lambda: self.update_map(self.robot_coord[0] , self.robot_coord[1] + 1), # right
             3 : lambda: self.update_map(self.robot_coord[0], self.robot_coord[1] - 1) # left

        }


        self.robot_found = {
             0 : lambda: self.find_path(self.robot_coord[0] - 1, self.robot_coord[1]), # forward
             1 : lambda: self.find_path(self.robot_coord[0] + 1, self.robot_coord[1]),  # back
             2 : lambda: self.find_path(self.robot_coord[0] , self.robot_coord[1] + 1), # right
             3 : lambda: self.find_path(self.robot_coord[0], self.robot_coord[1] - 1) # left

        }



        self.robot_push = {
             0 : lambda: self.push_wall(self.robot_coord[0] - 1, self.robot_coord[1]), # forward
             1 : lambda: self.push_wall(self.robot_coord[0] + 1, self.robot_coord[1]),  # back
             2 : lambda: self.push_wall(self.robot_coord[0] , self.robot_coord[1] + 1), # right
             3 : lambda: self.push_wall(self.robot_coord[0], self.robot_coord[1] - 1) # left

        }


        self.operators = {
            '<'  : lambda x, y: x <   y,
            '>'  : lambda x, y: x >   y,
            'OR' : lambda x, y: x or  y,
            '-'  : lambda x, y: x -   y,
            '+'  : lambda x, y: x +   y,
            '==' : lambda x, y: x ==  y
        }
        self.unary      = {
            'NOT': lambda x: not  x,
            'INC': lambda x: x + 1,
            'DEC': lambda x: x - 1
        }

        self.iter = 0


        # self.move_Back = {
        #     0 : lambda : self.direction,
        #     1 : lambda : forBack()
        # }

        # self.move_operators = ('FORW', 'BACK', 'RIGHT', 'LEFT')





    def Read(self):
        self.decl_buf['global']['map'] = ['DARRAYOFUINT_2', [[2, 2, 2, 2, 2, 2, 2, 2, 2],
                                                             [2, 1, 1, 1, 1, 1, 1, 1, 2],
                                                             [2, 1, 1, 1, 1, 1, 1, 1, 2],
                                                             [2, 1, 1, 0, 0, 1, 0, 0, 2],
                                                             [2, 1, 1, 0, 1, 0, 1, 1, 2],
                                                             [2 ,1, 1, 0, 0, 1, 0, 0, 2],
                                                             [2, 1, 1, 0, 0, 1, 0, 0, 2],
                                                             [2, 0, 0, 0, 0, 0, 0, 0, 2],
                                                             [2, 3, 2, 2, 2, 2, 2, 2, 2]]]

        # self.
        self.decl_buf['global']['MAX'] = ["UINT", sys.maxsize]
        self.decl_buf['global']['map'][1][self.robot_coord[0]][self.robot_coord[1]] = 5
        self.direction[0] = 1 # default forward

    def visit(self, node, scope_name='global'):
        function_name = 'visit_' + node.__class__.__name__
        return getattr(self, function_name)(node, scope_name=scope_name)


# поставлю по краям 2, чтобы не надо было делать много проверок на выход робота за рамки
    def Print(self):
        for i in self.decl_buf['global']['map'][1]:
            # print(i)
            self.fd.write(str(i) + '\n')
        self.fd.write("---------------------------------------------------" + '\n')

    def PrintN(self):
        for i in self.decl_buf['global']['map'][1]:
            # print(i)
            print(str(i) + '\n')
        print("---------------------------------------------------" + '\n')
        # self.


    def visit_Root(self, n, scope_name='global'):

        for ext in n.ext:
            self.visit(ext)


    def visit_Digit(self, n, scope_name='global'):
        return (int(n.value))





    # Теперь Id будет возвращать значение из списка или None, если его там нет
    def visit_ID(self, n, scope_name='global'):





        check = self.decl_buf[scope_name].get(n.name) #get возвращает None если элемент не существует
        # print('NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN', n.coord[0], n.coord[1])
        if not check:
            ref = self.decl_buf['global'].get(n.name)
            if not ref:
                print("Undeclared id {} on {}, {}".format(n.name, n.coord[0], n.coord[1]))
                self._error_flag = True
                return None
            return ref
        return check
    #Зачем столько раз нужно повторять? можно просто отправить идентификатор

    def visit_BOOL_TOF(self, n, scope_name='global'):
        if n.true_or_false == 'TRUE':
            return True
        return False

    #  унарный оператор только Not
    # если оператор является идентификатором, проверяем, чтобы он был именем переменной, иначе ОШИБКА
    # FALSE не обрабатывается, нужно включить
    def visit_UnaryOp(self, n, scope_name='global'):

        if type(n.expr) == ast.ID:
            ref = self.visit(n.expr, scope_name)
            return self.unary[n.op](ref[1]) # почему тут 1?
        return self.unary[n.op](self.visit(n.expr, scope_name=scope_name))
    # ищем в словаре операторов подходящий и передаем аргумент




    def visit_BinaryOp(self, n, scope_name='global'):




        if self._error_flag: # Видимо проблема может быть из-за флага
            return

        # готовлю левый операнд
        lvalue = self.visit(n.left, scope_name) # вернет или None или то, что надо (тип, значение)
        type_lvalue = type(lvalue)
        if type(n.left) == ast.ID:
            if not lvalue:
                print("Undec reference")
                self._error_flag = True
                return
            type_lvalue = lvalue[0]
            lvalue = lvalue[1] # присвоил значение
        # готовлю правый операнд

        rvalue = self.visit(n.right, scope_name=scope_name)
        type_rvalue = type(rvalue)
        if type(n.right) == ast.ID:
            if not rvalue:
                print("Undec reference")
                self._error_flag = True
                return
            type_rvalue = rvalue[0]
            rvalue = rvalue[1]  # присвоил значение

        flag, item = self.check_type(type_lvalue, lvalue, type_rvalue, rvalue)
        # print("-----------------------------------", flag, item)
        if flag:
            return self.operators[n.op](lvalue, rvalue)

        return



    def visit_Declaration(self, n, scope_name='global'):

        VarName = n.name.name # Нужно будет немного переделать потом (n.name - ID - класса)
        Type = self.visit(n.type, scope_name=scope_name)




        # проверка существования в области видимости переменной с таким именем
        if self.decl_buf[scope_name].get(VarName):
            print("Error at {}: redefinition of variable {} ".format(VarName, scope_name))
            self._error_flag = True
            return


        if n.init == None:
            # self.decl_buf[scope_name][VarName] = [Type, 0]
            flag, init = self.check_type(Type, None, int, 0)


            # типы подходящие
            if flag:
                self.decl_buf[scope_name][VarName] = [Type, init]
            else:
                print("Ошибка времени выполнения")
            return

        # print("N.init = ", n.init)

        val = self.visit(n.init, scope_name=scope_name) # то, чем будем инициализировать может приходить что-то из SIZE, например, но это будет число так что проблем нет

        # print("What ------ ", val)

        type_val = type(val)
        if type(n.init) == ast.ID:  # UINT a = b
            if not val:
                print("Undec reference")
                self._error_flag = True
                return
            type_val = val[0]
            val = val[1]

        flag, init = self.check_type(Type, None, type_val, val)

            # типы подходящие
        if flag:
            self.decl_buf[scope_name][VarName] = [Type, init]
        else:
            print("Ошибка времени выполнения")




    def visit_Decl(self, n, scope_name='global'):
        for i in n.declArray:
            self.visit(i, scope_name=scope_name)




    def visit_IdentifierType(self, n, scope_name='global'):
        return n.names



    def visit_TypeVector(self, n, scope_name='global'):
        return n.names





    # Сначала уловие добавляю в if <условие> , если условие прошло, то выполняю то, что было в iftrue
    # иначе, смотрю, если iffalse  не будет равно None, то вызову то, что лежит в iffalse
    def visit_If(self, n, scope_name='global'):

        if self._error_flag:
            pass

        condition = self.visit(n.cond, scope_name=scope_name)

        if type(n.cond) == ast.ID:
            if not condition:
                self._error_flag = True
                return

            condition = condition[1]


        if condition:
            return self.visit_Suite(n.iftrue, scope_name)
        else:
            if n.iffalse != None:
                return self.visit(n.iffalse, scope_name)
            else:
                return





    def visit_While(self, n, scope_name='global'):
        cnt = 0
        # print(n.cond)
        condition = self.visit(n.cond, scope_name=scope_name)
        # print(condition)
        if type(n.cond) == ast.ID:
            if not condition:
                self._error_flag = True
                return

            condition = condition[1]


        while condition:
            if cnt == 1000000:
                print("Runtime error at ")
                self._error_flag = True
                return


            cnt += 1
            # print(n.stmt)
            ret = self.visit(n.stmt, scope_name)

            if ret is not None:
                return ret

            condition = self.visit(n.cond, scope_name=scope_name)
            if type(n.cond) == ast.ID:
                if not condition:
                    self._error_flag = True
                    return

                condition = condition[1]




    # Нужно сделать массив, чтобы потом по нему проходить
    def visit_Suite(self, n, scope_name='global'):
        if n.block_items == None:
            return
        # print("BLOCK", n.block_items)
        for item in n.block_items:

            # одинокое объявление
            if type(item) in (ast.ID, ast.Digit):
                print("Error at {}: {} without target occured".format(item.coord, type(item)))
                self._error_flag = True
                continue
            self.visit(item, scope_name)




# пошла инициализация
    def visit_Assignment(self, n, scope_name='global'):

        lvalue = self.visit(n.lvalue, scope_name=scope_name)

        # если visit_ID вернул None - такого элемента не существует
        if lvalue == None:
            print("Необъявленный идентификатор")
            return




        rvalue = self.visit(n.rvalue, scope_name=scope_name)  # может быть бинарным выражением (добавляю, чтобы мог быть и массивом))
        # вылетало на этом месте
        type_rvalue = type(rvalue)






        if type(n.rvalue) == ast.ID:
            if not rvalue:
                print("Undec reference")
                self._error_flag = True
                return
            type_rvalue = rvalue[0]
            rvalue = rvalue[1]

        # print(self.decl_buf)

        # В начале была проверка на то, что переменная существует
        if self._error_flag:
            return


        if type(n.lvalue) == ast.CallArrayElement:
            value_t, index1 = self.test_for_array(n.lvalue, scope_name)
            if not value_t:
                return
            buf = value_t[1][index1]
            flag, rvalue = self.check_type(type(buf), buf, type_rvalue, rvalue)

            if not flag:
                return

            value_t[1][index1] = rvalue
            return  value_t[1][index1]



        if type(n.lvalue) == ast.CallDoubleArrayElement:
            value_t, index1, index2 = self.test_for_double_array(n.lvalue, scope_name)
            if not value_t:
                return
            buf = value_t[1][index1][index2]

            flag, rvalue = self.check_type(type(buf), buf, type_rvalue, rvalue)

            if not flag:
                return
            value_t[1][index1][index2] = rvalue
            return  value_t[1][index1][index2]



        flag, item = self.check_array_or_not(lvalue[0], lvalue[1], type_rvalue, rvalue, scope_name)


        if flag:
            if self.decl_buf[scope_name].get(n.lvalue.name):
                self.decl_buf[scope_name][n.lvalue.name][1] = item
                # print(self.decl_buf)
                return self.decl_buf[scope_name][n.lvalue.name][1]
            else:
                self.decl_buf['global'][n.lvalue.name][1] = item
                return self.decl_buf[scope_name][n.lvalue.name][1]
        else:
            print("Некорректные типы")
            return


    #Просто прошелся по аргументам и добавил переменные в словарь
    def visit_ParamList(self, n, scope_name='global'): # сюда в глобал будет передано имя функции
        for item in n.params:
            self.visit(item, scope_name)


    def check_array_or_not(self, type_lvalue, lvalue, type_rvalue, rvalue, scope_name):
        if type_rvalue == list or type_rvalue in self.double_array_type or type_rvalue in  self.array_type:  # тут нужна функция, которая будеп проверять тип
            if type_lvalue in self.double_array_type:
                flag, item = self.check_type_double_array(type_lvalue, lvalue, type_rvalue, rvalue, scope_name)
            else:
                flag, item = self.check_type_array(type_lvalue, lvalue, type_rvalue, rvalue)
        else:
            flag, item = self.check_type(type_lvalue, lvalue, type_rvalue, rvalue)

        return (flag, item)


    # call_function must to return return values
    def visit_FunctionDecl(self, n, scope_name='global'):
        # Добавлю новую область видимости
        self.decl_buf[n.name.name] = {}

        # Добавил аргументы в словарь
        self.visit(n.args, n.name.name)

        # Добавил возвращаемые значения в словарь
        self.visit(n.ret_values, n.name.name)








    def visit_CallFunction(self, n, scope_name='global'):



        if self._error_flag == True:
            return


        if not self.decl_buf.get(n.name.name):
            print("Function existing error")
            self._error_flag = True
            return


        # увеличивая переменную для количества вызовов функции
        function_dict[n.name.name][3] += 1
        count = function_dict[n.name.name][3]

        # формирую новое имя для области видимости имяфункции + _ +глубина рекурсии
        new_scope_name = n.name.name + "_" + str(count)


        # копирую словарь из области видимости, которой была вызвана функция
        self.decl_buf[new_scope_name] = copy.deepcopy(self.decl_buf[n.name.name])

        # области видимости меняю только тогда, когда обращаюсь в буферу

        func_dict = function_dict[n.name.name]





        # print("Заходит")
        if len(n.args) != len(func_dict[1]):
            self._error_flag = True
            print("Error number of variebles")
            del self.decl_buf[new_scope_name]

            # уменьшая счетчик глубины рекурсии
            function_dict[n.name.name][3] -= 1
            return
        else:

            # проверка вызова

            for i in range(len(n.args)):

                # print("Args", n.args[i])
                if type(n.args[i]) != ast.EmptyStatement:
                    value = self.visit(n.args[i], scope_name)



                # Те, которые пришли
                var_from_decl = self.decl_buf[new_scope_name][func_dict[1][i]] # Те, которые уже лежат в словаре после объявления

                # print("Уже лежат", var_from_decl)

                if type(n.args[i]) == ast.ID:
                    #  с массивами можем зайти только сюда
                    if not value:
                        self._error_flag = True
                        print("Error argument")
                        del self.decl_buf[new_scope_name]
                        function_dict[n.name.name][3] -= 1
                        return

                    # сюда нужно подставить проверку на массивы
                    flag, init = self.check_array_or_not(var_from_decl[0],var_from_decl[1], value[0], value[1], scope_name)# Пытаюсь сделать это функцией
                    if flag:
                        self.decl_buf[new_scope_name][func_dict[1][i]][1] = init
                    else:
                        print("Types error in call")
                        del self.decl_buf[new_scope_name]
                        function_dict[n.name.name][3] -= 1
                        return
                        # print("Type = ", flag, init)
                # # Новое
                elif type(n.args[i]) == ast.EmptyStatement:
                    pass


                else:
                    # print("Check type value", type(value), value)
                    # тут нужна проверка на массивы
                    flag, init = self.check_type(var_from_decl[0],var_from_decl[1], type(value), value)
                    if flag:
                        self.decl_buf[new_scope_name][func_dict[1][i]][1] = init
                    else:
                        print("Types error in call")
                        del self.decl_buf[new_scope_name]
                        function_dict[n.name.name][3] -= 1
                        return


            if len(n.ret_values) != len(func_dict[0]):
                print("Error numbers of return value")
            # print(func_dict[2])
            else:

                self.visit(func_dict[2].suite, new_scope_name)

            # Формирую возвращаемые значения
                for i in range(len(func_dict[0])):
                    var = self.decl_buf[new_scope_name][func_dict[0][i]]  # что положить
                    # Новое
                    if type(n.ret_values[i]) != ast.EmptyStatement:
                        var_out = self.decl_buf[scope_name][n.ret_values[i].name]
                        flag, init = self.check_array_or_not(var_out[0],var_out[1], var[0], var[1], scope_name)
                        if flag:
                            self.decl_buf[scope_name][n.ret_values[i].name][1] = init
                        else:
                            print("Error type of return values")


        # удаляю область видимости при выходе из функции
        del self.decl_buf[new_scope_name]

        # уменьшая счетчик глубины рекурсии
        function_dict[n.name.name][3] -= 1







# Предусмотрено реобразование типов из UINT в BOOLEAN  и наоборот
    def check_type(self, type_lvalue, lvalue,  type_rvalue, rvalue):




        if type_rvalue == 'UINT' or type_rvalue == 'CUINT' or type_rvalue == int:

            if type_lvalue == 'UINT' or type_lvalue == int:
                return (True, rvalue)
            elif type_lvalue == 'BOOLEAN' or type_lvalue == bool:

                if rvalue:       # Преобразование типов
                    return (True, True)
                else:
                    return (True, False)
            elif type_lvalue == 'CUINT' or type_lvalue == 'CBOOLEAN':
                print("Значения констант нельзя менять")
                return (False, None)

            else:
                return (False, None)



        if type_rvalue == 'BOOLEAN' or type_rvalue == 'CBOOLEAN' or type_rvalue == bool:
            # выражение после or не повлияет на присваивание, потому что нет типа bool, однако необходимо для бинарных выражений
            if type_lvalue == 'BOOLEAN' or type_lvalue == bool:
                return (True, rvalue)
            elif type_lvalue == 'UINT' or type_lvalue == int:
                if rvalue:
                    return (True, 1)
                else:
                    return (True, 0)
            else:
                return (False, None)

        return (False, None)


    # rvalue - массив массивов, type-rvalue - неважно
    def visit_Vector(self, n, scope_name='global'):

        VarName = n.name.name
        Type = self.visit(n.type, scope_name=scope_name)


        if self.decl_buf[scope_name].get(VarName):
            print("Error at {}: redefinition of variable {} ".format(VarName, scope_name))
            self._error_flag = True
            return

        # пока пустым оставлять нельзя
        if n.array == None:

            flag, init = self.check_type_array(Type, None, list, [], scope_name)


            if flag:
                self.decl_buf[scope_name][VarName] = [Type, init]
            else:
                print("Ошибка времени выполнения")
            return

        val = n.array  # то, чем будем инициализировать

        type_val = type(val)


        flag, init = self.check_type_array(Type, None, type_val, val, scope_name)

        # типы подходящие
        if flag:
            self.decl_buf[scope_name][VarName] = [Type, init]
        else:
            print("Ошибка времени выполнения")





    def visit_DoubleVector(self, n, scope_name='global'):

        VarName = n.name.name
        Type = self.visit(n.type, scope_name=scope_name)

        if self.decl_buf[scope_name].get(VarName):
            print("Error at {}: redefinition of variable {} ".format(VarName, scope_name))
            self._error_flag = True
            return



        # DARRAYOFBOOLEAN2 f   без инициализации (рассмотрю позже)
        if n.list == None:
            # self.decl_buf[scope_name][VarName] = [Type, 0]
            flag, init = self.check_type_double_array(Type, None, list, [], scope_name)

            # print(Type)
            # типы подходящие
            if flag:
                self.decl_buf[scope_name][VarName] = [Type, init]
            else:
                print("Ошибка времени выполнения")
            return

         # то, чем будем инициализировать
        val = n.list # массив массивов

        type_val = type(val)

        flag, init = self.check_type_double_array(Type, None, type_val, val, scope_name)

        # типы подходящие
        if flag:
            self.decl_buf[scope_name][VarName] = [Type, init]
        else:
            print("Ошибка времени выполнения")


    def check_type_double_array(self, type_lvalue, lvalue,  type_rvalue, rvalue, scope_name=None):

        # буду возвращать флаг и массив массивов


        if type_lvalue == self.double_array_type[0]:
            type_lvalue = self.array_type[0]
        else:
            type_lvalue = self.array_type[1]


        double_array = []




        for item in rvalue:

            flag, value = self.check_type_array(type_lvalue, lvalue, list, item)



            if not flag:
                return (False, [])

            double_array.append(value)

        return (True, double_array)





    def check_type_array(self, type_lvalue, lvalue,  type_rvalue, rvalue, scope_name=None):


        ret_list = []


        if type_lvalue == 'DARRAYOFUINT_1' or type_lvalue == list:

            if type_rvalue == 'DARRAYOFUINT_1':
                return (True, rvalue)


            if type_rvalue == 'DARRAYOFBOOLEAN_1':

                for item in rvalue:

                    flag, value = self.check_type('UINT', None, type(item), item)
                    if not flag:
                        return (False, 0)
                    ret_list.append(value)

                return (True, ret_list)


            if type_rvalue == list:


                for item in rvalue:


                    if type(item) in (ast.Digit, ast.BOOL_TOF, ast.UnaryOp, ast.BinaryOp):
                        value = self.visit(item, scope_name)
                        # print("Value", value)
                        flag, value = self.check_type('UINT', None, type(value), value)
                        if not flag:
                            return (False, [])

                    elif type(item) == ast.ID:  # UINT a = b
                        val = self.visit_ID(item, scope_name)
                        if not val:
                            print("Undec reference")
                            self._error_flag = True
                            return (False, 0)
                        type_val = val[0]
                        val = val[1]

                        flag, value = self.check_type('UINT', None, type_val, val)
                        if not flag:
                            return (False, 0)

                    # нужно для копирования
                    elif type(item) == int:
                        value = item

                    else:
                        print("Error")
                        self._error_flag = True
                        return (False, 0)
                    ret_list.append(value)

                return (True, ret_list)


        if type_lvalue == 'DARRAYOFBOOLEAN_1' or type_lvalue == list:

            if type_rvalue == 'DARRAYOFBOOLEAN_1':
                return (True, rvalue)


            if type_rvalue == 'DARRAYOFUINT_1':

                for item in rvalue:

                    flag, value = self.check_type('BOOLEAN', None, type(item), item)
                    if not flag:
                        return (False, 0)
                    ret_list.append(value)

                return (True, ret_list)





            if type_rvalue == list:

                for item in rvalue:




                    if type(item) in (ast.Digit, ast.BOOL_TOF, ast.UnaryOp, ast.BinaryOp):
                        value = self.visit(item, scope_name)
                        # print("Value", value)
                        flag, value = self.check_type('BOOLEAN', None, type(value), value)
                        if not flag:
                            return (False, [])



                    elif type(item) == ast.ID:  # UINT a = b
                        val = self.visit_ID(item, scope_name)

                        if not val:
                            print("Undec reference")
                            self._error_flag = True
                            return (False, [])
                        type_val = val[0]
                        val = val[1]

                        flag, value = self.check_type('BOOLEAN', None, type_val, val)
                        if not flag:
                            return (False, [])


                    elif type(item) == bool:
                        value = item


                    ret_list.append(value)

                return (True, ret_list)






    def visit_SizeArray1(self, n, scope_name='global'):

        VarName = n.name.name

        if not self.check_dict(VarName, scope_name):
            return


        value = self.decl_buf[scope_name].get(VarName)



        if value[0] not in self.array_type and \
                value[0] not in self.double_array_type:
            self._error_flag = True
            return



        return len(value[1])


    def visit_SizeArray2(self, n, scope_name='global'):

        VarName = n.name.name

        if not self.check_dict(VarName, scope_name):
            return


        value_t = self.check_double_array(VarName, scope_name)

        if not value_t:
            return

        arraySize = len(value_t)

        index = self.visit(n.index, scope_name)

        type_val = type(index)
        val = index

        if type(n.index) == ast.ID:  # UINT a = b

            if not index:
                print("Undec reference")
                self._error_flag = True
                return (False, 0)

            type_val = index[0]
            val = index[1]



        flag, value = self.check_type("UINT", None, type_val, val)

        if not flag:
            print("Incorrect index")
            return

        if index >= arraySize or index < 0:
            print("Ошибка времени выполнения")
            self._error_flag = True
            return

        return len(value_t[1][index])



# функция check_array  вообще не используем

    def visit_ArrayExtend1(self, n, scope_name='global'):

        VarName = n.name.name

        if not self.check_dict(VarName, scope_name):
            return



        value_t1 = self.check_array(VarName, scope_name)

        if not value_t1:
            self._error_flag = False

            value_t2 = self.check_double_array(VarName, scope_name)

            if not value_t2:
                return
        flag, size = self.check_parameter("UINT", None,  n.size, scope_name)


        if not flag:
            print("Incorrect size")
            return

        if size:
            if value_t1:
                if value_t1[0] == self.array_type[0]:
                    buf = [0] * size
                elif value_t1[0] == self.array_type[1]:
                    buf = [False] * size
                self.decl_buf[scope_name][VarName][1].extend(buf)

            else:
                arlen = len(value_t2[1])
                if arlen:
                    length = len(value_t2[1][arlen - 1])
                else:
                    length = 0
                if value_t2[0] == self.double_array_type[0]:
                    buf = [0] * length
                elif value_t2[0] == self.double_array_type[1]:
                    buf = [False] * length
                for i in range(size):
                    buf = buf.copy()
                    self.decl_buf[scope_name][VarName][1].append(buf)
                # print('In', self.decl_buf)



    def visit_ArrayExtend2(self, n, scope_name='global'):

        VarName = n.name.name


        # провряю словарь
        if not self.check_dict(VarName, scope_name):
            return


        # проверяю, что это двумерный массив
        value_t = self.check_double_array(VarName, scope_name)

        if not value_t:
            return

        flag1, size = self.check_parameter("UINT", None,  n.size, scope_name)
        flag2, index = self.check_parameter("UINT", None, n.index, scope_name)

        # print("Sixe, INDEX", size, index)

        if not flag1 or not flag2:
            print("Incorrect size")
            return

        if index >= len(value_t[1]) and index < 0:
            self._error_flag = True
            print("Error index")
            return

        if size:

            if value_t[0] == self.double_array_type[0]:
                buf = [0] * size
            elif value_t[0] == self.double_array_type[1]:
                buf = [False] * size



            if self.decl_buf[scope_name][VarName][1][index] == []:
                self.decl_buf[scope_name][VarName][1][index] = buf
            else:
                self.decl_buf[scope_name][VarName][1][index].extend(buf)
            # item.append(1)
            # print(self.decl_buf)







    def check_parameter(self, type_l, val_l,  parameter, scope_name='global'):

        print("Parameter", parameter)
        param = self.visit(parameter, scope_name)

        type_val = type(param)
        val = param

        if type(parameter) == ast.ID:  # UINT a = b

            if not param:
                print("Undec reference")
                self._error_flag = True
                return (False, 0)

            type_val = param[0]
            val = param[1]

        if self._error_flag:
            return





        flag, value = self.check_type(type_l, val_l, type_val, val)


        return (flag, value)



    def check_dict(self, name, scope_name='global'):

        if not self.decl_buf[scope_name].get(name):
            print("Existing error")
            self._error_flag = True
            return False
        return True



    def check_array(self, arrayName, scope_name='global'):
        value_t = self.decl_buf[scope_name].get(arrayName)

        # проверяем, то это действительно массив (надо будет занести в функцию)
        if value_t[0] not in self.array_type:
            self._error_flag = True
            print("Not array object")
            return
        return value_t



    # def check_arrays(self, arrayName, scope_name='global'):
    #     value_t = self.decl_buf[scope_name].get(arrayName)
    #
    #     if value_t[0] in self.array_type:
    #         return value_t
    #     elif value_t[0] in self.double_array_type:
    #         return value_t
    #     else:
    #         self._error_flag = True
    #         print("Not array object")
    #         return

    def check_arrays(self, arrayName, scope_name='global'):

        value_t = self.decl_buf[scope_name].get(arrayName)

        if value_t[0] in self.array_type:
            return value_t
        elif value_t[0] in self.double_array_type:
            return value_t
        else:
            self._error_flag = True
            print("Not array object")
            return



    def check_double_array(self, arrayName, scope_name='global'):
        value_t = self.decl_buf[scope_name].get(arrayName)

        # проверяем, то это действительно массив (надо будет занести в функцию)
        if value_t[0] not in self.double_array_type:
            self._error_flag = True
            print("Not array object")
            return
        return value_t



    def visit_CallArrayElement(self, n, scope_name='global'):
        value_t, aindex = self.test_for_array(n, scope_name)
        if not value_t:
            return
        return value_t[1][aindex]



    def test_for_array(self, n, scope_name):
        arrayName = n.name.name
        # если нет массива, в которому обращаемся в словаре
        if not self.check_dict(arrayName, scope_name):
            return (False, None)

        value_t = self.check_array(arrayName, scope_name)

        # проверяем, то это действительно массив (надо будет занести в функцию)
        if not value_t:
            return (False, None)

        arraySize = len(value_t[1])

        flag, aindex = self.check_parameter("UINT",None,  n.index, scope_name)
        if not flag:
            print("Incorrect size")
            return (False, None)

        if aindex >= arraySize or aindex < 0:
            print("Ошибка времени выполнения")
            self._error_flag = True
            return (False, None)

        return (value_t, aindex)



    def visit_CallDoubleArrayElement(self, n, scope_name='global'):
        value_t, index1, index2 = self.test_for_double_array(n, scope_name)
        if not value_t:
            return
        return value_t[1][index1][index2]


    def test_for_double_array(self, n, scope_name='global'):
        arrayName = n.name.name

        if not self.check_dict(arrayName, scope_name):
            return (False, None, None)
        value_t = self.check_double_array(arrayName, scope_name)
        arraySize = len(value_t[1])
        flag, index1 = self.check_parameter("UINT", None, n.index_1, scope_name)
        if not flag:
            print("Incorrect size")
            return (False, None, None)

        if index1 >= arraySize or index1 < 0:
            print("Ошибка времени выполнения")
            self._error_flag = True
            return (False, None, None)

        arraySize2 = len(value_t[1][index1])

        flag, index2 = self.check_parameter("UINT", None, n.index_2, scope_name)

        if not flag:
            print("Incorrect size")
            return (False, None, None)

        if index2 >= arraySize2 or index2 < 0:
            print("Ошибка времени выполнения")
            self._error_flag = True
            return (False, None, None)

        return (value_t, index1, index2)




# нужно сделать функцию которая бы проверяла можно ли идти на эту клетку (может быть либо конец границы, либо стенка)


# this functions i will use in another operators
    def change_direction(self, befor, after):
        self.direction[befor] = 0
        self.direction[after] = 1


    def goBack(self):
        index = np.nonzero(self.direction)[0][0]
        if not index:
            j = 1
        elif index == 1:
            j = 0
        elif index == 2:
            j = 3
        else:
            j = 2

        self.change_direction(index, j)

    def goForw(self):
        pass



    def goRight(self):
        index = np.nonzero(self.direction)[0][0]
        if not index:
            j = 2
        elif index == 1:
            j = 3
        elif index == 2:
            j = 1
        else:
            j = 0

        self.change_direction(index, j)

    def goLeft(self):
        index = np.nonzero(self.direction)[0][0]
        if not index:
            j = 3
        elif index == 1:
            j = 2
        elif index == 2:
            j = 0
        else:
            j = 1

        self.change_direction(index, j)






    def move_error(self, i, j):
        if self.decl_buf['global']['map'][1][i][j]: # we move only when thee cell is zero
            return False
        return True




    def update_map(self, ind_i, ind_j):
        if not self.move_error(ind_i, ind_j):
            return False
        i = self.robot_coord[0]
        j = self.robot_coord[1]
        self.decl_buf['global']['map'][1][i][j] = 0
        self.decl_buf['global']['map'][1][ind_i][ind_j] = 5
        self.robot_coord[0] = ind_i
        self.robot_coord[1] = ind_j
        return True





# есть функция, в которую передаём индекс начала, а он выдает кратчайшее расстояние в данном направлении

    def find_path(self, i, j):
        r_in = (i, j)
        r_out = (self.out_coord[0], self.out_coord[1])
        labirint = self.decl_buf['global']['map'][1]
        if labirint[i][j] == 1:
            self.fd.write("Path not found" + "\n")
            return False
        if labirint[i][j] == 3:
            # print("The robot came out of the maze")
            self.fd.write("The robot came out of the maze" + "\n")
            return 1
        path = [[0 if x == 0 or x == 5 else -1 for x in y] for y in labirint]
        path[r_in[0]][r_in[1]] = 1
        # for i in path:
        #     print(i)
        if not self.found(path, r_out):
            # print("Path not found")
            self.fd.write("Path not found" + "\n")
            return False
        print('\n')
        return path[r_out[0]][r_out[1]]



    def found(self, pathArr, finPoint):

        weight = 1
        for i in range(len(pathArr) * len(pathArr[0])):
            weight += 1
            for y in range(len(pathArr)):
                for x in range(len(pathArr[y])):
                    if pathArr[y][x] == (weight - 1):
                        if y > 0 and pathArr[y - 1][x] == 0:
                            pathArr[y - 1][x] = weight
                        if y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0:
                            pathArr[y + 1][x] = weight
                        if x > 0 and pathArr[y][x - 1] == 0:
                            pathArr[y][x - 1] = weight
                        if x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == 0:
                            pathArr[y][x + 1] = weight

                        if (abs(y - finPoint[0]) + abs(x - finPoint[1])) == 1:
                            pathArr[finPoint[0]][finPoint[1]] = weight
                            return True
        return False



#

    def push_wall(self, i, j):
        # print("I, J", i, j)
        # print("Direction", self.direction)
        map =  self.decl_buf['global']['map'][1]

        # проверяю тот, который пришел (эта клетка должна быть стеной)
        if map[i][j] != 1:
            # print("Не стена")
            return
        i_1 = i
        j_1 = j
        index = np.nonzero(self.direction)[0][0]
        if index == 0:
            # print("Ту0")
            i_1 -= 1
        elif index == 1:
            # print("Тут1")
            i_1 += 1
        elif index == 2:
            # print("Тут2")
            j_1 += 1
        else:
            # print("Тут")
            j_1 -= 1

        # проверяю следующую клетку (она должна быть пустой)
        if map[i_1][j_1] != 0:
            # print("Невозможно передвинуть стену")
            return


        # надо запомнить индекс клетки
        undo = self.robot_undo
        undo[0] = True
        undo[1] = [i, j] # откуда
        undo[2] = [i_1, j_1] # куда
        map[i][j] = 0
        map[i_1][j_1] = 1



# self.robot_undo = [False, [0, 0], [0, 0]] - 1 - была ли передвинута стена
#`                                            2 - из какой клетки
#                                             3 - в какую клетку

    def back_wall(self):
        # print(self.robot_undo[0])
        if not self.robot_undo[0]:
            # print("Передвинутых стен не было")
            # self.fd.write("Передвинутых стен не было" + '\n')
            return

        undo = self.robot_undo

        map = self.decl_buf['global']['map'][1]

        if map[undo[1][0]][undo[1][1]] != 0:
            # print("Невозможно вернуть стену на место")
            # self.fd.write("Невозможно вернуть стену на место" + '\n')
            return
        map[undo[2][0]][undo[2][1]] = 0
        map[undo[1][0]][undo[1][1]] = 1
        undo[0] = False


    def visit_RobotOperator(self, n, scope_name='global'):
        self.Print()
        if n.operator in self.move_operators:
            self.robot_turn[n.operator]()
            self.robot_move[np.nonzero(self.direction)[0][0]]()
        elif n.operator in self.size_operators:
            before = np.nonzero(self.direction)[0][0]
            self.robot_turn[n.operator]() # Повернул робота
            size = self.robot_found[np.nonzero(self.direction)[0][0]]()
            self.direction *= 0
            self.direction[before] = 1    # Повернул его обратно
            if size:
                return size
            else:
                return sys.maxsize

        elif n.operator in self.push_operators:
            self.robot_turn[n.operator]()
            self.robot_push[np.nonzero(self.direction)[0][0]]()
        else:
            self.back_wall()





















