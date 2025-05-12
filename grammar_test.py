from grammar import Grammar

# Cria uma instância da gramática e compila
g = Grammar()
g.build()

# String de entrada válida para a regra p9
input_string = '''PROCEDURE atualizar_observacoes DO
CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22 ;
CREATE TABLE completo FROM estacoes JOIN observacoes USING(Id);
END'''

# Faz o parsing
resultado = g.parse(input_string)

# Como estamos só printando reduções no método p_p9, não precisamos de assert
print("Parsing concluído.")
