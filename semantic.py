class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}

    def analyze(self, node):
        print(f"Analizando {node.type}...")  # Mensaje de depuración
        if node.type == 'program':
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

        elif node.type == 'sent':  # Detecta el nodo 'sent' y pasa el control a la sentencia adecuada
            sent_node = node.children[0]  # Asumiendo que el primer hijo es el tipo de sentencia real
            print(f"Analizando sentencia {sent_node.type}...")  # Mensaje de depuración
            self.analyze(sent_node)  # Llama recursivamente para analizar el tipo de sentencia real

        elif node.type == 'sent_assign':
            print(f"Analizando assign...")  # Mensaje de depuración
            self.analyze_assignment(node)

        elif node.type == 'sent_if':
            print(f"Analizando if...")  # Mensaje de depuración
            self.analyze_if(node)

        elif node.type == 'sent_while':
            print(f"Analizando while...")  # Mensaje de depuración
            self.analyze_while(node)

        elif node.type == 'sent_do':
            print(f"Analizando do while...")  # Mensaje de depuración
            self.analyze_do_while(node)

        elif node.type == 'sent_read':
            print(f"Analizando read...")  # Mensaje de depuración
            self.analyze_read(node)

        elif node.type == 'sent_write':
            print(f"Analizando write...")  # Mensaje de depuración
            self.analyze_write(node)

        elif node.type == 'bloque':
            print(f"Analizando bloque...")  # Mensaje de depuración
            for sent in node.children:
                self.analyze(sent)

        elif node.type == 'BREAK':
            print(f"Analizando break...")  # Mensaje de depuración
            # Aquí puedes manejar la lógica específica para break si es necesario

        else:
            print(f"Tipo de nodo desconocido: {node.type}")

    def analyze_declaration(self, node):
        #print(f"Analizando declaración: {node}")  # Mensaje de depuración
        tipo = node.children[0].leaf  # Tipo de la variable
        list_id = node.children[1]    # Lista de identificadores

        def propagate_type(list_id_node):
            # Si es un nodo de un identificador, lo procesamos
            if list_id_node.type == 'identifier':
                var_name = list_id_node.leaf
                if var_name in self.symbol_table:
                    #print(f"Variable '{var_name}' ya está declarada.")  # Depuración
                    raise SemanticError(f"Error: La variable '{var_name}' ya está declarada.")
                self.symbol_table[var_name] = {'type': tipo, 'value': None}  # Inicialmente sin valor
                list_id_node.semantic_annotation = tipo  # Anotar con el tipo
                #print(f"Anotación semántica añadida a {list_id_node}: {tipo}")  # Mensaje de depuración
            else:
                # Propagar recursivamente el tipo en la lista de identificadores
                for child in list_id_node.children:
                    propagate_type(child)

        # Iniciar la propagación del tipo desde la lista de identificadores
        propagate_type(list_id)

        #print(f"Declaración de variables completada con tipo '{tipo}'.")  # Mensaje de depuración

    def analyze_assignment(self, node):
        var_name = node.children[0].leaf  # Obtener el nombre de la variable
        expr = node.children[1]  # Obtener la expresión de asignación

        # Verificar si la variable está declarada
        if var_name not in self.symbol_table:
            raise SemanticError(f"Error: La variable '{var_name}' no está declarada.")

        # Obtener el tipo esperado de la variable
        expected_type = self.symbol_table[var_name]['type']

        # Evaluar el tipo y valor de la expresión (esto dependerá de tu implementación de 'evaluate_expression')
        actual_type, value = self.evaluate_expression(expr)

        # Verificar si el tipo de la expresión coincide con el tipo esperado
        if expected_type != actual_type:
            raise SemanticError(f"Error de tipos: Se esperaba '{expected_type}' pero se encontró '{actual_type}'.")

        # Actualizar la tabla de símbolos con el nuevo valor de la variable
        self.symbol_table[var_name]['value'] = value

        # Anotar el nodo de asignación con el tipo y valor de la expresión
        node.semantic_annotation = {'type': actual_type, 'value': value}

        # Propagar la anotación semántica a la variable
        node.children[0].semantic_annotation = {'type': actual_type, 'value': value}  # Nodo de la variable
        print(f"Asignación correcta: Variable '{var_name}' tiene tipo '{actual_type}' y valor '{value}'.")

        # Anotar el nodo de la expresión también, si es necesario
        expr.semantic_annotation = {'type': actual_type, 'value': value}


    def evaluate_expression(self, node):
        # Si el nodo es un factor (número, variable, booleano)
        if node.type == 'factor':
            if len(node.children) == 1:  # Caso de paréntesis o subexpresión
                return self.evaluate_expression(node.children[0])
            elif isinstance(node.leaf, (int, float)):
                tipo = 'float' if isinstance(node.leaf, float) else 'int'
                node.semantic_annotation = f"{node.leaf} ({tipo})"
                return tipo, node.leaf  # Devolver tipo y valor
            elif isinstance(node.leaf, str):
                if node.leaf.isdigit():
                    node.semantic_annotation = f"{int(node.leaf)} (int)"
                    return 'int', int(node.leaf)
                else:
                    if node.leaf in self.symbol_table:
                        tipo = self.symbol_table[node.leaf]['type']
                        valor = self.symbol_table[node.leaf].get('value', None)
                        node.semantic_annotation = f"{node.leaf} = {valor} ({tipo})"
                        return tipo, valor  # Devolver tipo y valor del identificador
                    else:
                        raise SemanticError(f"Variable '{node.leaf}' no declarada.")
            elif node.leaf in ['TRUE', 'FALSE']:
                bool_value = True if node.leaf == 'TRUE' else False
                node.semantic_annotation = f"{node.leaf} (bool)"
                return 'bool', bool_value

        # Si es un nodo 'unario', representa una operación como la negación (-x)
        elif node.type == 'unario':
            operator = node.children[0].leaf  # Obtener el operador unario
            operand_type, operand_value = self.evaluate_expression(node.children[1])  # Evaluar el operando

            if operator == '-':
                result = -operand_value  # Realizar la operación de negación
                node.semantic_annotation = f"{operator}{operand_value} = {result}"
                return operand_type, result
            elif operator == '!':
                result = not operand_value  # Realizar la operación lógica NOT
                node.semantic_annotation = f"!{operand_value} = {result}"
                return 'bool', result

        # Si es un nodo 'term', representa una multiplicación o división
        elif node.type == 'term':
            left_type, left_value = self.evaluate_expression(node.children[0])  # Evaluar el operando izquierdo
            node.semantic_annotation = f"{left_value} ({left_type})"

            if len(node.children) > 1:
                operator = node.children[1].leaf  # El operador, por ejemplo, '*' o '/'
                right_type, right_value = self.evaluate_expression(node.children[2])  # Evaluar el operando derecho

                # Realizar la operación sin promoción de tipos inicialmente
                if operator == '*':
                    result_value = left_value * right_value
                elif operator == '/':
                    if right_value == 0:
                        raise SemanticError("División por cero.")
                    result_value = left_value // right_value if left_type == 'int' and right_type == 'int' else left_value / right_value

                # Promoción de tipos si uno es float
                if left_type == 'float' or right_type == 'float':
                    result_value = float(result_value)

                node.semantic_annotation = f"{left_value} {operator} {right_value} = {result_value}"
                return 'float' if left_type == 'float' or right_type == 'float' else 'int', result_value

            return left_type, left_value

        # Si es un nodo 'expr', representa una suma o resta
        elif node.type == 'expr':
            left_type, left_value = self.evaluate_expression(node.children[0])  # Evaluar el operando izquierdo
            node.semantic_annotation = f"{left_value} ({left_type})"

            if len(node.children) > 1:  # Si hay más de un hijo, tenemos una operación binaria
                operator = node.children[1].leaf  # El operador, por ejemplo, '+' o '-'
                right_type, right_value = self.evaluate_expression(node.children[2])  # Evaluar el operando derecho

                # Realizar la operación sin promoción de tipos inicialmente
                if operator == '+':
                    result_value = left_value + right_value
                elif operator == '-':
                    result_value = left_value - right_value

                # Promoción de tipos si uno es float
                if left_type == 'float' or right_type == 'float':
                    result_value = float(result_value)

                node.semantic_annotation = f"{left_value} {operator} {right_value}"

                # Agregar el resultado parcial al proceso
                node.semantic_annotation += f" = {result_value}"
                node.children[0].semantic_annotation += f" {operator} {right_value} ({right_type}) = {result_value}"

                return 'float' if left_type == 'float' or right_type == 'float' else 'int', result_value

            return left_type, left_value

        raise SemanticError(f"Error inesperado en la expresión '{node.type}'.")


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

