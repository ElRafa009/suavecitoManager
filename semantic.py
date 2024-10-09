class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        if node.type == 'program':
            for child in node.children:
                self.analyze(child)
        elif node.type == 'decl':
            self.analyze_declaration(node)
        elif node.type == 'sent_assign':
            self.analyze_assignment(node)
        # Agrega aquí más reglas semánticas para otros tipos de nodos

    def analyze_declaration(self, node):
        tipo = node.children[0].leaf  # Tipo de la variable
        list_id = node.children[1]    # Lista de identificadores

        for id_node in list_id.children:
            var_name = id_node.leaf
            if var_name in self.symbol_table:
                raise SemanticError(f"Error: La variable '{var_name}' ya está declarada.")
            self.symbol_table[var_name] = tipo

    def analyze_assignment(self, node):
        var_name = node.children[0].leaf
        expr = node.children[1]

        if var_name not in self.symbol_table:
            raise SemanticError(f"Error: La variable '{var_name}' no está declarada.")
        
        expected_type = self.symbol_table[var_name]
        actual_type = self.evaluate_expression(expr)

        if expected_type != actual_type:
            raise SemanticError(f"Error de tipos: Se esperaba '{expected_type}' pero se encontró '{actual_type}'.")

    def evaluate_expression(self, node):
        # Implementa la evaluación de la expresión para obtener el tipo
        if node.type == 'expr':
            left_type = self.evaluate_expression(node.children[0])
            right_type = self.evaluate_expression(node.children[2])
            if left_type == right_type:
                return left_type
            else:
                raise SemanticError("Error de tipos en la expresión.")
        elif node.type == 'factor':
            if node.leaf.isdigit():
                return 'int'
            elif node.leaf in ['true', 'false']:
                return 'bool'
            else:
                return self.symbol_table.get(node.leaf, None)
        # Más reglas para otros tipos de nodos
