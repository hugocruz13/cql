class ExpEval:
    operators = {
        "IMPORT": lambda args: args[0] + args[1],
        "SELECT": lambda args: ExpEval._select(args),
        "*": lambda args: args[0] * args[1],
        "seq": lambda args: args[-1],
        "atr": lambda args: ExpEval._attrib(args),
        "esc": lambda args: print(args[0]),
        "_select": lambda args: ExpEval._select(args)
    }
    
    @staticmethod
    def evaluate(ast):
        if type(ast) is int:  # constant value, eg in (int, str)
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
            args = [ExpEval.evaluate(a) for a in ast['args']]
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
    def _select(args):
        if not args or len(args) != 2:
            raise Exception("Erro: o operador '_select' precisa de dois argumentos: as colunas e a tabela.")
        
        columns = args[0]  # Colunas a serem selecionadas
        table_key = args[1]  # Tabela 
        
        if table_key not in ExpEval.symbols:
            raise Exception(f"Erro: chave '{table_key}' não encontrada em ExpEval.symbols.")
        
        data = ExpEval.symbols[table_key]  # A lista de dados (ex: 'observacoes')
        
        if not isinstance(data, list):
            raise Exception(f"Erro: o valor de '{table_key}' não é uma lista.")
        
        # Seleciona apenas as colunas fornecidas
        result = []
        for item in data:
            selected_item = {col: item[col] for col in columns if col in item}
            result.append(selected_item)
        
        return result


# Exemplo de como incluir um dicionário
ExpEval.symbols = {
    'observacoes': [
        {'DataHoraObservacao': '2024-05-06 12:00', 'Id': 1, 'Valor': 35.6},
        {'DataHoraObservacao': '2024-05-06 13:00', 'Id': 2, 'Valor': 36.1}
    ]
}

