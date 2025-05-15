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

IMPORT TABLE estacoes FROM "estacoes.csv";
IMPORT TABLE observacoes FROM "observacoes.csv";

SELECT * FROM observacoes;
SELECT * FROM observacoes WHERE Temperatura < 18;
SELECT Id, Radiacao FROM observacoes WHERE Radiacao > 150;
SELECT * FROM observacoes LIMIT 2;

CREATE TABLE quentes SELECT * FROM observacoes WHERE Temperatura > 22;
EXPORT TABLE quentes AS "quentes.csv";

PRINT TABLE estacoes;

CREATE TABLE completo FROM estacoes JOIN observacoes USING(Id);
SELECT * FROM completo;

DISCARD TABLE quentes;
