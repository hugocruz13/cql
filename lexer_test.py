from lexer import ExpLexer

# Cria e constroi o analisador léxico
lexer = ExpLexer()
lexer.build()

teste_code = '''"observacoes.csv"'''

lexer.input(teste_code)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{str(tok)}")