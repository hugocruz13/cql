import csv

class ExpEval:

    operators = {
        "IMPORT": lambda args: ExpEval._import(args),
        "EXPORT": lambda args: ExpEval._export(args),
        "DISCARD": lambda args: ExpEval._discard(args),
        "RENAME": lambda args: ExpEval._rename(args),
        "PRINT": lambda args: ExpEval._print(args),       
        "SELECT": lambda args: ExpEval._select(args),
        "=": lambda args: ExpEval._equal(args),
        "<>": lambda args: ExpEval._not_equal(args),
        "<=": lambda args: ExpEval._less_or_equal(args),
        ">=": lambda args: ExpEval._greater_or_equal(args),
        "<": lambda args: ExpEval._less(args),
        ">": lambda args: ExpEval._greater(args),
    }
    
    @staticmethod
    def evaluate(ast):
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
            return f"Dados da tabela '{table}' imprimidos com sucesso."
        except Exception as e:
            raise Exception(f"Erro ao imprimir dados da tabela: {e}")

    @staticmethod
    def _select(args):
        try:
            if not args or len(args) < 2:
                raise Exception("Erro: SELECT precisa de pelo menos colunas e nome da tabela.")

            columns = args[0]
            table = args[1]
            filtro = None
            limit = None
            
            if len(args) >= 3 and callable(args[2]):
                filtro = args[2]
            if len(args) >= 4:
                try:
                    limit = int(args[3])
                except ValueError:
                    raise Exception("Erro: o limite deve ser um número inteiro.")

            if table not in ExpEval.symbols:
                raise Exception(f"Tabela '{table}' não existe.")

            data = ExpEval.symbols[table]

            if not isinstance(data, list) or not data:
                raise Exception(f"Tabela '{table}' sem dados válidos.")

            # Aplica filtro, se existir
            if filtro:
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

    @staticmethod
    def _equal(args):
        coluna= args[0]
        valor = float(args[1])
        
        def filtro(linha):
            try:
                return float(linha[coluna]) == valor
            except:
                return False
        return filtro

    @staticmethod
    def _not_equal(args):
        coluna= args[0]
        valor = float(args[1])
        
        def filtro(linha):
            try:
                return float(linha[coluna]) != valor
            except:
                return False
        return filtro

    @staticmethod
    def _less_or_equal(args):
        coluna= args[0]
        valor = float(args[1])
        
        def filtro(linha):
            try:
                return float(linha[coluna]) <= valor
            except:
                return False
        return filtro

    @staticmethod
    def _greater_or_equal(args):
        coluna= args[0]
        valor = float(args[1])
        
        def filtro(linha):
            try:
                return float(linha[coluna]) >= valor
            except:
                return False
        return filtro
    
    @staticmethod
    def _less(args):
        coluna= args[0]
        valor = float(args[1])
        
        def filtro(linha):
            try:
                return float(linha[coluna]) < valor
            except:
                return False
        return filtro
    
    @staticmethod
    def _greater(args):
        coluna= args[0]
        valor = float(args[1])
        
        def filtro(linha):
            try:
                return float(linha[coluna]) > valor
            except:
                return False
        return filtro
    


ExpEval.symbols = {} 
