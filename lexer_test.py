from lexer import ExpLexer

# Cria e constroi o analisador léxico
lexer = ExpLexer()
lexer.build()

teste_code = '''-- Isto e um comentário
IMPORT TABLE tabela1 FROM "dados.csv";
CREATE TABLE tabela FROM tabela1 JOIN tabela3 USING(id);
SELECT * FROM tabela WHERE coluna1 = 10 AND coluna2 >= 20 LIMIT 50;
'''

lexer.input(teste_code)

while True:
    tok = lexer.token()
    if not tok:
        break
    print(f"{str(tok)}")