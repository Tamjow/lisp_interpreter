# Parsing
from scheme_types import Exp, Atom, Symbol


def tokenize(chars: str) -> list:
    """Convert a string of characters into a list of tokens."""
    return chars.replace('(', ' ( ').replace(')', ' ) ').split()


def parse(program: str) -> Exp:
    """Read a Scheme expression from a string."""
    return read_from_tokens(tokenize(program))


def read_from_tokens(tokens: list) -> Exp:
    """Read an expression from a sequence of tokens."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF')
    token = tokens.pop(0)
    if token == '(':
        sub_expression = []
        while tokens[0] != ')':
            sub_expression.append(read_from_tokens(tokens))
        tokens.pop(0)  # pop off ')'
        return sub_expression
    elif token == ')':
        raise SyntaxError('unexpected )')
    else:
        return atom(token)


def atom(token: str) -> Atom:
    """Numbers become numbers; every other token is a symbol."""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)

