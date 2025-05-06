from lexer import ExpLexer
import ply.yacc as pyacc

class Grammar:

    def __init__(self):
        self.yacc = None
        self.lexer = None
        self.tokens = None

    def build(self, **kwargs):
        self.lexer = ExpLexer()
        self.lexer.build(**kwargs)
        self.tokens = self.lexer.tokens
        self.yacc = pyacc.yacc(module=self, **kwargs)

    def parse(self, string):
        self.lexer.input(string)
        return self.yacc.parse(lexer=self.lexer.lexer)

    # especificação da gramática G=<N,T,S,P>:
    #  N={PROG,CMDLIST,CMD,QRS,NEW,PROCS,CMTS,}  T={id, file, ';'}, S é o axioma da gramática
    #  P tem as seguintes regras de produção: 
    #   p1:    PROG → CMDLIST
	#   p2: CMDLIST → CMD 
	#   p3:         | CMD CMDLIST			
	#   p4:     CMD → CONF
	#   p5:         | QRS
	#   p6:         | NEW
	#   p7:         | PROCS
	#	p8:         | CMTS		
	#   p9:     CONF → "IMPORT" "TABLE" id "FROM" file ';'
	#	p10:         | "EXPORT" "TABLE" id "AS" file ';'
	#   p11:	     | "DISCARD" "TABLE" id ';'
	#   p12:	     | "RENAME" "TABLE" id id ';'
	#   p13:         | "PRINT" "TABLE" id ';'	
	#   p14:    QRS → "SELECT" SELEC "FROM" id ';' 
    #   p15:        | "SELECT" SELEC "FROM" id "WHERE" CONDLIST ';'
	#   p16:	    | "SELECT" SELEC "FROM" id "LIMIT" num ';' 
    #   p17:        | "SELECT" SELEC "FROM" id "WHERE" CONDLIST "LIMIT" num';'	
	#   p18:    SELEC → '*'
    #   p19:          | COLLIST		
	#   p20:    COLLIST → key
	#   p21:            | key, COLLIST
	#   p22:    CONDLIST → COND "AND" CONDLIST
    #   p23:             | COND	   
	#   p24:    COND → key Operador VALOR 
	#   p25:    Operador → '=' 
	#   p26:             | '<>' 
	#   p27:  		     | '<' 
	#	p28:      	     | '>' 
	#   p29:       	     | '<=' 
	#	p30:             | '>=' 
	#   p31:    VALOR → num
	#   p32:          | string
	#   p33:    NEW → "CREATE" "TABLE" id QRS ';'
	#	p34:        | "CREATE" "TABLE" id "FROM" id "JOIN" id "USING"'('key')' ';'
	#   p35:    PROCS → "PROCEDURE" nome "DO" CMDLIST "END"
	#   p36:          | "CALL" nome ';'
	#   p37:    CMTS → '--' ate ao fim
	#   p38:         | '{-' texto_varias_linhas '-}'
    # -----------------------------


    def p_p1(self, p):
        """ PROG  : CMDLIST """
        print('reduce', "PROG  : CMDLIST") 
    
    def p_p2(self, p):
        """ CMDLIST  : CMD """
        print('reduce', "CMDLIST  : CMD") 
    
    def p_p3(self, p):
        """ CMDLIST  : CMD CMDLIST	  """
        print('reduce', "CMDLIST  : CMD CMDLIST")
        
    def p_p4(self, p):
        """ CMD  : CONF	  """
        print('reduce', "CMD  : CONF") 

    def p_p9(self, p):
        """ CONF  : tk_import tk_table tk_id tk_from tk_file ';'"""
        file_path = p[5][1:-1] if p[5].startswith('"') and p[5].endswith('"') else p[5]
    
        # Estrutura de dados mais organizada
        p[0] = {
            'type': 'import_statement',
            'command': {
                'action': p[1],    # 'IMPORT'
                'target': p[2],    # 'TABLE'
            },
            'table': p[3],         # nome da tabela
            'source': file_path,   # caminho do arquivo sem aspas
            'position': {
                'line': p.lineno(1)  # linha onde começou a regra
            }
        }
    
        # Formatação de saída mais limpa
        print(f"{p[1]} {p[2]} {p[3]} {p[4]} {file_path};")


    # ---------------------------------------------  
    def p_error(self, p):
        if p:
            print(f"Syntax error: unexpected '{p.type}'")
        else:
            print("Syntax error: unexpected end of file")
        #exit(1)
