from lexer import ExpLexer


# Cria e constroi o analisador léxico
lexer = ExpLexer()
lexer.build()

teste_code = '''PROCEDURE atualizar_observacoes DO
CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22 ;
CREATE TABLE completo FROM estacoes JOIN observacoes USING(Id);
END'''

lexer.input(teste_code)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{str(tok)}")