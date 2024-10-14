class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = {}
    
    def get_symbol_table(self):
        return self.symbol_table

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
            if left_value is None:
                raise SemanticError("Error: Operando izquierdo en operación 'expr' no puede ser None.")
            node.semantic_annotation = f"{left_value} ({left_type})"

            if len(node.children) > 1:  # Si hay más de un hijo, tenemos una operación binaria
                operator = node.children[1].leaf  # El operador, por ejemplo, '+' o '-'
                right_type, right_value = self.evaluate_expression(node.children[2])  # Evaluar el operando derecho

                if right_value is None:
                    raise SemanticError("Error: Operando derecho en operación 'expr' no puede ser None.")

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



        # Si es un nodo 'exp_bool', representa una expresión booleana
        elif node.type == 'exp_bool':
            left_type, left_value = self.evaluate_expression(node.children[0])  # Evaluar el operando izquierdo
            node.semantic_annotation = f"{left_value} ({left_type})"

            if len(node.children) > 1:  # Si hay más de un hijo, tenemos una operación booleana
                operator = node.children[1].leaf  # El operador, por ejemplo, '>' o '=='
                right_type, right_value = self.evaluate_expression(node.children[2])  # Evaluar el operando derecho

                # Comprobar que los tipos son compatibles para la comparación
                if left_type != right_type:
                    raise SemanticError(f"Error: No se puede comparar {left_type} con {right_type}")

                # Realizar la operación booleana
                
                if operator == '==':
                    result_value = left_value == right_value
                elif operator == '!=':
                    result_value = left_value != right_value
                elif operator == '>':
                    result_value = left_value > right_value
                elif operator == '<':
                    result_value = left_value < right_value
                elif operator == '>=':
                    result_value = left_value >= right_value
                elif operator == '<=':
                    result_value = left_value <= right_value
                elif operator == '==':
                    result_value = left_value == right_value
                else:
                    raise SemanticError(f"Error: Operador desconocido '{operator}'")

                node.semantic_annotation = f"{left_value} {operator} {right_value} = {result_value}"
                return 'bool', result_value

            return 'bool', left_value
        
        # Si es un nodo 'comb', representa una combinación lógica (AND, OR)
        elif node.type == 'comb':
            left_type, left_value = self.evaluate_expression(node.children[0])  # Evaluar el operando izquierdo
            node.semantic_annotation = f"{left_value} ({left_type})"

            if len(node.children) > 1:  # Si hay más de un hijo, tenemos una operación de combinación lógica
                operator = node.children[1].leaf  # El operador, por ejemplo, 'and' o 'or'
                right_type, right_value = self.evaluate_expression(node.children[2])  # Evaluar el operando derecho

                # Comprobar que ambos operandos son booleanos
                if left_type != 'bool' or right_type != 'bool':
                    raise SemanticError(f"Error: Operaciones lógicas solo se pueden realizar entre booleanos, pero se encontró {left_type} y {right_type}")

                # Realizar la operación lógica
                if operator == 'and':
                    result_value = left_value and right_value
                elif operator == 'or':
                    result_value = left_value or right_value

                node.semantic_annotation = f"{left_value} {operator} {right_value} = {result_value}"
                return 'bool', result_value

            return 'bool', left_value
        
        # Si es un nodo 'igualdad', representa una operación de igualdad (==, !=)
        elif node.type == 'igualdad':
            left_type, left_value = self.evaluate_expression(node.children[0])  # Evaluar el operando izquierdo
            if left_value is None:
                raise SemanticError("Error: Operando izquierdo en operación 'igualdad' no puede ser None.")
            node.semantic_annotation = f"{left_value} ({left_type})"
            
            if len(node.children) > 1:  # Si hay más de un hijo, tenemos una operación de igualdad
                operator = node.children[1].leaf  # El operador, por ejemplo, '==' o '!='
                right_type, right_value = self.evaluate_expression(node.children[2])
                if right_value is None:
                    raise SemanticError("Error: Operando derecho en operación 'igualdad' no puede ser None.")

                # Comprobar que los tipos son compatibles para la comparación
                if left_type != right_type:
                    raise SemanticError(f"Error: No se puede comparar {left_type} con {right_type}")

                # Realizar la operación de igualdad
                if operator == '==':
                    result_value = left_value == right_value
                elif operator == '!=':
                    result_value = left_value != right_value
                else:
                    raise SemanticError(f"Error: Operador desconocido '{operator}'")
                
                node.semantic_annotation = f"{left_value} {operator} {right_value} = {result_value}"
                return 'bool', result_value
            
            return 'bool', left_value



        # Si es un nodo 'rel', representa una operación relacional (>, <, >=, <=)
        elif node.type == 'rel':
            left_type, left_value = self.evaluate_expression(node.children[0])  # Evaluar el operando izquierdo
            if left_value is None:
                raise SemanticError("Error: Operando izquierdo en operación 'rel' no puede ser None.")
            node.semantic_annotation = f"{left_value} ({left_type})"

            if len(node.children) > 1:  # Si hay más de un hijo, tenemos una operación relacional
                operator = node.children[1].leaf  # El operador, por ejemplo, '>' o '<'
                right_type, right_value = self.evaluate_expression(node.children[2])  # Evaluar el operando derecho
                if right_value is None:
                    raise SemanticError("Error: Operando derecho en operación 'rel' no puede ser None.")

                # Comprobar que los tipos son compatibles para la comparación
                if left_type != right_type:
                    raise SemanticError(f"Error: No se puede comparar {left_type} con {right_type}")

                # Realizar la operación relacional
                
                if operator == '>':
                    result_value = left_value > right_value
                elif operator == '<':
                    result_value = left_value < right_value
                elif operator == '>=':
                    result_value = left_value >= right_value
                elif operator == '<=':
                    result_value = left_value <= right_value
                elif operator == '==':
                    result_value = left_value == right_value
                else:
                    raise SemanticError(f"Error: Operador desconocido '{operator}'")

                node.semantic_annotation = f"{left_value} {operator} {right_value} = {result_value}"
                return 'bool', result_value

            return 'bool', left_value


        raise SemanticError(f"Error inesperado en la expresión '{node.type}'.")


    def analyze_if(self, node):
        condition = node.children[0]
        cond_type, cond_value = self.analyze_condition(condition)  # Obtener el tipo y el valor de la condición
        print(f"Condición: {cond_value} ({cond_type})")  # Depuración

        if cond_type != 'bool':
            raise SemanticError(f"Error: Se esperaba un tipo booleano en la condición, pero se encontró '{cond_type}'.")

        if cond_value:  # Usar el valor evaluado de la condición
            if_true_block = node.children[1]
            self.analyze(if_true_block)
        else:
            if len(node.children) > 2:
                if_false_block = node.children[2]
                print("Analizando else_part...")  # Depuración
                if if_false_block.type == 'else_part':
                    if if_false_block.children:  # Verifica que else_part no esté vacío
                        self.analyze(if_false_block.children[0])
                    else:
                        print("Else_part está vacío, no hay nada que analizar.")
                else:
                    print(f"Tipo de nodo desconocido: {if_false_block.type}")



    def analyze_while(self, node):
        condition = node.children[0]
        cond_type, cond_value = self.analyze_condition(condition)  # Obtener el tipo y el valor de la condición
        print(f"Condición del while: {cond_value} ({cond_type})")  # Depuración

        if cond_type != 'bool':
            raise SemanticError(f"Error: Se esperaba un tipo booleano en la condición, pero se encontró '{cond_type}'.")

        while cond_value:  # Reevaluar la condición en cada iteración del bucle
            while_body = node.children[1]  # El cuerpo del while
            for child in while_body.children:
                self.analyze(child)
            cond_type, cond_value = self.analyze_condition(condition)  # Reevaluar la condición en cada iteración

    def analyze_do_while(self, node):
        do_body = node.children[0]  # El cuerpo del do-while
        condition = node.children[1]  # La condición es el último hijo

        while True:
            for stmt in do_body.children:
                self.analyze(stmt)
            cond_type, cond_value = self.analyze_condition(condition)  # Obtener el tipo y el valor de la condición
            print(f"Condición del until: {cond_value} ({cond_type})")  # Depuración

            if cond_type != 'bool':
                raise SemanticError(f"Error: Se esperaba un tipo booleano en la condición, pero se encontró '{cond_type}'.")

            if cond_value:
                break



   # def analyze_read(self, node):
     #   variable_name = node.children[0].leaf
      #  value = input(f"Introduzca un valor para {variable_name}: ")
        # Aquí deberías manejar la conversión de `value` al tipo adecuado (int, float, etc.)
        # y almacenarlo en la variable correspondiente en tu contexto de ejecución.
       # self.set_variable_value(variable_name, value)  # Asumiendo que tienes una función para establecer el valor de la variable

    def analyze_read(self, node):
        # Por ahora, no hacer nada o imprimir un mensaje de depuración
        variable_name = node.children[0].leaf
        print(f"Leyendo variable '{variable_name}' (acción no implementada)")
        # O también puedes asignar un valor por defecto
        self.set_variable_value(variable_name, 0)  # Valor por defecto 0


    #def analyze_write(self, node):
     #   variable_name = node.children[0].leaf
        # Aquí deberías obtener el valor de `variable_name` de tu contexto de ejecución
      #  value = self.get_variable_value(variable_name)
       # print(f"{variable_name} = {value}")
    def analyze_write(self, node):
        # Por ahora, no hacer nada o imprimir un mensaje de depuración
        variable_name = node.children[0].leaf
        print(f"Escribiendo variable '{variable_name}' (acción no implementada)")
        # O también puedes simular la escritura con un valor por defecto
        value = self.get_variable_value(variable_name) if variable_name in self.symbol_table else "undefined"
        print(f"{variable_name} = {value}")


    def analyze_condition(self, node):
        cond_type, cond_value = self.evaluate_expression(node)  # Analizar la expresión de la condición
        if cond_type != 'bool':
            raise SemanticError(f"Error: Se esperaba un tipo booleano en la condición, pero se encontró '{cond_type}'.")
        return cond_type, cond_value  # Devuelve el tipo y el valor de la condición
