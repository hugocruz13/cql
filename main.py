# arith.py
from grammar import ExpGrammar
from exp_eval import ExpEval
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(sort_dicts=False)

lg = ExpGrammar()
lg.build()


if len(sys.argv) == 2:
	with open(sys.argv[1], "r") as file:
		contents = file.read()
		try:
			tree = lg.parse(contents)
			pp.pprint(tree)
			resultado = ExpEval.evaluate(tree)
			print(f"<< {resultado}")
		except Exception as e:
			print(e, file=sys.stderr)
else:
	for expr in iter(lambda: input(">> "), ""):
		try:
			ast = lg.parse(expr)
			resultado = ExpEval.evaluate(ast)
			#if res is not None:
			print(f"<< {resultado}")
		except Exception as e:
			print(e)



