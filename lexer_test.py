from lexer import ExpLexer

# Cria e constroi o analisador léxico
lexer = ExpLexer()
lexer.build()

teste_code = '''{--DDASDAS 
CREATE TABLE completo FROM estacoes JOIN observacoes USING(Id);--}'''

lexer.input(teste_code)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{str(tok)}")