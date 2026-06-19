from sly import Lexer
from sly import Parser

import Asm
from Asm import Asm


class BasicLexer(Lexer):
    tokens = { NAME, NUMBER, STRING, IF, THEN, ELSE, FOR, FUN, TO, ARROW, EQEQ,PUSH,POP,LARROW }
    ignore = '\t '
    ignore_comment = r';.*'

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';','}','{','^','v',':','[',']' }

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

    @_('IF condition THEN statement ELSE statement')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('FUN NAME "(" ")" ARROW statement')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('NAME "(" ")"')
    def statement(self, p):
        return ('fun_call', p.NAME)

    @_('expr EQEQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)



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



class BasicExecute:

    def __init__(self, tree, env,Asm):
        self.env = env
        self.Asm=Asm
        print(tree)
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':

            if node[1] == None:
                self.walkTree(node[2])
            else:
                for i in node[1]:

                    self.walkTree(i)
                #self.walkTree(node[2])


        if node[0]=='pop_stream':
            v = self.walkTree(node[1])
            return v

        if node[0]=='push_stream':
            v = self.walkTree(node[1])
            return v

        if node[0]=='Pipe':
            l = self.walkTree(node[1])
            r = self.walkTree(node[2])
            if not isinstance(l, list):
                return None
            if not isinstance(r, tuple):
                return None
            if not r[0] == 'reg':
                return None
            reg = self.walkTree(r)
            self.Asm.emit_stack_offset_read(l[0], reg)
            return r
        if node[0]=='Stream':
            l = self.walkTree(node[1])
            r = self.walkTree(node[2])
            if not isinstance(l, list):
                return None
            if not isinstance(r,tuple):
                return None
            if not r[0]=='reg':
                return None
            reg = self.walkTree(r)
            self.Asm.emit_stack_offset_write(l[0],reg)
            return r
        if node[0]=='push':
            v1=self.walkTree(node[1])
            old_v1=v1
            if isinstance(v1,tuple):
                if v1[0]=='reg':
                    v1=self.walkTree(v1)
                    self.Asm.emit_push_reg(v1)

            return old_v1
        if node[0]=='pop':
            v1 = self.walkTree(node[1])
            old_v1 = v1
            if isinstance(v1, tuple):
                if v1[0] == 'reg':
                    v1 = self.walkTree(v1)
                    self.Asm.emit_pop_reg(v1)

            return old_v1
        if node[0]=='deref':
            v1=self.walkTree(node[1])
            v1_old=v1
            if isinstance(v1, tuple):
                v1=self.walkTree(v1)
            self.Asm.emit_load_reg_ptr(v1,v1)
            return v1_old

        if node[0]=='tuple':
            return tuple(self.walkTree(i) for i in node[1])

        if node[0]=='list':
            return list(self.walkTree(i) for i in node[1])


        if node[0] == 'num':
            return node[1]

        if node[0] == 'str':
            return node[1]

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])

        if node[0] == 'condition_eqeq':
            v1=self.walkTree(node[1])
            v2=self.walkTree(node[2])
            if isinstance(v1,tuple) and isinstance(v2,tuple):
                val1 = self.walkTree(v1)
                val2 = self.walkTree(v2)
                if val1 and val2 in self.Asm.registers:
                    self.Asm.emit_universal_cmp(val1,val2)
                    return val1
            if isinstance(v1, tuple):
                val1 = self.walkTree(v1)
                val2 = self.walkTree(v2)
                if val1 in self.Asm.registers:
                    self.Asm.emit_cmp_reg_imm(val1, val2)
                    return val1
            if isinstance(v2, tuple):
                val1 = self.walkTree(v1)
                val2 = self.walkTree(v2)
                if val2 in self.Asm.registers:
                    self.Asm.emit_cmp_reg_imm(val2, val1)
                    return val2

            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0


        if node[0]=='add_reg_reg':
            v1=self.walkTree(node[1])
            v2=self.walkTree(node[2])

            print(self.Asm.emit_add_reg_reg(v1,v2))
            return v1

        if node[0] in ('add_reg_regx','sub_reg_regx','mul_reg_regx','add_reg_reg','sub_reg_reg','mul_reg_regx'):
            v1 = self.walkTree(node[1])
            v2 = self.walkTree(node[2])
            if node[0][0:3]=='sub':
                self.Asm.emit_sub_reg_reg(v2,v1)
                return v2
            elif node[0][0:3]=='mul':
                self.Asm.emit_mul_reg_reg(v1,v2)
            else:
                print(self.Asm.emit_add_reg_reg(v1,v2))
            return v1

        if node[0] in ('add_reg_imm','sub_reg_imm','mul_reg_imm'):
            v1=self.walkTree(node[1])
            v2=self.walkTree(node[2])
            if node[0][0:3]=='sub':
                self.Asm.emit_sub_reg_imm(v1,v2)
            elif node[0][0:3]=='mul':
                self.Asm.emit_mul_reg_imm(v1,v2)
            else:
                self.Asm.emit_add_reg_imm(v1,v2)
            return v1

        if node[0]=='reg':
            return node[1]


        if node[0] in ('add','sub','mul'):
            s=node[0]
            val1 = self.walkTree(node[1])
            val2 = self.walkTree(node[2])

            v2 = isinstance(val2,tuple)
            v1 = isinstance(val1, tuple)
            if v1 and v2:

                if val1[0]=='reg'and val2[0]=='reg':
                    return (f'{s}_reg_reg', val1[1], val2[1])

            if v1:
                if not v2:
                    return (f'{s}_reg_imm', val1, val2)

                if val1[0]=='reg':
                    return (f'{s}_reg_imm', val1[1], val2)

                if val2[0]==f'{s}_reg_reg':
                    return ('add_reg_regx',val1[1],val2)
                if val2[0]==f'{s}_reg_regx':
                    return (f'{s}_reg_regx',val1[1],val2)



            if v2:
                if not v1:
                    print(val2,val1)
                    return (f'{s}_reg_imm', val2, val1)
                if val2[0]=='reg':
                    return (f'{s}_reg_reg', val2[1], val1)
                if val1[0]==f'{s}_reg_regx':

                    return (f'{s}_reg_regx',val2[1],val1)
                if val1[0]==f'{s}_reg_reg':
                    return (f'{s}_reg_regx',val2[1],val1)

            if node[0]=='sub':
                return self.walkTree(node[1]) - self.walkTree(node[2])
            if node[0]=='mul':
                return self.walkTree(node[1]) * self.walkTree(node[2])
            return self.walkTree(node[1]) + self.walkTree(node[2])

        if node[0] == 'redacted':


            val1 = self.walkTree(node[1])
            val2 = self.walkTree(node[2])

            v2 = isinstance(val2,tuple)
            v1 = isinstance(val1, tuple)
            if v1 and v2:

                if val1[0]=='reg'and val2[0]=='reg':
                    return ('add_reg_reg', val1[1], val2[1])

            if v1:
                if not v2:
                    return ('add_reg_imm', val1, val2)

                if val1[0]=='reg':
                    return ('add_reg_imm', val1[1], val2)

                if val2[0]=='add_reg_reg':
                    return ('add_reg_regx',val1[1],val2)
                if val2[0]=='add_reg_regx':
                    return ('add_reg_regx',val1[1],val2)



            if v2:
                if not v1:
                    print(val2,val1)
                    return ('add_reg_imm', val2, val1)
                if val2[0]=='reg':
                    return ('add_reg_reg', val2[1], val1)
                if val1[0]=='add_reg_regx':

                    return ('add_reg_regx',val2[1],val1)
                if val1[0]=='add_reg_reg':
                    return ('add_reg_regx',val2[1],val1)


            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])


        if node[0] in ('var_assign_pe','var_assign_se','var_assign_me'):
            # if runtime
            type = node[0][11:13]
            if node[1].lower() in self.Asm.registers:
                val = self.walkTree(node[2])

                if isinstance(val, tuple):

                    v = self.walkTree(val)
                    if v in self.Asm.registers:
                        if v.lower() == node[1].lower():
                            return
                        if type=='pe':
                            self.Asm.emit_add_reg_reg(node[1], v)
                        if type=='se':
                            self.Asm.emit_sub_reg_reg(node[1], v)
                        if type=='me':
                            self.Asm.emit_mul_reg_reg(node[1], v)

                    return 0
                if type=='pe':
                    print(self.Asm.emit_add_reg_imm(node[1], val))
                if type=='se':
                    print(self.Asm.emit_sub_reg_imm(node[1], val))
                if type=='me':
                    print(self.Asm.emit_mul_reg_imm(node[1], val))

                return
            self.env[node[1]] += self.walkTree(node[2])
            return node[1]

        if node[0] == 'var_assign':
            #if runtime
            if node[1].lower() in self.Asm.registers:
                val = self.walkTree(node[2])
                if isinstance(val,tuple):


                    v = self.walkTree(val)
                    if v in self.Asm.registers:
                        if v.lower()==node[1].lower():
                            return
                        self.Asm.emit_mov_reg_reg(node[1],v)
                    return 0
                print(self.Asm.emit_mov_imm(node[1],val))
                return
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                if node[1] in self.Asm.registers:
                    return ('reg',node[1])
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 0

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))


if __name__ == '__main__':
    lexer = BasicLexer()
    parser = BasicParser()
    Asm = Asm()
    env = {}
    while True:
        try:
            with open('Dasm.asm','r') as f:
                text = f.read()

        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            BasicExecute(tree, env,Asm)
            print(Asm.code)
            print(Asm.code.hex(' ').upper())
            break
