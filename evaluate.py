import math
import operator as op

from scheme_types import *


class Env(dict):
    """An environment: a dict of {'var': val} pairs, with an outer Env."""

    def __init__(self, params=(), args=(), outer=None):
        super().__init__()
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var):
        """Find the innermost Env where var appears."""
        return self if (var in self) else self.outer.find(var)


class Procedure(object):
    """A user-defined Scheme procedure."""

    def __init__(self, params, body, env):
        self.params, self.body, self.env = params, body, env

    def __call__(self, *args):
        return evaluate(self.body, Env(self.params, args, self.env))


# region Methods for handling more than 2 arguments fo basic maths operations
def summ(number, *args):
    total = number
    for num in args:
        total = total + num
    return total


def subb(number, *args):
    total = number
    for num in args:
        total = total - num
    return total


def mull(number, *args):
    total = number
    for num in args:
        total = total * num
    return total


def divv(number, *args):
    total = number
    for num in args:
        total = total / num
    return total


# endregion Methods for handling more than 2 arguments fo basic maths operations

def standard_env() -> Env:
    """An environment with some Scheme standard procedures."""
    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update({
        '+': summ, '-': subb, '*': mull, '/': divv,
        '>': op.gt, '<': op.lt, '>=': op.ge, '<=': op.le, '=': op.eq,
        'abs': abs,
        'append': summ,
        'apply': lambda proc, args: proc(*args),
        'begin': lambda *x: x[-1],
        'car': lambda x: x[0],
        'cdr': lambda x: x[1:],
        'cons': lambda x, y: [x] + y,
        'eq?': op.is_,
        'expt': pow,
        'equal?': op.eq,
        'length': len,
        'list': lambda *x: List(x),
        'list?': lambda x: isinstance(x, List),
        'map': map,
        'max': max,
        'min': min,
        'not': op.not_,
        'null?': lambda x: x == [],
        'number?': lambda x: isinstance(x, Number),
        'print': print,
        'procedure?': callable,
        'round': round,
        'symbol?': lambda x: isinstance(x, Symbol),
    })
    return env


global_env = standard_env()


def evaluate(x: Exp, env=global_env) -> Exp:
    """Evaluate an expression in an environment."""
    if isinstance(x, Symbol):  # variable reference
        return env.find(x)[x]
    elif not isinstance(x, List):  # constant
        return x
    operation, *args = x
    if operation == 'quote':  # quotation
        return args[0]
    elif operation == 'if':  # conditional
        (test, conseq, alt) = args
        exp = (conseq if evaluate(test, env) else alt)
        return evaluate(exp, env)
    elif operation == 'define':  # definition
        (symbol, exp) = args
        env[symbol] = evaluate(exp, env)
    elif operation == 'set!':  # assignment
        (symbol, exp) = args
        env.find(symbol)[symbol] = evaluate(exp, env)
    elif operation == 'lambda':  # procedure
        (params, body) = args
        return Procedure(params, body, env)
    else:  # procedure call
        proc = evaluate(operation, env)
        values = [evaluate(arg, env) for arg in args]
        return proc(*values)
