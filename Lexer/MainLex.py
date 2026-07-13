from sly import Lexer

class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ,PUSH,POP,LARROW }
    ignore = '\t '
    ignore_comment = r';.*'

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';','}','{','^','v',':','[',']','>','<','%' }

    # Define tokens
    IF = r'IF'
    THEN = r'THEN'
    ELSE = r'ELSE'
    FOR = r'FOR'
    FUN = r'FUN'
    TO = r'TO'
    ARROW = r'->'
    LARROW = r'<-'
    POP = r'v:'
    PUSH = r'\^:'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'


    EQEQ = r'=='
    #NEQEQ = r'!='


    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'#.*')
    def COMMENT(self, t):
        pass

    @_(r'\n+')
    def newline(self,t ):
        self.lineno = t.value.count('\n')