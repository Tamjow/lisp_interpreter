# lisp_interpreter
A small lisp interpreter based on Peter Norvig's lispy.

To start using it run the lisp.py file, which will start a lisp repl (Read–eval–print loop), which can be used to test lisp expressions.

Examples:

lisp> (+ 1 2 3)
6


lisp> (define factorial (lambda (n) (if (<= n 1) 1 (* n (factorial (- n 1))))))
lisp> (factorial 5)
120
