
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'AND ASSIGN BOOL BREAK COMMA DIVIDE DO ELSE EQ FALSE FI FLOAT GE GT IDENTIFIER IF INT LBRACE LE LPAREN LT MINUS NE NOT NUMBER OR PLUS POWER PROGRAM RBRACE READ RPAREN SEMICOLON TB TIMES TRUE UNTIL WHILE WRITEprogram : PROGRAM LBRACE list_decl list_sent RBRACElist_decl : list_decl decl\n                 | decl\n                 | emptydecl : tipo list_id SEMICOLONtipo : INT\n            | FLOAT\n            | BOOLlist_id : list_id COMMA IDENTIFIER\n               | IDENTIFIERlist_sent : list_sent sent\n                 | sent\n                 | emptysent : sent_if\n            | sent_while\n            | sent_do\n            | sent_read\n            | sent_write\n            | bloque\n            | sent_assign\n            | BREAKsent_if : IF LPAREN exp_bool RPAREN bloque else_part FIelse_part : ELSE bloque\n                 | emptysent_while : WHILE LPAREN exp_bool RPAREN bloquesent_do : DO bloque UNTIL LPAREN exp_bool RPAREN SEMICOLONsent_read : READ IDENTIFIER SEMICOLONsent_write : WRITE exp_bool SEMICOLONbloque : LBRACE list_sent RBRACEsent_assign : IDENTIFIER ASSIGN exp_bool SEMICOLONexp_bool : exp_bool OR comb\n                | combcomb : comb AND igualdad\n            | igualdadigualdad : igualdad EQ rel\n                | igualdad NE rel\n                | relrel : expr op_rel exprop_rel : LT\n              | LE\n              | GT\n              | GEexpr : expr PLUS term\n            | expr MINUS term\n            | termterm : term TIMES unario\n            | term DIVIDE unario\n            | unariounario : PLUS unario\n              | MINUS unario\n              | factorfactor : NUMBER\n              | IDENTIFIER\n              | LPAREN exp_bool RPARENempty :'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,33,],[0,-1,]),'LBRACE':([2,3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,22,23,26,32,34,53,55,59,61,79,80,82,94,97,100,102,],[3,-55,11,-3,-4,11,11,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,11,11,-11,-5,-29,-27,-28,11,11,-30,-25,11,-22,-26,]),'BREAK':([3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,22,23,32,34,53,55,59,61,82,94,100,102,],[-55,23,-3,-4,23,23,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,23,-11,-5,-29,-27,-28,-30,-25,-22,-26,]),'INT':([3,4,5,6,13,53,],[8,8,-3,-4,-2,-5,]),'FLOAT':([3,4,5,6,13,53,],[9,9,-3,-4,-2,-5,]),'BOOL':([3,4,5,6,13,53,],[10,10,-3,-4,-2,-5,]),'IF':([3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,22,23,32,34,53,55,59,61,82,94,100,102,],[-55,24,-3,-4,24,24,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,24,-11,-5,-29,-27,-28,-30,-25,-22,-26,]),'WHILE':([3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,22,23,32,34,53,55,59,61,82,94,100,102,],[-55,25,-3,-4,25,25,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,25,-11,-5,-29,-27,-28,-30,-25,-22,-26,]),'DO':([3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,22,23,32,34,53,55,59,61,82,94,100,102,],[-55,26,-3,-4,26,26,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,26,-11,-5,-29,-27,-28,-30,-25,-22,-26,]),'READ':([3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,22,23,32,34,53,55,59,61,82,94,100,102,],[-55,27,-3,-4,27,27,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,27,-11,-5,-29,-27,-28,-30,-25,-22,-26,]),'WRITE':([3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,22,23,32,34,53,55,59,61,82,94,100,102,],[-55,29,-3,-4,29,29,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,29,-11,-5,-29,-27,-28,-30,-25,-22,-26,]),'IDENTIFIER':([3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,27,29,32,34,35,36,39,45,47,52,53,54,55,59,61,62,63,64,65,66,67,68,69,70,71,72,74,75,81,82,94,100,102,],[-55,28,-3,-4,31,-6,-7,-8,28,28,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,38,51,28,-11,51,51,51,51,51,51,-5,78,-29,-27,-28,51,51,51,51,51,51,51,-39,-40,-41,-42,51,51,51,-30,-25,-22,-26,]),'RBRACE':([3,4,5,6,11,12,13,14,15,16,17,18,19,20,21,22,23,32,34,53,55,59,61,82,94,100,102,],[-55,-55,-3,-4,-55,33,-2,-12,-13,-14,-15,-16,-17,-18,-19,-20,-21,55,-11,-5,-29,-27,-28,-30,-25,-22,-26,]),'LPAREN':([24,25,29,35,36,39,45,47,52,58,62,63,64,65,66,67,68,69,70,71,72,74,75,81,],[35,36,52,52,52,52,52,52,52,81,52,52,52,52,52,52,52,-39,-40,-41,-42,52,52,52,]),'ASSIGN':([28,],[39,]),'PLUS':([29,35,36,39,44,45,46,47,48,49,50,51,52,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,81,87,88,89,90,91,92,],[45,45,45,45,67,45,-45,45,-48,-51,-52,-53,45,45,45,45,45,45,45,45,-39,-40,-41,-42,-49,45,45,-50,45,67,-43,-44,-46,-47,-54,]),'MINUS':([29,35,36,39,44,45,46,47,48,49,50,51,52,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,81,87,88,89,90,91,92,],[47,47,47,47,68,47,-45,47,-48,-51,-52,-53,47,47,47,47,47,47,47,47,-39,-40,-41,-42,-49,47,47,-50,47,68,-43,-44,-46,-47,-54,]),'NUMBER':([29,35,36,39,45,47,52,62,63,64,65,66,67,68,69,70,71,72,74,75,81,],[50,50,50,50,50,50,50,50,50,50,50,50,50,50,-39,-40,-41,-42,50,50,50,]),'SEMICOLON':([30,31,38,40,41,42,43,46,48,49,50,51,60,73,76,78,83,84,85,86,87,88,89,90,91,92,99,],[53,-10,59,61,-32,-34,-37,-45,-48,-51,-52,-53,82,-49,-50,-9,-31,-33,-35,-36,-38,-43,-44,-46,-47,-54,102,]),'COMMA':([30,31,78,],[54,-10,-9,]),'UNTIL':([37,55,],[58,-29,]),'OR':([40,41,42,43,46,48,49,50,51,56,57,60,73,76,77,83,84,85,86,87,88,89,90,91,92,95,],[62,-32,-34,-37,-45,-48,-51,-52,-53,62,62,62,-49,-50,62,-31,-33,-35,-36,-38,-43,-44,-46,-47,-54,62,]),'RPAREN':([41,42,43,46,48,49,50,51,56,57,73,76,77,83,84,85,86,87,88,89,90,91,92,95,],[-32,-34,-37,-45,-48,-51,-52,-53,79,80,-49,-50,92,-31,-33,-35,-36,-38,-43,-44,-46,-47,-54,99,]),'AND':([41,42,43,46,48,49,50,51,73,76,83,84,85,86,87,88,89,90,91,92,],[63,-34,-37,-45,-48,-51,-52,-53,-49,-50,63,-33,-35,-36,-38,-43,-44,-46,-47,-54,]),'EQ':([42,43,46,48,49,50,51,73,76,84,85,86,87,88,89,90,91,92,],[64,-37,-45,-48,-51,-52,-53,-49,-50,64,-35,-36,-38,-43,-44,-46,-47,-54,]),'NE':([42,43,46,48,49,50,51,73,76,84,85,86,87,88,89,90,91,92,],[65,-37,-45,-48,-51,-52,-53,-49,-50,65,-35,-36,-38,-43,-44,-46,-47,-54,]),'LT':([44,46,48,49,50,51,73,76,88,89,90,91,92,],[69,-45,-48,-51,-52,-53,-49,-50,-43,-44,-46,-47,-54,]),'LE':([44,46,48,49,50,51,73,76,88,89,90,91,92,],[70,-45,-48,-51,-52,-53,-49,-50,-43,-44,-46,-47,-54,]),'GT':([44,46,48,49,50,51,73,76,88,89,90,91,92,],[71,-45,-48,-51,-52,-53,-49,-50,-43,-44,-46,-47,-54,]),'GE':([44,46,48,49,50,51,73,76,88,89,90,91,92,],[72,-45,-48,-51,-52,-53,-49,-50,-43,-44,-46,-47,-54,]),'TIMES':([46,48,49,50,51,73,76,88,89,90,91,92,],[74,-48,-51,-52,-53,-49,-50,74,74,-46,-47,-54,]),'DIVIDE':([46,48,49,50,51,73,76,88,89,90,91,92,],[75,-48,-51,-52,-53,-49,-50,75,75,-46,-47,-54,]),'ELSE':([55,93,],[-29,97,]),'FI':([55,93,96,98,101,],[-29,-55,100,-24,-23,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'list_decl':([3,],[4,]),'decl':([3,4,],[5,13,]),'empty':([3,4,11,93,],[6,15,15,98,]),'tipo':([3,4,],[7,7,]),'list_sent':([4,11,],[12,32,]),'sent':([4,11,12,32,],[14,14,34,34,]),'sent_if':([4,11,12,32,],[16,16,16,16,]),'sent_while':([4,11,12,32,],[17,17,17,17,]),'sent_do':([4,11,12,32,],[18,18,18,18,]),'sent_read':([4,11,12,32,],[19,19,19,19,]),'sent_write':([4,11,12,32,],[20,20,20,20,]),'bloque':([4,11,12,26,32,79,80,97,],[21,21,21,37,21,93,94,101,]),'sent_assign':([4,11,12,32,],[22,22,22,22,]),'list_id':([7,],[30,]),'exp_bool':([29,35,36,39,52,81,],[40,56,57,60,77,95,]),'comb':([29,35,36,39,52,62,81,],[41,41,41,41,41,83,41,]),'igualdad':([29,35,36,39,52,62,63,81,],[42,42,42,42,42,42,84,42,]),'rel':([29,35,36,39,52,62,63,64,65,81,],[43,43,43,43,43,43,43,85,86,43,]),'expr':([29,35,36,39,52,62,63,64,65,66,81,],[44,44,44,44,44,44,44,44,44,87,44,]),'term':([29,35,36,39,52,62,63,64,65,66,67,68,81,],[46,46,46,46,46,46,46,46,46,46,88,89,46,]),'unario':([29,35,36,39,45,47,52,62,63,64,65,66,67,68,74,75,81,],[48,48,48,48,73,76,48,48,48,48,48,48,48,48,90,91,48,]),'factor':([29,35,36,39,45,47,52,62,63,64,65,66,67,68,74,75,81,],[49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,49,]),'op_rel':([44,],[66,]),'else_part':([93,],[96,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM LBRACE list_decl list_sent RBRACE','program',5,'p_program','sintac.py',14),
  ('list_decl -> list_decl decl','list_decl',2,'p_list_decl','sintac.py',18),
  ('list_decl -> decl','list_decl',1,'p_list_decl','sintac.py',19),
  ('list_decl -> empty','list_decl',1,'p_list_decl','sintac.py',20),
  ('decl -> tipo list_id SEMICOLON','decl',3,'p_decl','sintac.py',27),
  ('tipo -> INT','tipo',1,'p_tipo','sintac.py',31),
  ('tipo -> FLOAT','tipo',1,'p_tipo','sintac.py',32),
  ('tipo -> BOOL','tipo',1,'p_tipo','sintac.py',33),
  ('list_id -> list_id COMMA IDENTIFIER','list_id',3,'p_list_id','sintac.py',37),
  ('list_id -> IDENTIFIER','list_id',1,'p_list_id','sintac.py',38),
  ('list_sent -> list_sent sent','list_sent',2,'p_list_sent','sintac.py',45),
  ('list_sent -> sent','list_sent',1,'p_list_sent','sintac.py',46),
  ('list_sent -> empty','list_sent',1,'p_list_sent','sintac.py',47),
  ('sent -> sent_if','sent',1,'p_sent','sintac.py',54),
  ('sent -> sent_while','sent',1,'p_sent','sintac.py',55),
  ('sent -> sent_do','sent',1,'p_sent','sintac.py',56),
  ('sent -> sent_read','sent',1,'p_sent','sintac.py',57),
  ('sent -> sent_write','sent',1,'p_sent','sintac.py',58),
  ('sent -> bloque','sent',1,'p_sent','sintac.py',59),
  ('sent -> sent_assign','sent',1,'p_sent','sintac.py',60),
  ('sent -> BREAK','sent',1,'p_sent','sintac.py',61),
  ('sent_if -> IF LPAREN exp_bool RPAREN bloque else_part FI','sent_if',7,'p_sent_if','sintac.py',65),
  ('else_part -> ELSE bloque','else_part',2,'p_else_part','sintac.py',69),
  ('else_part -> empty','else_part',1,'p_else_part','sintac.py',70),
  ('sent_while -> WHILE LPAREN exp_bool RPAREN bloque','sent_while',5,'p_sent_while','sintac.py',74),
  ('sent_do -> DO bloque UNTIL LPAREN exp_bool RPAREN SEMICOLON','sent_do',7,'p_sent_do','sintac.py',78),
  ('sent_read -> READ IDENTIFIER SEMICOLON','sent_read',3,'p_sent_read','sintac.py',82),
  ('sent_write -> WRITE exp_bool SEMICOLON','sent_write',3,'p_sent_write','sintac.py',86),
  ('bloque -> LBRACE list_sent RBRACE','bloque',3,'p_bloque','sintac.py',90),
  ('sent_assign -> IDENTIFIER ASSIGN exp_bool SEMICOLON','sent_assign',4,'p_sent_assign','sintac.py',94),
  ('exp_bool -> exp_bool OR comb','exp_bool',3,'p_exp_bool','sintac.py',98),
  ('exp_bool -> comb','exp_bool',1,'p_exp_bool','sintac.py',99),
  ('comb -> comb AND igualdad','comb',3,'p_comb','sintac.py',106),
  ('comb -> igualdad','comb',1,'p_comb','sintac.py',107),
  ('igualdad -> igualdad EQ rel','igualdad',3,'p_igualdad','sintac.py',114),
  ('igualdad -> igualdad NE rel','igualdad',3,'p_igualdad','sintac.py',115),
  ('igualdad -> rel','igualdad',1,'p_igualdad','sintac.py',116),
  ('rel -> expr op_rel expr','rel',3,'p_rel','sintac.py',123),
  ('op_rel -> LT','op_rel',1,'p_op_rel','sintac.py',127),
  ('op_rel -> LE','op_rel',1,'p_op_rel','sintac.py',128),
  ('op_rel -> GT','op_rel',1,'p_op_rel','sintac.py',129),
  ('op_rel -> GE','op_rel',1,'p_op_rel','sintac.py',130),
  ('expr -> expr PLUS term','expr',3,'p_expr','sintac.py',134),
  ('expr -> expr MINUS term','expr',3,'p_expr','sintac.py',135),
  ('expr -> term','expr',1,'p_expr','sintac.py',136),
  ('term -> term TIMES unario','term',3,'p_term','sintac.py',143),
  ('term -> term DIVIDE unario','term',3,'p_term','sintac.py',144),
  ('term -> unario','term',1,'p_term','sintac.py',145),
  ('unario -> PLUS unario','unario',2,'p_unario','sintac.py',152),
  ('unario -> MINUS unario','unario',2,'p_unario','sintac.py',153),
  ('unario -> factor','unario',1,'p_unario','sintac.py',154),
  ('factor -> NUMBER','factor',1,'p_factor','sintac.py',161),
  ('factor -> IDENTIFIER','factor',1,'p_factor','sintac.py',162),
  ('factor -> LPAREN exp_bool RPAREN','factor',3,'p_factor','sintac.py',163),
  ('empty -> <empty>','empty',0,'p_empty','sintac.py',170),
]
