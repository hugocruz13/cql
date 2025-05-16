from grammar import Grammar
from eval import ExpEval
import sys
from pprint import PrettyPrinter

debug_mode = False
pp = PrettyPrinter(sort_dicts=False)

lg = Grammar()
lg.build()


if len(sys.argv) == 2:
	with open(sys.argv[1], "r") as file:
		contents = file.read()
		try:
			tree = lg.parse(contents)
			if debug_mode:pp.pprint(tree)
			resultado = ExpEval.evaluate(tree)
			print(f"<< {resultado}")
		except SyntaxError as e:
			print(e)
		except Exception as e:
			print(e, file=sys.stderr)
else:
	for expr in iter(lambda: input("CQL >> "), ""):
		if expr.upper() == "EXIT":
			break
		try:
			ast = lg.parse(expr)
			if debug_mode:pp.pprint(ast)
			resultado = ExpEval.evaluate(ast)
			if resultado is not None:
				print(f"<< {resultado}")
		except SyntaxError as e:
			print(e)
		except Exception as e:
			print(e)



