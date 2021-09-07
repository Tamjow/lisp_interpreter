from parse import parse
from evaluate import evaluate
from scheme_types import List


def repl(prompt='lisp> '):
    """A prompt-read-eval-print loop."""
    while True:
        value = evaluate(parse(input(prompt)))
        if value is not None:
            print(py2scheme(value))


def py2scheme(expression):
    """Convert a Python object back into a Scheme-readable string."""
    if isinstance(expression, List):
        return '(' + ' '.join(map(py2scheme, expression)) + ')'
    else:
        return str(expression)


if __name__ == '__main__':
    repl()
