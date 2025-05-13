from grammar import Grammar
from eval import ExpEval
import sys
from pprint import PrettyPrinter

pp = PrettyPrinter(sort_dicts=False)

lg = Grammar()
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
	for expr in iter(lambda: input("CQL >> "), ""):
		try:

			ast = lg.parse(expr)
			pp.pprint(ast)
			resultado = ExpEval.evaluate(ast)
			#if resultado is not None:
			print(f"<< {resultado}")
		except SyntaxError as e:
			print(e)
		except Exception as e:
			print(e)



