from sly import  Parser
from Lexer.MainLex import  BasicLexer
class BasicParser(Parser):
    tokens = BasicLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS','deref','push','pop'),
        )

    def __init__(self):
        self.env = { }

    # @_('')
    # def statement(self, p):
    #     pass

    @_('statements')
    def program(self, p):
        return ('program',p.statements)

    @_('statements statement')
    def statements(self, p):
        return p.statements+[ p.statement]

    @_('statement')
    def statements(self, p):
        return [p.statement]

    @_("Body")
    def statement(self, p):
        return p.Body

    @_("'{' procs '}'")
    def Body(self, p):
        return p.procs

    @_("procs ',' proc")
    def procs(self, p):
        return p.procs + [p.proc]

    @_('proc')
    def procs(self, p):
        return [p.proc]

    @_('statement')
    def proc(self, p):
        return p.statement



    @_('FOR var_assign TO expr THEN statement')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    # @_('"(" expr "," expr "," expr ")"')
    # def setup(self,p):
    #     return

    @_('FOR tuple  statement ')
    def statement(self, p):
        return ('For_loop', p.tuple,[p.statement])

    @_('NAME condition  statement ')
    def statement(self, p):
        if p.NAME == 'while':
            return ('While_loop', p.condition,[p.statement])



    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    # @_('FUN NAME "(" ")" ARROW statement')
    # def statement(self, p):
    #     return ('fun_def', p.NAME, p.statement)

    @_('FUN NAME "(" ")" ":" expr statement')
    def statement(self, p):
        return ('fun_def_ret', p.NAME, [p.statement],p.expr)

    @_('FUN NAME "(" ")" statement')
    def statement(self, p):
        return ('fun_def', p.NAME, [p.statement])





    @_('NAME "(" ")"')
    def statement(self, p):
        return ('fun_call', p.NAME)

    @_('expr EQEQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('expr ">" "=" expr')
    def condition(self, p):
        return ('condition_geqeq', p.expr0, p.expr1)

    @_('expr "<" "=" expr')
    def condition(self, p):
        return ('condition_leqeq', p.expr0, p.expr1)

    @_('expr "!" "=" expr')
    def condition(self, p):
        return ('condition_neqeq', p.expr0, p.expr1)

    @_('expr ">" expr')
    def condition(self, p):
        return ('condition_g', p.expr0, p.expr1)

    @_('expr "<" expr')
    def condition(self, p):
        return ('condition_l', p.expr0, p.expr1)




    @_('ARROW expr EQEQ expr')
    def statement(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "+" "=" expr')
    def var_assign(self, p):
        return ('var_assign_pe', p.NAME, p.expr)

    @_('NAME "-" "=" expr')
    def var_assign(self, p):
        return ('var_assign_pe', p.NAME, p.expr)

    @_('NAME "*" "=" expr')
    def var_assign(self, p):
        return ('var_assign_pe', p.NAME, p.expr)



    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)

    @_("tuple")
    def expr(self, p):
        return p[0]

    @_("list")
    def expr(self, p):
        return p[0]

    @_('"(" elements ")"')
    def tuple(self, p):
        return ('tuple', p[1])

    @_('"[" elements "]"')
    def list(self, p):
        return ('list', p[1])

    @_("elements ',' element")
    def elements(self, p):
        return p[0] + p[2]

    @_("element")
    def elements(self, p):
        return p[0]

    # subsection element of elepments

    @_("'%' statement '%'")
    def expr(self,p):
        return p.statement

    @_("'<' expr '>'" )
    def statement(self,p):
        return p.expr

    @_("expr")
    def element(self, p):
        return [p[0]]
    # @_('expr')
    # def statement(self, p):
    #     return (p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"*" expr %prec deref')
    def expr(self,p):
        return ('deref',p.expr)

    @_('PUSH expr %prec push')
    def expr(self, p):
        return ('push', p.expr)

    @_('PUSH Stream_Load')
    def expr(self, p):
        return ('push_stream', p.Stream_Load)

    @_('"(" expr LARROW expr ")"')
    def Stream_Load(self, p):
        return ("Stream", p.expr0,p.expr1)

    @_('"(" expr ARROW expr ")"')
    def Pipe_Load(self,p):
        return ("Pipe", p.expr0,p.expr1)

    @_('POP expr %prec pop')
    def expr(self, p):
        return ('pop', p.expr)

    @_('POP Pipe_Load')
    def expr(self, p):
        return ('pop_stream', p.Pipe_Load)



    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)
