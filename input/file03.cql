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

SELECT * FROM observacoes;

CREATE TABLE estacao_e2 SELECT * FROM observacoes WHERE Id = 'E2';
EXPORT TABLE estacao_e2 AS "estacao_e2.csv";

SELECT Id, Radiacao FROM observacoes WHERE Radiacao > 180;

DISCARD TABLE estacao_e2;

PROCEDURE filtros_personalizados DO
  SELECT * FROM observacoes WHERE Temperatura > 22;
  SELECT * FROM observacoes WHERE Radiacao < 50;
  SELECT Id FROM observacoes WHERE Temperatura > 20 AND Radiacao > 150;
END

CALL filtros_personalizados;

