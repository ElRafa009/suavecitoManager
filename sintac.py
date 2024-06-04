import ply.yacc as yacc
from lexer import tokens
from graphviz import Digraph

# Nodo del árbol sintáctico abstracto
class ASTNode:
    def __init__(self, type, children=None, leaf=None, level=1):
        self.type = type
        self.children = children if children is not None else []
        self.leaf = leaf
        self.level = level if level is not None else 1

        # Función para agregar nodos y aristas al gráfico del árbol
    def add_nodes(self, graph):
        if self:
            graph.node(str(id(self)), f"{self.type}\n{self.leaf if self.leaf else ''}\n{self.level}")
            for child in self.children:
                child.add_nodes(graph)
                graph.edge(str(id(self)), str(id(child)))

def calculate_levels(node, level=1):
    node.level = level
    for child in node.children:
        calculate_levels(child, level + 1)

last_valid_tokens = []
# Lista para almacenar los errores sintácticos
syntax_errors = []

# Reglas gramaticales
def p_program(p):
    '''program : PROGRAM LBRACE list_decl list_sent RBRACE'''
    p[0] = ASTNode('program', [p[3], p[4]])

def p_list_decl(p):
    '''list_decl : list_decl decl
                 | decl
                 | empty'''
    if len(p) == 3:
        p[0] = ASTNode('list_decl', [p[1], p[2]])
    else:
        p[0] = ASTNode('list_decl', [p[1]])

def p_decl(p):
    '''decl : tipo list_id SEMICOLON'''
    p[0] = ASTNode('decl', [p[1], p[2]])

def p_tipo(p):
    '''tipo : INT
            | FLOAT
            | BOOL'''
    p[0] = ASTNode('tipo', leaf=p[1])

def p_list_id(p):
    '''list_id : list_id COMMA IDENTIFIER
               | IDENTIFIER'''
    if len(p) == 4:
        p[0] = ASTNode('list_id', [p[1], ASTNode('identifier', leaf=p[3])])
    else:
        p[0] = ASTNode('list_id', [ASTNode('identifier', leaf=p[1])])

def p_list_sent(p):
    '''list_sent : list_sent sent
                 | sent
                 | empty'''
    if len(p) == 3:
        p[0] = ASTNode('list_sent', [p[1], p[2]])
    else:
        p[0] = ASTNode('list_sent', [p[1]])

def p_sent(p):
    '''sent : sent_if
            | sent_while
            | sent_do
            | sent_read
            | sent_write
            | bloque
            | sent_assign
            | BREAK'''
    p[0] = ASTNode('sent', [p[1]])

def p_sent_if(p):
    '''sent_if : IF LPAREN exp_bool RPAREN bloque else_part FI'''
    p[0] = ASTNode('sent_if', [p[3], p[5], p[6]])

def p_else_part(p):
    '''else_part : ELSE bloque
                 | empty'''
    p[0] = ASTNode('else_part', [p[2]] if len(p) == 3 else [p[1]])

def p_sent_while(p):
    '''sent_while : WHILE LPAREN exp_bool RPAREN bloque'''
    p[0] = ASTNode('sent_while', [p[3], p[5]])

def p_sent_do(p):
    '''sent_do : DO bloque UNTIL LPAREN exp_bool RPAREN SEMICOLON'''
    p[0] = ASTNode('sent_do', [p[2], p[5]])

def p_sent_read(p):
    '''sent_read : READ IDENTIFIER SEMICOLON'''
    p[0] = ASTNode('sent_read', [ASTNode('identifier', leaf=p[2])])

def p_sent_write(p):
    '''sent_write : WRITE exp_bool SEMICOLON'''
    p[0] = ASTNode('sent_write', [p[2]])

def p_bloque(p):
    '''bloque : LBRACE list_sent RBRACE'''
    p[0] = ASTNode('bloque', [p[2]])

def p_sent_assign(p):
    '''sent_assign : IDENTIFIER ASSIGN exp_bool SEMICOLON'''
    p[0] = ASTNode('sent_assign', [ASTNode('identifier', leaf=p[1]), p[3]])

def p_exp_bool(p):
    '''exp_bool : exp_bool OR comb
                | comb'''
    if len(p) == 4:
        p[0] = ASTNode('exp_bool', [p[1], ASTNode('operator', leaf=p[2]), p[3]])
    else:
        p[0] = ASTNode('exp_bool', [p[1]])

def p_comb(p):
    '''comb : comb AND igualdad
            | igualdad'''
    if len(p) == 4:
        p[0] = ASTNode('comb', [p[1], ASTNode('operator', leaf=p[2]), p[3]])
    else:
        p[0] = ASTNode('comb', [p[1]])

def p_igualdad(p):
    '''igualdad : igualdad EQ rel
                | igualdad NE rel
                | rel'''
    if len(p) == 4:
        p[0] = ASTNode('igualdad', [p[1], ASTNode('operator', leaf=p[2]), p[3]])
    else:
        p[0] = ASTNode('igualdad', [p[1]])

def p_rel(p):
    '''rel : expr op_rel expr'''
    p[0] = ASTNode('rel', [p[1], p[2], p[3]])

def p_op_rel(p):
    '''op_rel : LT
              | LE
              | GT
              | GE'''
    p[0] = ASTNode('op_rel', leaf=p[1])

