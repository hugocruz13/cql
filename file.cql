IMPORT TABLE estacoes FROM "estacoes.csv"; --TESTE
SELECT * FROM observacoes;
CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22 ;
PROCEDURE atualizar_observacoes DO
    CREATE TABLE mais_quentes SELECT * FROM observacoes WHERE Temperatura > 22 ;
    CREATE TABLE completo FROM estacoes JOIN observacoes USING(Id);
END