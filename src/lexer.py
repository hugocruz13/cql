import ply.lex as plex

class ExpLexer:
    # -------------------------------------
    # parameterização do analisador léxico 
    
    reservedwords = { 
                      'IMPORT': 'tk_import',  
                      'TABLE' : 'tk_table',
                      'EXPORT': 'tk_export',  
                      'DISCARD': 'tk_discard',  
                      'RENAME': 'tk_rename',  
                      'PRINT': 'tk_print',  
                      'FROM': 'tk_from',
                      'WHERE': 'tk_where', 
                      'AND': 'tk_and', 
                      'LIMIT': 'tk_limit', 
                      'JOIN': 'tk_join', 
                      'AS': 'tk_as',
                      'CREATE': 'tk_create',
                      'PROCEDURE' : 'tk_procedure', 
                      'DO' : 'tk_do', 
                      'CALL': 'tk_call',
                      'USING': 'tk_using',
                      'SELECT': 'tk_select',
                      'END':'tk_end'                    
                    }
    tk_reserved = list(set( reservedwords.values())) 
    tokens   = ("tk_operator", "tk_id", "tk_file", "tk_num" ,"tk_num_dec", "tk_string") + tuple(tk_reserved)
    literals = ['(', ')', '*', ';', ',']
    t_ignore = ' \n\t' # espaços são ignorados 
    
    # Linha de comentários. 
    def t_tk_cmts_line(self, t):
        r"--[^\n]*"
        pass
    
    # Bloco de comentários. 
    def t_tk_cmts_block(self, t):
        r"\{-[\s\S]*?-\}" # Verificar se da depois ([\s\S]*?- qualquer letra e com enter, *?-0 ou mais ocorrências,lazy)
        pass
    
    # Operadores.
    def t_tk_operator(self, t):
        r"=|<>|<=|>=|<|>"
        return t
    
    # Colunas, Tabelas, Procedures ou Palavras reservadas.
    def t_tk_id(self, t):
        r"[a-zA-Z][a-zA-Z0-9_]+" 
        t.type = self.reservedwords.get(t.value.upper(),'tk_id')
        return t

    # Números decimais.
    def t_tk_num_dec(self, t):
        r"[-]?[0-9]+[.][0-9]+"
        t.value = float(t.value)
        return t

    # Números inteiros.
    def t_tk_num(self, t):
        r"[0-9]+" 
        t.value = int(t.value)
        return t
    
    # Caminho para o ficheiro e o proprio ficheiro.
    def t_tk_file(self, t):
        r'"[^"]+\.[a-zA-Z0-9]+"'
        return t 
    
    # String delimitadas por ''.
    def t_tk_string(self, t):
        r"'[^']*'"
        return t

    # --------------------------------------

    # --------------------------------------

    # métodos do objeto
    def __init__(self):
        self.lexer = None
    
    def build(self, **kwargs):
        self.lexer = plex.lex(module=self, **kwargs)

    def input(self, string):
        self.lexer.input(string)
    
    def token(self):
        token = self.lexer.token()
        return token if token is None else token.type 
     
    def t_error(self, t):
        raise SyntaxError(f"Unexpected token: [{t.value[:10]}]") 

    # --------------------------------------
