IMPORT TABLE observacoes FROM "../data/observacoes.csv"; --teste
SELECT * FROM observacoes;
SELECT Temperatura FROM observacoes WHERE Temperatura > 22;  
SELECT Id,Temperatura FROM observacoes WHERE Temperatura > 22 AND Id = 'E1';  
SELECT Id FROM observacoes WHERE Id = 'E4'; 
SELECT Temperatura,Radiacao FROM observacoes WHERE Temperatura > 16 AND Radiacao >= 100;  
EXPORT TABLE observacoes AS "obs.csv";
PRINT TABLE observacoes;
SELECT Radiacao,Temperatura FROM observacoes WHERE Temperatura > 16 AND Radiacao >= 100 LIMIT 1;