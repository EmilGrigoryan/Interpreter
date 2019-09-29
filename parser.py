from ply import yacc

import abstract_tree as ast


from lexer import Lexer


function_dict = {}

def coordinate(p, token_idx):
    last_cr = p.lexer.lexdata.rfind('\n', 0, p.lexpos(token_idx))
    if last_cr < 0:
        last_cr = -1
    column = (p.lexpos(token_idx) - (last_cr))
    return (p.lineno(token_idx), column)

class ParseError(Exception):pass


def parse_error(self, msg, coord):
    raise ParseError("%s: %s" % (coord, msg))


buffer = Lexer(parse_error)
buffer.run()
tokens = buffer.tokens



precedence = (
    ('left', 'OR'),
    ('left',  'EQUAL'),
    ('left', 'GT', 'LT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'INC', 'DEC')
)




def p_root(p):
    """ root :      file_input
    """

    if p[1] is None:
        p[0] = ast.Root([])
    else:
        p[0] = ast.Root(p[1])
#


def p_file_input_1(p):
    """ file_input : NEWLINE
    """
    p[0] = []



def p_file_input_2(p):
    """ file_input : statement
                    | function_def
    """
    p[0] = p[1]



def p_file_input_3(p):
    """ file_input :  file_input statement
    """
    p[1].extend([p[2]])
    p[0] = p[1]
    # print(p[0])



def p_file_input_4(p):
    """ file_input :  file_input function_def
    """
    p[1].append(p[2])
    p[0] = p[1]


def p_statement(p):
    """ statement : simple_stmt
                    | compound_stmt """
    p[0] = p[1]
    # print("In statement", p[0])
#


# def p_simple_stmt_1(p):
#     """ simple_stmt :  small_stmt NEWLINE
#                         | small_stmt"""
#     p[0] = p[1]
#


def p_simple_stmt_1(p):
    """ simple_stmt :  small_stmt NEWLINE"""
    p[0] = p[1]


def p_small_stmt(p):
    """small_stmt : declarations
                    | assignment_expression
                    | call_function
                    | array_extend1
                    | array_extend2
                    | robot_operators
                    """
    p[0] = p[1]


def p_len_robot_operators(p):
    ''' len_robot_operators :   GETF
                              | GETB
                              | GETR
                              | GETL
                              '''
    p[0] = ast.RobotOperator(p[1])

def p_robot_operators(p):
    ''' robot_operators : FORW
                        | BACK
                        | RIGHT
                        | LEFT
                        | PUSHF
                        | PUSHB
                        | PUSHR
                        | PUSHL
                        | UNDO
                        '''
    p[0] = ast.RobotOperator(p[1])

def p_array_extend1(p):
    ''' array_extend1 : EXTEND1 identifier  binary_expression'''
    p[0] = ast.ArrayExtend1(p[2], p[3])



def p_array_extend2(p):
    ''' array_extend2 : EXTEND2 identifier LBRACKET binary_expression RBRACKET binary_expression'''
    p[0] = ast.ArrayExtend2(p[2], p[4], p[6])


def p_array_functions_1(p):
    ''' array_functions : SIZE1 identifier '''
    p[0] = ast.SizeArray1(p[2])



def p_array_functions_2(p):
    ''' array_functions : SIZE2 identifier LBRACKET binary_expression RBRACKET'''
    p[0] = ast.SizeArray2(p[2], p[4])




def p_type_vector(p):
    ''' type_vector : DARRAYOFUINT_1
                    | DARRAYOFBOOLEAN_1'''
    p[0] = ast.TypeVector(p[1])



def p_type_double_vector(p):
    ''' type_double_vector : DARRAYOFUINT_2
                           | DARRAYOFBOOLEAN_2'''
    p[0] = ast.TypeVector(p[1])


def p_declarations(p):
    '''declarations : declaration
                    | array_declaration'''
    p[0] = ast.Decl(p[1])




def p_array_declaration_1(p):
    ''' array_declaration : type_vector identifier EQUALS vector_init'''

    p[0] = [ast.Vector(p[1], p[2], p[4])]


def p_array_declaration_2(p):
    ''' array_declaration : type_double_vector identifier EQUALS double_vector_init'''

    p[0] = [ast.DoubleVector(p[1], p[2], p[4])]



def p_array_declaration_3(p):
    ''' array_declaration : type_vector identifier '''
    p[0] = [ast.Vector(p[1], p[2], None)]


def p_array_declaration_4(p):
    ''' array_declaration : type_double_vector identifier '''
    p[0] = [ast.DoubleVector(p[1], p[2], None)]


def p_vector_init(p):
    ''' vector_init : LBRACKET vector_list RBRACKET'''
    # print(p[2])
    p[0] = p[2]

# def p_vector_init_error(p):
#     ''' vector_init : '''

def p_double_vector_init(p):
    ''' double_vector_init : LBRACKET double_vector_list RBRACKET'''
    p[0] = p[2]

def p_double_vector_list_1(p):
    ''' double_vector_list : vector_list SEMICOLON vector_list'''
    p[0] = [p[1], p[3]]



def p_double_vector_list_2(p):
    ''' double_vector_list : double_vector_list SEMICOLON vector_list'''
    p[1].append(p[3])
    p[0] = p[1]

# array = [1, 2, 1, 2, 4]

def p_vector_list_1(p):
    ''' vector_list : binary_expression'''
    p[0]= [p[1]]


def p_vector_list_2(p):
    ''' vector_list : vector_list COMMA binary_expression'''
    p[1].append(p[3])
    p[0] = p[1]


def p_declaration(p):
    """ declaration       : type_specifier init_declarator_list
    """
    a = []
    for i in p[2]:
        a.append(ast.Declaration(p[1], i['decl'], i['init']))
    p[0] = a
#

def p_type_specifier(p):
    """ type_specifier            : UINT
                                  | BOOLEAN
                                  | CUINT
                                  | CBOOLEAN
        """
    p[0] = ast.IdentifierType(p[1])


# от init_declarator пришел словарь c двумя полями (ключ - значение) 1-{decl : Name, init: [наши данные]}
def p_init_declarator_list(p):
    """ init_declarator_list    : init_declarator
                                | init_declarator_list COMMA init_declarator
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]

    else:
        p[0] = [p[1]]


def p_init_declarator(p):
    """ init_declarator : declarator
                        | declarator EQUALS initializer
    """
    p[0] = dict(decl=p[1], init=(p[3] if len(p) > 2 else None))




def p_declarator(p):
    """ declarator  : id_declarator
    """
    p[0] = p[1]



def p_id_declarator_1(p):
    """ id_declarator  : direct_id_declarator
    """
    p[0] = p[1]




def p_direct_id_declarator_1(p):
    """ direct_id_declarator   : identifier
    """
    p[0] = p[1]


def p_direct_id_declarator_2(p):
    """ direct_id_declarator   : LPAREN id_declarator RPAREN
    """
    p[0] = p[2]



def p_initializer_1(p):
    """ initializer : assignment_expression
    """

    p[0] = p[1]



def p_compound_stmt(p):
    """compound_stmt :  if_stmt
                        | while_stmt"""
    p[0] = p[1]
    # print(p[0])



def p_if_stmt_1(p):
    """if_stmt : IF LPAREN expression RPAREN suite pass_new_line"""
    p[0] = ast.If(p[3], p[5], None)
    # print("If stmt", p[0])


# оотсутствует условие
def p_if_stmt_error(p):
    """if_stmt : IF LPAREN  RPAREN suite pass_new_line"""
    tup = coordinate(p, 2)
    print("Отсутствует условие у оператора, строка № {}, столбец № {}".format(tup[0], tup[1]))
    p[0] = ast.If(None, p[4], None)


def p_if_stmt_2(p):
    """if_stmt : IF LPAREN expression RPAREN suite NEWLINE ELSE suite pass_new_line"""
    p[0] = ast.If(p[3], p[5], p[8], None)


def p_if_stmt_error2(p):
    """if_stmt : IF LPAREN expression RPAREN suite ELSE suite pass_new_line"""
    tup = coordinate(p, 6)
    print("Отсутствует символ переноса строки, строка № {}, столбец № {}".format(tup[0], tup[1]))
    p[0] = ast.If(p[3], None, p[8], None)


def p_while_stmt(p):
    """while_stmt : WHILE LPAREN expression RPAREN DO suite pass_new_line"""
    p[0] = ast.While(p[3], p[6], None)



def p_while_stmt_error(p):
    """while_stmt : WHILE LPAREN expression RPAREN  suite pass_new_line"""
    tup = coordinate(p, 4)
    print("Отсутствует DO при объявлении цикла, строка № {}, столбец № {}".format(tup[0], tup[1]))
    p[0] = ast.While(p[3], p[5], None)



def p_suite_1(p):
    """suite : pass_new_line small_stmt"""
    p[0] = ast.Suite([p[2]], None)
    # print("In suite1", p[0])


def p_suite_2(p):
    """suite :  pass_new_line LBRACE pass_new_line big_stmt pass_new_line RBRACE """
    p[0] = ast.Suite(p[4], None)
    # print("In suite2", p[0])


def p_big_stmt(p):
    """big_stmt :  pass_new_line"""
    p[0] = []
    # print("in big stam", p[0])



def p_big_stmt_1(p):
    """big_stmt : statement"""
    p[0] = [p[1]]



def p_big_stmt_2(p):
    """big_stmt :  big_stmt statement"""
    p[1].append(p[2])
    p[0] = p[1]
    # print("in big stam2", p[0])




def p_expression(p):
    """ expression  : assignment_expression
        """
    # print("In expression", p[1])
    if len(p) == 2:
        p[0] = p[1]



def p_assignment_expression(p):
    """ assignment_expression   : binary_expression
                                | initializer EQUALS unary_expression
                                | initializer EQUALS binary_expression
        """
    # print("In assignment", p[1])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast.Assignment(p[2], p[1], p[3])
    # print(p[0])





def p_binary_expression(p):
    """ binary_expression   : cast_expression
                            | binary_expression LT binary_expression
                            | binary_expression GT binary_expression
                            | binary_expression OR binary_expression
                            | binary_expression MINUS binary_expression
                            | binary_expression PLUS binary_expression
                            | binary_expression EQUAL binary_expression
        """
    # print("In binary", p[1])
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ast.BinaryOp(p[2], p[1], p[3], p[1].coord)

#Потом добавятся операторы робота
def p_cast_expression(p):
    """ cast_expression : unary_expression
                        | array_functions
                        | call_array_element
                        | len_robot_operators
                        | call_double_array_element
                        """


    p[0] = p[1]


def p_call_array_element(p):
    """ call_array_element : identifier LBRACKET binary_expression RBRACKET"""
    # print("In call array")
    p[0] = ast.CallArrayElement(p[1], p[3])
    # print(p[0])


def p_call_double_array_element(p):
    ''' call_double_array_element : identifier LBRACKET binary_expression COMMA binary_expression RBRACKET'''
    p[0] = ast.CallDoubleArrayElement(p[1], p[3], p[5])


def p_unary_expression_1(p):
    """ unary_expression    : postfix_expression """
    # print("In unary", p[1])
    p[0] = p[1]


def p_unary_expression_2(p):
    """ unary_expression    : INC unary_expression
                            | DEC unary_expression
                            | unary_operator cast_expression
    """
    # p[0] = ast.UnaryOp(p[1], p[2], p[2].coord)
    p[0] = ast.UnaryOp(p[1], p[2])



def p_unary_operator(p):
    """ unary_operator  : NOT"""
    p[0] = p[1]



def p_unary_operator_error(p):
    """ unary_operator  : NOT NOT"""
    tup = coordinate(p, 1)
    print("Встречено два аргумента NOT, строка № {}, столбец № {}".format(tup[0], tup[1]))
    p[0] = p[1]

def p_postfix_expression_1(p):
    """ postfix_expression  : primary_expression """

    p[0] = p[1]



def p_primary_expression_1(p):
        """ primary_expression  : identifier
                                | digit
                                | bool"""
        # print('In primary_epresion', p[1])
        p[0] = p[1]


def p_primary_expression_4(p):
    """ primary_expression  : LPAREN expression RPAREN """
    p[0] = p[2]


def p_identifier(p):
    """ identifier  : ID """
    # print("Identifier", p[1])
    p[0] = ast.ID(p[1], coordinate(p, 1))



def p_digit_1(p):
    """ digit    : DIGIT
    """

    p[0] = ast.Digit('int', p[1], None)


def p_bool(p):
    """ bool : TRUE
    |           FALSE"""
    p[0] = ast.BOOL_TOF(p[1])


def p_error(p):
    print('Unexpected token:', p)

# над этим нужно поработать
def p_pass_new_line(p):
    """pass_new_line : empty
                        | NEWLINE"""
    # print("In PASS", p[1])
    p[0] = []
    # print(p[0])


def p_empty(p):
    """empty : """
    p[0] = ast.EmptyStatement()
    # print("In enpty", p[0])







def p_function_def(p):
    '''function_def : return_values FUNCTION identifier LPAREN params RPAREN  suite pass_new_line'''
    p[0] = ast.FunctionDecl(p[1], p[3], p[5], p[7])
    if function_dict.get(p[3].name):
        print("ERROR  function definition is already exists" )
    else:
        a = []
        for i in p[5].params:
            a.append(i.name.name)
        b = []
        for i in p[1].params:
            b.append(i.name.name)


        function_dict[p[3].name] = ([b, a, ast.FunctionCall(p[3],  p[7]), 0])


def p_function_def_error(p):
    '''function_def : return_values FUNCTION LPAREN params RPAREN  suite pass_new_line'''
    tup = coordinate(p, 2)
    print("Отсутствует имя функции, строка № {}, столбец № {} ".format(tup[0], tup[1]))
    p[0] = ast.FunctionDecl(p[1], None, p[4], p[6])






# Нужно сделать класс под параметры
def p_return_values_1(p):
    ''' return_values : type_specifier init_declarator'''
    # if type(p[])
    p[0] = ast.ParamList([ast.Declaration(p[1], p[2]['decl'], p[2]['init'])])


# [UINT a = 2, BOOLEAN f = false FUNCTION ...
def p_return_values_2(p):
    ''' return_values : LBRACKET params RBRACKET '''
    p[0] = p[2]
    # print(p[0])



def p_params(p):# declfrations
    '''params : param'''
    p[0] = ast.ParamList(p[1])




def p_param(p):#declaration
    '''param : param_list'''
    a = []
    # print(p[1])
    for i in p[1]:
        if type(i) in (ast.DoubleVector, ast.Vector):
            a.append(i)
        else:
            a.append(ast.Declaration(i[0], i[1]['decl'], i[1]['init']))
    p[0] = a


def p_param_list_1(p):
    '''param_list : type_specifier init_declarator'''
    a = [(p[1], p[2])]
    p[0] = a
    # print(p[0])
#

def p_param_list_2(p):
    ''' param_list : type_vector identifier EQUALS vector_init'''
    p[0] = [ast.Vector(p[1], p[2], p[4])]


def p_param_list_3(p):
    ''' param_list : type_double_vector identifier EQUALS double_vector_init'''
    p[0] = [ast.DoubleVector(p[1], p[2], p[4])]


def p_param_list_4(p):
    '''param_list : param_list COMMA type_specifier init_declarator'''
    p[1].append((p[3], p[4]))
    p[0] = p[1]



def p_param_list_5(p):
    p[1].append(ast.Vector(p[3], p[4], p[6]))
    p[0] = p[1]




def p_param_list_6(p):
    '''param_list : param_list COMMA type_double_vector identifier EQUALS double_vector_init'''
    p[1].append(ast.DoubleVector(p[3], p[4], p[6]))
    p[0] = p[1]



def p_call_function(p):
    ''' call_function : return_values_call EQUALS identifier LPAREN params_call RPAREN'''
    p[0] = ast.CallFunction(p[1], p[3], p[5])




def p_params_call(p):
    '''params_call : param_call'''
    p[0] = p[1]


def p_param_call(p):
    ''' param_call : param_call_list'''
    p[0] = p[1]



def p_param_call_list_1(p):
    '''param_call_list : initializer
                        | empty'''
    p[0] = [p[1]]




def p_param_call_list_4(p):
    '''param_call_list : param_call_list COMMA initializer'''
    p[1].append(p[3])
    p[0] = p[1]

def p_param_call_list_5(p):
    '''param_call_list : param_call_list COMMA empty'''
    p[1].append(p[3])
    p[0] = p[1]






def p_return_values_call_2(p):
    ''' return_values_call : LBRACKET return_call_list RBRACKET '''
    p[0] = p[2]




# Раскоментиовал, чтобы можно было использовать без аргументов
def p_return_call_list_1(p):
    '''return_call_list : identifier
                            | empty'''
    p[0] = [p[1]]




def p_return_call_list_2(p):
    '''return_call_list : return_call_list COMMA identifier'''
    p[1].append(p[3])
    p[0] = p[1]

def p_return_call_list_3(p):
    '''return_call_list : return_call_list COMMA empty'''
    p[1].append(p[3])
    p[0] = p[1]



parser = yacc.yacc()

def build_tree(code):
    return parser.parse(code, debug=False)


