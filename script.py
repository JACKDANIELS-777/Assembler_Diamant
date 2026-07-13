
from sly import Parser
from Lexer.MainLex import BasicLexer
from Parser.MainParser import BasicParser
from WalkTree.MainWalkTree import  BasicExecute
from HelpClasses.Asm import Asm


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
            import time
            a=time.time()
            # Ultimate mute switch
            b = print
            #print = lambda *args, **kwargs: None
            tree = parser.parse(lexer.tokenize(text))
            BasicExecute(tree, env,Asm)

            b(Asm.finalize_program().hex(' ').upper())
            b(time.time()-a)
            #Asm.write_exe('a.exe')
            break