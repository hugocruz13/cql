from grammar import Grammar

# Cria uma instância da gramática e compila
g = Grammar()
g.build()

# String de entrada válida para a regra p9
input_string = '''SELECT * FROM observacoes WHERE Temperatura = "teste";'''

# Faz o parsing
resultado = g.parse(input_string)

# Como estamos só printando reduções no método p_p9, não precisamos de assert
print("Parsing concluído.")
