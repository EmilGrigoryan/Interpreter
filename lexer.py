import sys

from ply import lex
from ply.lex import TOKEN


class Lexer:
    def __init__(self, error_func):
        self.error_func = error_func

    def run(self):
        self.lexer = lex.lex(object=self)


    def reset_lineno(self):
        self.lexer.lineno = 1


    def input(self, text):
        self.lexer.input(text)


    def find_tok_column(self, token):
        last_cr = self.lexer.lexdata.rfind('\n', 0, token.lexpos)
        return token.lexpos - last_cr


    def _error(self, msg, token):
        location = self._make_tok_location(token)
        self.error_func(msg, location[0], location[1])
        self.lexer.skip(1)


    def _make_tok_location(self, token):
        return (token.lineno, self.find_tok_column(token))



    tok = (
            'IF', 'WHILE', 'OR', 'INC', 'DEC', 'TRUE', 'FALSE', 'ELSE',
            'NOT', 'DO', 'UINT', 'BOOLEAN', 'CUINT', 'CBOOLEAN', 'FUNCTION',
            'DARRAYOFUINT_1', 'DARRAYOFBOOLEAN_1', 'SIZE1', 'EXTEND1',
            'DARRAYOFUINT_2', 'DARRAYOFBOOLEAN_2', 'SIZE2', 'EXTEND2',
            'FORW', 'BACK','RIGHT','LEFT','GETF','GETB','GETR','GETL',
            'PUSHF', 'PUSHB', 'PUSHR', 'PUSHL', 'UNDO'
    )




    keyword_map = {}
    for keyword in tok:
        keyword_map[keyword] = keyword




    tokens = tok + (
        'MINUS', 'PLUS',
        'LPAREN', 'RPAREN',         # ( )
        'LBRACKET', 'RBRACKET',     # [ ], .
        'LBRACE', 'RBRACE',      # { }
        'COMMA',
        'ID', 'NEWLINE',  'DIGIT',
        'LT', 'GT',
        'EQUALS',
        'EQUAL',
        'SEMICOLON',
    )



    identifier = r'[a-zA-Z_][0-9a-zA-Z_]*'

    t_ignore = ' \t'
    newline = r'\n+'



    @TOKEN(newline)
    def t_NEWLINE(self, t):
        t.lexer.lineno += t.value.count("\n")
        return t
    t_DIGIT             = r'0|([1-9][0-9]*)'
    t_LT                = r'<'
    t_GT                = r'>'
    t_PLUS              = r'\+'
    t_MINUS             = r'\-'
    t_EQUALS            = r'='
    t_EQUAL             = r'=='
    t_LPAREN            = r'\('
    t_RPAREN            = r'\)'
    t_LBRACKET          = r'\['
    t_RBRACKET          = r'\]'
    t_LBRACE            = r'\{'
    t_RBRACE            = r'\}'
    t_COMMA             = r','
    t_SEMICOLON         = r';'

    @TOKEN(identifier)
    def t_ID(self, t):
        t.type = self.keyword_map.get(t.value, "ID")
        return t




    def t_error(self, t):
        msg = 'Illegal character %s' % repr(t.value[0])
        self._error(msg, t)





