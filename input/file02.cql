{--
Disciplina: Processamento de Linguagem 

CQL

Trabalho Prático de Processamento de Linguagens

Grupo 06: 
23016 – Dani Carvalho da Cruz
23279 – Hugo Ferreira Baptista
23010 – Hugo Tiago Mendes Cruz

Professor: Óscar Ribeiro

Licenciatura em Engenharia de Sistemas Informáticos
--}

IMPORT TABLE observacoes FROM "observacoes.csv";

PROCEDURE consulta_rapida DO
  SELECT * FROM observacoes WHERE Radiacao > 200;
  SELECT * FROM observacoes WHERE Temperatura BETWEEN 15 AND 20;
  SELECT * FROM observacoes LIMIT 5;
END

CALL consulta_rapida;

DELETE consulta_rapida;


SELECT * FROM observacoes WHERE Temperatura > 20 AND Radiacao > 120;

SELECT DataHoraObservacao, Temperatura FROM observacoes WHERE Temperatura > 24;

CREATE TABLE primeiras SELECT * FROM observacoes LIMIT 3;

PRINT TABLE primeiras;

EXPORT TABLE primeiras AS "primeiras.csv";






