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
    #   p1:      PROG → CMDLIST
	#   p2:   CMDLIST → CMD 
	#   p3:           | CMD CMDLIST			
	#   p4:       CMD → CONF
	#   p5:           | QRS
	#   p6:           | NEW
	#   p7:           | PROCS
	#	p8:           | CMTS		
	#   p9:      CONF → "IMPORT" "TABLE" id "FROM" file ';'
	#	p10:          | "EXPORT" "TABLE" id "AS" file ';'
	#   p11:	      | "DISCARD" "TABLE" id ';'
	#   p12:	      | "RENAME" "TABLE" id id ';'
	#   p13:          | "PRINT" "TABLE" id ';'	
	#   p14:      QRS → "SELECT" SELEC "FROM" id ';' 
    #   p15:          | "SELECT" SELEC "FROM" id "WHERE" CONDLIST ';'
	#   p16:	      | "SELECT" SELEC "FROM" id "LIMIT" num ';' 
    #   p17:          | "SELECT" SELEC "FROM" id "WHERE" CONDLIST "LIMIT" num';'	
	#   p18:    SELEC → '*'
    #   p19:          | COLLIST		
	#   p20:  COLLIST → key
	#   p21:          | key, COLLIST
	#   p22: CONDLIST → COND "AND" CONDLIST
    #   p23:          | COND	   
	#   p24:     COND → key OPERADOR VALOR 
	#   p25: OPERADOR → operador
	#   p26:    VALOR → num
	#   p27:          | string
    #   p28:          | numdec
	#   p29:      NEW → "CREATE" "TABLE" id "SELECT" SELEC "FROM" id "WHERE" CONDLIST ';'
	#	p30:          | "CREATE" "TABLE" id "FROM" id "JOIN" id "USING"'('key')' ';'
	#   p31:    PROCS → "PROCEDURE" nome "DO" CMDLIST "END"
	#   p32:          | "CALL" nome ';'
	#   p33:     CMTS → '--' ate ao fim
	#   p34:          | '{-' texto_varias_linhas '-}'
    # -----------------------------


    def p_p1(self, p):
        """ PROG  : CMDLIST """
        print('reduce', "PROG  : CMDLIST") 
        p[0] = p[1]
    
    def p_p2(self, p):
        """ CMDLIST  : CMD """
        print('reduce', "CMDLIST  : CMD") 
        p[0] = p[1]
    
    def p_p3(self, p):
        """ CMDLIST  : CMD CMDLIST	  """
        print('reduce', "CMDLIST  : CMD CMDLIST")
        p[0] = {'op': 'seq', 'args': [p[1], p[2]]}
        
    def p_p4(self, p):
        """ CMD  : CONF	  """
        print('reduce', "CMD  : CONF") 
        p[0] = p[1]
    
    def p_p5(self, p):
        """ CMD  : QRS	  """
        print('reduce', "CMD  : QRS") 
        p[0] = p[1]

    def p_p6(self, p):
        """ CMD  : NEW	  """
        print('reduce', "CMD  : NEW")
        p[0] = p[1] 

    def p_p7(self, p):
        """ CMD  : PROCS	  """
        print('reduce', "CMD  : PROCS")
        p[0] = p[1]   

    def p_p8(self, p):
        """ CMD  : CMTS	  """
        print('reduce', "CMD  : CMTS")
        p[0] = p[1]           

    def p_p9(self, p):
        """ CONF  : tk_import tk_table tk_id tk_from tk_file ';'"""
        print('reduce', "CONF  : tk_import tk_table tk_id tk_from tk_file ';'")
        p[0] = {'op': p[1], 'args': [p[3], p[5].strip('"')]} #strip remover caracteres do início e do fim de uma string

    def p_p10(self, p):
        """ CONF  : tk_export tk_table tk_id tk_as tk_file ';'"""
        print('reduce', "CONF  : tk_export tk_table tk_id tk_as tk_file ';'")
        p[0] = {'op':p[1],'args':[p[3],p[5].strip('"')]} #strip remover caracteres do início e do fim de uma string

    def p_p11(self, p):
        """ CONF  : tk_discard tk_table tk_id ';'"""
        print('reduce', "CONF  : tk_discard tk_table tk_id ';'")
        p[0] = {'op':p[1],'args':p[3]}

    def p_p12(self, p):
        """ CONF  : tk_rename tk_table tk_id tk_id ';'"""
        print('reduce', "CONF  : tk_rename tk_table tk_id tk_id ';'")
        p[0] = {'op':p[1],'args':[p[3],p[4]]}

    def p_p13(self, p):
        """ CONF  : tk_print tk_table tk_id ';'"""
        print('reduce', "CONF  : tk_print tk_table tk_id ';'")
        p[0] = {'op':p[1],'args':p[3]}
        
    def p_p14(self, p):
        """ QRS  : tk_select SELEC tk_from tk_id ';' """
        print('reduce', "QRS  : tk_select SELEC tk_from tk_id ';'")
        p[0] = {'op':p[1],'args':[p[2], p[4]]}
    
    def p_p15(self, p):
        """ QRS  : tk_select SELEC tk_from tk_id tk_where CONDLIST ';' """
        print('reduce', "QRS  : tk_select SELEC tk_from tk_id tk_where CONDLIST ';'")
        p[0] = {'op':p[1],'args':[p[2], p[4], p[6]]}

    def p_p16(self, p):
        """ QRS  : tk_select SELEC tk_from tk_id tk_limit tk_num ';' """
        print('reduce', "QRS  : tk_select SELEC tk_from tk_id tk_limit tk_num ';'")

    def p_p17(self, p):
        """ QRS  : tk_select SELEC tk_from tk_id tk_where CONDLIST tk_limit tk_num ';' """
        print('reduce', "QRS  : tk_select SELEC tk_from tk_id tk_where CONDLIST tk_limit tk_num ';'")

    def p_p18(self, p):
        """ SELEC  : '*' """
        print('reduce', "SELEC  : '*'")

    def p_p19(self, p):
        """ SELEC  : COLLIST """
        print('reduce', "SELEC  : COLLIST")
        p[0] = p[1]

    def p_p20(self, p):
        """ COLLIST  : tk_id """
        print('reduce', "COLLIST  : tk_id")
        p[0] = p[1]
    
    def p_p21(self, p):
        """ COLLIST  : tk_id ',' COLLIST """
        print('reduce', "COLLIST  : tk_id ',' COLLIST")
        p[0] = [p[1]] + p[3]
                        
    def p_p22(self, p):
        """ CONDLIST  : COND tk_and CONDLIST """
        print('reduce', "CONDLIST  : COND tk_and CONDLIST")
        
    def p_p23(self, p):
        """ CONDLIST  : COND """
        print('reduce', "CONDLIST  : COND")
    
    def p_p24(self, p):
        """ COND  : tk_id OPERADOR VALOR """
        print('reduce', "COND  : tk_id OPERADOR VALOR")

    def p_p25(self, p):                            
        """ OPERADOR  : tk_operator """
        print('reduce', "OPERADOR  : tk_operator")
        p[0] = p[1]

    def p_p26(self, p):
        """ VALOR  : tk_num """
        print('reduce', "VALOR  : tk_num")
        p[0] = p[1]

    def p_p27(self, p):
        """ VALOR  : tk_string """
        print('reduce', "VALOR  : tk_string")
        p[0] = p[1]

    def p_p28(self, p):
        """ VALOR  : tk_num_dec """
        print('reduce', "VALOR  : tk_num_dec")     
        p[0] = p[1] 

    def p_p29(self, p):
        """ NEW  : tk_create tk_table tk_id QRS"""
        print('reduce', "NEW  : tk_create tk_table tk_id QRS")
        
    def p_p30(self, p):
        """ NEW  : tk_create tk_table tk_id tk_from tk_id tk_join tk_id tk_using '(' tk_id ')' ';' """
        print('reduce', "NEW  : tk_create tk_table tk_id tk_from tk_id tk_join tk_id tk_using '(' tk_id ')' ';'")

    def p_p31(self, p):
        """ PROCS  : tk_procedure tk_id tk_do CMDLIST tk_end"""
        print('reduce', "PROCS  : tk_procedure tk_id tk_do CMDLIST tk_end")

    def p_p32(self, p):
        """ PROCS  : tk_call tk_id ';' """
        print('reduce', "PROCS  : tk_call tk_id ';'")

    def p_p33(self, p):
        """ CMTS  : tk_cmts_line """
        print('reduce', "CMTS  : tk_cmts_line")

    def p_p34(self, p):
        """ CMTS  : tk_cmts_block """
        print('reduce', "CMTS  : tk_cmts_block") 

    # ---------------------------------------------  
    def p_error(self, p):
        if p:
            print(f"Syntax error: unexpected '{p.type}'")
        else:
            print("Syntax error: unexpected end of file")
        #exit(1)
