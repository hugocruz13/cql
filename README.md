[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/uCocwY5e)
Processamento de Linguagens (ESI) - laboral
-----

## Trabalho prático 

### Grupo  06     

| Número | Nome          |
|--------|---------------|
| 23010  | Hugo Cruz     |
| 23016  | Dani Cruz     |
| 23279  | Hugo Baptista |

### Estrutura do projeto

  [/src](./src)   source-code

  [/img](./img) gramatica / árvore abstrata / árvore semântica
  
  [/doc](./src)   documentação / relatório do trabalho prático

  [/data](./data) ficheiros de dados a serem usados no programa (.csv) 

  [/input](./input)  CQL - Comma Query Language  (.cql)

### Dependências de módulos externos 

- [`ply`](https://pypi.org/project/ply/) — **Python Lex-Yacc**


### Exemplos de Comandos 
---
###### Importar e eliminar tabelas

```sql
IMPORT TABLE obs FROM "observacoes.csv";
```

```sql
DISCARD TABLE obs;
```
---
###### Queries

```sql
SELECT * FROM observacoes WHERE Temperatura > 10 AND Radiacao > 100 LIMIT 1;
```
---
###### Criação de Novas Tabelas

```sql
CREATE TABLE completo SELECT * FROM observacoes WHERE Temperatura > 10;
```

```sql
CREATE TABLE completo FROM est JOIN obs USING(Id);
```
---
###### Procedimentos
```sql
PROCEDURE selecionar DO
  SELECT * FROM observacoes WHERE Temperatura > 22;
  SELECT * FROM observacoes WHERE Temperatura > 10 AND Radiacao > 100;
  SELECT * FROM observacoes LIMIT 2;
END
```

```sql
CALL selecionar;
```

```sql
DELETE selecionar;
```
---
#### Ficheiro de entrada

```PYTHON
python main.py ../input/file01.cql 
```

```PYTHON
python main.py ../input/file02.cql 
```

```PYTHON
python main.py ../input/file03.cql 
```

#### Modo interativo 

```bash
python main.py 
CQL >> IMPORT TABLE obs FROM "observacoes.csv" ;  
CQL >> SELECT * FROM obs WHERE Temperatura > 10 AND Radiacao > 100;
CQL >> EXIT
```







