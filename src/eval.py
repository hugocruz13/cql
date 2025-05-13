import csv

class ExpEval:

    operators = {
        "IMPORT": lambda args: ExpEval._import(args),
        "EXPORT": lambda args: ExpEval._export(args),
        "DISCARD": lambda args: ExpEval._discard(args),
        "RENAME": lambda args: ExpEval._rename(args),
        "PRINT": lambda args: ExpEval._print(args),       
        "SELECT": lambda args: ExpEval._select(args),
        "AND": lambda args: ExpEval.evaluate(args),
        "=": lambda args: ExpEval._equal(args),
        "<>": lambda args: ExpEval._not_equal(args),
        "<=": lambda args: ExpEval._less_or_equal(args),
        ">=": lambda args: ExpEval._greater_or_equal(args),
        "<": lambda args: ExpEval._less(args),
        ">": lambda args: ExpEval._greater(args),
        "CREATE": lambda args: ExpEval._create(args),
        "PROCEDURE": lambda args: ExpEval._procedure(args),
        "CALL": lambda args: ExpEval._call(args),
        "DELETE": lambda args: ExpEval._delete(args),
        "seq": lambda args: ExpEval._seq(args)
    }
    
    @staticmethod
    def evaluate(ast):
        #float
        if type(ast) is float:
            return ast
        if type(ast) is int:
            return ast
        if type(ast) is dict:  # { 'op': ... , 'args': ...}
            return ExpEval._eval_operator(ast)
        if type(ast) is str:
            return ast
        if type(ast) is list:
            return ast
        raise Exception(f"Unknown AST type")
    
    @staticmethod
    def _eval_operator(ast):
        if 'op' in ast:
            op = ast["op"]
            raw_args = ast['args']

            if not isinstance(raw_args, list):
                raw_args = [raw_args]

            if op == "PROCEDURE":
                if op in ExpEval.operators:
                    func = ExpEval.operators[op]
                    return func(raw_args)
                else:
                    raise Exception(f"Erro ao criar o procedure {op}")

            args = [ExpEval.evaluate(a) for a in raw_args]

            if op in ExpEval.operators:
                func = ExpEval.operators[op]
                return func(args)
            else:
                raise Exception(f"Unknown operator {op}")

        if 'var' in ast:
            varid = ast["var"]
            if varid in ExpEval.symbols:
                return ExpEval.symbols[varid]
            raise Exception(f"error: local variable '{varid}' referenced before assignment")

        raise Exception('Undefined AST')
    
    @staticmethod
    def _import(args):
        if not args or len(args) != 2:
            raise Exception("Erro: o operador 'IMPORT' precisa de dois argumentos: nome da tabela e ficheiro.")
        
        table = args[0]
        file_path = args[1]

        if table in ExpEval.symbols:
            raise Exception(f"Tabela'{table}' já existe.")
        
        try:
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                data = [row for row in reader]
                ExpEval.symbols[table] = data  # Armazena na 'tabela'
                return f"Tabela '{table}' criada com sucesso! "
        except FileNotFoundError:
            raise Exception(f"Erro: ficheiro '{file_path}' não encontrado.")
        except Exception as e:
            raise Exception(f"Erro ao importar ficheiro: {e}")
    
    @staticmethod
    def _export(args):
        if not args or len(args) != 2:
            raise Exception("Erro: o operador 'Export' precisa de dois argumentos: nome da tabela e ficheiro.")
        
        table = args[0]
        file_path = args[1]

        if table not in ExpEval.symbols:
            raise Exception(f"Erro: a tabela '{table}' não existe !")
    
        data = ExpEval.symbols[table]  #Dados que a tabela tem! 

        if not isinstance(data, list) or not data:
            raise Exception(f"Erro: a tabela '{table}' não contém dados válidos.")
    
        #Colunas 
        fieldnames = data[0].keys()

        try:
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()  # Escreve o cabeçalho
                        writer.writerows(data)  # Escreve os dados
                        return f"Tabela '{table}' exportada com sucesso! "
 
        except Exception as e:
            raise Exception(f"Erro ao exportar ficheiro: {e}")


    @staticmethod
    def _discard(args):
        if not args or len(args) != 1:
            raise Exception("Erro: o operador 'DISCARD' precisa de um argumento: a tabela.")
        
        table = args[0]
        
        if table not in ExpEval.symbols:
            raise Exception(f"Erro: a tabela '{table}' não existe")
    
        try:
            del ExpEval.symbols[table]
            return f"Tabela '{table}' eliminada com sucesso."
        except Exception as e:
            raise Exception(f"Erro ao eliminar a tabela: {e}")

    @staticmethod
    def _rename(args):
        if not args or len(args) != 2:
            raise Exception("Erro: o operador 'RENAME' precisa de dois argumento: nome atual, novo nome")
        
        table = args[0]
        table_nova = args[1]
        
        if table not in ExpEval.symbols:
            raise Exception(f"Erro: a tabela '{table}' não existe")
    
        try:
            ExpEval.symbols[table_nova] = ExpEval.symbols[table] 
            del ExpEval.symbols[table]
            return f"Nome da tabela '{table}' alterado para '{table_nova}' com sucesso! "
        except Exception as e:
            raise Exception(f"Erro ao eliminar a tabela: {e}")
        
    @staticmethod
    def _print(args):
        if not args or len(args) != 1:
            raise Exception("Erro: o operador 'PRINT' precisa de um argumento: a tabela.")
        
        table = args[0]
        
        if table not in ExpEval.symbols:
            raise Exception(f"Erro: a tabela '{table}' não existe")

        data = ExpEval.symbols[table]  #Dados que a tabela selecionada tem!

        if not isinstance(data, list) or not data:
            raise Exception(f"Erro: a tabela '{table}' não contém dados válidos.")

        try:
            for item in data:
                print(item)
        except Exception as e:
            raise Exception(f"Erro ao imprimir dados da tabela: {e}")

    @staticmethod
    def _select(args):
        try:
            if not args or len(args) < 2:
                raise Exception("Erro: SELECT necessita do nome da tabela e as colunas a selecionar.")

            columns = args[0] # Colunas a devolver pode ser [teste,test1] ou '*'
            table = args[1] # Tabela onde vamos aplicar o filtro
            filtros = [] # Lista dos filtros
            limit = None

            if columns != "*" and not isinstance(columns, list):
                raise Exception("Erro: colunas devem ser '*' ou uma lista de nomes de colunas.")

            # Se houver 3 argumentos significa que estamos a utilizar o WHERE
            if len(args) >= 3:
                if callable(args[2]):
                    filtros.append(args[2])  # Adiciona o primeiro filtro
                elif isinstance(args[2], list):  # Se for uma lista de filtros
                    filtros.extend(args[2])  # Adiciona todos os filtros dessa lista

            # Se houver 4 argumentos significa que estamos a utilizar o LIMIT
            if len(args) >= 4:
                try:
                    limit = int(args[3])
                except ValueError:
                    raise Exception("Erro: o limite deve ser um número inteiro.")

            # Verifica se a tabela existe
            if table not in ExpEval.symbols:
                raise Exception(f"Tabela '{table}' não existe.")

            # Recolhe os dados da tabela
            data = ExpEval.symbols[table]

            if not isinstance(data, list) or not data:
                raise Exception(f"Tabela '{table}' sem dados válidos.")

            # Aplica os filtros, se existir
            for filtro in filtros:
                data = list(filter(filtro, data))

            # Aplica LIMIT, se existir
            if limit is not None:
                data = data[:limit]

            # Aplica projeção de colunas
            if columns == "*":
                return data
            else:
                selected_data = []
                for row in data:
                    new_row = {col: row[col] for col in columns if col in row}
                    selected_data.append(new_row)
                return selected_data

        except Exception as e:
            raise Exception(f"Erro ao selecionar dados: {e}")

    #Filtros axiliares ao metedos _select 
    @staticmethod
    def _equal(args):
        try:
            coluna= args[0] # Coluna a filtrar.
            valor = args[1] # Valor a filtrar.
            
            # Metodo é guardado em memória para ser usado mais tarde.
            def filtro(linha):
                try:
                    return linha[coluna] == valor
                except:
                    return False
            return filtro
        
        except Exception as e:
            raise Exception(f"Erro ao criar filtro: {e}") 

    @staticmethod
    def _not_equal(args):
        try:
            coluna= args[0] # Coluna a filtrar.
            valor = args[1] # Valor a filtrar.       

            # Metodo é guardado em memória para ser usado mais tarde.
            def filtro(linha):
                try:
                    return linha[coluna] != valor
                except:
                    return False
            return filtro
        except Exception as e:
            raise Exception(f"Erro ao criar filtro: {e}") 

    @staticmethod
    def _less_or_equal(args):
        try:
            if isinstance(args[1], str):
                raise Exception("Erro: A operação <= não permite strings")
            
            coluna= args[0]
            valor = float(args[1])
            
            def filtro(linha):
                try:
                    return float(linha[coluna]) <= valor
                except:
                    return False
            return filtro
        except Exception as e:
            raise Exception(f"Erro ao selecionar dados: {e}") 
    @staticmethod
    def _greater_or_equal(args):
        try:
            if isinstance(args[1], str):
                raise Exception(f"Erro ao criar filtro: {e}")
            
            coluna= args[0]
            valor = float(args[1])
            
            def filtro(linha):
                try:
                    return float(linha[coluna]) >= valor
                except:
                    return False
            return filtro
        except Exception as e:
            raise Exception(f"Erro ao criar filtro: {e}")    
    @staticmethod
    def _less(args):
        try:
            if isinstance(args[1], str):
                raise Exception("Erro: A operação < não permite strings")
            coluna= args[0]
            valor = float(args[1])
            
            def filtro(linha):
                try:
                    return float(linha[coluna]) < valor
                except:
                    return False
            return filtro
        except Exception as e:
            raise Exception(f"Erro ao criar filtro: {e}") 
    
    @staticmethod
    def _greater(args):
        try:
            if isinstance(args[1], str):
                raise Exception("Erro: A operação > não permite strings")
            coluna= args[0]
            valor = float(args[1])
            
            def filtro(linha):
                try:
                    return float(linha[coluna]) > valor
                except:
                    return False
            return filtro
        except Exception as e:
            raise Exception(f"Erro ao criar filtro: {e}") 
        
    @staticmethod
    def _create(args):
        if not args or len(args) != 2:
            raise Exception("Erro: o operador 'CREATE' precisa de dois argumentos: nome da tabela e os dados.")
        
        table = args[0]
        data = args[1]

        if table in ExpEval.symbols:
            raise Exception(f"Tabela'{table}' já existe.")
        try:
                ExpEval.symbols[table] = data  # Armazena na 'tabela'
                return f"Tabela '{table}' criada com sucesso! "
        except Exception as e:
            raise Exception(f"Erro ao importar ficheiro: {e}")
        
    @staticmethod
    def _procedure(args):
        if not args or len(args) != 2:
            raise Exception("Erro: o operador 'PROCEDURE' precisa de dois argumentos: nome do procedimento e comandos.")

        proc_name = args[0]
        commands = args[1]

        if proc_name in ExpEval.procedure:
            raise Exception(f"Procedimento '{proc_name}' já existe.")

        if not isinstance(commands, dict):
            raise Exception("Erro: os comandos do procedimento devem estar em uma lista.")

        try:
            ExpEval.procedure[proc_name] = commands
            return f"Procedimento '{proc_name}' criado com sucesso!"
        except Exception as e:
            raise Exception(f"Erro ao criar o procedure: {e}")
    
    @staticmethod
    def _call(args):
        if not args or len(args) != 1:
            raise Exception("Erro: o operador 'CALL' apenas precisa de 1 argumento.")

        proc_name = args[0]

        if proc_name not in ExpEval.procedure:
            raise Exception(f"Procedimento '{proc_name}' não existe.")

        try:
            procedure_body = ExpEval.procedure[proc_name]
            result = ExpEval.evaluate(procedure_body)
            print("Procedure executado com sucesso!")
            return result
        except Exception as e:
            raise Exception(f"Erro ao criar o procedure: {e}")
        
    @staticmethod
    def _delete(args):
        if not args or len(args) != 1:
            raise Exception("Erro: o operador 'DELETE' apenas precisa de 1 argumento.")

        proc_name = args[0]

        if proc_name not in ExpEval.procedure:
            raise Exception(f"Procedimento '{proc_name}' não existe.")

        try:
            del ExpEval.procedure[proc_name]
            return f"Procedure '{proc_name}' eliminada com sucesso."
        except Exception as e:
            raise Exception(f"Erro ao criar o procedure: {e}")
    
    @staticmethod
    def _seq(args):
        results = []
        for cmd in args:
            result = ExpEval.evaluate(cmd)
            results.append(result)
        return results


ExpEval.symbols = {} 
ExpEval.procedure = {}