def p_expr(p):
    '''expr : expr PLUS term
            | expr MINUS term
            | term'''
    if len(p) == 4:
        p[0] = ASTNode('expr', [p[1], ASTNode('operator', leaf=p[2]), p[3]])
    else:
        p[0] = ASTNode('expr', [p[1]])

def p_term(p):
    '''term : term TIMES unario
            | term DIVIDE unario
            | unario'''
    if len(p) == 4:
        p[0] = ASTNode('term', [p[1], ASTNode('operator', leaf=p[2]), p[3]])
    else:
        p[0] = ASTNode('term', [p[1]])

def p_unario(p):
    '''unario : PLUS unario
              | MINUS unario
              | factor'''
    if len(p) == 3:
        p[0] = ASTNode('unario', [ASTNode('operator', leaf=p[1]), p[2]])
    else:
        p[0] = ASTNode('unario', [p[1]])

def p_factor(p):
    '''factor : NUMBER
              | IDENTIFIER
              | LPAREN exp_bool RPAREN'''
    if len(p) == 2:
        p[0] = ASTNode('factor', leaf=p[1])
    else:
        p[0] = ASTNode('factor', [p[2]])

def p_empty(p):
    '''empty :'''
    p[0] = ASTNode('empty')

# Definir un diccionario que mapee las reglas gramaticales a los tokens esperados
expected_tokens_map = {
    'program': ['{'],
    'list_decl': ['INT', 'FLOAT', 'BOOL', 'IDENTIFIER', 'EPSILON'],
    'decl': ['INT', 'FLOAT', 'BOOL'],
    'tipo': ['INT', 'FLOAT', 'BOOL'],
    'list_id': ['IDENTIFIER'],
    'list_sent': ['IF', 'WHILE', 'DO', 'READ', 'WRITE', '{', 'IDENTIFIER', 'BREAK', 'EPSILON'],
    'sent': ['IF', 'WHILE', 'DO', 'READ', 'WRITE', '{', 'IDENTIFIER', 'BREAK'],
    'sent_if': ['IF'],
    'sent_while': ['WHILE'],
    'sent_do': ['DO'],
    'sent_read': ['READ'],
    'sent_write': ['WRITE'],
    'bloque': ['{'],
    'sent_assign': ['IDENTIFIER'],
    'exp_bool': ['(', 'IDENTIFIER', 'INTEGER', 'REAL', 'TRUE', 'FALSE'],
    'comb': ['(', 'IDENTIFIER', 'INTEGER', 'REAL', 'TRUE', 'FALSE'],
    'igualdad': ['(', 'IDENTIFIER', 'INTEGER', 'REAL', 'TRUE', 'FALSE'],
    'rel': ['(', 'IDENTIFIER', 'INTEGER', 'REAL', 'TRUE', 'FALSE'],
    'op_rel': ['LT', 'LE', 'GT', 'GE'],
    'expr': ['-', 'IDENTIFIER', 'INTEGER', 'REAL', 'TRUE', 'FALSE'],
    'term': ['-', 'IDENTIFIER', 'INTEGER', 'REAL', 'TRUE', 'FALSE'],
    'unario': ['NOT', '-'],
    'factor': ['(', 'IDENTIFIER', 'INTEGER', 'REAL', 'TRUE', 'FALSE']
}

def p_error(p):
    global syntax_errors
    global last_valid_tokens

    if last_valid_tokens:
        last_valid_token_index = len(last_valid_tokens) - 1
        last_valid_token = last_valid_tokens[last_valid_token_index]
        last_valid_token_type = last_valid_token.type
        expected_tokens = expected_tokens_map.get(last_valid_token_type, ['<TOKEN>'])

        next_token = None
        for token_type in expected_tokens:
            for token in last_valid_tokens[::-1]:
                if token.type == token_type:
                    next_token = token.value
                    break
            if next_token:
                break

        error_message = f"Sintax error: Unexpected token '{p.value}' in line {p.lineno}. Expected token(s): {', '.join(expected_tokens)} Next token: '{next_token}'."
    else:
        expected_tokens = expected_tokens_map.get('program', ['<TOKEN>'])
        error_message = f"Sintax error: Unexpected token '{p.value}' in line {p.lineno}. Expected token(s): {', '.join(expected_tokens)}"

    syntax_errors.append(error_message)

    # Limpiar lista de tokens válidos para evitar duplicados en errores
    last_valid_tokens = []
    
# Construcción del parser
parser = yacc.yacc()

# Función para dibujar el AST
def draw_ast(node):
    def add_nodes_edges(graph, node):
        if node:
            graph.node(str(id(node)), f"{node.type}\n{node.leaf if node.leaf else ''}\n{node.level}")
            for child in node.children:
                graph.edge(str(id(node)), str(id(child)))
                add_nodes_edges(graph, child)

    dot = Digraph()
    add_nodes_edges(dot, node)
    return dot

# Función para analizar el código y devolver el resultado y los errores
def parse_code(code):
    global syntax_errors
    syntax_errors = []  # Reiniciar la lista de errores
    
    # Análisis sintáctico
    result = parser.parse(code)
    
    # Devolver el resultado y los errores sintácticos
    return result, syntax_errors
