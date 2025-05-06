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
                      'PROCEDURE' : 'tk_prcedure', 
                      'DO' : 'tk_do', 
                      'CALL': 'tk_call',
                      'USING': 'tk_using',
                      'SELECT': 'tk_select'                      
                    }
    tk_reserved = list(set( reservedwords.values())) 
    tokens   = ("tk_cmts_line", "tk_cmts_block", "tk_operator", "tk_key", "tk_id", "tk_nome", "tk_file", "tk_num" , "tk_reserved") + tuple(tk_reserved)
    literals = ['(', ')', '*', ';', ',']
    t_ignore = ' \n' # espaços são ignorados 

    # Comentários
    def t_tk_reserved(self, t):
        r'IMPORT|TABLE|EXPORT|DISCARD|RENAME|PRINT|FROM|WHERE|AND|LIMIT|JOIN|AS|CREATE|PROCEDURE|DO|CALL|USING|SELECT'
        t.type = self.reservedwords.get(t.value,'tk_reserved') # palavra reservada?
        return t
    
    # Comentários
    def t_tk_cmts_line(self, t):
        r"--[^\n]*"
        return t
    
    def t_tk_cmts_block(self, t):
        r"\{-[\s\S]*?-\}" # Verificar se da depois ([\s\S]*?- qualquer letra e com enter, *?-0 ou mais ocorrências,lazy)
        return t
    
    # Operadores
    def t_tk_operator(self, t):
        r"=|<>|<=|>=|<|>"
        return t

    # Colunas 
    def t_tk_key(self, t):
        r"[A-Z][a-z]*" 
        return t
  
    # Nome Tabelas
    def t_tk_id(self, t):
        r"[a-z]+" # Depois tem de incluir _
        return t
    
    # Nome Procedure
    def t_tk_nome(self, t):
        r"[a-z_]+" #Falta completar melhor
        return t
    
    # Num
    def t_tk_num(self, t):
        r"[0-9]+" 
        return t
    
    # File
    def t_tk_file(self, t):
        r'"[a-z]+[.][a-z]+"'
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
        print(f"Unexpected token: [{t.value[:10]}]")
        exit(1)
    # --------------------------------------
