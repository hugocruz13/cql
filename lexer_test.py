from lexer import ExpLexer

# Cria e constroi o analisador léxico
lexer = ExpLexer()
lexer.build()

teste_code = '''-- Isto e um comentário
IMPORT TABLE tabela FROM "dados.csv";
CREATE TABLE tabela FROM tabela JOIN tabela USING(Id);
SELECT * FROM tabela WHERE Coluna = 10 AND Coluna >= 20 LIMIT 50;
'''

lexer.input(teste_code)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{str(tok)}")