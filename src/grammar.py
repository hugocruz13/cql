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
	#   p8:      CONF → "IMPORT" "TABLE" id "FROM" file ';'
	#	p9:           | "EXPORT" "TABLE" id "AS" file ';'
	#   p10:	      | "DISCARD" "TABLE" id ';'
	#   p11:	      | "RENAME" "TABLE" id id ';'
	#   p12:          | "PRINT" "TABLE" id ';'	
	#   p13:      QRS → "SELECT" SELEC "FROM" id ';' 
    #   p14:          | "SELECT" SELEC "FROM" id "WHERE" CONDLIST ';'
	#   p15:	      | "SELECT" SELEC "FROM" id "LIMIT" num ';' 
    #   p16:          | "SELECT" SELEC "FROM" id "WHERE" CONDLIST "LIMIT" num';'	
	#   p17:    SELEC → '*'
    #   p18:          | COLLIST		
	#   p19:  COLLIST → key
	#   p20:          | key, COLLIST
	#   p21: CONDLIST → COND "AND" CONDLIST
    #   p22:          | COND	   
	#   p23:     COND → key OPERADOR VALOR 
	#   p24: OPERADOR → operador
	#   p25:    VALOR → num
	#   p26:          | string
    #   p27:          | numdec
	#   p28:      NEW → "CREATE" "TABLE" QRS
	#	p29:          | "CREATE" "TABLE" id "FROM" id "JOIN" id "USING"'('key')' ';'
	#   p30:    PROCS → "PROCEDURE" nome "DO" CMDLIST "END"
	#   p31:          | "CALL" nome ';'
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
        """ CONF  : tk_import tk_table tk_id tk_from tk_file ';'"""
        print('reduce', "CONF  : tk_import tk_table tk_id tk_from tk_file ';'")
        p[0] = {'op': p[1], 'args': [p[3], p[5].strip('"')]} #strip remover caracteres do início e do fim de uma string

    def p_p9(self, p):
        """ CONF  : tk_export tk_table tk_id tk_as tk_file ';'"""
        print('reduce', "CONF  : tk_export tk_table tk_id tk_as tk_file ';'")
        p[0] = {'op':p[1],'args':[p[3],p[5].strip('"')]} #strip remover caracteres do início e do fim de uma string

    def p_p10(self, p):
        """ CONF  : tk_discard tk_table tk_id ';'"""
        print('reduce', "CONF  : tk_discard tk_table tk_id ';'")
        p[0] = {'op':p[1],'args':p[3]}

    def p_p11(self, p):
        """ CONF  : tk_rename tk_table tk_id tk_id ';'"""
        print('reduce', "CONF  : tk_rename tk_table tk_id tk_id ';'")
        p[0] = {'op':p[1],'args':[p[3],p[4]]}

    def p_p12(self, p):
        """ CONF  : tk_print tk_table tk_id ';'"""
        print('reduce', "CONF  : tk_print tk_table tk_id ';'")
        p[0] = {'op':p[1],'args':p[3]}
        
    def p_p13(self, p):
        """ QRS  : tk_select SELEC tk_from tk_id ';' """
        print('reduce', "QRS  : tk_select SELEC tk_from tk_id ';'")
        p[0] = {'op':p[1],'args':[p[2], p[4]]}
    
    def p_p14(self, p):
        """ QRS  : tk_select SELEC tk_from tk_id tk_where CONDLIST ';' """
        print('reduce', "QRS  : tk_select SELEC tk_from tk_id tk_where CONDLIST ';'")
        p[0] = {'op':p[1],'args':[p[2], p[4], p[6]]}

    def p_p15(self, p):
        """ QRS  : tk_select SELEC tk_from tk_id tk_limit tk_num ';' """
        print('reduce', "QRS  : tk_select SELEC tk_from tk_id tk_limit tk_num ';'")
        p[0] = {'op':p[1],'args':[p[2], p[4], p[6]]}

    def p_p16(self, p):
        """ QRS  : tk_select SELEC tk_from tk_id tk_where CONDLIST tk_limit tk_num ';' """
        print('reduce', "QRS  : tk_select SELEC tk_from tk_id tk_where CONDLIST tk_limit tk_num ';'")
        p[0] = {'op':p[1],'args':[p[2], p[4], p[6], p[8]]}

    def p_p17(self, p):
        """ SELEC  : '*' """
        print('reduce', "SELEC  : '*'")
        p[0] = p[1]

    def p_p18(self, p):
        """ SELEC  : COLLIST """
        print('reduce', "SELEC  : COLLIST")
        p[0] = p[1]

    def p_p19(self, p):
        """ COLLIST  : tk_id """
        print('reduce', "COLLIST  : tk_id")
        p[0] = [p[1]]
    
    def p_p20(self, p):
        """ COLLIST  : tk_id ',' COLLIST """
        print('reduce', "COLLIST  : tk_id ',' COLLIST")
        p[0] = [p[1]] + p[3]
                        
    def p_p21(self, p):
        """ CONDLIST  : COND tk_and CONDLIST """
        print('reduce', "CONDLIST  : COND tk_and CONDLIST")
        p[0] = {'op': 'AND', 'args': [p[1], p[3]]}
        
    def p_p22(self, p):
        """ CONDLIST  : COND """
        print('reduce', "CONDLIST  : COND")
        p[0] = p[1]
    
    def p_p23(self, p):
        """ COND  : tk_id OPERADOR VALOR """
        print('reduce', "COND  : tk_id OPERADOR VALOR")
        p[0] = {'op': p[2], 'args': [p[1], p[3]]}

    def p_p24(self, p):                            
        """ OPERADOR  : tk_operator """
        print('reduce', "OPERADOR  : tk_operator")
        p[0] = p[1]

    def p_p25(self, p):
        """ VALOR  : tk_num """
        print('reduce', "VALOR  : tk_num")
        p[0] = p[1]

    def p_p26(self, p):
        """ VALOR  : tk_string """
        print('reduce', "VALOR  : tk_string")
        p[0] = p[1].strip("'")

    def p_p27(self, p):
        """ VALOR  : tk_num_dec """
        print('reduce', "VALOR  : tk_num_dec")     
        p[0] = p[1] 

    def p_p28(self, p):
        """ NEW  : tk_create tk_table tk_id QRS"""
        print('reduce', "NEW  : tk_create tk_table tk_id QRS")
        p[0] = {'op': p[1], 'args': [p[3], p[4]]}
        
    def p_p29(self, p):
        """ NEW  : tk_create tk_table tk_id tk_from tk_id tk_join tk_id tk_using '(' tk_id ')' ';' """
        print('reduce', "NEW  : tk_create tk_table tk_id tk_from tk_id tk_join tk_id tk_using '(' tk_id ')' ';'")
        p[0] = {'op': p[1],'args': [p[3],{'op': 'join','args': [p[5], p[7], p[10]]}]}

    def p_p30(self, p):
        """ PROCS  : tk_procedure tk_id tk_do CMDLIST tk_end"""
        print('reduce', "PROCS  : tk_procedure tk_id tk_do CMDLIST tk_end")
        p[0] = {'op': p[1], 'args': [p[2], p[4]]}

    def p_p31(self, p):
        """ PROCS  : tk_call tk_id ';' """
        print('reduce', "PROCS  : tk_call tk_id ';'")
        p[0] = {'op': p[1], 'args': p[2]}

    # ---------------------------------------------  
    def p_error(self, p):
        if p:
            print(f"Syntax error: unexpected '{p.type}'")
        else:
            print("Syntax error: unexpected end of file")
        #exit(1)
