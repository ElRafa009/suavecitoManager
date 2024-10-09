class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        print(f"Analizando {node.type}...")  # Mensaje de depuración
        if node.type == 'program':
            print(f"Analizando program...")  # Mensaje de depuración
            for child in node.children:
                self.analyze(child)
        elif node.type == 'list_decl':
            print(f"Analizando lista de declaraciones...")  # Mensaje de depuración
            for decl in node.children:
                self.analyze(decl)  # Analiza cada declaración en la lista
        elif node.type == 'list_sent':
            print(f"Analizando lista de sentencias...")  # Mensaje de depuración
            for sent in node.children:
                self.analyze(sent)  # Analiza cada sentencia en la lista
        elif node.type == 'decl':
            print(f"Analizando decl...")  # Mensaje de depuración
            self.analyze_declaration(node)
        elif node.type == 'sent_assign':
            print(f"Analizando assign...")  # Mensaje de depuración
            self.analyze_assignment(node)
        elif node.type == 'if':
            print(f"Analizando if...")  # Mensaje de depuración
            self.analyze_if(node)
        elif node.type == 'while':
            print(f"Analizando while...")  # Mensaje de depuración
            self.analyze_while(node)
        elif node.type == 'do_while':
            print(f"Analizando do while...")  # Mensaje de depuración
            self.analyze_do_while(node)
        else:
            print(f"Tipo de nodo desconocido: {node.type}")


    def analyze_declaration(self, node):
        print(f"Analizando declaración: {node}")  # Mensaje de depuración
        tipo = node.children[0].leaf  # Tipo de la variable
        list_id = node.children[1]    # Lista de identificadores

        def propagate_type(list_id_node):
            # Si es un nodo de un identificador, lo procesamos
            if list_id_node.type == 'identifier':
                var_name = list_id_node.leaf
                if var_name in self.symbol_table:
                    print(f"Variable '{var_name}' ya está declarada.")  # Depuración
                    raise SemanticError(f"Error: La variable '{var_name}' ya está declarada.")
                self.symbol_table[var_name] = tipo
                list_id_node.semantic_annotation = tipo  # Anotar con el tipo
                print(f"Anotación semántica añadida a {list_id_node}: {tipo}")  # Mensaje de depuración
            else:
                # Propagar recursivamente el tipo en la lista de identificadores
                for child in list_id_node.children:
                    propagate_type(child)

        # Iniciar la propagación del tipo desde la lista de identificadores
        propagate_type(list_id)

        print(f"Declaración de variables completada con tipo '{tipo}'.")  # Mensaje de depuración



    def analyze_assignment(self, node):
        var_name = node.children[0].leaf
        expr = node.children[1]

        if var_name not in self.symbol_table:
            raise SemanticError(f"Error: La variable '{var_name}' no está declarada.")
        
        expected_type = self.symbol_table[var_name]
        actual_type = self.evaluate_expression(expr)

        if expected_type != actual_type:
            raise SemanticError(f"Error de tipos: Se esperaba '{expected_type}' pero se encontró '{actual_type}'.")

        # Anotar el nodo de asignación con el tipo de la expresión
        node.semantic_annotation = actual_type

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
            elif node.leaf.replace('.', '', 1).isdigit() and node.leaf.count('.') < 2:
                return 'float'
            elif node.leaf in ['true', 'false']:
                return 'bool'
            else:
                return self.symbol_table.get(node.leaf, None)
        # Más reglas para otros tipos de nodos

    def analyze_if(self, node):
        condition = node.children[0]  # Supongamos que la condición es el primer hijo
        self.analyze_condition(condition)  # Analizar la condición

        for child in node.children[1:]:  # Analizar el cuerpo del if
            self.analyze(child)

    def analyze_while(self, node):
        condition = node.children[0]
        self.analyze_condition(condition)  # Analizar la condición

        for child in node.children[1:]:  # Analizar el cuerpo del while
            self.analyze(child)

    def analyze_do_while(self, node):
        for child in node.children[:-1]:  # Analizar el cuerpo del do
            self.analyze(child)
        
        condition = node.children[-1]
        self.analyze_condition(condition)  # Analizar la condición

    def analyze_condition(self, node):
        # Asumiendo que la condición es de tipo booleano
        actual_type = self.evaluate_expression(node)
        if actual_type != 'bool':
            raise SemanticError(f"Error: Se esperaba un tipo booleano en la condición, pero se encontró '{actual_type}'.")

