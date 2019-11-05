from lark import Lark, InlineTransformer
from pathlib import Path

from .runtime import Symbol


class LispTransformer(InlineTransformer):
    def start(self, *args): 
        return [Symbol.BEGIN, *args]
    
    def list(self, *args):
        return list(args)

    def atom(self, args):
        if(str(args) == '#t'):
            return True
        elif (str(args) == '#f'):
            return False
        else:
            try:
                return int(args)
            except ValueError:
                try:
                    return float(args)
                except ValueError:
                    if(args.type == 'STRING'):
                        res = str(args)[1:-1]
                        res = res.replace("\\n","\n").replace("\\t","\t").replace("\\","")
                        return res
                    else:    
                        return Symbol(str(args))

def parse(src: str):
    """
    Compila string de entrada e retorna a S-expression equivalente.
    """
    return parser.parse(src)


def _make_grammar():
    """
    Retorna uma gramática do Lark inicializada.
    """

    path = Path(__file__).parent / 'grammar.lark'
    with open(path) as fd:
        grammar = Lark(fd, parser='lalr', transformer=LispTransformer())
    return grammar

parser = _make_grammar()